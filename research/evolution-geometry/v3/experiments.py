"""Dimension, potential, coupling, variation and causality checks for V3."""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

from mesh import Slab, axial_complex, maximal_cubes, metric_intervals, spacetime_slab
from homogeneous import Frusta
from regge import GeometryError, Regge, potential
from stationary import solve_slab

p=argparse.ArgumentParser()
p.add_argument("results",type=Path)
p.add_argument("--section",choices=["mesh","homogeneous","slab","wave","all"],default="all")
args=p.parse_args()
out=args.results
out.mkdir(parents=True,exist_ok=True)


def mesh_checks():
    rows=[]
    for n in range(1,5):
        slab=spacetime_slab([3]*n,3)
        sites=slab.sites*np.array([.41]+[1]*n)
        r=Regge(slab)
        flat=metric_intervals(sites,r.edges,lambda x:np.diag([-1]+[1]*n))
        q=np.zeros(len(sites))
        _,g,f,defect,vol=r.evaluate(flat,q,.1)
        delta=np.max(abs(defect[~r.exterior]),initial=0.)
        field=np.max(abs(f[r.free_vertices]),initial=0.)
        gravity=np.max(abs(g[r.free_edges]),initial=0.)
        clock=np.max(r.temporal_norm(flat,sites[:,0]))
        assert max(delta,field,gravity)<4e-12 and np.isclose(clock,-1)
        assert np.isclose(vol.sum(),.82*2**n)
        rng=np.random.default_rng(225+n)
        s=flat+rng.uniform(-.00012,.00012,len(flat))
        phi=rng.uniform(-.12,.12,len(sites))
        for matter in ["axial","affine"]:
            fn=lambda e,u:r.evaluate(e,u,.17,potential(.6,.7),matter=matter,cosmological=.04)
            _,ds,df,*_=fn(s,phi)
            u=np.zeros_like(s)
            u[r.free_edges]=rng.normal(size=len(r.free_edges))
            u/=np.linalg.norm(u)
            v=rng.normal(size=len(phi))
            v/=np.linalg.norm(v)
            h=2e-5
            error=abs((fn(s+h*u,phi+h*v)[0]-fn(s-h*u,phi-h*v)[0])/(2*h)-(ds@u+df@v))
            assert error<4e-8
            rows.append((n,len(sites),len(slab.simplices),matter,delta,gravity,field,clock,vol.sum(),error))
    pd.DataFrame(rows,columns=["n","nodes","simplices","matter","flat_deficit","flat_edge_residual",
                              "flat_field_residual","inverse_clock_norm","volume","gradient_error"]
                 ).to_csv(out/"verification.csv",index=False)

    # Two squares share a side, but a third cell has only one active axis.
    nodes,_,_=axial_complex((3,2))
    masks={a:({0,1} if a[0]<2 else {0}) for a in nodes}
    _,edges,cubes=axial_complex((3,2),masks)
    kinds=sorted({len(x[1]) for x in maximal_cubes(cubes)})
    assert kinds==[1,2] and all((a,b) in edges for a,b in [((1,0),(2,0)),((1,1),(2,1))])
    try:
        spacetime_slab((3,2),2,masks)
    except ValueError as error:
        assert "Non-pure" in str(error)
    else:
        raise AssertionError("Mixed dimension passed the fixed-D constructor")
    bad=spacetime_slab((3,3),3)
    r=Regge(bad)
    metric=metric_intervals(bad.sites,r.edges,lambda _:np.diag([-1,1,1]))
    try:
        r.evaluate(metric,np.zeros(r.nv))
    except GeometryError:
        pass
    else:
        raise AssertionError("Null geometry passed the regular-sector constructor")


    shifted=spacetime_slab([3,3],3)
    r=Regge(shifted)
    coordinates=shifted.sites*np.array([.41,1,1])
    A=np.array([[1.,0.,0.],[.13,1.,0.],[0.,0.,1.]])
    s=metric_intervals(coordinates,r.edges,lambda _:A.T@np.diag([-1,1,1])@A)
    phi=np.zeros(r.nv)
    V0=.002
    G=.13
    a=r.evaluate(s,phi,G,potential(constant=V0),matter="affine")
    b=r.evaluate(s,phi,G,potential(),matter="affine",cosmological=8*np.pi*G*V0)
    difference=max(abs(a[0]-b[0]),np.max(abs(a[1]-b[1])),np.max(abs(a[2]-b[2])))
    assert difference<1e-12
    shift_defect=np.max(abs(a[3][~r.exterior]))
    assert shift_defect<1e-12
    # A field impulse acts directly only on staircase legs, even under this shift.
    center=r.free_vertices[0]
    phi[center]=1
    _,_,gradient,*_=r.evaluate(s,phi,matter="axial")
    allowed={v for e in shifted.axial_edges if center in e for v in e}
    assert set(np.flatnonzero(abs(gradient)>1e-12))<=allowed
    pd.DataFrame([(shift_defect,difference,r.temporal_norm(s,coordinates[:,0]).max())],
                 columns=["shifted_flat_deficit","vacuum_potential_equivalence","max_clock_norm"]
                 ).to_csv(out/"controls.csv",index=False)

    # Static conical geometry: piecewise flat away from one, timelike central link.
    count=5
    alpha=np.pi/3
    duration=.39
    triangles=[tuple(sorted((0,i+1,(i+1)%count+1))) for i in range(count)]
    cells=[]
    for triangle in triangles:
        for split in range(3):
            cells.append([*triangle[:split+1],*[j+count+1 for j in triangle[split:]]])
    sites=np.asarray([(t,v) for t in [0,1] for v in range(count+1)])
    model=Regge(Slab(sites,np.asarray(cells),set()))
    src,dst=sites[model.edges.T]
    same=src[:,1]==dst[:,1]
    radius=(src[:,1]==0)|(dst[:,1]==0)
    square=np.where(same,0.,np.where(radius,1.,2*(1-np.cos(alpha))))
    square-=(dst[:,0]-src[:,0])**2*duration**2
    _,_,_,deficit,_=model.evaluate(square,np.zeros(len(sites)),matter="affine")
    h=model.hinges.index((0,count+1))
    expected=2*np.pi-count*alpha
    assert not model.exterior[h] and abs(deficit[h]-expected)<2e-12
    assert np.max(model.temporal_norm(square,sites[:,0]*duration))<0
    pd.DataFrame([(count,alpha,deficit[h],expected)],columns=["sectors","angle","measured","expected"]
                 ).to_csv(out/"cone.csv",index=False)

    # Exact fixed-background affine linear scalar, with an intentionally wrong interior guess.
    slab=spacetime_slab([3,3],3)
    engine=Regge(slab)
    x=slab.sites*np.array([.41,1,1])
    s=metric_intervals(x,engine.edges,lambda _:np.diag([-1,1,1]))
    phi=.2+.04*x[:,0]+.03*x[:,1]
    guess=phi.copy()
    guess[engine.free_vertices]+=1
    fitted=solve_slab(engine,s,guess,geometry_fixed=True,matter="axial")
    err=np.linalg.norm(fitted.field-phi,np.inf)
    assert fitted.stationary and err<1e-10
    pd.DataFrame([(len(engine.free_vertices),err)],columns=["free_nodes","field_error"]
                 ).to_csv(out/"fixed_scalar.csv",index=False)


