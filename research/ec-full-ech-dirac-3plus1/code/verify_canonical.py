"""Exact scalar Legendre momentum, chiral normalization and scalar source identities."""
import json
from pathlib import Path
import sympy as s

def main():
 N,sg,v,bQ,Q2,V,h,g,a,AQ,A2=s.symbols('N sqrtgamma phidot shiftQ Q2 V h g a AQ A2',real=True);Pi=(v-bQ)/N
 L=N*sg*(Pi**2/2-Q2/2-V-h*(a*Pi+AQ)-g*A2)
 canonical=s.diff(L,v);assert s.simplify(canonical-sg*(Pi-h*a))==0
 Hamilton=s.simplify(canonical*v-L);target=N*sg*(Pi**2/2+Q2/2+V+h*AQ+g*A2)+bQ*canonical
 assert s.simplify(Hamilton-target)==0
 phi,M,beta=s.symbols('phi M beta',real=True,positive=True);X=s.sqrt(s.Rational(2,3))*phi/M+s.asinh(4*beta/M**2)
 theta=s.Rational(3,4)*(s.atan(s.sinh(X))-s.atan(4*beta/M**2));hh=s.sqrt(s.Rational(3,8))/(M*s.cosh(X));assert s.simplify(s.diff(theta,phi)-hh)==0
 # Equivalence between Pi evolution using Ward and canonical-density flux.
 nPi,Dlap,accQ,K,hp,na,divAsp,accAsp,Vp,gp,qpAsp=s.symbols('nPi Dlap accQ K hp na divAsp accAsp Vp gp qpAsp')
 # W=n(a)-K*a+div(Asp)+acc.Asp. Remove time derivative of a from p_phi equation.
 W=na-K*a+divAsp+accAsp
 pi_normal=Dlap+accQ+K*Pi-Vp+h*W-gp*A2
 pdensity=s.expand(pi_normal-hp*Pi*a-h*na-K*(Pi-h*a))
 expected=Dlap+accQ-Vp-gp*A2-hp*Pi*a+h*(divAsp+accAsp)
 assert s.simplify(pdensity-expected)==0
 result={'momentum':'p_phi=sqrt(gamma)(Pi-h a), a=-n_mu A^mu; Pi=(phidot-shift^i D_i phi)/N','Hamiltonian_scalar_interaction':'N sqrtgamma[Pi^2/2+Q^2/2+V+h Asp.Q+g A^2]+(shift.Q) p_phi, with Pi=p_phi/sqrtgamma+h a. Dirac primary momenta must be included separately.','canonical_density_evolution':'dt p_phi-di(shift^i p_phi)=di[N sqrtgamma(Q^i+h Asp^i)]-N sqrtgamma[Vprime+gprime A^2+hprime(a Pi+Asp.Q)]','chiral_angle':str(theta),'residuals':{'Legendre_momentum':'0','Hamiltonian':'0','chiral_angle_derivative':'0','canonical_vs_normal_scalar_evolution':'0'},'scope':'Classical field identities. Quantum chiral anomalies and reduced fermionic Dirac brackets are not evaluated.'}
 (Path(__file__).resolve().parents[1]/'results/05_canonical_scalar.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS scalar canonical shift, Hamiltonian, chiral angle and ADM scalar equivalence')
if __name__=='__main__':main()
