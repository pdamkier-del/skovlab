"""Independent quadrature, finite-temperature checks and sharp Pauli cutoff bound."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import expit
from quantum_gas import GA,charge,pressure,thermal_integrals,correlator

def main():
 rows=[]
 for T in [.2,1.]:
  for x in [0,.5,2,10]:
   mu=x*T;q=thermal_integrals(T,mu);d=charge(T,mu);rho=3*pressure(T,mu)
   assert abs(q['charge']-d)<2e-10*max(1,abs(d))
   assert abs(q['rho']-rho)<2e-10*max(1,abs(rho))
   # Opposite-chirality Dirac channels, equal chemical potentials: axial mean=0.
   Q=correlator([d,d],[1,-1]);assert abs(Q+2*d*d)<1e-12*max(1,abs(Q))
   rows.append(dict(T=T,mu=mu,one_Weyl=q,unpolarized_Dirac_A2=Q,Dirac_total_density=2*q['total_particles_and_antiparticles'],relative_contact_at_fixed_free_charges=GA*abs(Q)/(2*rho)))
 # Pauli bound for arbitrary isotropic nonthermal f_+/- supported p<=Lambda.
 # Piecewise constant occupations allow exact shell integrals; no quadrature ambiguity.
 rng=np.random.default_rng(91812);records=[];maxfrac=0
 for g in [1,2,6,24]:
  bound=(g+1)/(24*np.pi**2) # kappa=Lambda=1
  for _ in range(200):
   edges=np.linspace(0,1,17);f=rng.random((g,2,16));d=((f[:,0]-f[:,1])@np.diff(edges**3))/(6*np.pi**2)
   E=float(np.sum((f[:,0]+f[:,1])@np.diff(edges**4))/(8*np.pi**2));signs=rng.choice([-1,1],g)
   ratio=GA*abs(correlator(d,signs))/E;maxfrac=max(maxfrac,ratio/bound);assert ratio<=bound+1e-14
  # Sharp saturation: all full particle seas, same axial sign.
  d=np.repeat(1/(6*np.pi**2),g);E=g/(8*np.pi**2);ratio=GA*abs(correlator(d,np.ones(g)))/E
  assert abs(ratio-bound)<1e-14
  pb=np.sqrt(24*np.pi**2/(g+1));species_proxy=g*pb**2/(16*np.pi**2)
  records.append(dict(Weyl_channels=g,sharp_ratio_bound_coefficient=bound,formal_saturated_bounce_p_in_Mbar=pb,species_loop_proxy_at_formal_equality=species_proxy))
 result={'state':'Independent gauge-invariant isotropic massless Weyl Gaussian channels, particles and antiparticles; Minkowski vacuum Wick ordering; leading contact only.','thermal_checks':rows,'cutoff_bound':'GA B / rho0 <= (g+1) kappa Lambda^2/(24 pi^2); B=(sum s_i d_i)^2+sum d_i^2. Sharp for full aligned zero-temperature seas.','cutoff_checks':records,'random_distributions_tested':800,'maximum_random_fraction_of_bound':maxfrac,'scope':'Conditional theorem in stated Gaussian cutoff class. No anomalous pairing, cross-channel coherence or non-Gaussian correlations. Thermal tails are not compact support; no hard-cutoff bound is applied to untruncated Fermi-Dirac tails.'}
 (Path(__file__).resolve().parents[1]/'results/02_thermal_and_pauli_bounds.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS thermal integrals and 800 Pauli distributions; sharp bound saturated')
if __name__=='__main__':main()
