"""Massless kappa=1 full affine curvature from the corrected ECD torsion convention.
A diagnostic only: no modification of metric or spinor evolution equations.
"""
import argparse,itertools,json
from pathlib import Path
import numpy as np
from strong_benchmark import ecd,PlanarGrid,exact

EPS=np.zeros((4,4,4,4))
for perm in itertools.permutations(range(4)):
    EPS[perm]=(-1)**sum(perm[i]>perm[j] for i in range(4) for j in range(i+1,4))


def connection(grid,state):
    g,p,psi=state;dg,_=ecd.derivatives(grid,g,p)
    src=ecd.matter(g,dg,psi,grid.grad(psi),mass=0.);f=src['frame']
    Tframe=-.5*np.einsum('abcd,...d->...abc',EPS,src['axial'])
    C=.5*np.einsum('...rs,...as,...bm,...cn,...abc->...rmn',f['inv'],f['co'],f['co'],f['co'],Tframe,optimize=True)
    return f['connection']+C,f,src


def measure(grid,state,delta=1e-4):
    g=state[0];Gamma,f,src=connection(grid,state);tangent=ecd.rhs(grid,state,mass=0.)
    plus=tuple(a+delta*b for a,b in zip(state,tangent));minus=tuple(a-delta*b for a,b in zip(state,tangent))
    dt=(connection(grid,plus)[0]-connection(grid,minus)[0])/(2*delta)
    dGamma=np.concatenate([dt[...,None,:,:,:],grid.grad(Gamma)],axis=3)
    shape=g.shape[:-2];Riem=np.zeros(shape+(4,4,4,4))
    for mu in range(4):
        for nu in range(4):
            Riem[...,mu,nu]=dGamma[...,mu,:,nu,:]-dGamma[...,nu,:,mu,:]+Gamma[..., :,mu,:]@Gamma[..., :,nu,:]-Gamma[..., :,nu,:]@Gamma[..., :,mu,:]
    Ric=np.einsum('...rsrn->...sn',Riem);inv=f['inv'];scalar=np.einsum('...ab,...ab->...',inv,Ric)
    low=np.einsum('...ar,...rsmn->...asmn',g,Riem)
    raised=np.einsum('...ab,...cd,...ef,...gh,...bdfh->...aceg',inv,inv,inv,inv,low,optimize=True)
    K=np.einsum('...abcd,...abcd->...',low,raised)
    frame=np.einsum('...ma,...nb,...pc,...qd,...mnpq->...abcd',f['e'],f['e'],f['e'],f['e'],low,optimize=True)
    return {'delta':delta,'full_R_min':float(np.min(scalar)),'full_R_max':float(np.max(scalar)),'full_K_min':float(np.min(K)),'full_K_max':float(np.max(K)),'full_orthonormal_component_max_abs':float(np.max(abs(frame))),'torsion2_min':float(np.min(-1.5*src['axial2'])),'torsion2_max':float(np.max(-1.5*src['axial2'])),'scope':'Full affine Riemann. Time derivatives use a centered tangent-state difference; spatial derivatives use the existing FD operator. Lorentzian scalar contractions can cancel.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    grid=PlanarGrid(5);records=[]
    for volume in [1.,.5,.125]:
        t=-np.log(volume)/3;state,truth=exact(grid,t,D0=0.)
        for delta in [1e-3,5e-4,2.5e-4]:
            r=measure(grid,state,delta);r.update({'volume':volume,'harmonic_time':t,'exact_full_R':0.,'exact_full_K':128/volume**4,'exact_metric_R':-6/volume**2,'exact_metric_K':60/volume**4,'full_K_relative_error':abs(r['full_K_max']/(128/volume**4)-1)})
            records.append(r)
    from periodic_3d_data import construct
    spatial=[]
    for n in [9,17,33]:
        g,st,initial=construct(n=n)
        probes=[measure(g,st,d) for d in [1e-4,5e-5]]
        spatial.append({'n':n,'initial_data':initial,'curvature_probes':probes})
    report={'spatial_initial_data_checks':spatial,'hypothesis':'The full-connection scalar vanishes on the exact massless isotropic branch while full curvature nevertheless grows; an independent full-Riemann diagnostic must detect it.','parameters':{'n0':4.,'mass':0.,'D0':0.,'kappa':1.},'records':records,'classification':'Analytical exact benchmark with numerical diagnostic validation; not a proof that arbitrary ECD data reach unlimited compression or that finite invariants certify completeness.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
