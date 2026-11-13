"""Symbolic checks of analytical statements; no time integration or parameter search."""
import importlib.util
from pathlib import Path
import unittest
import sympy as s

z=s.symbols('z',real=True)
X=s.symbols('X',positive=True,real=True)
Y,Q=s.symbols('Y Q',real=True)
angle=s.symbols('theta',real=True)
n,m,c,G,k=s.symbols('n m c G k',positive=True,real=True)
from sympy.physics.matrices import mgamma
eta=[-1,1,1,1];gamma=[eta[i]*mgamma(i) for i in range(4)]
g5=-s.I*gamma[0]*gamma[1]*gamma[2]*gamma[3]


def derived_fields():
    psi=s.sqrt(n)*X**-3*s.Matrix([s.I*s.sin(angle),0,s.cos(angle),0])
    bar=s.conjugate(psi).T*gamma[0]
    axial=[s.simplify((bar*g5*a*psi)[0]) for a in gamma]
    spatial=[-Y/X*gamma[1]*gamma[3]*psi,-Y/X*gamma[2]*gamma[3]*psi,
             -3*Y/X*psi+s.sqrt(n)*X**-3*s.Matrix([s.I*c*s.cos(angle),0,-c*s.sin(angle),0])]
    B=m*s.eye(4)+2*G*sum((eta[i]*axial[i]*g5*gamma[i] for i in range(4)),s.zeros(4))
    dt=s.simplify(-gamma[0]*(sum((gamma[i+1]*spatial[i]/X**2 for i in range(3)),s.zeros(4,1))+s.I*B*psi))
    cov=[dt]+spatial;adj=[s.conjugate(v).T*gamma[0] for v in cov]
    lower=[-gamma[0]]+[X**2*a for a in gamma[1:]]
    square=sum(eta[i]*axial[i]**2 for i in range(4))
    T=s.Matrix(4,4,lambda i,j:s.simplify(-s.I/4*((bar*lower[i]*cov[j]-adj[j]*lower[i]*psi)[0]+(bar*lower[j]*cov[i]-adj[i]*lower[j]*psi)[0])+(G*eta[i]*(1 if i==0 else X**4)*square if i==j else 0)))
    return psi,bar,axial,dt,T


