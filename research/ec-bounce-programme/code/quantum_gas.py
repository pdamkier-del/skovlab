"""Minimal-ECD, leading vacuum-Wick massless isotropic quasifree source.
No interacting evolution or curved-space renormalized stress is asserted.
A channel is one Weyl particle/antiparticle pair, not one Dirac species.
"""
import numpy as np
from scipy.integrate import quad
from scipy.special import expit
PI=np.pi
GA=3/16 # kappa=1

def charge(T,mu):return mu*T*T/6+mu**3/(6*PI**2)
def pressure(T,mu):return 7*PI**2*T**4/360+mu*mu*T*T/12+mu**4/(24*PI**2)
def correlator(charges,signs):
 d=np.asarray(charges);s=np.asarray(signs)
 return -float((s@d)**2+d@d)
def thermal_integrals(T,mu):
 """Independent continuum momentum integrals; no polynomial formulas used."""
 assert T>0
 plus=lambda p:expit((mu-p)/T)
 minus=lambda p:expit((-mu-p)/T)
 opts=dict(epsabs=2e-11,epsrel=2e-11)
 d=quad(lambda p:p*p*(plus(p)-minus(p)),0,np.inf,**opts)[0]/(2*PI**2)
 rho=quad(lambda p:p**3*(plus(p)+minus(p)),0,np.inf,**opts)[0]/(2*PI**2)
 total=quad(lambda p:p*p*(plus(p)+minus(p)),0,np.inf,**opts)[0]/(2*PI**2)
 var=quad(lambda p:p**4*(plus(p)*(1-plus(p))+minus(p)*(1-minus(p))),0,np.inf,**opts)[0]/(2*PI**2)
 return dict(charge=d,rho=rho,total_particles_and_antiparticles=total,free_total_energy_variance_per_volume=var)
