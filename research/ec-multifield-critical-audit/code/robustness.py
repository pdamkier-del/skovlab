"""Smallest homogeneous full-six-spinor test after the analytical/physical audit.
No fluid closure. Diagonal Bianchi I retained only when full momentum/off-diagonal
stress checks pass. This is not a general 3+1 solver or physical fermion simulation.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from field_source import source,modes,DIRS,G5,GAMMA
GA=3/16


def pack(x,H,psi):return np.r_[x,H,psi.real.ravel(),psi.imag.ravel()]
def unpack(y):return y[:3],y[3:6],y[6:30].reshape(6,4)+1j*y[30:54].reshape(6,4)


def rhs(y,mom,mass=0.,contact=True):
    x,H,psi=unpack(y);a=np.exp(x);src=source(a,H,psi,mom,mass=mass,contact=contact)
    dH=-np.sum(H)*H+src['P']+(src['E']-np.sum(src['P']))/2
    return pack(H,dH,src['dt'])


def rk4(y,dt,mom,mass=0.,contact=True):
    a=rhs(y,mom,mass,contact);b=rhs(y+dt*a/2,mom,mass,contact);c=rhs(y+dt*b/2,mom,mass,contact);d=rhs(y+dt*c,mom,mass,contact)
    return y+dt*(a+2*b+2*c+d)/6


def reference_parameters():
    p=1.;L=2*np.pi;n0=6/L**3;ab=np.sqrt(GA*n0/p);q=np.sqrt(p*n0/3)
    def a(eta):return np.sqrt(ab*ab+q*q*eta*eta)
    def clock(eta):return .5*(eta*a(eta)+ab*ab/q*np.arcsinh(q*eta/ab))
    def phase(eta):return p*eta-1.5*np.arctan(q*eta/ab)
    ei=-ab/q;ti=clock(ei);tf=-ti
    return {'p':p,'L':L,'n0':n0,'ab':ab,'q':q,'eta_i':ei,'ti':ti,'tf':tf,'duration':tf-ti},a,clock,phase


def initial(case='exact',contact=True):
    par,a,clock,phase=reference_parameters();ai=a(par['eta_i']);nf=np.repeat(par['n0']/6,6);mom=DIRS.copy();psi=np.sqrt(nf/ai**3)[:,None]*modes()*np.exp(-1j*phase(par['eta_i']))
    shear=np.zeros(3);mass=0.
    if case=='pair_amplitude_minus_2percent':psi[:2]*=np.sqrt(.98)
    elif case=='x_momentum_plus_2percent':mom[:2]*=1.02
    elif case=='shear_2percent':shear=np.array([.02,-.02,0])*par['q']/par['ab']**2
    elif case=='mass_1percent_pb':mass=.01/par['ab']
    elif case in ['opposite_chirality_1percent','balanced_chirality']:
        fraction=.01 if case=='opposite_chirality_1percent' else .5
        psi=np.sqrt(nf/ai**3)[:,None]*(np.sqrt(1-fraction)*modes()+np.sqrt(fraction)*modes(chirality=-1))*np.exp(-1j*phase(par['eta_i']))
    elif case!='exact':raise ValueError(case)
    src=source(np.repeat(ai,3),np.zeros(3),psi,mom,mass=mass,contact=contact)
    E=src['E'];H=-np.sqrt((E+.5*np.sum(shear**2))/3)+shear
    return pack(np.log(np.repeat(ai,3)),H,psi),mom,mass,par


def diagnostics(y,mom,mass,contact):
    x,H,psi=unpack(y);a=np.exp(x);s=source(a,H,psi,mom,mass,contact=contact);v=np.prod(a)
    C=sum(H[i]*H[j] for i in range(3) for j in range(i))-s['E']
    derivative=rhs(y,mom,mass,contact);dH=derivative[3:6]
    K=4*(np.sum((dH+H*H)**2)+sum(H[i]**2*H[j]**2 for i in range(3) for j in range(i)))
    number=v*np.sum(abs(psi)**2,axis=1);T=s['T'];off=T[1:,1:]-np.diag(np.diag(T)[1:])
    # Complete effective source, not a prescribed EOS.
    R=s['E']-np.sum(s['P']);torsion=-1.5*s['axial2'] if contact else 0.
    return {'volume':float(v),'Hmean':float(np.mean(H)),'constraint':float(C),'momentum_max':float(np.max(abs(T[0,1:]))),'offdiag_max':float(np.max(abs(off))),'metric_R':float(R),'metric_K':float(K),'torsion2':float(torsion),'number':number,'source':s}


def integrate(case='exact',steps=256,contact=True):
    y,mom,mass,par=initial(case,contact);dt=par['duration']/steps;t=par['ti'];d=diagnostics(y,mom,mass,contact);number0=d['number'];scale=par['p']*par['n0']/par['ab']**4
    rows=[];maxC=maxQ=maxM=maxO=0.;event=None;minimum=d['volume'];status='completed';states=[]
    def row():
        nonlocal maxC,maxQ,maxM,maxO,minimum
        z=diagnostics(y,mom,mass,contact);minimum=min(minimum,z['volume']);maxC=max(maxC,abs(z['constraint'])/scale);maxQ=max(maxQ,float(np.max(abs(z['number']/number0-1))));maxM=max(maxM,z['momentum_max']);maxO=max(maxO,z['offdiag_max'])
        return {k:z[k] for k in ['volume','Hmean','constraint','momentum_max','offdiag_max','metric_R','metric_K','torsion2']}|{'t':t}
    previous=row();rows.append(previous)
    for i in range(steps):
        old=y.copy();oldt=t;y=rk4(y,dt,mom,mass,contact);t=par['ti']+(i+1)*dt
        if not np.all(np.isfinite(y)) or np.min(np.exp(y[:3]))<par['ab']*1e-3:status='inconclusive conditioning stop';break
        now=row()
        if maxC>.01 or maxM>1e-7*scale or maxO>1e-7*scale:status='inconclusive constraint/symmetry stop';break
        if previous['Hmean']<0<=now['Hmean'] and event is None:
            # Reintegrate only within the current RK step to locate the turn; no H projection.
            h=brentq(lambda h:float(np.mean(unpack(rk4(old,h,mom,mass,contact))[1])),0,dt,xtol=1e-14)
            turn=rk4(old,h,mom,mass,contact);v=diagnostics(turn,mom,mass,contact)
            event={'t':oldt+h,'volume':v['volume'],'mean_Hdot':float(np.mean(rhs(turn,mom,mass,contact)[3:6])),'metric_R':v['metric_R'],'metric_K':v['metric_K'],'torsion2':v['torsion2'],'scope':'Homogeneous normal/material total-current volume turn in this symmetric pair family; not a finite cloud or general 3D test.'}
        if (i+1)%max(1,steps//32)==0:rows.append(now)
        previous=now
    final=diagnostics(y,mom,mass,contact)
    error=None
    if case=='exact' and contact and status=='completed':
        _,af,clock,phase=reference_parameters();eta=-par['eta_i'];aa=af(eta);HH=par['q']**2*eta/aa**3
        ps=np.sqrt(par['n0']/6/aa**3)*modes()*np.exp(-1j*phase(eta));ref=pack(np.log(np.repeat(aa,3)),np.repeat(HH,3),ps)
        error=[float(np.linalg.norm(y[:3]-ref[:3])),float(np.linalg.norm(y[3:6]-ref[3:6])),float(np.linalg.norm(y[6:]-ref[6:]))]
    return {'case':case,'contact':contact,'mass':mass,'steps':steps,'dt':dt,'parameters':par,'status':status,'event':event,'max_constraint_over_fixed_rho_b':maxC,'max_relative_species_number_drift':maxQ,'max_momentum':maxM,'max_offdiagonal_stress':maxO,'exact_endpoint_errors':error,'minimum_sampled_volume':minimum,'final_Hmean':final['Hmean'],'final_volume':final['volume'],'rows':rows},y


def run_all():
    exact=[]
    for steps in [64,128,256]:r,_=integrate(steps=steps);exact.append(r)
    perturb=[]
    for case in ['pair_amplitude_minus_2percent','x_momentum_plus_2percent','shear_2percent','mass_1percent_pb','opposite_chirality_1percent']:
        pair=[]
        for steps in [128,256]:r,_=integrate(case,steps);pair.append(r)
        perturb.append({'case':case,'records':pair})
    # Separate torsion-free constraints at the same declared modes/charges and initial a.
    # Its exact radiation crunch is before the benchmark final time; demonstrate approach only.
    y,mom,mass,par=initial('exact',False);ai=np.exp(y[0]);q=par['q'];crunch=(ai*ai)/(2*q)
    tf_duration=.8*crunch;dt=tf_duration/256;Q0=diagnostics(y,mom,0.,False)['number'];maxC=0.
    for _ in range(256):
        y=rk4(y,dt,mom,0.,False);d=diagnostics(y,mom,0.,False);maxC=max(maxC,abs(d['constraint'])/(par['p']*par['n0']/par['ab']**4))
    comparison={'initial_scale_factor':ai,'initial_H_torsion_free':float(unpack(initial('exact',False)[0])[1][0]),'initial_H_ECD':float(unpack(initial()[0])[1][0]),'time_to_exact_radiation_crunch_from_initial':crunch,'integrated_fraction':.8,'endpoint':{k:d[k] for k in ['volume','Hmean','metric_R','metric_K']},'max_constraint_over_reference_rho_b':maxC,'max_final_number_drift':float(np.max(abs(d['number']/Q0-1))),'classification':'No bounce before this cutoff; the exact separate radiation solution reaches zero a in finite proper time with divergent metric Kretschmann.'}
    return {'gate':'Independent action audit passed; Pauli/EFT audit fails a controlled physical bounce. Only this small classical homogeneous test is justified, not a 3D extension.','exact_refinement':exact,'perturbations':perturb,'torsion_free':comparison,'scope':'Proper-time homogeneous full-six-spinor modes, paired opposite beams; spatial derivatives exact analytically. No spatial refinement, arbitrary amplitude imbalance, inhomogeneous stability, quantum state evolution or general geodesic completeness for perturbed cases.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();out=run_all();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2,allow_nan=False)+'\n');print('wrote',args.output)