class AnalyticBounce(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.psi,cls.bar,cls.axial,cls.dt,cls.T=derived_fields()

    def test_current_and_fierz(self):
        current=[s.simplify((self.bar*a*self.psi)[0]) for a in gamma]
        self.assertEqual(current,[n/X**6,0,0,0])
        self.assertEqual(self.axial,[0,0,0,n/X**6])
        self.assertEqual(s.simplify((self.bar*self.psi)[0]-n*s.cos(2*angle)/X**6),0)

    def test_complete_stress_and_momentum(self):
        E=m*n*s.cos(2*angle)/X**6+G*n*n/X**12-c*n/X**8
        expected=s.diag(E,G*n*n/X**8,G*n*n/X**8,G*n*n/X**8-c*n/X**4)
        self.assertEqual(s.simplify(s.trigsimp(self.T-expected)),s.zeros(4))
        for i in range(1,4):self.assertEqual(self.T[0,i],0)

    def test_trace_and_focusing_identity(self):
        trace=-self.T[0,0]+sum(self.T[i,i]/X**4 for i in range(1,4))
        self.assertEqual(s.trigsimp(trace+m*n*s.cos(2*angle)/X**6-2*G*n*n/X**12),0)
        focus=self.T[0,0]+sum(self.T[i,i]/X**4 for i in range(1,4))
        self.assertEqual(s.trigsimp(focus-(m*n*s.cos(2*angle)/X**6+4*G*n*n/X**12-2*c*n/X**8)),0)

    def test_spatial_scalar_curvature_from_christoffel(self):
        x,y=s.symbols('x y');chi=s.Function('chi')(z);coords=[x,y,z]
        metric=s.eye(3)*chi**4;inv=metric.inv()
        con=[[[s.simplify(sum(inv[a,l]*(s.diff(metric[l,j],coords[i])+s.diff(metric[l,i],coords[j])-s.diff(metric[i,j],coords[l])) for l in range(3))/2) for j in range(3)] for i in range(3)] for a in range(3)]
        R=s.Matrix(3,3,lambda i,j:s.simplify(sum(s.diff(con[a][i][j],coords[a])-s.diff(con[a][i][a],coords[j])+sum(con[a][a][b]*con[b][i][j]-con[a][j][b]*con[b][i][a] for b in range(3)) for a in range(3))))
        self.assertEqual(s.simplify(s.trace(inv*R)+8*s.diff(chi,z,2)/chi**5),0)

    def test_exact_hamiltonian_ode(self):
        E=m*n*s.cos(2*c*z)/X**6+G*n*n/X**12-c*n/X**8
        chi2=-k*s.Rational(1,4)*(m*n*s.cos(2*c*z)/X+G*n*n/X**7-c*n/X**3)
        self.assertEqual(s.simplify(-8*chi2/X**5-2*k*E),0)

    def test_current_acceleration_including_geometry(self):
        dj=s.simplify((s.conjugate(self.dt).T*gamma[0]*gamma[3]*self.psi+self.bar*gamma[3]*self.dt)[0])
        acceleration=s.trigsimp(dj/X**2/(n/X**6))
        expected=2*Y/X**5+2*m*s.sin(2*angle)/X**2
        self.assertEqual(s.simplify(acceleration-expected),0)
        derivative=Y*s.diff(expected,X)+Q*s.diff(expected,Y)+c*s.diff(expected,angle)
        self.assertEqual(s.simplify(derivative.subs({X:1,Y:0,angle:0})-2*Q-4*m*c),0)

    def test_open_parameter_band_not_an_isolated_tuning(self):
        b,d=s.symbols('b d',positive=True)
        rate=4*m*c-k*m*n+s.Rational(3,2)*k*c*n-s.Rational(5,2)*k*G*n*n
        expected=2*m*m+s.Rational(20,3)*m*b+s.Rational(8,3)*b*b+(4*m+8*b)*d
        self.assertEqual(s.simplify(rate.subs({n:16*b/(3*k),G:3*k/16,c:m/2+2*b+d})-expected),0)

    def test_exact_positive_energy_bounce_witness(self):
        # c=3m/4, n=m/(3 k), G=3 k/16.
        replace={c:3*m/4,n:m/(3*k),G:3*k/16}
        E=m*n+G*n*n-c*n;F=m*n+4*G*n*n-2*c*n
        normal=-k*F/2
        material=normal-k*E/2+4*m*c
        self.assertEqual(s.simplify(E.subs(replace)-5*m*m/(48*k)),0)
        self.assertEqual(s.simplify(normal.subs(replace)-m*m/24),0)
        self.assertEqual(s.simplify(material.subs(replace)-287*m*m/96),0)

    def test_material_turn_from_differentiated_dirac_not_raychaudhuri(self):
        E=m*n+G*n*n-c*n;focus=m*n+4*G*n*n-2*c*n
        q=-k*E/4;theta_normal_dot=-k*focus/2
        # Differentiate the actual upper-component Dirac RHS along z.
        f=self.dt[0]
        fprime=(Y*s.diff(f,X)+Q*s.diff(f,Y)+c*s.diff(f,angle)).subs({X:1,Y:0,angle:0,Q:q})
        frequency=m+2*G*n-c
        second_lower=fprime-(m+2*G*n)*frequency*s.sqrt(n)-theta_normal_dot*s.sqrt(n)/2
        density_second=s.simplify(2*n*frequency**2+2*s.sqrt(n)*second_lower)
        expected=4*m*c-k*m*n+s.Rational(3,2)*k*c*n-s.Rational(5,2)*k*G*n*n
        self.assertEqual(s.simplify(-density_second/n-expected),0)

    def test_witness_energy_conditions_are_not_hidden(self):
        r={c:3*m/4,n:m/(3*k),G:3*k/16}
        E=m*n+G*n*n-c*n;Pz=G*n*n-c*n
        self.assertEqual(s.simplify((E+Pz).subs(r)),-m*m/(8*k))

    def test_flat_reference_contains_negative_frequency_sector(self):
        alpha=gamma[0]*gamma[3]
        plus=s.sqrt(n)/2*s.Matrix([1,0,1,0]);minus=s.sqrt(n)/2*s.Matrix([-1,0,1,0])
        hp=c*alpha+m*gamma[0];hm=-c*alpha+m*gamma[0];energy=s.sqrt(m*m+c*c)
        average=(s.conjugate(plus).T*hp*plus+s.conjugate(minus).T*hm*minus)[0]
        self.assertEqual(s.simplify(average),-c*n)
        negative=(s.conjugate(plus).T*(s.eye(4)-hp/energy)*plus/2+s.conjugate(minus).T*(s.eye(4)-hm/energy)*minus/2)[0]
        self.assertEqual(s.simplify((negative/n).subs(c,3*m/4)),s.Rational(4,5))

    def test_contact_removal_comparison(self):
        F=m*n+4*G*n*n-2*c*n;E=m*n+G*n*n-c*n
        normal=-k*F/2;material=normal-k*E/2+4*m*c
        self.assertEqual(s.expand(normal-normal.subs(G,0)),-2*k*G*n*n)
        self.assertEqual(s.expand(material-material.subs(G,0)),-s.Rational(5,2)*k*G*n*n)

    def test_homogeneous_flat_turn_cannot_bounce(self):
        shear=s.symbols('shear',nonnegative=True)
        # E= mS+G n² = -shear/(2 k) at H=0, R3=0.
        mS=-shear/(2*k)-G*n*n
        normal=k*mS/2
        self.assertEqual(s.expand(normal),-shear/4-k*G*n*n/2)

    def test_independent_general_tensor_engine_at_fixed_points(self):
        import numpy as np
        root=Path(__file__).resolve().parents[2]/'ec-full-3plus1'/'ecd.py'
        spec=importlib.util.spec_from_file_location('bounce_engine_check',root)
        mod=importlib.util.module_from_spec(spec)
        import sys
        sys.modules[spec.name]=mod;spec.loader.exec_module(mod)
        for chi,chi_prime,theta in [(1.,0.,0.),(1.2,.03,.2),(.9,-.04,-.3)]:
            density=.013;mass=.17;slope=.08;kappa=1.1
            g=np.diag([-1.,chi**4,chi**4,chi**4]);dg=np.zeros((4,4,4));dg[3,1:,1:]=np.eye(3)*4*chi**3*chi_prime
            p=np.sqrt(density)*chi**-3*np.array([1j*np.sin(theta),0,np.cos(theta),0]);ds=np.zeros((3,4),complex)
            ds[2]=-3*chi_prime/chi*p+np.sqrt(density)*chi**-3*np.array([1j*slope*np.cos(theta),0,-slope*np.sin(theta),0])
            got=mod.matter(g,dg,p,ds,mass,kappa)
            expected=np.array(self.T.subs({X:chi,Y:chi_prime,angle:theta,n:density,m:mass,c:slope,G:3*kappa/16}),float)
            np.testing.assert_allclose(got['stress'],expected,atol=2e-16)
            wave=dg.copy();wave[0,0,3]=wave[0,3,0]=-2*chi_prime/chi
            harmonic=np.einsum('bc,abc->a',np.linalg.inv(g),mod.christoffel(g,wave))
            np.testing.assert_allclose(harmonic,0,atol=1e-14)
            gauged=mod.matter(g,wave,p,ds,mass,kappa)
            np.testing.assert_allclose(gauged['stress'],expected,atol=2e-16)
            np.testing.assert_allclose(gauged['dt'],got['dt'],atol=2e-16)

if __name__=='__main__':unittest.main()
