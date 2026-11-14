"""Exact six-field massless chiral ECD benchmark, derived from the common action.
No fluid pressure ansatz and no numerical search for a bounce.
"""
import unittest
import sympy as s
from sympy.physics.matrices import mgamma

class ChiralBenchmark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a,cls.H,cls.n,cls.p,cls.G=s.symbols('a H n p G',positive=True,real=True)
        a,H,n,p,G=cls.a,cls.H,cls.n,cls.p,cls.G
        eta=[-1,1,1,1];g=[eta[i]*mgamma(i) for i in range(4)];g5=-s.I*g[0]*g[1]*g[2]*g[3]
        dirs=[([1,0,0],s.Matrix([1,-1])/s.sqrt(2)),([-1,0,0],s.Matrix([1,1])/s.sqrt(2)),([0,1,0],s.Matrix([1,-s.I])/s.sqrt(2)),([0,-1,0],s.Matrix([1,s.I])/s.sqrt(2)),([0,0,1],s.Matrix([0,1])),([0,0,-1],s.Matrix([1,0]))]
        fields=[s.sqrt(n/6)*s.Matrix.vstack(v,v)/s.sqrt(2) for _,v in dirs]
        bars=[s.conjugate(v).T*g[0] for v in fields]
        cls.current=[s.simplify(sum((b*g[j]*v)[0] for b,v in zip(bars,fields))) for j in range(4)]
        cls.axial=[s.simplify(sum((b*g5*g[j]*v)[0] for b,v in zip(bars,fields))) for j in range(4)]
        square=s.simplify(sum(eta[j]*cls.axial[j]**2 for j in range(4)));T=s.zeros(4);res=[];freq=p/a-2*G*n
        cls.free_eigen_residuals=[]
        for (d,_),v,b in zip(dirs,fields,bars):
            cls.free_eigen_residuals.append(s.simplify(sum((d[j]*g[0]*g[j+1]*v for j in range(3)),s.zeros(4,1))-v))
            cls.free_eigen_residuals.append(s.simplify(g5*v-v))
            D=[(-3*H/2-s.I*freq)*v]+[s.I*p*d[j-1]*v+a*H/2*g[0]*g[j]*v for j in range(1,4)]
            adj=[s.conjugate(q).T*g[0] for q in D]
            equation=s.I*sum((g[j]/(a if j else 1)*D[j] for j in range(4)),s.zeros(4,1))-2*G*sum((eta[j]*cls.axial[j]*g5*g[j]*v for j in range(4)),s.zeros(4,1))
            res.append(s.simplify(equation));lower=[-g[0]]+[a*g[j] for j in range(1,4)]
            T+=s.Matrix(4,4,lambda i,j:-s.I/4*((b*lower[i]*D[j]-adj[j]*lower[i]*v)[0]+(b*lower[j]*D[i]-adj[i]*lower[j]*v)[0]))
        T+=G*s.diag(-1,a*a,a*a,a*a)*square
        cls.T=s.simplify(T);cls.dirac_residuals=res

    def test_chirality_and_free_positive_energy_modes(self):
        for r in self.free_eigen_residuals:self.assertEqual(r,s.zeros(4,1))

    def test_total_current_is_timelike_axial_current_is_timelike(self):
        self.assertEqual(self.current,[self.n,0,0,0]);self.assertEqual(self.axial,[-self.n,0,0,0])

    def test_all_six_nonlinear_dirac_equations(self):
        for r in self.dirac_residuals:self.assertEqual(r,s.zeros(4,1))

    def test_full_sum_stress_without_spin_averaging(self):
        a,n,p,G=self.a,self.n,self.p,self.G
        E=p*n/a-G*n*n;P=p*n/(3*a)-G*n*n
        self.assertEqual(s.simplify(self.T-s.diag(E,a*a*P,a*a*P,a*a*P)),s.zeros(4))

    def test_conformal_closed_form_satisfies_both_einstein_equations(self):
        eta=s.symbols('eta',real=True);k,G,n0,p=s.symbols('k G n0 p',positive=True)
        ab2=G*n0/p;q2=k*p*n0/3;a=s.sqrt(ab2+q2*eta**2)
        H=s.diff(a,eta)/a**2;dH=s.diff(H,eta)/a;density=n0/a**3
        E=p*density/a-G*density*density;P=p*density/(3*a)-G*density*density
        self.assertEqual(s.simplify(3*H*H-k*E),0)
        self.assertEqual(s.simplify(dH+k*(E+P)/2),0)

    def test_exact_phase_and_accelerated_efold_count(self):
        x,p=s.symbols('x p',real=True,positive=True)
        eta=3*x/(4*p);phase=3*x/4-s.Rational(3,2)*s.atan(x)
        # theta' = p - 2 G n0 / a² = p [1 - 2/(1+x²)]
        self.assertEqual(s.simplify(s.diff(phase,x)/(s.diff(eta,x))-p*(1-2/(1+x*x))),0)
        N=s.log(1+x*x)/2
        self.assertEqual(s.simplify(N.subs(x,1)),s.log(2)/2)
        acceleration=(1-x*x)/(1+x*x)**3
        self.assertEqual(acceleration.subs(x,1),0)
        self.assertEqual(s.limit(N,x,s.oo),s.oo)

    def test_proper_and_null_affine_clocks_extend_both_ways(self):
        eta=s.symbols('eta',real=True);b,q=s.symbols('b q',positive=True)
        a=s.sqrt(b*b+q*q*eta*eta)
        proper=(eta*a+b*b/q*s.asinh(q*eta/b))/2
        self.assertEqual(s.simplify(s.diff(proper,eta)-a),0)
        affine=b*b*eta+q*q*eta**3/3
        self.assertEqual(s.expand(s.diff(affine,eta)-a*a),0)
        self.assertEqual(s.limit(proper,eta,s.oo),s.oo)
        self.assertEqual(s.limit(proper,eta,-s.oo),-s.oo)
        self.assertEqual(s.limit(affine,eta,s.oo),s.oo)
        self.assertEqual(s.limit(affine,eta,-s.oo),-s.oo)

    def test_torsion_free_comparison_has_radiation_curvature_singularity(self):
        eta=s.symbols('eta',negative=True);q=s.symbols('q',positive=True);a=-q*eta
        H=s.diff(a,eta)/a**2;dH=s.diff(H,eta)/a
        scalar=6*(dH+2*H*H);kretsch=12*((dH+H*H)**2+H**4)
        self.assertEqual(s.simplify(scalar),0)
        self.assertEqual(s.limit(kretsch,eta,0,dir='-'),s.oo)

    def test_pauli_normalized_six_mode_scale(self):
        L,kappa=s.symbols('L kappa',positive=True);p=2*s.pi/L;n0=6/L**3;G=3*kappa/16
        rho_b=p**3/(G*G*n0)
        self.assertEqual(s.simplify(rho_b),1024*s.pi**3/(27*kappa*kappa))
        self.assertGreater(float((rho_b*kappa*kappa).simplify()),1000)

    def test_positive_scalar_curvature_efold_bound_for_single_field(self):
        m,k,R=s.symbols('m k R',positive=True);G=3*k/16
        roots=[(m-s.sqrt(m*m-8*G*R/k))/(4*G),(m+s.sqrt(m*m-8*G*R/k))/(4*G)]
        for n in roots:self.assertEqual(s.simplify(k*m*n-2*k*G*n*n-R),0)
        self.assertEqual(s.simplify(k*m*m/(8*G)),2*m*m/3)

if __name__=='__main__':unittest.main()