def continuum(n,G,model,q,v,until,Lambda=0.):
    V,Vp=model
    def rhs(t,x):
        a,phi,velocity=x
        H=np.sqrt((16*np.pi*G*(.5*velocity**2+V(phi))+2*Lambda)/(n*(n-1)))
        return [a*H,velocity,-n*H*velocity-Vp(phi)]
    return solve_ivp(rhs,(0,until),[*q,v],rtol=2e-12,atol=1e-13,method="DOP853",dense_output=True)


def spectral_dim(n,a,u,L):
    lam=4*np.sin(np.pi*np.arange(L)/L)**2/a**2
    weights=np.exp(-u*lam)
    return 2*n*u*(lam@weights)/weights.sum()


def homogeneous():
    cases=[
        ("mass_refine",2,.15,.55,0.,.22,.08,"axial",0.,[.24,.12,.06]),
        ("mass_refine",3,.15,.55,0.,.22,.08,"axial",0.,[.24,.12,.06]),
        ("affine_control",2,.15,.55,0.,.22,.08,"affine",0.,[.24,.12]),
        ("affine_control",3,.15,.55,0.,.22,.08,"affine",0.,[.24,.12]),
        ("massless",2,.07,0.,0.,.10,.13,"axial",0.,[.20,.10]),
        ("quartic",3,.08,0.,1.25,.26,-.04,"axial",0.,[.20,.10]),
        ("weak_coupling",3,.02,.55,0.,.22,.08,"axial",0.,[.20,.10]),
        ("lambda_vacuum",2,.15,0.,0.,0.,0.,"axial",.02,[.20,.10]),
    ]
    rows,checks=[],[]
    failed=[]
    for name,n,G,mass,quartic,phi,velocity,matter,Lambda,hvals in cases:
        model=potential(mass,quartic)
        r=Frusta(n,G,model,matter,Lambda)
        for h0 in hvals:
            h=h0
            ell0=h0/.24 if name=="mass_refine" else 1.
            a=np.array([ell0,phi])
            try:
                b=r.start(a,velocity,h)
            except GeometryError:
                failed.append((name,n,h0,ell0,0,float("nan"),"initial lapse"))
                continue
            ref=continuum(n,G,model,a,velocity,12,Lambda)
            time=0.
            intervals=[]
            history=[a,b]
            for step in range(40):
                layer=r.evaluate(a,b,h)
                intervals.append((h,layer))
                time+=h
                rho=.5*((b[1]-a[1])/h)**2+model[0]((a[1]+b[1])/2)
                compare=ref.sol(time)
                errors=abs(compare[:2]-b)/[ell0,1.]
                eig_dim=spectral_dim(n,b[0],4.,64)
                dims=[spectral_dim(n,b[0],4.,N) for N in [16,32,64]]
                ricci=np.nan
                if len(intervals)>1:
                    past=intervals[-2][1]
                    ricci=4*(.5*(past[7]+layer[7])+past[6]+layer[5])/(past[3]+layer[3])
                at_hinge=ref.sol(time-h)
                ricci_ref=8*np.pi*G*(-at_hinge[2]**2+2*(n+1)/(n-1)*model[0](at_hinge[1]))+2*(n+1)/(n-1)*Lambda
                rows.append((name,n,G,mass,quartic,matter,Lambda,h0,ell0,step+1,time,h,layer[4],b[0],b[1],
                             rho,rho*b[0]**n,abs(layer[1][-1]),layer[2],ricci,ricci_ref,eig_dim,*dims,
                             np.log(3**n) if rho>1e-16 else np.nan,*errors))
                if time>=.85:
                    break
                c,hnew,residual=r.step(a,b,h)
                if residual>3e-9:
                    failed.append((name,n,h0,ell0,step+1,residual,"DEL/lapse"))
                    break
                a,b,h=b,c,hnew
                history.append(c)
            forward=np.array([v[1][1] for v in intervals])
            backward=np.array([r.evaluate(history[i+1],history[i],intervals[i][0])[1]
                               for i in range(len(intervals))])
            reverse=np.max(abs(backward-forward[:,[2,3,0,1,4]]))
            del_residual=np.max(abs(forward[:-1,2:4]+forward[1:,:2]),initial=0.)
            lapse=np.max(abs(forward[:,-1]))
            assert reverse<1e-9 and del_residual<3e-9 and lapse<3e-9
            checks.append((name,n,h0,ell0,time,reverse,del_residual,lapse,*errors))
            print(name,n,h0,"t",round(time,4),"errors",errors,flush=True)
    cols=["case","n","G","mass","quartic","matter","Lambda","h0","ell0","step","time","duration","strut_proper_time",
          "scale","phi","density","rho_volume","lapse_residual","max_bulk_deficit","ricci","ricci_reference",
          "effective_dimension","dim_L16","dim_L32","dim_L64","site_entropy","scale_error","field_error"]
    pd.DataFrame(rows,columns=cols).to_csv(out/"homogeneous.csv",index=False)
    pd.DataFrame(checks,columns=["case","n","h0","ell0","end","reverse_error","DEL","lapse","scale_error","field_error"]
                 ).to_csv(out/"homogeneous_checks.csv",index=False)
    pd.DataFrame(failed,columns=["case","n","h0","ell0","last_step","rejected_residual","reason"]
                 ).to_csv(out/"homogeneous_rejections.csv",index=False)


    rows=[]
    for n in [2,3]:
        for scheme in ["axial","affine"]:
            G=.15
            model=potential(.55)
            engine=Frusta(n,G,model,scheme)
            for h in [.24,.12,.06,.03]:
                ell=h/.24
                a=np.array([ell,.22])
                b=engine.start(a,.08,h)
                ref=continuum(n,G,model,a,.08,1.5)
                delta=0.
                lapse=0.
                for i in range(1,round(.96/h)+1):
                    metrics=engine.evaluate(a,b,h)
                    # Normalize the lapse variation by the initial cell volume.
                    lapse=max(lapse,abs(metrics[1][-1])/ell**n)
                    if i<round(.96/h):
                        c,e=engine.step_fixed_time(a,b,h)
                        a,b=b,c
                        delta=max(delta,e)
                err=abs(b-ref.sol(.96)[:2])/[ell,1.]
                rows.append((n,scheme,h,ell,delta,lapse,*err))
    pd.DataFrame(rows,columns=["n","matter","h","ell","DEL","normalized_lapse_residual","scale_error",
                               "field_error"]).to_csv(out/"fixed_time_convergence.csv",index=False)


