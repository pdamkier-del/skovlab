"""Periodic constrained massless ECD data and convergent planar strong contraction.
A 1+1 symmetry benchmark evaluated by the existing general 3+1 tensor/RK engine.
"""
import argparse,json,time,platform
from pathlib import Path
import numpy as np
import scipy
from scipy.integrate import solve_bvp
from scipy.signal import resample
from scipy.optimize import brentq
import sys
sys.path.insert(0,str(Path(__file__).resolve().parents[2]/'ec-general-investigation'))
from kinematics import kinematics
from strong_benchmark import ecd,PlanarGrid,diagnostic,curvature


def periodic_data(n0=4.,epsilon=.02,length=8.,tolerance=1e-11,mode=1):
    if n0<=0 or not 0<=abs(epsilon)<1 or length<=0:raise ValueError('Require positive density/length and |epsilon|<1.')
    GA=3/16
    def seed(z):return n0*(1+epsilon*np.cos(2*np.pi*mode*z/length))
    def fun(z,y,p):
        u,du,I=y;K=np.exp(p[0])
        return np.array([du,K*K/12*np.exp(4*u)-GA/4*seed(z)**2*np.exp(-8*u)-du*du,u])
    def bc(a,b,p):return np.array([a[0]-b[0],a[1]-b[1],a[2],b[2]])
    z=np.linspace(-length/2,length/2,81)
    result=solve_bvp(fun,bc,z,np.zeros((3,len(z))),p=[np.log(.75*n0)],tol=tolerance,max_nodes=20000)
    if not result.success:raise RuntimeError('Periodic continuum BVP did not converge: '+result.message)
    return result,{'n0':n0,'epsilon':epsilon,'length':length,'tolerance':tolerance,'Ktrace':float(np.exp(result.p[0])),'BVP_nodes':len(result.x),'max_BVP_RMS_residual':float(np.max(result.rms_residuals)),'mode':mode}


def sample_data(grid,solution,parameters):
    z=grid.xyz[...,2];u=solution.sol(z.ravel())[0].reshape(z.shape);chi=np.exp(u)
    seed=parameters['n0']*(1+parameters['epsilon']*np.cos(2*np.pi*parameters.get('mode',1)*z/parameters['length']))
    g=np.broadcast_to(np.diag(ecd.ETA),z.shape+(4,4)).copy();g[...,1:,1:]=np.eye(3)*chi[...,None,None]**4
    K=g[...,1:,1:]*parameters['Ktrace']/3
    p=ecd.harmonic_initial_velocity(grid,g,K)
    psi=np.zeros(z.shape+(4,),complex);psi[...,2]=np.sqrt(seed)*chi**-3
    return g,p,psi


def source(grid,state):
    dg,_=ecd.derivatives(grid,state[0],state[1]);s=ecd.matter(state[0],dg,state[2],grid.grad(state[2]),mass=0.)
    inv=s['frame']['inv'];return inv@s['stress']@inv,s['frame']['connection'],s


def stress_divergence(grid,snap,dt):
    """Centered evolved-state time difference and full covariant divergence."""
    T,con,_=snap[1];time=(snap[2][0]-snap[0][0])/(2*dt);ds=grid.grad(T)
    divergence=time[...,0,:]+np.einsum('...iin->...n',ds[..., :,1:,:])+np.einsum('...mml,...ln->...n',con,T)+np.einsum('...nml,...ml->...n',con,T)
    terms=[time[...,0,:],np.einsum('...iin->...n',ds[..., :,1:,:]),np.einsum('...mml,...ln->...n',con,T),np.einsum('...nml,...ml->...n',con,T)]
    scale=max(sum(float(np.sqrt(np.mean(x*x))) for x in terms),1e-30)
    return {'stress_divergence_RMS':float(np.sqrt(np.mean(divergence**2))),'stress_divergence_relative_RMS':float(np.sqrt(np.mean(divergence**2))/scale)}


