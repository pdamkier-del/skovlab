"""Independent source checks outside the isotropic exact trajectory."""
import json
from pathlib import Path
import numpy as np
from field_source import source,modes,DIRS,action_density
from robustness import initial,rhs,unpack

def main():
 a=np.array([.8,1.1,1.4]);H=np.array([-.13,-.08,-.11]);N=np.repeat([.02,.03,.04],2);v=np.prod(a)
 psi=np.sqrt(N/v)[:,None]*modes();s=source(a,H,psi,DIRS);r=np.array([2*N[2*i]/a[i]/v for i in range(3)]);st=3/16*(N.sum()/v)**2
 assert abs(s['E']-(r.sum()-st))<1e-13
 assert np.max(abs(s['P']-(r-st)))<1e-13
 assert np.max(abs(s['T'][0,1:]))<1e-13
 # Einstein trace reversed gives v''/v=sum(r)>0, without assuming conserved shear.
 dH=-H.sum()*H+s['P']+(s['E']-s['P'].sum())/2
 convex=H.sum()**2+dH.sum();assert abs(convex-r.sum())<1e-13
 unbalanced=psi.copy();unbalanced[0]*=.9
 bad=source(a,H,unbalanced,DIRS)
 assert np.max(abs(bad['T'][0,1:]))>1e-4
 conservation=[]
 for case in ['exact','pair_amplitude_minus_2percent','mass_1percent_pb','opposite_chirality_1percent']:
  y,mom,mass,par=initial(case);dy=rhs(y,mom,mass);x,h,p=unpack(y);base=source(np.exp(x),h,p,mom,mass=mass)
  vals=[]
  for eps in [1e-6,5e-7]:
   es=[]
   for z in [y+eps*dy,y-eps*dy]:
    xx,hh,pp=unpack(z);es.append(source(np.exp(xx),hh,pp,mom,mass=mass)['E'])
   res=(es[0]-es[1])/(2*eps)+np.sum(h*(base['E']+base['P']))
   vals.append(float(res/(par['p']*par['n0']/par['ab']**4)))
  assert abs(vals[-1])<1e-6;conservation.append({'case':case,'energy_conservation_over_fixed_rho_b':vals})
 # Independent off-shell lapse variation at the bounce, where phase frequency is negative.
 n0=6/(2*np.pi)**3;ab=np.sqrt(3/16*n0);p=np.sqrt(n0/6/ab**3)*modes();sb=source(np.repeat(ab,3),np.zeros(3),p,DIRS)
 dn=1e-5;f=lambda lapse:action_density(lapse,np.repeat(ab,3),p,sb['dt'],DIRS)
 E=-(f(1+dn)-f(1-dn))/(2*dn)/ab**3
 err=abs(E-sb['E'])/(n0/ab**4);assert err<1e-8
 result={'anisotropic_paired_source_error':float(abs(s['E']-(r.sum()-st))),'volume_convexity_residual':float(convex-r.sum()),'unbalanced_pair_momentum_constraint_violation':float(np.max(abs(bad['T'][0,1:]))),'conservation':conservation,'bounce_offshell_energy_error_over_rho_b':float(err),'bounce_phase_frequency':float(1/ab-2*3/16*n0/ab**3),'scope':'Source/ODE checks; no quantum-state closure or spatial stability claim.'}
 dest=Path(__file__).resolve().parents[1]/'results/04_additional_checks.json';dest.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
