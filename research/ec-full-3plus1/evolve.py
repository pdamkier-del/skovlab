"""Short-time full 3+1 ECD research runs, with explicit verification stops."""
import argparse,json,platform,time
from pathlib import Path
import numpy as np
from ecd import Grid,rk4,diagnostics,characteristic_step
from initial_data import seed_spinor,solve_constraints


def evolve(n=9,half_width=4.,amplitude=.025,radius=2.5,mass=.1,phase=0.,spin_twist=.7,K0=.002,duration=.02,dt=.005):
    values=[half_width,amplitude,radius,mass,phase,spin_twist,K0,duration,dt]
    if not all(np.isfinite(v) for v in values):raise ValueError('All parameters must be finite.')
    if not isinstance(n,int) or n<7 or n>25 or n%2!=1:raise ValueError('Use odd grid size 7..25.')
    if not (2<=half_width<=20 and 0<=amplitude<=.05 and .5<=radius<half_width/1.15 and 0<=mass<=1 and abs(phase)<=1 and abs(spin_twist)<=3 and abs(K0)<=.01 and 0<duration<=.1 and 0<dt<=min(.01,duration)):raise ValueError('Parameters exceed the supported short-time weak-field experiment range.')
    start=time.monotonic();grid=Grid(n,half_width);seed=seed_spinor(grid,amplitude,radius,phase)
    angle=spin_twist*grid.xyz[...,0]/(2*radius);c=np.cos(angle);s=np.sin(angle)
    for a,b in [(0,1),(2,3)]:
        olda=seed[...,a].copy();oldb=seed[...,b].copy();seed[...,a]=c*olda-s*oldb;seed[...,b]=s*olda+c*oldb
    # A declared free mean-curvature profile, not an independently imposed Hubble rate.
    Ktrace=K0*np.exp(-np.sum(grid.xyz**2,axis=-1)/2)
    state,initial=solve_constraints(grid,seed,Ktrace,mass=mass)
    core=(slice(2,-2),)*3;center=(n//2,)*3;rows=[];t=0.;reason='requested-time-completed';number0=None
    def record():
        nonlocal number0
        d=diagnostics(grid,state,mass=mass)
        if number0 is None:number0=d['number']
        E=d['E'][core];H=d['H'][core]
        # Fixed scale from initial matter density, never reset to hide constraint growth.
        scale=max(rows[0]['energy_max']*2 if rows else np.max(np.abs(E))*2,1e-12)
        row={'t':t,'energy_max':float(np.max(E)),'H_center':float(d['H'][center]),'H_min':float(np.min(H)),'H_max':float(np.max(H)),
             'hamiltonian_max':float(np.max(np.abs(d['hamiltonian'][core]))),'momentum_max':float(np.max(np.abs(d['momentum'][core]))),
             'harmonic_max':float(np.max(np.abs(d['harmonic'][core]))),'number':d['number'],'relative_number_change':float((d['number']-number0)/max(abs(number0),1e-30)),
             'axial_abs_max':float(np.sqrt(np.max(np.abs(d['axial2'][core])))),
             'friedmann_identity_error':float(np.max(np.abs(d['friedmann_residual'][core]-d['hamiltonian'][core]))),
             'lapse_min':float(np.min(d['lapse'])),'constraint_scaled':float(np.max(np.abs(d['hamiltonian'][core]))/scale),
             'energy_xy':d['E'][:,:,n//2].tolist(),'H_xy':d['H'][:,:,n//2].tolist()}
        if not all(np.isfinite(v) for v in row.values() if isinstance(v,(int,float))):raise ValueError('Nonfinite diagnostics; no physical result.')
        rows.append(row);return row
    last=record()
    while t<duration-1e-14:
        if last['constraint_scaled']>.05:reason='constraint-limit';break
        if last['lapse_min']<.2:reason='coordinate-limit';break
        if last['energy_max']>.01 or last['axial_abs_max']>.1:reason='operational-field-limit';break
        h=min(dt,duration-t,characteristic_step(grid,state[0]))
        try:state=rk4(grid,state,h,mass=mass)
        except (np.linalg.LinAlgError,ValueError,FloatingPointError):reason='numerical-error';break
        t+=h;last=record()
    if reason=='requested-time-completed' and last['constraint_scaled']>.05:reason='constraint-limit'
    result={'model':'General spatially varying classical neutral ECD; harmonic-coordinate 3+1 prototype',
            'status':reason,'parameters':dict(n=n,half_width=half_width,amplitude=amplitude,radius=radius,mass=mass,phase=phase,spin_twist=spin_twist,K0=K0,duration=duration,dt=dt),
            'units':'c = hbar = kappa = 1','initial_constraints':initial,'rows':rows,
            'scope':['All 10 metric components, their 10 time derivatives, and 4 complex spinor components evolve on a 3D grid.',
                     'No spatial symmetry, spin averaging, perfect-fluid closure, or imposed bounce force.',
                     'Only a finite cube with prescribed outer metric velocity and spinor data; no constraint-preserving exterior construction.',
                     'Reported extrema exclude two outer grid layers. This does not prove causal insulation for all numerical modes.',
                     'No tracked material volume, ADM mass at infinity, global bounce, horizon or singularity conclusion.',
                     'Short weak-field tests do not establish nonlinear stability for strong collapse.'],
            'bounce':'not-assessed','elapsed_seconds':round(time.monotonic()-start,3),'python':platform.python_version(),'numpy':np.__version__}
    return result,state


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--n',type=int,default=9);parser.add_argument('--duration',type=float,default=.02);parser.add_argument('--dt',type=float,default=.005);parser.add_argument('--output',type=Path,default=Path('solution.json'));parser.add_argument('--fields',type=Path)
    args=parser.parse_args();result,state=evolve(n=args.n,duration=args.duration,dt=args.dt)
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    if args.fields:np.savez_compressed(args.fields,g=state[0],metric_time_derivative=state[1],psi=state[2],parameters=json.dumps(result['parameters']))
    print(result['status'],result['elapsed_seconds'],'s;',args.output)
