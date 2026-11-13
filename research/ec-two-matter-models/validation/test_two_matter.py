"""Limited covariant/state/exterior checks; no field evolution or ADM expansion."""
import unittest
import sympy as s
from sympy.physics.matrices import mgamma

ETA=s.diag(-1,1,1,1)
GAMMA=[ETA[i,i]*mgamma(i) for i in range(4)]
G5=-s.I*GAMMA[0]*GAMMA[1]*GAMMA[2]*GAMMA[3]


class TwoMatterChecks(unittest.TestCase):
    def zero(self,value):
        if isinstance(value,s.MatrixBase):
            self.assertEqual(s.simplify(value),s.zeros(*value.shape))
        else:
            self.assertEqual(s.simplify(s.expand(value)),0)

    def test_01_classical_single_spinor_Fierz_identities(self):
        real=s.symbols("x0:4",real=True);imag=s.symbols("y0:4",real=True)
        psi=s.Matrix([real[i]+s.I*imag[i] for i in range(4)])
        bar=psi.H*GAMMA[0]
        vector=s.Matrix([(bar*GAMMA[i]*psi)[0] for i in range(4)])
        axial=s.Matrix([(bar*G5*GAMMA[i]*psi)[0] for i in range(4)])
        scalar=(bar*psi)[0];pseudo=(s.I*bar*G5*psi)[0]
        self.zero((vector.T*ETA*vector)[0]+scalar**2+pseudo**2)
        self.zero((axial.T*ETA*axial)[0]-scalar**2-pseudo**2)
        self.zero((vector.T*ETA*axial)[0])

    def test_02_on_shell_Dirac_stress_and_Hamiltonian_check(self):
        n,m,G=s.symbols("n m G",positive=True)
        psi=s.Matrix([0,0,s.sqrt(n),0]);bar=psi.H*GAMMA[0]
        axial=s.Matrix([(bar*G5*GAMMA[i]*psi)[0] for i in range(4)])
        J2=(axial.T*ETA*axial)[0]
        energy=m+2*G*n
        eq=(energy*GAMMA[0]-m*s.eye(4)
            -2*G*sum((ETA[i,i]*axial[i]*G5*GAMMA[i] for i in range(4)),s.zeros(4)))*psi
        self.zero(eq)
        self.zero(J2-n*n)
        # psi=e^{-i E t} psi0, with no spatial derivative.
        psi_dot=-s.I*energy*psi;bar_dot=s.I*energy*bar
        T=s.zeros(4)
        for i in range(4):
            for j in range(4):
                dpi=psi_dot if i==0 else s.zeros(4,1)
                dpj=psi_dot if j==0 else s.zeros(4,1)
                dbi=bar_dot if i==0 else s.zeros(1,4)
                dbj=bar_dot if j==0 else s.zeros(1,4)
                gi=ETA[i,i]*GAMMA[i];gj=ETA[j,j]*GAMMA[j]
                T[i,j]=-s.I*((bar*gi*dpj-dbj*gi*psi)[0]
                            +(bar*gj*dpi-dbi*gj*psi)[0])/4+G*ETA[i,j]*J2
        self.zero(T[0,0]-(m*n+G*n*n))
        for i in range(1,4):
            self.zero(T[i,i]-G*n*n)
        self.zero(T[0,0]-((bar*psi)[0]*m+G*J2))
        self.zero(T[0,0]+sum(T[i,i] for i in range(1,4))-(m*n+4*G*n*n))

    def test_03_ADM_normal_and_projector_for_general_spatial_metric(self):
        N=s.symbols("N",positive=True);b=s.Matrix(s.symbols("b0:3"))
        aa,bb,cc,dd,ee,ff=s.symbols("a b c d e f",real=True)
        gamma=s.Matrix([[aa,dd,ee],[dd,bb,ff],[ee,ff,cc]])
        metric=s.zeros(4);metric[0,0]=-N*N+(b.T*gamma*b)[0]
        metric[0,1:4]=(gamma*b).T;metric[1:4,0]=gamma*b;metric[1:4,1:4]=gamma
        normal=s.Matrix([1/N,*[-v/N for v in b]])
        low=s.Matrix([-N,0,0,0])
        self.zero(metric*normal-low)
        self.zero((normal.T*metric*normal)[0]+1)
        projector=s.eye(4)+normal*low.T
        self.zero(projector*projector-projector)
        self.zero(projector*normal)

    def test_04_source_projection_with_tilt_and_focusing_trace(self):
        v=s.symbols("v",real=True);W=1/s.sqrt(1-v*v)
        normal=s.Matrix([W,W*v,0,0]);low=ETA*normal
        eps,Px,Py,Pz,Q=s.symbols("eps Px Py Pz Q",real=True)
        T=s.diag(eps,Px,Py,Pz);T[0,1]=T[1,0]=-Q
        E=(normal.T*T*normal)[0]
        self.zero(E-W**2*(eps-2*Q*v+Px*v*v))
        spatial_cov_projector=s.eye(4)+low*normal.T
        momentum=-spatial_cov_projector*T*normal
        self.zero((normal.T*momentum)[0])
        trace=s.trace(ETA*T)
        S=trace+E
        self.zero(E+trace/2-(E+S)/2)
        # In the rest frame the trace-free stress/flux do not change R_uu.
        e,p,pi1,pi2,k=s.symbols("e p pi1 pi2 k")
        tr=-e+(p+pi1)+(p+pi2)+(p-pi1-pi2)
        self.zero(k*(e+tr/2)-k*(e+3*p)/2)

    def test_05_equal_one_body_data_do_not_fix_pair_contact(self):
        ann=s.Matrix([[0,1],[0,0]]);Z=s.diag(1,-1)
        c=[s.kronecker_product(ann,s.eye(2)),s.kronecker_product(Z,ann)]
        double=c[0].H*c[0]*c[1].H*c[1]
        # Half empty/half doubly occupied versus one fermion with random spin.
        stateA=s.diag(s.Rational(1,2),0,0,s.Rational(1,2))
        stateB=s.diag(0,s.Rational(1,2),s.Rational(1,2),0)
        for i in range(2):
            for j in range(2):
                self.zero(s.trace((stateA-stateB)*c[i].H*c[j]))
        self.assertEqual(s.trace(stateA*double),s.Rational(1,2))
        self.assertEqual(s.trace(stateB*double),0)
        self.assertNotEqual(s.trace(stateA*(-6*double)),s.trace(stateB*(-6*double)))

    def test_06_two_beam_moments_allow_anisotropic_stress(self):
        m,p,A=s.symbols("m p A",positive=True);E=s.sqrt(m*m+p*p)
        plus=s.Matrix([E,0,0,p]);minus=s.Matrix([E,0,0,-p])
        N=A*(plus+minus)/E
        T=A*(plus*plus.T+minus*minus.T)/E
        self.zero((plus.T*ETA*plus)[0]+m*m)
        self.zero(N[0]-2*A);self.zero(N[3])
        self.zero(T[0,0]-2*A*E)
        self.zero(T[3,3]-2*A*p*p/E)
        self.zero(T[1,1]);self.zero(T[2,2]);self.zero(T[0,3])
        self.zero(s.trace(ETA*T)+2*A*m*m/E)

    def test_07_spin_curvature_force_is_mass_shell_tangent(self):
        p=s.symbols("p0:4");spin=s.MutableDenseMatrix(4,4,lambda i,j:0)
        for i in range(4):
            for j in range(i+1,4):
                spin[i,j]=s.symbols(f"S{i}{j}");spin[j,i]=-spin[i,j]
        # Only R_{mu nu ab}=-R_{nu mu ab} is needed for p.F=0.
        def curvature(i,j,a,b):
            if i==j or a==b: return 0
            sign=(1 if i<j else -1)*(1 if a<b else -1)
            return sign*s.Symbol(f"R{min(i,j)}{max(i,j)}{min(a,b)}{max(a,b)}")
        force=[-sum(curvature(i,j,a,b)*p[j]*spin[a,b]
                    for j in range(4) for a in range(4) for b in range(4))/2 for i in range(4)]
        self.zero(sum(p[i]*force[i] for i in range(4)))

    def test_08_regular_full_curvature_boundary_for_Dirac_contortion(self):
        k=s.symbols("k",nonzero=True);axial=s.symbols("J0:4")
        C=lambda a,i,j:k*sum(s.LeviCivita(a,i,j,d)*axial[d] for d in range(4))/4
        # Smooth metric junction; zero exterior; local unit normal e_1.
        delta=lambda a,c,i,j:ETA[a,a]*(-int(i==1)*C(a,j,c)+int(j==1)*C(a,i,c))
        coefficients=[delta(a,c,i,j) for a in range(4) for c in range(4)
                      for i in range(4) for j in range(4)]
        matrix,rhs=s.linear_eq_to_matrix(coefficients,axial)
        self.assertEqual(matrix.rank(),4)
        self.assertEqual(rhs,s.zeros(256,1))
        for value in coefficients:
            self.zero(value.subs(dict.fromkeys(axial,0)))

    def test_09_electromagnetic_exterior_is_not_GR_vacuum(self):
        Q,r=s.symbols("Q r",positive=True)
        E=Q/(4*s.pi*r*r)
        self.zero(4*s.pi*r*r*E-Q)
        self.zero(E*E/2-Q*Q/(32*s.pi**2*r**4))
        self.assertGreater((E*E/2).subs({Q:1,r:1}),0)
        # Net charge alone does not constrain transverse/radiative field energy.
        radiation=s.symbols("radiation",nonzero=True,real=True)
        self.assertNotEqual(radiation**2,0)

    def test_10_current_compression_and_directional_volume_distinction(self):
        n,theta=s.symbols("n theta")
        # Divergence of n u = 0: material derivative of n plus n Theta.
        ndot=-n*theta
        self.zero(ndot+n*theta)
        # Zero volume expansion can coexist with an actively contracting axis.
        rates=[-2,1,1]
        self.assertEqual(sum(rates),0)
        self.assertLess(rates[0],0)
        # A direction at an instantaneous turn need not stop total contraction.
        self.assertEqual([0,-1,-2][0],0)
        self.assertLess(sum([0,-1,-2]),0)


if __name__=="__main__":
    unittest.main(verbosity=2)