def slabs():
    rows=[]
    for n,G,matter in [(2,.03,"axial"),(2,.03,"affine"),(2,.3,"axial"),(3,.03,"axial")]:
        slab=spacetime_slab([3]*n,3)
        t=(slab.sites[:,0]-1)*.41
        r=Regge(slab)
        model=potential(.65)
        ref=continuum(n,G,model,[1.,.2],.09,2.)
        sites=(slab.sites-1)*np.array([.41]+[1]*n)
        metric=lambda x:np.diag([-1.]+[ref.sol(x[0]+.41)[0]**2]*n)
        S=metric_intervals(sites,r.edges,metric)
        P=ref.sol(t+.41)[1]
        E,F=r.free_edges,r.free_vertices
        time_leg=S[E]<0
        result=solve_slab(r,S,P,Gnewton=G,model=model,matter=matter,clock=t)
        residue=np.r_[result.edge_residual,result.field_residual]
        error=np.max(abs(residue))
        rows.append((n,G,matter,len(E),len(F),result.iterations,result.start_residual,error,
                     np.max(abs(result.edge_residual[time_leg])),
                     float(max(np.max(abs(result.intervals-S)),np.max(abs(result.field-P)))),
                     result.stationary))
        print("unrestricted",n,G,matter,error,flush=True)
    pd.DataFrame(rows,columns=["n","G","matter","free_edges","free_nodes","iterations","start_residual","end_residual",
                               "timelike_residual","displacement","stationary"]).to_csv(out/"slab_attempts.csv",index=False)