def tangent_conservation(grid,state):
    """Independent local tangent derivative; separate from evolved snapshot differences."""
    tangent=ecd.rhs(grid,state,mass=0.);reports=[]
    for delta in [1e-5,5e-6]:
        plus=tuple(a+delta*b for a,b in zip(state,tangent));minus=tuple(a-delta*b for a,b in zip(state,tangent))
        reports.append(stress_divergence(grid,[source(grid,minus),source(grid,state),source(grid,plus)],delta))
    return {'deltas':[1e-5,5e-6],'records':reports,'interpretation':'Chain derivative of the semidiscrete full stress along its evolved-state RHS; not an extra evolution or a replacement for snapshot conservation.'}


def run(n=33,steps=160,duration=.45,solution=None,parameters=None,keep_fields=False):
    start=time.monotonic()
    if solution is None:solution,parameters=periodic_data()
    grid=PlanarGrid(n,parameters['length']/2);state=sample_data(grid,solution,parameters);dt=duration/steps
    initial=diagnostic(grid,state);Q0=initial['number'];rows=[];snap=[];maxcfl=0.;maxcharge=0.
    def row(t):
        d=diagnostic(grid,state)
        dg,_=ecd.derivatives(grid,state[0],state[1]);kin=kinematics(state[0],dg,state[2],grid.grad(state[2]),mass=0.)
        if not np.all(kin['valid']):raise RuntimeError('Current rest frame is not regular.')
        return {'t':t,'Theta_current_min':float(np.min(kin['theta'])),'Theta_current_max':float(np.max(kin['theta'])),'current_density_min':float(np.min(kin['density'])),'current_density_max':float(np.max(kin['density'])),'Hamiltonian_max':float(np.max(abs(d['hamiltonian']))),'Hamiltonian_relative':float(np.max(abs(d['hamiltonian']))/max(2*np.max(abs(d['E'])),1e-30)),'momentum_max':float(np.max(abs(d['momentum']))),'harmonic_max':float(np.max(abs(d['harmonic']))),'charge_relative':d['number']/Q0-1,'Hnormal_min':float(np.min(d['H'])),'Hnormal_max':float(np.max(d['H'])),'lapse_min':float(np.min(d['lapse'])),'energy_max':float(np.max(d['E'])),'proper_slice_volume':float(np.sum(np.sqrt(d['det_spatial']))*grid.dx*parameters['length']**2)}
    rows.append(row(0.))
    for step in range(steps):
        maxcfl=max(maxcfl,dt/ecd.characteristic_step(grid,state[0]))
        if maxcfl>1:raise RuntimeError('Chosen timestep exceeds declared characteristic bound.')
        state=ecd.rk4(grid,state,dt,mass=0.)
        d=row((step+1)*dt);rows.append(d);maxcharge=max(maxcharge,abs(d['charge_relative']))
        if not all(np.isfinite(x) for x in d.values()):raise FloatingPointError('Nonfinite diagnostic; no physical conclusion.')
        if d['lapse_min']<.05:raise RuntimeError('Declared coordinate-conditioning limit reached.')
        if step>=steps-3:snap.append(source(grid,state))
    R,K=curvature(grid,state);_,_,src=snap[-1];A2=src['axial2'];torsion2=-1.5*A2
    # Trace equation evaluated against a metric-Riemann calculation (RHS supplies g_tt).
    trace_defect=R+2*(3/16)*A2
    fields=tuple(resample(x,65,axis=2) for x in state)
    out={'n':n,'steps':steps,'dt':dt,'duration':duration,'initial_data':parameters,'initial':rows[0],'final':rows[-1],'max_charge_drift':maxcharge,'max_Hamiltonian_relative':max(x['Hamiltonian_relative'] for x in rows),'max_momentum':max(x['momentum_max'] for x in rows),'max_harmonic':max(x['harmonic_max'] for x in rows),'max_dt_over_characteristic_bound':maxcfl,'min_Hnormal_max_over_time':min(x['Hnormal_max'] for x in rows),'max_Hnormal_over_time':max(x['Hnormal_max'] for x in rows),'max_Theta_current_over_time':max(x['Theta_current_max'] for x in rows),'curvature':{'metric_R_min':float(np.min(R)),'metric_R_max':float(np.max(R)),'metric_Kretschmann_max_abs':float(np.max(abs(K))),'torsion2_min':float(np.min(torsion2)),'torsion2_max':float(np.max(torsion2)),'trace_identity_max_abs':float(np.max(abs(trace_defect))),'interpretation':'Finite endpoint only; no regularity/completeness theorem. Time-second metric jets use the evolution RHS.'},'conservation':stress_divergence(grid,[snap[-2],snap[-1],source(grid,ecd.rk4(grid,state,dt,mass=0.))],dt),'tangent_conservation':tangent_conservation(grid,state),'seconds':time.monotonic()-start,'rows':rows[::max(1,steps//10)]}
    if keep_fields:return out,fields,state
    return out,fields


def lift_check(solution,parameters):
    a=PlanarGrid(9,parameters['length']/2);b=ecd.Grid(9,parameters['length']/2,'periodic')
    sa=sample_data(a,solution,parameters);sb=sample_data(b,solution,parameters)
    errors=[]
    for f,g in zip(ecd.rhs(a,sa,mass=0.),ecd.rhs(b,sb,mass=0.)):
        errors.append(float(np.max(abs(g-np.broadcast_to(f,g.shape)))))
    for f,g in zip(ecd.rk4(a,sa,.001,mass=0.),ecd.rk4(b,sb,.001,mass=0.)):
        errors.append(float(np.max(abs(g-np.broadcast_to(f,g.shape)))))
    return {'grid':9,'RHS_and_RK_step_max_absolute_differences':errors,'restriction':'A lift check verifies translation-invariant implementation equivalence, not transverse stability.'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    sol,params=periodic_data();records=[];states=[]
    for n in [17,33,65,129]:
        r,st=run(n=n,steps=240,solution=sol,parameters=params);records.append(r);states.append(st)
        print('completed spatial n=',n,'H error=',r['final']['Hamiltonian_relative'],flush=True)
    differences=[[float(np.sqrt(np.mean(abs(a-b)**2))) for a,b in zip(states[i],states[i+1])] for i in range(len(states)-1)]
    orders=[[float(brentq(lambda p:(records[i]['n']**(-p)-records[i+1]['n']**(-p))/(records[i+1]['n']**(-p)-records[i+2]['n']**(-p))-differences[i][j]/differences[i+1][j],.1,8)) for j in range(3)] for i in range(2)]
    # Separate same-grid temporal differences; no substitution for spatial refinement.
    temporal=[];ts=[]
    for steps in [60,120,240]:
        r,st=run(n=65,steps=steps,solution=sol,parameters=params);temporal.append(r);ts.append(st)
    terr=[[float(np.sqrt(np.mean(abs(a-b)**2))) for a,b in zip(ts[i],ts[i+1])] for i in range(2)]
    report={'hypothesis':'A periodic constrained planar perturbation of the massless contracting branch is resolved at strong curvature over t in [0,.45].','environment':{'python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__},'initial_data':params,'spatial_records':records,'comparison':'Fourier resampling each final field onto 65 shared uniform physical locations on the same torus.','spatial_successive_RMS_differences':differences,'spatial_observed_orders':orders,'temporal_records':temporal,'temporal_successive_RMS_differences':terr,'temporal_ratios':[terr[0][j]/terr[1][j] for j in range(3)],'full_grid_lift':lift_check(sol,params),'scope':'Planar periodic classical single-field benchmark. No general 3D stability, material bounce, finite cloud or physical EFT conclusion.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');print('wrote',args.output)
if __name__=='__main__':main()
