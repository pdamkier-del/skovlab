"""Raychaudhuri balance on saved full fields; no re-evolution or new forces.
The kinematic identity uses Levi-Civita curvature after eliminating EC torsion.
"""
import argparse,json,hashlib
from pathlib import Path
import numpy as np
from strong_benchmark import ecd
from planar_contraction import kinematics
from checkpoints import load_checkpoint


def kinetic(grid,state):
    g,p,psi=state;dg=np.concatenate([p[...,None,:,:],grid.grad(g)],axis=3)
    out=kinematics(g,dg,psi,grid.grad(psi),mass=0.)
    if not np.all(out['valid']):raise ValueError('No regular current frame for focusing diagnostic.')
    return out


def stats(a):return {'min':float(np.min(a)),'max':float(np.max(a)),'mean':float(np.mean(a)),'RMS':float(np.sqrt(np.mean(a*a)))}


def measure(grid,state,delta=1e-4):
    kin=kinetic(grid,state);tangent=ecd.rhs(grid,state,mass=0.)
    plus=kinetic(grid,tuple(a+delta*b for a,b in zip(state,tangent)))
    minus=kinetic(grid,tuple(a-delta*b for a,b in zip(state,tangent)))
    dt_theta=(plus['theta']-minus['theta'])/(2*delta)
    dt_a=(plus['acceleration']-minus['acceleration'])/(2*delta)
    g,p,psi=state;dg,dd=ecd.derivatives(grid,g,p);dd[...,0,0,:,:]=tangent[1]
    _,Ric,_=ecd.ricci_reduced(g,dg,dd);Gamma=ecd.christoffel(g,dg)
    u=kin['u'];theta=kin['theta'];a=kin['acceleration']
    theta_dot=u[...,0]*dt_theta+np.sum(u[...,1:]*grid.grad(theta),axis=-1)
    div_a=dt_a[...,0]+np.einsum('...ii->...',grid.grad(a)[..., :,1:])+np.einsum('...mml,...l->...',Gamma,a)
    Ruu=np.einsum('...a,...ab,...b->...',u,Ric,u)
    volume=-theta**2/3;shear=-kin['shear_norm'];rotation=kin['vorticity_norm']
    source=-(kin['energy_current_frame']+3*kin['mean_stress'])/2
    # Exact on-shell one-spinor source identity, NOT a fixed-data torsion-removal experiment.
    contact=-2*(3/16)*kin['density']**2;other=source-contact
    base=volume+shear+rotation+div_a
    geometric=base-Ruu;effective=base+source
    terms={'material_theta_dot':theta_dot,'volume_focusing':volume,'shear_focusing':shear,'vorticity_defocusing':rotation,'acceleration_divergence':div_a,'metric_Ricci_focusing':-Ruu,'effective_source_focusing':source,'explicit_contact_source_identity':contact,'other_source_identity':other,'geometric_identity_residual':theta_dot-geometric,'effective_source_balance_residual':theta_dot-effective,'Einstein_Ricci_source_mismatch':Ruu+source}
    out={'delta':delta,'terms':{name:stats(value) for name,value in terms.items()},'Theta_current':stats(theta),'normal_frame_lorentz_factor':stats(kin['W']),'interpretation':'Pointwise Levi-Civita current-Raychaudhuri balance on a saved semidiscrete state; tangent and spatial finite-difference errors are separate. Contact splitting is an on-shell source identity, not causal torsion attribution.'}
    return out


def main():
    p=argparse.ArgumentParser();p.add_argument('--input',type=Path,required=True);p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    run=json.loads(args.input.read_text());root=Path(__file__).resolve().parents[1]
    if len(run['spatial_records'])!=3:raise ValueError('Wait for the completed three-resolution C08 dataset.')
    records=[]
    for row in run['spatial_records']:
        endpoint=[a for a in row['checkpoint_manifest'] if a['status']=='completed'][-1]
        path=root/endpoint['path']
        if hashlib.sha256(path.read_bytes()).hexdigest()!=endpoint['sha256']:raise ValueError('Checkpoint file hash does not match evolution manifest.')
        grid,state,metadata=load_checkpoint(path)
        probes=[measure(grid,state,d) for d in [1e-4,5e-5]]
        records.append({'n':grid.n,'time':metadata['coordinate_time'],'checkpoint':endpoint['path'],'file_sha256':endpoint['sha256'],'probes':probes})
        print('processed focusing n',grid.n,flush=True)
    errors=[r['probes'][-1]['terms']['geometric_identity_residual']['RMS'] for r in records]
    source_errors=[r['probes'][-1]['terms']['effective_source_balance_residual']['RMS'] for r in records]
    orders=lambda a:[float(np.log(a[i]/a[i+1])/np.log(records[i+1]['n']/records[i]['n'])) for i in range(2)]
    result={'geometric_residual_observed_orders':orders(errors),'source_balance_residual_observed_orders':orders(source_errors),'averaging':'Arithmetic coordinate-grid means and RMS; no proper-volume weighting.','hypothesis':'Identify which current-Raychaudhuri terms dominate the observed spin-texture contraction, with a separately measured geometric identity and Einstein-source replacement.','records':records,'no_re_evolution':True,'scope':'Massless kappa1, single regular commuting spinor, C08 finite-time periodic family. No global turn, quantum state or matched torsion-free comparison.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n');print('wrote',args.output)
if __name__=='__main__':main()
