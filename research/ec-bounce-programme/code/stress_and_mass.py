"""Symbolic thermodynamic ensemble checks and a separate massive Dirac trace."""
import json
from pathlib import Path
import sympy as s
import numpy as np
from scipy.integrate import quad
from scipy.special import expit
from quantum_gas import GA

def main():
 T,mu,G,g=s.symbols('T mu G g',positive=True);pi=s.pi
 # g equally populated, same axial-sign Weyl channels, particles+antiparticles.
 d=mu*T*T/6+mu**3/(6*pi*pi);P0=g*(7*pi*pi*T**4/360+mu*mu*T*T/12+mu**4/(24*pi*pi));B=g*(g+1)*d*d
 P1=B;E1=s.simplify(T*s.diff(P1,T)+mu*s.diff(P1,mu)-P1);assert s.simplify(E1-5*B)==0
 # Fixed entropy and charge: first-order shifts from susceptibility matrix.
 Hess=s.hessian(P0,(T,mu));grad=s.Matrix([s.diff(B,T),s.diff(B,mu)])
 shift=-Hess.inv()*grad;DeltaE=s.simplify(5*B+(s.Matrix([s.diff(3*P0,T),s.diff(3*P0,mu)]).T*shift)[0]);DeltaP=s.simplify(B+(s.Matrix([s.diff(P0,T),s.diff(P0,mu)]).T*shift)[0])
 assert s.simplify(DeltaE+B)==0 and s.simplify(DeltaP+B)==0
 a,R,C=s.symbols('a R C',positive=True);E=R/a**4-C/a**6;P=R/(3*a**4)-C/a**6
 conservation=s.simplify(a*s.diff(E,a)+3*(E+P));assert conservation==0
 r=s.symbols('r');cs=(s.Rational(4,9)-2*r)/(s.Rational(4,3)-2*r)
 # Full massive Dirac matrices independently built with SymPy, no old gamma import.
 I=s.eye(2);Z=s.zeros(2);sigma=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
 gamma=[Z.row_join(I).col_join(I.row_join(Z))]+[Z.row_join(x).col_join((-x).row_join(Z)) for x in sigma]
 gamma5=-s.I*gamma[0]*gamma[1]*gamma[2]*gamma[3]
 D,S=s.symbols('D S',real=True);cov=(D*s.eye(4)+S*gamma[0])/4;mat=[gamma[0]*gamma5*x for x in gamma]
 Q=s.simplify(sum(sign*(s.trace(M*cov)**2-s.trace(M*cov*M*cov)) for sign,M in zip([-1,1,1,1],mat)))
 assert s.simplify(Q+D*D/2+S*S)==0
 massive=[]
 for mass,temp,chem in [(1,.05,1.05),(1,.4,0.),(.1,1.,0.),(1,.2,2.)]:
  f=lambda p,sgn:expit((sgn*chem-np.hypot(p,mass))/temp)
  integ=lambda fn:quad(fn,0,np.inf,epsabs=1e-10,epsrel=1e-10)[0]/np.pi**2
  dn=integ(lambda p:p*p*(f(p,1)-f(p,-1)))
  sc=integ(lambda p:p*p*mass/np.hypot(p,mass)*(f(p,1)+f(p,-1)))
  energy=integ(lambda p:p*p*np.hypot(p,mass)*(f(p,1)+f(p,-1)))
  density=integ(lambda p:p*p*(f(p,1)+f(p,-1)))
  assert abs(dn)<=density+1e-10 and sc<=density+1e-10
  massive.append(dict(mass=mass,T=temp,mu=chem,net_charge=dn,scalar_condensate_medium=sc,rho0=energy,A2=-dn*dn/2-sc*sc,contact_fraction=GA*(dn*dn/2+sc*sc)/energy))
 # Independent low-momentum Pauli inequality saturation check via actual integrals.
 nr=[]
 for z in [.01,.1,.3]:
  m=1.;pmax=z*m;n=pmax**3/(3*np.pi**2)
  sc=quad(lambda p:p*p*m/np.hypot(p,m),0,pmax,epsabs=1e-15)[0]/np.pi**2
  e=quad(lambda p:p*p*np.hypot(p,m),0,pmax,epsabs=1e-15)[0]/np.pi**2
  ratio=GA*(n*n/2+sc*sc)/e;bound=GA*pmax**3/(2*np.pi**2*m)
  assert ratio<=bound+1e-15;nr.append(dict(p_over_m=z,actual_contact_fraction=ratio,conditional_bound=bound))
 result={'ensemble':'Omega1/V=G Q=-G B; P(T,mu)=P0+G B, E(T,mu)=3P0+5G B. At fixed physical entropy and charges, DeltaE=DeltaP=-G B at first order.','symbolic_checks':{'grand_energy_minus_5GB':str(s.simplify(E1-5*B)),'fixed_entropy_charge_DeltaE_over_G':str(DeltaE),'fixed_entropy_charge_DeltaP_over_G':str(DeltaP),'adiabatic_conservation':str(conservation)},'formal_adiabatic_sound_speed_squared':str(cs),'formal_gradient_sign_change_r':2/9,'formal_enthalpy_zero_r':2/3,'formal_flat_bounce_r':1,'stability_scope':'Sound-speed result belongs to the extrapolated local-equilibrium first-order fluid. It is not a controlled proof of a quantum gradient instability at these large corrections.','massive_unpolarized_Dirac_trace':str(Q),'massive_thermal_examples':massive,'nonrelativistic_checks':nr,'nonrelativistic_bound':'For unpolarized independent free Dirac species, p<=P<<m and occupations<=1: |DeltaE|/rho0 <= G P^3/(2 pi^2 m) = (G m^2)(P/m)^3/(2 pi^2). No interspecies axial Hartree term in this state.'}
 (Path(__file__).resolve().parents[1]/'results/03_stress_and_mass.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS ensemble Legendre transform, conservation, massive trace, nonrelativistic bounds')
if __name__=='__main__':main()
