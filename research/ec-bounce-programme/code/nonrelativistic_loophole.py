"""Test the cold-gas/radiation scaling loophole, including fermion rest energy.
This is an equilibrium reference-state test, not reproduction of a 2PI solution.
"""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.special import expit
from scipy.optimize import brentq
from quantum_gas import GA

def cold(m,T):
 # p=sqrt(2mT)*x; mu=m, stable expression for (sqrt(m^2+p^2)-m)/T.
 scale=np.sqrt(2*m*T)
 def occ(x):return expit(-2*m*x*x/(np.hypot(m,scale*x)+m))
 C=scale**3/np.pi**2
 n=C*quad(lambda x:x*x*occ(x),0,20,epsabs=1e-12)[0]
 S=C*quad(lambda x:x*x*m/np.hypot(m,scale*x)*occ(x),0,20,epsabs=1e-12)[0]
 E=C*quad(lambda x:x*x*np.hypot(m,scale*x)*occ(x),0,20,epsabs=1e-12)[0]
 return n,S,E

def main():
 rows=[]
 for m in [.01,.1,1.]:
  for z in [1e-4,1e-3,.01]:
   T=m*z;n,S,E=cold(m,T);contact=GA*(n*n/2+S*S);rad=np.pi**2*T**4/15
   rows.append(dict(mass=m,T_over_m=z,n_over_mT_power3half=n/(m*T)**1.5,contact_over_fermion_energy=contact/E,fermion_energy_over_photon_energy=E/rad))
 # Find an artificially suggested cancellation if the positive fermion rest
 # energy is omitted. G is fixed by minimal ECD; no sign or coupling scan.
 m=.1
 def ratio(z):
  T=m*z;n,S,E=cold(m,T)
  return GA*(n*n/2+S*S)/(np.pi**2*T**4/15)
 z=brentq(lambda z:np.log(ratio(z)),1e-7,.01,xtol=1e-15)
 n,S,E=cold(m,m*z);contact=GA*(n*n/2+S*S)
 assert abs(ratio(z)-1)<1e-7 and contact/E<1e-6
 result={'question':'Can cold Pauli-compatible fermions cancel radiation below cutoff when their rest energy is retained?','assumptions':'Unpolarized equilibrium free massive Dirac gas with mu=m and T<<m; negligible antiparticles exp(-2m/T); leading normal-ordered contact, plus photons.','cold_examples':rows,'false_radiation_only_turn':{'m':m,'GA_m_squared':GA*m*m,'T_over_m':z,'contact_over_radiation':ratio(z),'contact_over_full_positive_energy':contact/(E+contact),'omitted_fermion_energy_over_radiation':E/contact},'conclusion':'Radiation-only balance is spurious in this state: positive fermion rest energy dominates. Not a no-go for non-equilibrium coherent or correlated 2PI states.'}
 (Path(__file__).resolve().parents[1]/'results/04_nonrelativistic_loophole.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS cold-gas check; omitted rest-energy factor:',E/contact)
if __name__=='__main__':main()
