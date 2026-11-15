"""Amplitude-independent cutoff bound for isotropic parity-even Gaussian states,
including particle/antiparticle coherence; not a theorem for all quantum ECD.
"""
import json
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.integrate import quad
from covariance_hf import initial,observables,G

def main():
 rng=np.random.default_rng(705);rows=[]
 for mass in [.0,.1,.5]:
  cutoff=.1;x,w=leggauss(40);p=cutoff*(x+1)/2;wt=w*cutoff/2*p*p/(2*np.pi**2);E=np.hypot(p,mass);nhat=np.stack([mass/E,np.zeros_like(p),p/E],axis=-1)
  I=2*np.sum(wt/E);ind=quad(lambda p:p*p/np.hypot(p,mass) if p else 0,0,cutoff,epsabs=1e-14)[0]/np.pi**2
  assert abs(I-ind)<1e-14
  fractions=[]
  for _ in range(400):
   q=rng.uniform(-.8,.8,len(p));direction=rng.normal(size=(len(p),3));direction/=np.linalg.norm(direction,axis=-1)[:,None];r=direction*(rng.random(len(p))*(1-abs(q)))[:,None]
   delta=r+nhat;e=1+np.sum(nhat*r,axis=-1);rho=2*np.sum(wt*E*e);D=2*np.sum(wt*q);S=2*np.sum(wt*delta[:,0]);B=D*D/2+S*S
   assert np.all(q*q<=e+1e-13) and np.all(np.sum(delta*delta,axis=-1)<=2*e+1e-13)
   ratio=G*B/rho;bound=2.5*G*I;assert ratio<=bound+1e-13;fractions.append(ratio/bound)
  rows.append({'mass':mass,'cutoff':cutoff,'I':float(I),'sharpness':'This Cauchy bound is sufficient, not claimed sharp.','contact_fraction_bound':float(2.5*G*I),'maximum_random_fraction_of_bound':float(max(fractions))})
 c=initial(192,angle=.05);o=observables(c['initial'],c);I=2*np.sum(c['w']/np.hypot(c['p'],.1));actual=G*abs(o['Q'])/o['rho_free'];assert actual<2.5*G*I
 result={'state_class':'One isotropic parity-even Dirac Gaussian state, full equal-time covariance 0<=R_h(p)<=1, arbitrary momentum-dependent particle/antiparticle coherence. Vacuum is instantaneous free Minkowski projector. Fixed physical cutoff Lambda.','proof_variables':'R=( (1+q)I+r.sigma )/2, |r|<=1-|q|; n=b/E, delta=r+n, e=1+n.r. Then q^2<=e and |delta|^2<=2e.','bound':'B=D^2/2+S^2 <= (5/2) I rho_free; I=2 int d^3p/(2pi)^3 /E <= Lambda^2/(2pi^2). Thus G B/rho_free <=5 G Lambda^2/(4 pi^2)=15 kappa Lambda^2/(64 pi^2).','scope':'Gaussian Wick source Q=-D^2/2-S^2; no independent species axial Hartree term in this parity-even state. This is nonperturbative in covariance/coherence amplitude, not in omitted interaction diagrams or curved-space renormalization.','random_admissible_covariances_tested':1200,'tests':rows,'predeclared_coherent_state':{'actual_contact_fraction':float(actual),'bound':float(2.5*G*I)},'conclusion':'Particle-antiparticle coherence alone in this state class cannot force a flat positive-free-energy cancellation while the stated contact bound is below one and omitted stress terms remain sufficiently small.'}
 (Path(__file__).resolve().parents[1]/'results/08_coherent_pauli_bound.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS coherent covariance bound for 1200 admissible spectra; example',actual,'<',2.5*G*I)
if __name__=='__main__':main()
