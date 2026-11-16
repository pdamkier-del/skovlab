"""Independent matter stress/current conservation on spatially varying jets.
Scalar and Dirac tangent equations are coupled; gravity is a fixed test background.
Not a trajectory, quantum state, or general 3+1 evolution benchmark.
"""
import json
from pathlib import Path
import numpy as np
from ech import *
from initial_data import fd,fd2,L,KMODE

def main():
 rows=[];p=Parameters()
 for n in [65,129,257,513]:
  z=np.arange(n)*L/n;dx=L/n;w=.2+.01*np.sin(KMODE*z);Pi=.001*np.cos(KMODE*z)
  psi=.004*np.stack([1+.1*np.cos(KMODE*z),.1j*np.sin(KMODE*z),.8+.05j*np.cos(2*KMODE*z),.1*np.cos(KMODE*z)],axis=1)*np.exp(.1j*np.sin(2*KMODE*z))[:,None]
  metric=np.broadcast_to(np.diag(ETA),(n,4,4)).copy();dg=np.zeros((n,4,4,4));dp=np.zeros((n,3,4),complex);dp[:,2]=fd(psi,dx);dw=np.zeros((n,4));dw[:,0]=Pi;dw[:,3]=fd(w,dx)
  src=source(metric,dg,psi,dp,w,dw,p);psi_t=src['dtpsi'];Pi_t=fd2(w,dx)+src['scalar_force'];dpt=np.zeros_like(dp);dpt[:,2]=fd(psi_t,dx);dwt=np.zeros_like(dw);dwt[:,0]=Pi_t;dwt[:,3]=fd(Pi,dx)
  probes=[]
  for eps in [1e-3,5e-4]:
   plus=source(metric,dg,psi+eps*psi_t,dp+eps*dpt,w+eps*Pi,dw+eps*dwt,p)
   minus=source(metric,dg,psi-eps*psi_t,dp-eps*dpt,w-eps*Pi,dw-eps*dwt,p)
   dt=(plus['T']-minus['T'])/(2*eps);div=-dt[:,0,:]+fd(src['T'][:,3,:],dx)
   dj=(plus['current'][:,0]-minus['current'][:,0])/(2*eps)+fd(src['current'][:,3],dx)
   def explicit_interaction(s,grad):
    al=np.einsum('nab,nb->na',metric,s['Acoord']);return s['couplings']['h'][:,None,None]*(al[:,:,None]*grad[:,None,:]+grad[:,:,None]*al[:,None,:])/2
   badbase=src['T']-explicit_interaction(src,dw);badplus=plus['T']-explicit_interaction(plus,dw+eps*dwt);badminus=minus['T']-explicit_interaction(minus,dw-eps*dwt)
   baddiv=-(badplus-badminus)[:,0,:]/(2*eps)+fd(badbase[:,3,:],dx)
   probes.append({'tangent_step':eps,'full_stress_divergence_max':float(np.max(abs(div))),'current_divergence_max':float(np.max(abs(dj))),'omitted_explicit_axial_stress_divergence_max':float(np.max(abs(baddiv)))})
  rows.append({'nodes':n,'probes':probes})
 ratios=[rows[i]['probes'][-1]['full_stress_divergence_max']/rows[i+1]['probes'][-1]['full_stress_divergence_max']for i in range(3)]
 assert all(3.5<x<4.5 for x in ratios),ratios
 assert rows[-1]['probes'][-1]['omitted_explicit_axial_stress_divergence_max']>10*rows[-1]['probes'][-1]['full_stress_divergence_max']
 result={'parameters':p.__dict__,'data':'Periodic varying phi, Pi and all four complex Dirac components; independent centered stress/current divergence versus coupled matter tangent evolution.','records':rows,'spatial_stress_error_ratios':ratios,'scope':'Second-order spatial derivative consistency; tangent difference probes are not temporal evolution/refinement. Omitting the explicit derivative-coupling stress does not approach the conserved source.'}
 (Path(__file__).resolve().parents[1]/'results/06_matter_conservation.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS inhomogeneous coupled stress/current conservation and missing-stress falsification')
if __name__=='__main__':main()
