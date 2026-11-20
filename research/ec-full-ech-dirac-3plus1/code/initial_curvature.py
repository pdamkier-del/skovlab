"""Initial normal-time derivatives and full Cartan curvature of constrained data.
This evaluates the general equations on a planar T^3 datum; no evolution search.
"""
import json
from pathlib import Path
from types import SimpleNamespace
import numpy as np
from scipy.interpolate import CubicHermiteSpline
from ech import *
from initial_data import fields,fd,fd2,PARS
from curvature import metric_curvature,full_curvature

def retained_solution(record):
 r=record['raw'];s=CubicHermiteSpline(r['BVP_grid'],r['BVP_logchi'],r['BVP_derivative'])
 return SimpleNamespace(p=np.array([r['Ktrace']]),sol=lambda z:np.array([s(z),s(z,1)]))

def jets(f):
 g=f['metric'];dg=f['dg'];n=len(g);dx=f['dx'];K=f['K'];s=f['src'];sp=g[:,1:,1:];iv=np.linalg.inv(sp)
 dd3=np.zeros((n,3,3,3,3));dd3[:,2,2]=fd2(sp,dx)
 geom3=metric_curvature(sp,dg[:,1:,1:,1:],dd3)
 zeros=np.zeros_like(K);_,kt,_=adm_rhs(sp,K,np.ones(n),np.zeros((n,3)),np.zeros((n,3)),zeros,geom3['Ricci'],zeros,zeros,s['rho'],s['J'],s['Sij'],PARS.M)
 ddg=np.zeros((n,4,4,4,4));ddg[:,3,3]=fd2(g,dx);ddg[:,0,3,1:,1:]=ddg[:,3,0,1:,1:]=-2*f['ktr']/3*dg[:,3,1:,1:];ddg[:,0,0,1:,1:]=-2*kt
 ddphi=np.zeros((n,4,4));ddphi[:,3,3]=fd2(f['phi'],dx)
 lap=np.einsum('nij,nij->n',iv,ddphi[:,1:,1:]-np.einsum('nkij,nk->nij',geom3['Gamma'],f['dphi'][:,1:]))
 ddphi[:,0,0]=lap+s['scalar_force'];dpsi=np.concatenate([s['dtpsi'][:,None,:],f['dpsi']],axis=1)
 return ddg,ddphi,dpsi,geom3

def main():
 root=Path(__file__).resolve().parents[1];data=json.loads((root/'results/02_initial_data.json').read_text());rows=[];checkpoint=None
 for case in data['cases']:
  mode=case['mode'];sol=retained_solution(case);series=[]
  for nodes in [65,129,257]:
   f=fields(sol,nodes,mode);ddg,ddphi,dpsi,geo3=jets(f);src=f['src'];iv=np.linalg.inv(f['metric'][:,1:,1:]);S=np.einsum('nij,nij->n',iv,src['Sij']);focusing=-f['ktr']**2/3-(src['rho']+S)/(2*PARS.M**2)
   probes=[]
   for delta in [1e-4,5e-5]:
    d=full_curvature(f['metric'],f['dg'],ddg,f['phi'],f['dphi'],ddphi,f['psi'],dpsi,PARS,delta,torsion=mode=='echd')
    Ein=d['metric']['G']-src['T']/PARS.M**2
    Herror=np.max(abs(d['Holst']-src['couplings']['z'])) if mode=='echd' else np.max(abs(d['Holst']))
    trace=np.max(abs(PARS.M**2*d['full_scalar']+2*PARS.beta*d['Holst']-PARS.mass*src['scalar_bilinear'])) if mode=='echd' else None
    probes.append({'tangent_step':delta,'Einstein_residual_max':float(np.max(abs(Ein))),'auxiliary_H_minus_z_max':float(Herror),'original_trace_residual_max':None if trace is None else float(trace),'full_R_min':float(d['full_scalar'].min()),'full_R_max':float(d['full_scalar'].max()),'full_K_min':float(d['full_K'].min()),'full_K_max':float(d['full_K'].max()),'metric_R_min':float(d['metric']['scalar'].min()),'metric_R_max':float(d['metric']['scalar'].max())})
   series.append({'nodes':nodes,'normal_Theta':-f['ktr'],'normal_Theta_dot_min':float(focusing.min()),'normal_Theta_dot_max':float(focusing.max()),'momentum_max':float(np.max(abs(src['J']))),'curvature_probes':probes})
   assert focusing.max()<0
   if mode=='echd' and nodes==257:
    checkpoint={'scope':'Constrained initial planar T^3 scalar/classical-Dirac datum, not evolved spacetime or physical fermion state','parameters':PARS.__dict__,'z':f['z'].tolist(),'metric':f['metric'].tolist(),'metric_time_derivative':f['dg'][:,0].tolist(),'Ktrace':f['ktr'],'phi':f['phi'].tolist(),'normal_scalar_Pi':np.zeros(nodes).tolist(),'psi_real':f['psi'].real.tolist(),'psi_imag':f['psi'].imag.tolist(),'geometric_and_material_expansion_initially_equal':'Both are -Ktrace, since vector current equals the normal pointwise at this datum. Their subsequent derivatives need not agree.'}
  if mode=='echd':
   errors=[x['curvature_probes'][-1]['auxiliary_H_minus_z_max']for x in series];assert max(errors)<1e-10,errors
   errors2=[x['curvature_probes'][-1]['original_trace_residual_max']for x in series];assert errors2[-1]<errors2[0]/10,errors2
  rows.append({'mode':mode,'initial_slice_refinement':series})
 report={'main_action':PARS.__dict__,'cases':rows,'scope':'No spacetime evolution. Normal-time jets use the derived ADM/scalar/Dirac equations; scalar and original trace identities are independently probed from full reconstructed curvature. Geometric Einstein residual includes independent initial constraint truncation.','interpretation':'All three separately constrained data families are initially contracting and normal-focusing. This is not a trajectory-level no-bounce theorem or a physical quantum source test.'}
 (root/'results/04_initial_Cartan_curvature.json').write_text(json.dumps(report,indent=2)+'\n');(root/'results/04_initial_fields.json').write_text(json.dumps(checkpoint,separators=(',',':'))+'\n');print('PASS mixed inhomogeneous initial Cartan curvature, original trace and focusing checks')
if __name__=='__main__':main()
