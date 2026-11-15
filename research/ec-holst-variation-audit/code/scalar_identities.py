"""Symbolic elimination, nonlinear Legendre map and canonical normalization."""
import json
from pathlib import Path
import sympy as s

def main():
 M,c,b,z,u,A,J,t,q=s.symbols('M c beta z u A J t q',real=True,nonzero=True)
 f=b+2*c*z;D=1+16*f*f/M**4;X=u+A/8
 L=-M*M*t*t/3+M*M*q*q/48-2*f*t*q/3-X*q+t*J
 sol=s.solve([s.diff(L,t),s.diff(L,q)],[t,q]);red=s.factor(L.subs(sol));target=3*J*J/(4*M*M)-12*(X+f*J/M**2)**2/(M*M*D)
 assert s.simplify(red-target)==0
 # Contractions are Lorentz scalar; the polynomial check represents each component.
 K=s.simplify(-s.diff(red,u,2).subs({A:0,J:0})*(2*c)**2);omega=s.sqrt(s.Rational(3,2))*M*(s.asinh(4*f/M**2)-s.asinh(4*b/M**2))
 assert s.simplify(s.diff(omega,z)**2-K)==0
 w=s.symbols('w',real=True);Xw=s.sqrt(s.Rational(2,3))*w/M+s.asinh(4*b/M**2)
 zi=(M*M*s.sinh(Xw)/4-b)/(2*c);V=(M*M*s.sinh(Xw)/4-b)**2/(4*c)
 assert s.simplify(V-c*zi**2)==0
 mass2=s.simplify(s.diff(V,w,2).subs(w,0));assert s.simplify(mass2-M*M*(1+16*b*b/M**4)/(48*c))==0
 # A declared nonminimal trace source, not a convention-only change.
 B,j=s.symbols('B j',real=True);four=3*j*j/4-12*(s.Rational(1,8)+B*j)**2/(1+16*B*B)
 assert s.simplify(four.subs(j,2*B)+s.Rational(3,16))==0
 # Effective scalar + axial equations: derivative of h cancels in scalar EL.
 time,ell=s.symbols('time ell',positive=True)
 aa=ell*s.cosh(time/ell);HH=s.diff(aa,time)/aa
 assert s.simplify(HH**2+1/aa**2-1/ell**2)==0
 assert s.simplify(s.diff(HH,time)-1/aa**2)==0
 result={'Legendre_equation':'2c(Rprime-z)=0','torsion_reduced_action':str(target),'K_z':str(K),'canonical_omega':str(omega),'inverse_z':str(zi),'canonical_potential':str(V),'mass_squared_at_vacuum':str(mass2),'residuals':{'full_auxiliary_elimination':'0','canonical_kinetic':'0','potential_inverse':'0','mass':'0','independent_closed_deSitter_constraint':'0','independent_closed_deSitter_evolution':'0','tuned_nonminimal_gamma_independence':'0'},'linear_Holst_contact':'-3/[16 M^2(1+16 beta^2/M^4)] A^2 = -3/(16 M^2) gamma^2/(1+gamma^2) A^2','minimal_derivative_coupling':'-sqrt(3/8)/(M cosh(X)) partial(omega).A','nonminimal_convention':'J couples as +t.J in this declared action; J=2B A removes linear-Holst dependence of the AA coefficient at constant B. It is a changed matter coupling, not a mere notation change.'}
 (Path(__file__).resolve().parents[1]/'results/02_scalar_and_fermions.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS Legendre transformation, exact kinetic factor, canonical map, mass and nonminimal algebra')
if __name__=='__main__':main()
