"""Short genuinely three-dimensional strong-curvature torus evolution.
Uses the unchanged general ECD RHS/RK4, C07 spin texture, and lossless checkpoints.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.signal import resample
from scipy.optimize import brentq
from spin_texture_data import construct,ecd
from checkpoints import save_checkpoint,load_checkpoint
from torsion_curvature import measure as full_curvature
import hashlib,os,platform,scipy
from planar_contraction import source,stress_divergence,tangent_conservation,kinematics
from strong_benchmark import curvature


PROGRAMME=Path(__file__).resolve().parents[1]
CODE_HASHES={name:hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest() for name in ['spin_texture_evolution.py','spin_texture_data.py','checkpoints.py','torsion_curvature.py','strong_benchmark.py','periodic_3d_data.py','planar_contraction.py']}
CODE_HASHES['kinematics.py']=hashlib.sha256((PROGRAMME.parent/'ec-general-investigation'/'kinematics.py').read_bytes()).hexdigest()
CODE_HASHES['ecd.py']=hashlib.sha256((PROGRAMME.parent/'ec-full-3plus1'/'ecd.py').read_bytes()).hexdigest()

def run(n=17,steps=40,duration=.2,spin_amplitude=.2,checkpoint_root=None):
    if steps<2 or duration<=0:raise ValueError('Positive duration and at least two steps required.')
    start=time.monotonic();grid,state,initial=construct(n=n,spin_amplitude=spin_amplitude);dt=duration/steps
    config={'parameters':initial['parameters'],'n':n,'steps':steps,'duration':duration,'dt':dt,'code_sha256':CODE_HASHES,'environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},'baseline_commit':'c9926a3f6edb4730a87f5f5da4dbe1aa367bbb82'}
    run_id=hashlib.sha256(json.dumps(config,sort_keys=True).encode()).hexdigest()[:12]
    checkpoints=[];curvature_records=[]
    def persist(step,status='checkpoint',reason=None,probe=True):
        if checkpoint_root is None:return
        path=Path(checkpoint_root)/f'n{n}_s{steps}_{run_id}'/f'step{step:05d}_{status}.npz'
        save_checkpoint(path,grid,state,time=step*dt,step=step,config=config,status=status,reason=reason)
        check_grid,check_state,metadata=load_checkpoint(path,allow_rejected=True)
        checkpoints.append({'path':os.path.relpath(path,PROGRAMME),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'bytes':path.stat().st_size,'time':step*dt,'step':step,'status':status,'reason':reason,'field_hashes':metadata['field_hashes']})
        if probe and status!='rejected':
            probes=[full_curvature(check_grid,check_state,delta) for delta in [1e-4,5e-5]]
            curvature_records.append({'time':step*dt,'checkpoint':os.path.relpath(path,PROGRAMME),'probes':probes})
    Q0=ecd.diagnostics(grid,state,mass=0.)['number'];rows=[];snap=[];maxcfl=0.
    def record(t):
        d=ecd.diagnostics(grid,state,mass=0.);dg,_=ecd.derivatives(grid,state[0],state[1]);kin=kinematics(state[0],dg,state[2],grid.grad(state[2]),mass=0.)
        if not np.all(kin['valid']):raise RuntimeError('Current rest frame unresolved.')
        r={'t':t,'Hamiltonian_relative':float(np.max(abs(d['hamiltonian']))/max(2*np.max(abs(d['E'])),1e-30)),'Hamiltonian_max':float(np.max(abs(d['hamiltonian']))),'momentum_max':float(np.max(abs(d['momentum']))),'harmonic_max':float(np.max(abs(d['harmonic']))),'charge_relative':d['number']/Q0-1,'Hnormal_min':float(np.min(d['H'])),'Hnormal_max':float(np.max(d['H'])),'Theta_current_min':float(np.min(kin['theta'])),'Theta_current_max':float(np.max(kin['theta'])),'lapse_min':float(np.min(d['lapse'])),'spatial_determinant_min':float(np.min(d['det_spatial'])),'density_min':float(np.min(kin['density'])),'density_max':float(np.max(kin['density'])),'slice_volume':float(np.sum(np.sqrt(d['det_spatial']))*grid.dx**3)}
        if not all(np.isfinite(x) for x in r.values()):raise FloatingPointError('Nonfinite diagnostic; no physical outcome.')
        if r['Hamiltonian_relative']>.05:raise RuntimeError('Declared 5% relative constraint stop.')
        if r['lapse_min']<.1:raise RuntimeError('Declared coordinate lapse stop.')
        rows.append(r)
    record(0.);persist(0,'initial')
    status='completed within declared finite-interval numerical controls';reason=None;completed_steps=0
    for step in range(steps):
        maxcfl=max(maxcfl,dt/ecd.characteristic_step(grid,state[0]))
        if maxcfl>1:
            status='inconclusive numerical stop';reason='Declared characteristic step bound exceeded.';persist(step,'checkpoint',reason,probe=False);break
        previous=state
        try:
            state=ecd.rk4(grid,state,dt,mass=0.);record((step+1)*dt)
        except (RuntimeError,ValueError,FloatingPointError,np.linalg.LinAlgError) as exc:
            status='inconclusive numerical/coordinate stop';reason=str(exc)
            try:persist(step+1,'rejected',reason,probe=False)
            except ValueError:pass
            state=previous;persist(step,'checkpoint','last accepted before: '+reason,probe=False);break
        completed_steps=step+1
        if completed_steps in [steps//2,steps]:persist(completed_steps,'completed' if completed_steps==steps else 'checkpoint')
        if step>=steps-2:snap.append(source(grid,state))
    R,K=curvature(grid,state)
    conservation=None
    if completed_steps==steps:
        plus=source(grid,ecd.rk4(grid,state,dt,mass=0.));conservation=stress_divergence(grid,[snap[0],snap[1],plus],dt)
    fields=[]
    for a in state:
        for axis in range(3):a=resample(a,17,axis=axis)
        fields.append(a)
    report={'checkpoint_manifest':checkpoints,'full_curvature_history':curvature_records,'completed_steps':completed_steps,'termination_reason':reason,'n':n,'steps':steps,'dt':dt,'duration':duration,'initial_data':initial,'initial':rows[0],'final':rows[-1],'max_Hamiltonian_relative':max(x['Hamiltonian_relative'] for x in rows),'max_momentum':max(x['momentum_max'] for x in rows),'max_harmonic':max(x['harmonic_max'] for x in rows),'max_charge_drift':max(abs(x['charge_relative']) for x in rows),'max_Theta_current_over_time':max(x['Theta_current_max'] for x in rows),'max_Hnormal_over_time':max(x['Hnormal_max'] for x in rows),'max_CFL_ratio':maxcfl,'slice_volume_ratio':rows[-1]['slice_volume']/rows[0]['slice_volume'],'metric_R_range':[float(np.min(R)),float(np.max(R))],'metric_Kretschmann_max_abs':float(np.max(abs(K))),'conservation':conservation,'tangent_conservation':tangent_conservation(grid,state),'rows':rows[::max(1,steps//10)],'seconds':time.monotonic()-start,'status':status}
    return report,fields


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--checkpoints',type=Path,required=True);args=p.parse_args()
    report={'hypothesis':'A constrained real spatial spin texture remains resolved during short full 3D contraction, with full field persistence and full torsionful curvature probes.','spatial_records':[],'scope':'Single massless classical ECD field, L=8, theta=.2 sin(kx), periodic 3D seed; no physical quantum-state, finite-cloud or general-stability claim.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    def checkpoint():args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    states=[]
    for n in [9,17,33]:
        r,s=run(n=n,checkpoint_root=args.checkpoints);report['spatial_records'].append(r);states.append(s);checkpoint();
        if r['completed_steps']!=r['steps']:return
        print('completed full 3D n',n,'H',r['final']['Hamiltonian_relative'],flush=True)
    diff=[[float(np.sqrt(np.mean(abs(a-b)**2))) for a,b in zip(states[i],states[i+1])] for i in range(2)]
    report['spatial_successive_RMS_differences']=diff
    report['spatial_observed_orders']=[float(brentq(lambda p:(9**(-p)-17**(-p))/(17**(-p)-33**(-p))-diff[0][j]/diff[1][j],.1,8)) for j in range(3)]
    temporal=[];ts=[]
    for steps in [20,40,80]:
        if steps==40:r,s=report['spatial_records'][1],states[1]
        else:r,s=run(n=17,steps=steps,checkpoint_root=args.checkpoints)
        temporal.append(r);ts.append(s)
    err=[[float(np.sqrt(np.mean(abs(a-b)**2))) for a,b in zip(ts[i],ts[i+1])] for i in range(2)]
    report['temporal_records']=temporal;report['temporal_successive_RMS_differences']=err;report['temporal_ratios']=[err[0][j]/err[1][j] for j in range(3)]
    prior=json.loads((PROGRAMME/'results'/'cycle05_full3d.json').read_text())
    report['matched_fixed_polarization_comparison']=[{'n':a['n'],'theta0_volume_ratio':b['slice_volume_ratio'],'theta02_volume_ratio':a['slice_volume_ratio'],'difference':a['slice_volume_ratio']-b['slice_volume_ratio'],'restrictions':'Same n_seed and classical charge; constraints resolved separately; different spin states. Not torsion-free attribution.'} for a,b in zip(report['spatial_records'],prior['spatial_records'])]
    report['comparison']='All final fields Fourier-resampled to 17³ shared physical points; no spectral change to evolution. Original full fields persist in the checkpoint manifest.' 
    checkpoint();print('wrote',args.output)
if __name__=='__main__':main()
