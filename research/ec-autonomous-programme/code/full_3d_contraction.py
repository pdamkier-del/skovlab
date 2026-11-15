"""Short genuinely three-dimensional strong-curvature torus evolution.
Uses only the existing general ECD RHS/RK4 and the C04 constrained data family.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.signal import resample
from scipy.optimize import brentq
from periodic_3d_data import construct,ecd
from planar_contraction import source,stress_divergence,tangent_conservation,kinematics
from strong_benchmark import curvature


def run(n=17,steps=40,duration=.2):
    start=time.monotonic();grid,state,initial=construct(n=n);dt=duration/steps
    Q0=ecd.diagnostics(grid,state,mass=0.)['number'];rows=[];snap=[];maxcfl=0.
    def record(t):
        d=ecd.diagnostics(grid,state,mass=0.);dg,_=ecd.derivatives(grid,state[0],state[1]);kin=kinematics(state[0],dg,state[2],grid.grad(state[2]),mass=0.)
        if not np.all(kin['valid']):raise RuntimeError('Current rest frame unresolved.')
        r={'t':t,'Hamiltonian_relative':float(np.max(abs(d['hamiltonian']))/max(2*np.max(abs(d['E'])),1e-30)),'Hamiltonian_max':float(np.max(abs(d['hamiltonian']))),'momentum_max':float(np.max(abs(d['momentum']))),'harmonic_max':float(np.max(abs(d['harmonic']))),'charge_relative':d['number']/Q0-1,'Hnormal_min':float(np.min(d['H'])),'Hnormal_max':float(np.max(d['H'])),'Theta_current_min':float(np.min(kin['theta'])),'Theta_current_max':float(np.max(kin['theta'])),'lapse_min':float(np.min(d['lapse'])),'spatial_determinant_min':float(np.min(d['det_spatial'])),'density_min':float(np.min(kin['density'])),'density_max':float(np.max(kin['density'])),'slice_volume':float(np.sum(np.sqrt(d['det_spatial']))*grid.dx**3)}
        if not all(np.isfinite(x) for x in r.values()):raise FloatingPointError('Nonfinite diagnostic; no physical outcome.')
        if r['Hamiltonian_relative']>.05:raise RuntimeError('Declared 5% relative constraint stop.')
        if r['lapse_min']<.1:raise RuntimeError('Declared coordinate lapse stop.')
        rows.append(r)
    record(0.)
    for step in range(steps):
        maxcfl=max(maxcfl,dt/ecd.characteristic_step(grid,state[0]))
        if maxcfl>1:raise RuntimeError('Declared characteristic step bound exceeded.')
        state=ecd.rk4(grid,state,dt,mass=0.);record((step+1)*dt)
        if step>=steps-2:snap.append(source(grid,state))
    plus=source(grid,ecd.rk4(grid,state,dt,mass=0.));R,K=curvature(grid,state)
    conservation=stress_divergence(grid,[snap[0],snap[1],plus],dt)
    fields=[]
    for a in state:
        for axis in range(3):a=resample(a,17,axis=axis)
        fields.append(a)
    report={'n':n,'steps':steps,'dt':dt,'duration':duration,'initial_data':initial,'initial':rows[0],'final':rows[-1],'max_Hamiltonian_relative':max(x['Hamiltonian_relative'] for x in rows),'max_momentum':max(x['momentum_max'] for x in rows),'max_harmonic':max(x['harmonic_max'] for x in rows),'max_charge_drift':max(abs(x['charge_relative']) for x in rows),'max_Theta_current_over_time':max(x['Theta_current_max'] for x in rows),'max_Hnormal_over_time':max(x['Hnormal_max'] for x in rows),'max_CFL_ratio':maxcfl,'slice_volume_ratio':rows[-1]['slice_volume']/rows[0]['slice_volume'],'metric_R_range':[float(np.min(R)),float(np.max(R))],'metric_Kretschmann_max_abs':float(np.max(abs(K))),'conservation':conservation,'tangent_conservation':tangent_conservation(grid,state),'rows':rows[::max(1,steps//10)],'seconds':time.monotonic()-start,'status':'completed within declared finite-interval numerical controls'}
    return report,fields


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    report={'hypothesis':'The original full 3+1 tensor engine resolves a short strong-curvature contraction with genuine variation in all three spatial coordinates.','spatial_records':[],'scope':'Single neutral massless commuting Dirac field, periodic torus, C04 constrained seed; not arbitrary 3D stability or a physical finite cloud.'}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    def checkpoint():args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    states=[]
    for n in [9,17,33]:
        r,s=run(n=n);report['spatial_records'].append(r);states.append(s);checkpoint();print('completed full 3D n',n,'H',r['final']['Hamiltonian_relative'],flush=True)
    diff=[[float(np.sqrt(np.mean(abs(a-b)**2))) for a,b in zip(states[i],states[i+1])] for i in range(2)]
    report['spatial_successive_RMS_differences']=diff
    report['spatial_observed_orders']=[float(brentq(lambda p:(9**(-p)-17**(-p))/(17**(-p)-33**(-p))-diff[0][j]/diff[1][j],.1,8)) for j in range(3)]
    temporal=[];ts=[]
    for steps in [20,40,80]:
        if steps==40:r,s=report['spatial_records'][1],states[1]
        else:r,s=run(n=17,steps=steps)
        temporal.append(r);ts.append(s)
    err=[[float(np.sqrt(np.mean(abs(a-b)**2))) for a,b in zip(ts[i],ts[i+1])] for i in range(2)]
    report['temporal_records']=temporal;report['temporal_successive_RMS_differences']=err;report['temporal_ratios']=[err[0][j]/err[1][j] for j in range(3)]
    report['comparison']='All final fields Fourier-resampled to 17³ shared physical points; no spectral change to evolution.'
    checkpoint();print('wrote',args.output)
if __name__=='__main__':main()
