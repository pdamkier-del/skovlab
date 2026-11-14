import sys,unittest,itertools
from pathlib import Path
import sympy as s
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kinematics import curvature_density_bound,positive_ricci_efold_bound

class AnalyticRelations(unittest.TestCase):
    def test_torsion_contraction_without_fierz_assumption(self):
        k=s.symbols('k',positive=True);A=s.symbols('A0:4',real=True);eta=[-1,1,1,1]
        total=0
        for a,b,c in itertools.product(range(4),repeat=3):
            T=-k*sum(s.LeviCivita(a,b,c,d)*A[d] for d in range(4))/2
            total+=eta[a]*eta[b]*eta[c]*T*T
        self.assertEqual(s.expand(total+s.Rational(3,2)*k*k*sum(eta[i]*A[i]**2 for i in range(4))),0)

    def test_trace_dominates_any_scalar_bilinear_at_infinite_density(self):
        n,m,k,G,beta=s.symbols('n m k G beta',positive=True)
        R=k*m*n*s.cos(beta)-2*k*G*n*n
        self.assertEqual(s.limit(R/(n*n),n,s.oo),-2*k*G)

    def test_full_connection_scalar_can_hide_metric_and_torsion_divergence(self):
        k,n,m,S=s.symbols('k n m S',positive=True);G=3*k/16
        metric=k*m*S-2*k*G*n*n
        full=metric+3*k*k*n*n/8
        self.assertEqual(s.expand(full),k*m*S)
        self.assertEqual(s.expand(full.subs(m,0)),0)
        self.assertEqual(s.expand(metric.subs(m,0)),-3*k*k*n*n/8)

    def test_curvature_bound_root_and_compression_fold(self):
        m,k,L=s.symbols('m k L',positive=True);G=3*k/16
        maximum=(m+s.sqrt(m*m+8*G*L/k))/(4*G)
        self.assertEqual(s.simplify(2*G*maximum**2-m*maximum-L/k),0)
        bound=curvature_density_bound(.1,1.,.01)
        self.assertGreater(bound,0)
        with self.assertRaises(ValueError):curvature_density_bound(.1,0,.01)

    def test_density_and_torsion_efold_scalings(self):
        N,n0,k=s.symbols('N n0 k',real=True,positive=True);n=n0*s.exp(-3*N)
        self.assertEqual(s.simplify(n*n/(n0*n0)),s.exp(-6*N))
        self.assertEqual(s.simplify(-s.log(n/n0)/3),N)

    def test_volume_tilt_and_clock_rates(self):
        theta,u0,Dn,Wdot,W=s.symbols('theta u0 Dn Wdot W')
        # d ln n/dt = (-theta + div j/n)/u0 along the current.
        density_rate=(theta-Dn)/(3*u0);source_rate=Dn/(3*u0)
        self.assertEqual(s.simplify(density_rate+source_rate-theta/(3*u0)),0)
        slice_rate=theta/(3*u0)-Wdot/(3*W)
        self.assertEqual(s.simplify(slice_rate+Wdot/(3*W)-theta/(3*u0)),0)

    def test_local_bounce_taylor_does_not_fix_total_folds(self):
        t,B,C=s.symbols('t B C',real=True)
        theta=B*t+C*t*t/2
        N=s.integrate(theta,(t,0,t))/3
        self.assertEqual(s.expand(N),B*t*t/6+C*t**3/18)
        self.assertEqual(s.simplify((B*t*t/6).subs(B,s.Rational(287,96))),s.Rational(287,576)*t*t)

    def test_total_axial_current_has_no_total_density_fierz_identity(self):
        n=s.symbols('n',positive=True)
        first=s.Matrix([0,0,0,n]);second=-first
        self.assertEqual((first+second).dot(first+second),0)
        self.assertNotEqual(0,(2*n)**2)

    def test_finite_species_bilinear_bounds_in_fixed_cases(self):
        import numpy as np
        from kinematics import ecd
        rng=np.random.default_rng(58);metric=np.diag(ecd.ETA)
        for count in [1,2,6]:
            fields=rng.normal(size=(count,4))+1j*rng.normal(size=(count,4))
            bars=fields.conj()@ecd.GAMMA[0]
            j=np.einsum('fi,aij,fj->a',bars,ecd.GAMMA,fields).real
            A=np.einsum('fi,aij,fj->a',bars,np.array([ecd.G5@g for g in ecd.GAMMA]),fields).real
            n2=-j@metric@j;axial=A@metric@A
            self.assertLessEqual(abs(axial),n2+1e-10)
            scalars=np.einsum('fi,fi->f',bars,fields).real
            self.assertLessEqual(np.sum(np.abs(scalars)),np.sqrt(n2)+1e-10)

    def test_positive_ricci_phase_necessary_efold_bound(self):
        m,k,L=s.symbols('m k L',positive=True);G=3*k/16
        lower=(-m+s.sqrt(m*m+8*G*L/k))/(4*G)
        self.assertEqual(s.simplify(k*m*lower+2*k*G*lower**2-L),0)
        # The single-field bound for a de Sitter curvature R=12 H².
        N=s.symbols('N',positive=True)
        x=s.tanh(3*N/2)
        self.assertEqual(s.simplify(1-x*x-1/s.cosh(3*N/2)**2),0)
        b=positive_ricci_efold_bound(1.,1.,.12)
        self.assertGreater(b['necessary_net_efold_bound'],0)
        with self.assertRaises(ValueError):positive_ricci_efold_bound(0,1,.1)
        with self.assertRaises(ValueError):positive_ricci_efold_bound(1,1,1.)

    def test_average_and_evolution_do_not_commute(self):
        # Two followed infinitesimal volumes: the domain log-volume is not
        # the unweighted arithmetic mean of their local log-volumes.
        import numpy as np
        N=np.array([.1,.3]);domain=np.log(np.mean(np.exp(3*N)))/3
        self.assertGreater(domain,np.mean(N))

if __name__=='__main__':unittest.main()
