import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

parser = argparse.ArgumentParser()
parser.add_argument("results", type=Path)
out = parser.parse_args().results
out.mkdir(parents=True,exist_ok=True)
rng = np.random.default_rng(5281)


def laplace(field, dim):
    result = -2*dim*field
    for axis in range(-dim,0):
        result += np.roll(field,1,axis)+np.roll(field,-1,axis)
    return result


def evolve(field, law, dx, dim, courant, times):
    mass = field.sum(axis=tuple(range(-dim,0)))*dx**dim
    largest=field.max(axis=tuple(range(-dim,0)))
    t=0.
    for target in times:
        while t<target-1e-13:
            if law == "porous":
                flux=field**2
                derivative=2*field.max()
            else:
                flux=field/(1+law*field)
                derivative=1
            step=min(target-t,courant*dx**2/(2*dim*max(derivative,1e-10)))
            field=field+(step/dx**2)*laplace(flux,dim)
            t+=step
        assert field.min()>=-1e-12
        assert np.all(field.max(axis=tuple(range(-dim,0)))<=largest+1e-12)
        err=np.max(abs(field.sum(axis=tuple(range(-dim,0)))*dx**dim-mass))
        assert err<1e-9
        yield target,field,err


def feedback():
    rows=[]
    gallery={}
    for dim,L,side,courant in [(1,96,24,.8),(1,192,24,.8),(2,48,24,.8),
                               (2,96,24,.8),(2,96,24,.25),(2,128,24,.8),(2,192,48,.8)]:
        dx=side/L
        coords=(np.arange(L)-L//2)*dx
        axes=np.ix_(*[coords]*dim)
        x=axes[0]
        for dist in [3,6,9]:
            squared=sum(a*a for a in axes[1:])
            r_a=(x+dist/2)**2+squared
            r_b=(x-dist/2)**2+squared
            a=2*np.exp(-r_a/(2*.9**2))
            b=2*np.exp(-r_b/(2*.9**2))
            # All four preparations include the same constant background.
            initial=.05+np.array([a*0,a,b,a+b])
            for beta in [0,1,4]:
                previous=np.sum(initial[3]**2)
                times=[0,.25,.5,1,2,4,8,16,32]
                frames=[]
                for t,e,error in evolve(initial,beta,dx,dim,courant,times):
                    baseline,A,B,AB=e
                    variance=np.sum(AB**2)
                    assert variance<=previous+1e-9
                    previous=variance
                    residual=AB-A-B+baseline
                    d_b=AB-A
                    idx=(coords[:,None] if dim==2 else coords)
                    if dim==2:
                        idx=np.broadcast_to(idx,AB.shape)
                    dxb=(idx-dist/2+side/2)%side-side/2
                    local_near=(r_b<2**2)&(dxb<0)
                    local_far=(r_b<2**2)&(dxb>0)
                    near=(residual[local_near].sum()-residual[local_far].sum())*dx**dim
                    angular_offset = lambda mass: side/(2*np.pi)*np.angle(
                        np.sum(mass*np.exp(2j*np.pi*dxb/side)))
                    shift=angular_offset(d_b)-angular_offset(B-baseline)
                    rel=np.linalg.norm(residual.ravel())/np.linalg.norm((AB-baseline).ravel())
                    linear_shift=np.sum(residual*dxb)/np.sum(d_b)
                    rows.append((dim,L,side,courant,dist,beta,t,error,rel,A.max(),AB.max(),
                                 near,shift,linear_shift,np.sum(residual)*dx**dim))
                    if (dim,L,courant)==(2,48,.8):
                        frames.append({"t":t,"range":[float(AB.min()),float(AB.max())],
                                       "field":np.round(AB,4).ravel().tolist(),
                                       "residual":np.round(residual,5).ravel().tolist()})
                if frames:
                    gallery[f"{dist}/{beta}"]=frames
    cols=["dim","L","side","courant","distance","beta","t","balance","residual","peak_single",
          "peak_pair","near_minus_far","circular_shift","linear_shift","residual_mass"]
    pd.DataFrame(rows,columns=cols).to_csv(out/"metric_feedback.csv",index=False)
    (out/"metric_frames.json").write_text(json.dumps(gallery,separators=(",",":")))


def barenblatt():
    rows=[]
    for dim in [1,2]:
        for n in [64,128,192]:
            dx=24/n
            x=(np.arange(n)-n//2)*dx
            squared=sum(a*a for a in np.ix_(*[x]*dim))
            alpha=dim/(dim+2)
            beta=1/(dim+2)
            k=beta/4
            exact=lambda t: t**(-alpha)*np.maximum(.45-k*squared*t**(-2*beta),0)
            for t,e,err in evolve(exact(1),"porous",dx,dim,.8,[0,1,3,7,15]):
                reference=exact(1+t)
                relative=np.sum(abs(e-reference))/np.sum(reference)
                msd=np.sum(squared*e)/e.sum()
                ref_msd=np.sum(squared*reference)/reference.sum()
                rows.append((dim,n,t,relative,msd,ref_msd,err))
    pd.DataFrame(rows,columns=["dim","L","t","error_l1","msd","exact_msd","balance"]).to_csv(out/"barenblatt.csv",index=False)


feedback()
barenblatt()