def waves():
    rows=[]
    for n in [1,2,3]:
        for spacing in [.2,.1,.05]:
            dt=spacing*.37
            k=np.arange(1,n+1)*.7
            mass=.4
            # Mode of the orthogonal axial action, in a periodic or infinite grid.
            Omega2=mass**2+4*np.sum(np.sin(k*spacing/2)**2)/spacing**2
            omega=2*np.arcsin(dt*np.sqrt(Omega2)/2)/dt
            expected=np.sqrt(mass*mass+k@k)
            phase_speed=omega/np.linalg.norm(k)
            group_speed=np.linalg.norm(np.sin(k*spacing)/(spacing*np.sqrt(Omega2)*np.sqrt(1-dt*dt*Omega2/4)))
            rows.append((n,spacing,dt,omega,expected,phase_speed,group_speed))
    pd.DataFrame(rows,columns=["n","dx","dt","omega","continuum","phase_speed","group_speed"]).to_csv(
        out/"dispersion.csv",index=False)
    rows=[]
    for dx in [.2,.1,.05]:
        x=np.arange(-20,20,dx)
        dt=.37*dx
        M=.4
        K=lambda u:(2*u-np.roll(u,1)-np.roll(u,-1))/dx**2+M*M*u
        a0=np.maximum(1-x*x,0)**2
        a=a0.copy()
        b=a0-.5*dt**2*K(a0)
        norm=lambda a,b:dx*.5*(np.sum(((b-a)/dt)**2)+a@K(b))
        initial=norm(a,b)
        duration=round(5/dt)
        for i in range(duration+1):
            if i%max(1,duration//10)==0:
                residual=abs(norm(a,b)/initial-1)
                assert residual<2e-12
                support=np.max(abs(x[np.abs(a)>1e-14]))
                assert support<1+(i+.1)*dx+1e-11
                d=(b-a)/dt
                edge=(np.roll(a,-1)-a)/dx
                energy=.5*(d*d+M*M*a*a)+.25*(edge*edge+np.roll(edge*edge,1))
                probability=energy/energy.sum()
                probability=probability[probability>0]
                rows.append((dx,i*dt,support,residual,-probability@np.log(probability)))
            if i<duration:
                a,b=b,2*b-a-dt**2*K(b)
        for _ in range(duration):
            a,b=2*a-b-dt**2*K(a),a
        assert max(abs(a-a0))<1e-11
    pd.DataFrame(rows,columns=["dx","time","stencil_support","relative_shadow_energy_error","site_entropy"]
                 ).to_csv(out/"wave.csv",index=False)


for key,fn in [("mesh",mesh_checks),("homogeneous",homogeneous),("slab",slabs),("wave",waves)]:
    if args.section in [key,"all"]:
        fn()
