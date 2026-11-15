"""Finite-amplitude/mode tests of constrained planar contraction; not 3D stability."""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import brentq
from planar_contraction import periodic_data,run


def summary(r):
    initial,final=r['initial'],r['final']
    def contrast(x):return (x['current_density_max']-x['current_density_min'])/(x['current_density_max']+x['current_density_min'])
    ci,cf=contrast(initial),contrast(final)
    return {'n':r['n'],'steps':r['steps'],'initial_density_contrast':ci,'final_density_contrast':cf,'density_contrast_amplification':cf/ci,'slice_volume_ratio':final['proper_slice_volume']/initial['proper_slice_volume'],'max_Theta_current_over_time':r['max_Theta_current_over_time'],'max_Hnormal_over_time':r['max_Hnormal_over_time'],'max_relative_Hamiltonian':r['max_Hamiltonian_relative'],'max_momentum':r['max_momentum'],'max_harmonic':r['max_harmonic'],'max_charge_drift':r['max_charge_drift'],'final_lapse_min':final['lapse_min'],'max_CFL_ratio':r['max_dt_over_characteristic_bound'],'curvature':r['curvature'],'conservation':r['conservation'],'tangent_conservation':r['tangent_conservation'],'status':'completed; finite-interval evidence only'}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    report={'hypothesis':'Continued contraction of the selected planar branch persists under larger constraint-consistent seed variations over t in [0,.8].','duration':.8,'spatial_steps':400,'criterion':'No sampled current/normal turn; all data remain finite and spacelike; errors must decrease with resolution. This is not a general or asymptotic stability theorem.','cases':[]}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    def checkpoint():args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    for epsilon,mode in [(.1,1),(.3,1),(.1,4),(.3,4)]:
        sol,params=periodic_data(epsilon=epsilon,mode=mode);case={'parameters':params,'runs':[]};states=[]
        for n in [65,129,257]:
            try:
                r,st=run(n=n,steps=400,duration=.8,solution=sol,parameters=params);case['runs'].append(summary(r));states.append(st)
                print('completed epsilon',epsilon,'mode',mode,'n',n,'Hres',r['max_Hamiltonian_relative'],flush=True)
            except (ValueError,RuntimeError,FloatingPointError,np.linalg.LinAlgError) as e:
                case['runs'].append({'n':n,'status':'inconclusive numerical or coordinate stop','reason':str(e)});break
        if len(states)==3:
            diff=[[float(np.sqrt(np.mean(abs(a-b)**2))) for a,b in zip(states[i],states[i+1])] for i in range(2)]
            case['successive_RMS_differences']=diff
            try:case['observed_spatial_orders']=[float(brentq(lambda p:(65**(-p)-129**(-p))/(129**(-p)-257**(-p))-diff[0][j]/diff[1][j],.1,8)) for j in range(3)]
            except ValueError:case['spatial_order_status']='outside fitted order interval; inconclusive'
        report['cases'].append(case);checkpoint()
    sol,params=periodic_data(epsilon=.3,mode=4);temporal=[];ts=[]
    for steps in [200,400,800]:
        r,st=run(n=129,steps=steps,duration=.8,solution=sol,parameters=params);temporal.append(summary(r));ts.append(st)
    err=[[float(np.sqrt(np.mean(abs(a-b)**2))) for a,b in zip(ts[i],ts[i+1])] for i in range(2)]
    report['separate_time_test']={'parameters':params,'n':129,'runs':temporal,'successive_RMS_differences':err,'ratios':[err[0][j]/err[1][j] for j in range(3)]}
    report['interpretation']='Only bounded-amplitude selected modes on a periodic planar classical branch; no transverse perturbations, bounce candidate, oscillations, global regularity or fermionic quantum validity established.'
    checkpoint();print('wrote',args.output)
if __name__=='__main__':main()
