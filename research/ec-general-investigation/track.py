"""Passive material/normal e-fold tracking on the existing 3D ECD evolution.
No new forces, closures or extrapolation beyond its short weak-field regime.
"""
import argparse,json
from pathlib import Path
import numpy as np
from kinematics import ecd,kinematics,normal_kinematics,efolds_from_density
from initial_data import solve_constraints


def interpolate(grid,array,points):
    """Trilinear primitive reconstruction and its exact piecewise derivatives."""
    points=np.atleast_2d(np.asarray(points,float))
    if np.any(np.abs(points)>grid.half_width):raise ValueError('Trajectory left the numerical domain.')
    q=(points+grid.half_width)/grid.dx;base=np.minimum(np.floor(q).astype(int),grid.n-2);f=q-base
    shape=(len(points),)+array.shape[3:];value=np.zeros(shape,dtype=array.dtype);grad=np.zeros((len(points),3)+array.shape[3:],dtype=array.dtype)
    extra=(None,)*(array.ndim-3)
    for i in range(2):
        for j in range(2):
            for k in range(2):
                bit=np.array([i,j,k]);w=np.where(bit,f,1-f);a=array[base[:,0]+i,base[:,1]+j,base[:,2]+k]
                weight=np.prod(w,axis=1);value+=a*weight[(slice(None),)+extra]
                for axis in range(3):
                    other=[b for b in range(3) if b!=axis];dw=(1 if bit[axis] else -1)*np.prod(w[:,other],axis=1)/grid.dx
                    grad[:,axis]+=a*dw[(slice(None),)+extra]
    return value,grad


def at_points(grid,state,field_rhs,points,mass=.1):
    g,dgspace=interpolate(grid,state[0],points);p,_=interpolate(grid,state[1],points)
    psi,ds=interpolate(grid,state[2],points);dtpsi,_=interpolate(grid,field_rhs[2],points)
    dg=np.concatenate([p[:,None],dgspace],axis=1)
    result=kinematics(g,dg,psi,ds,mass=mass,dt_psi=dtpsi)
    if not np.all(result['valid']):raise ValueError('Material current frame is zero, null or numerically unresolved.')
    return result


def tracer_rhs(grid,state,fields,material,normal,mass=.1):
    a=at_points(grid,state,fields,material[:,:3],mass)
    ng,nd=interpolate(grid,state[0],normal[:,:3]);np_,_=interpolate(grid,state[1],normal[:,:3])
    b=normal_kinematics(ng,np.concatenate([np_[:,None],nd],axis=1))
    rate=a['matter_efold_coordinate_rate'];J=material[:,8:].reshape(-1,3,3)
    out=np.zeros_like(material);out[:,:3]=a['velocity'];out[:,3]=1/a['u'][:,0];out[:,4]=rate
    out[:,5]=np.maximum(rate,0);out[:,6]=np.maximum(-rate,0);out[:,7]=a['continuity_efold_coordinate_defect'];out[:,8:]=(a['velocity_gradient']@J).reshape(-1,9)
    no=np.zeros_like(normal);no[:,:3]=-b['beta'];no[:,3]=b['lapse'];no[:,4]=b['normal_efold_coordinate_rate']
    return out,no


def coupled_step(grid,state,material,normal,dt,mass=.1):
    """The field stages exactly match ecd.rk4; only passive variables are added."""
    def stage(base,k,h):
        vals=[]
        for index,(a,b) in enumerate(zip(base,k)):
            v=a+h*b if index==0 else a.copy()
            if index:v[grid.interior]=a[grid.interior]+h*b[grid.interior]
            vals.append(v)
        return tuple(vals)
    states=[state];flows=[material];normals=[normal];ks=[];km=[];kn=[]
    for i in range(4):
        f=ecd.rhs(grid,states[i],mass=mass);a,b=tracer_rhs(grid,states[i],f,flows[i],normals[i],mass)
        ks.append(f);km.append(a);kn.append(b)
        if i<3:
            h=dt/2 if i<2 else dt
            states.append(stage(state,f,h));flows.append(material+h*a);normals.append(normal+h*b)
    fields=tuple((ks[0][j]+2*ks[1][j]+2*ks[2][j]+ks[3][j])/6 for j in range(3))
    return stage(state,fields,dt),material+dt*(km[0]+2*km[1]+2*km[2]+km[3])/6,normal+dt*(kn[0]+2*kn[1]+2*kn[2]+kn[3])/6


def run(n=9,duration=.02,dt=.005):
    if n not in [7,9,13,17] or not 0<duration<=.02 or not 0<dt<=.005:raise ValueError('Tracking audit is restricted to declared short weak-field tests.')
    grid=ecd.Grid(n);state,initial=solve_constraints(grid)
    positions=np.array([[.2,.3,.1],[-.3,.1,-.2],[.1,-.2,.3]])
    material=np.zeros((len(positions),17));material[:,:3]=positions;material[:,8:]=np.eye(3).reshape(1,9)
    normal=np.zeros((len(positions),5));normal[:,:3]=positions
    first=at_points(grid,state,ecd.rhs(grid,state),positions)
    initial_rest_inverse=np.linalg.inv(np.linalg.cholesky(first['rest_metric']).swapaxes(-1,-2))
    t=0.;rows=[];status='requested-time-completed';scale=None
    def record():
        nonlocal scale
        a=at_points(grid,state,ecd.rhs(grid,state),material[:,:3]);J=material[:,8:].reshape(-1,3,3)
        gram=J.swapaxes(-1,-2)@a['rest_metric']@J;C=initial_rest_inverse.swapaxes(-1,-2)@gram@initial_rest_inverse
        eigen=np.linalg.eigvalsh(C)
        if np.any(eigen<=0) or np.any(np.linalg.det(J)<=0):raise ValueError('Unresolved or nonpositive material deformation.')
        directional=.5*np.log(eigen);volume=directional.sum(axis=-1)/3
        sliced=(np.log(np.linalg.det(J))+.5*np.log(np.linalg.det(a['spatial_metric']))-.5*np.log(np.linalg.det(first['spatial_metric'])))/3
        density=efolds_from_density(first['density'],a['density'])
        d=ecd.diagnostics(grid,state);core=(slice(2,-2),)*3
        if scale is None:scale=max(2*float(np.max(np.abs(d['E'][core]))),1e-12)
        rows.append({'t':t,'proper_time':material[:,3].tolist(),'position':material[:,:3].tolist(),
            'N_material_integral':material[:,4].tolist(),'N_expansion':material[:,5].tolist(),'N_contraction_magnitude':material[:,6].tolist(),
            'N_density_reference':density.tolist(),'N_geometric_rest_volume':volume.tolist(),'N_slice_volume':sliced.tolist(),
            'N_directional_principal_stretches':directional.tolist(),'W':a['W'].tolist(),'N_normal':normal[:,4].tolist(),
            'normal_proper_time':normal[:,3].tolist(),'normal_position':normal[:,:3].tolist(),
            'continuity_integral_defect':material[:,7].tolist(),'material_expansion':a['theta'].tolist(),
            'volume_integral_error':(volume-material[:,4]).tolist(),
            'density_continuity_balance_error':(material[:,4]-density-material[:,7]).tolist(),
            'tilt_volume_identity_error':(volume-sliced-np.log(a['W']/first['W'])/3).tolist(),
            'constraint_scaled':float(np.max(np.abs(d['hamiltonian'][core]))/scale)})
    record()
    while t<duration-1e-14:
        if rows[-1]['constraint_scaled']>.05:status='constraint-limit';break
        h=min(dt,duration-t,ecd.characteristic_step(grid,state[0]))
        try:state,material,normal=coupled_step(grid,state,material,normal,h)
        except (ValueError,np.linalg.LinAlgError):status='trajectory-or-numerical-limit';break
        t+=h;record()
    if rows[-1]['constraint_scaled']>.05:status='constraint-limit'
    return {'status':status,'model':'single neutral classical ECD; passive weak-field tracking','units':'c = hbar = kappa = 1 (reduced Planck units)',
        'parameters':{'n':n,'half_width':4,'duration':duration,'dt':dt,'mass':.1,'kappa':1.,'seed_amplitude':.025,'seed_radius':2.5,'additional_spin_twist':0.,'Ktrace_peak':.002,'initial_positions':positions.tolist(),'seed':'existing seed_spinor defaults'},
        'initial_constraints':initial,'rows':rows,'bounce':'not-assessed',
        'scope':['Passive infinitesimal-volume tracers of the existing general 3D single-spinor ECD equations.',
                 'N_material_integral uses the material proper clock. N_normal follows different normal trajectories.',
                 'Trilinear primitive reconstruction produces a measured current-continuity defect; density-only values are not silently substituted.',
                 'Directional e-folds are principal rest-frame stretches, not integrals of arbitrary coordinate-axis rates.',
                 'No finite whole-cloud rest volume, inflation duration, global bounce or exterior matching is established.']}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--n',type=int,default=9);p.add_argument('--dt',type=float,default=.005);p.add_argument('--output',type=Path,default=Path('tracked-efolds.json'));args=p.parse_args()
    report=run(n=args.n,dt=args.dt);args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');print(report['status'],args.output)
