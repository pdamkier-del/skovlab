"""Limited action/state/scale checks. No evolution or dense-matter EOS solver."""
import math
import unittest
import sympy as s
from sympy.physics.matrices import mgamma

ETA = [-1, 1, 1, 1]
LOW = [mgamma(i) for i in range(4)]
UP = [ETA[i]*LOW[i] for i in range(4)]
G5 = -s.I*UP[0]*UP[1]*UP[2]*UP[3]


class ECMatterChecks(unittest.TestCase):
    def zero(self, expr):
        if isinstance(expr, s.MatrixBase):
            self.assertEqual(s.simplify(expr), s.zeros(*expr.shape))
        else:
            self.assertEqual(s.simplify(expr), 0)

    def test_01_negative_Clifford_sign_and_canonical_time_coefficient(self):
        for a in range(4):
            for b in range(4):
                rhs=-2*ETA[a]*s.eye(4) if a==b else s.zeros(4)
                self.zero(UP[a]*UP[b]+UP[b]*UP[a]-rhs)
        # bar(psi)=psi^dagger gamma^0 gives +i psi^dagger d_t psi.
        self.zero(UP[0]*UP[0]-s.eye(4))

    def test_02_chirality_and_antisymmetric_spin_variation(self):
        self.zero(G5*G5-s.eye(4))
        for a in range(4):
            self.zero(G5*UP[a]+UP[a]*G5)
        tensor=lambda a,b,c: UP[a]*(UP[b]*UP[c]-UP[c]*UP[b])+(UP[b]*UP[c]-UP[c]*UP[b])*UP[a]
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    self.zero(tensor(a,b,c)+tensor(b,a,c))
                    self.zero(tensor(a,b,c)+tensor(a,c,b))

    @staticmethod
    def axial_tensors():
        axial=s.symbols("a0:4",real=True)
        lower=lambda a,b,c:-sum(s.LeviCivita(a,b,c,d)*axial[d] for d in range(4))/6
        cont=lambda a,b,c:(lower(a,b,c)-lower(b,c,a)+lower(c,a,b))/2
        return axial,lower,cont

    def test_03_full_axial_torsion_reconstruction_and_contortion(self):
        axial,T,K=self.axial_tensors()
        for d in range(4):
            # epsilon^{abcd}=-epsilon_{abcd} in this Lorentz frame.
            self.zero(sum(-s.LeviCivita(a,b,c,d)*T(a,b,c) for a in range(4)
                          for b in range(4) for c in range(4))-axial[d])
        for a in range(4):
            self.zero(sum(ETA[b]*T(b,a,b) for b in range(4)))
            for b in range(4):
                for c in range(4):
                    self.zero(K(a,b,c)-T(a,b,c)/2)
                    self.zero(K(a,b,c)+K(c,b,a))

    def test_04_scalar_curvature_auxiliary_coefficient(self):
        axial,T,K=self.axial_tensors()
        Ku=lambda a,b,c:ETA[a]*K(a,b,c)
        deltaR=sum(ETA[j]*sum(Ku(i,i,m)*Ku(m,j,j)-Ku(i,j,m)*Ku(m,i,j)
                   for i in range(4) for m in range(4)) for j in range(4))
        self.zero(deltaR-sum(ETA[d]*axial[d]**2 for d in range(4))/24)

    def test_05_Dirac_contortion_coupling_with_explicit_gamma_matrices(self):
        axial,T,K=self.axial_tensors()
        connection=lambda mu,a,b:ETA[a]*ETA[b]*K(a,mu,b)
        coupling=s.zeros(4)
        for mu in range(4):
            for a in range(4):
                for b in range(4):
                    comm=LOW[a]*LOW[b]-LOW[b]*LOW[a]
                    coupling+=s.I*connection(mu,a,b)*(UP[mu]*comm+comm*UP[mu])/16
        expected=sum((ETA[d]*axial[d]*G5*UP[d] for d in range(4)),s.zeros(4))/8
        self.zero(coupling-expected)

    def test_06_algebraic_Cartan_elimination_including_material_term(self):
        kappa=s.symbols("kappa",positive=True)
        axial=s.symbols("a0:4");current=s.symbols("J0:4")
        L=sum(ETA[d]*(axial[d]**2/(48*kappa)+axial[d]*current[d]/8) for d in range(4))
        solution=s.solve([s.diff(L,a) for a in axial],axial,dict=True)[0]
        for d in range(4):
            self.zero(solution[axial[d]]+3*kappa*current[d])
        self.zero(L.subs(solution)+3*kappa*sum(ETA[d]*current[d]**2 for d in range(4))/16)
        # Eliminating the gravitational term alone would give the wrong sign/factor.
        gravity_only=sum(ETA[d]*axial[d]**2/(48*kappa) for d in range(4))
        self.zero(gravity_only.subs(solution)-3*kappa*sum(ETA[d]*current[d]**2 for d in range(4))/16)

    def test_07_Dirac_principal_cone(self):
        cov=s.symbols("xi0:4",real=True)
        symbol=sum((UP[d]*cov[d] for d in range(4)),s.zeros(4))
        norm=sum(ETA[d]*cov[d]**2 for d in range(4))
        self.zero(symbol*symbol+norm*s.eye(4))
        self.zero(symbol.det()-norm**2)

    def test_08_Wick_exchange_in_nonrelativistic_normal_state(self):
        up,down=s.symbols("n_up n_down",nonnegative=True)
        R=s.diag(up,down)
        pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
        direct=sum(s.trace(sig*R)**2 for sig in pauli)
        exchange=sum(s.trace(sig*R*sig*R) for sig in pauli)
        self.zero(direct-(up-down)**2)
        self.zero(direct-exchange+6*up*down)
        n,z=s.symbols("n z",real=True)
        self.zero((direct-exchange).subs({up:n*(1+z)/2,down:n*(1-z)/2})
                  +s.Rational(3,2)*n*n*(1-z*z))

    def test_09_independent_Fock_space_contact_factor(self):
        ann=s.Matrix([[0,1],[0,0]]);Z=s.diag(1,-1)
        c=[s.kronecker_product(ann,s.eye(2)),s.kronecker_product(Z,ann)]
        number=[v.H*v for v in c]
        pauli=[s.Matrix([[0,1],[1,0]]),s.Matrix([[0,-s.I],[s.I,0]]),s.diag(1,-1)]
        spin=[sum((c[a].H*sig[a,b]*c[b] for a in range(2) for b in range(2)),s.zeros(4))
              for sig in pauli]
        normal_ordered=sum((v*v for v in spin),s.zeros(4))-3*(number[0]+number[1])
        self.zero(normal_ordered+6*number[0]*number[1])
        self.assertEqual(list(normal_ordered.diagonal()),[0,0,0,-6])

    def test_10_state_dependent_thermodynamics(self):
        n,G,z,T=s.symbols("n G z T",real=True)
        f=-s.Rational(3,2)*G*n*n*(1-z*z)
        self.zero(n*s.diff(f,n)-f-f)
        self.zero(f-T*s.diff(f,T)-f)
        # A variable correlator must also be differentiated.
        C=s.Function("C")(n)
        variable=G*C*n*n
        self.zero(n*s.diff(variable,n)-variable-G*(C*n*n+n**3*s.diff(C,n)))

    def test_11_total_current_requires_cross_species(self):
        J=s.symbols("J0:4");K=s.symbols("K0:4")
        total=sum(ETA[d]*(J[d]+K[d])**2 for d in range(4))
        self.zero(total-sum(ETA[d]*(J[d]**2+K[d]**2+2*J[d]*K[d]) for d in range(4)))

    def test_12_physical_scales_and_invalid_nonrelativistic_extrapolation(self):
        M=2.435e18;G=3/(16*M*M);hbarc=.1973269804
        n0=.16*hbarc**3;m=.939
        self.assertTrue(3.16e-38<G<3.17e-38)
        self.assertTrue(6.20e-41<1.5*G*n0/m<6.22e-41)
        ncrit=m/(1.5*G);pcrit=(3*math.pi**2*ncrit)**(1/3)
        self.assertGreater(pcrit/m,1e12)
        g,C,p,MP=s.symbols("g C p MP",positive=True)
        density=g*p**3/(6*s.pi**2);energy=g*p**4/(8*s.pi**2)
        self.zero((3/(16*MP**2))*C*density**2/energy-g*C*p**2/(24*s.pi**2*MP**2))

    def test_13_previous_Weyssenhoff_sound_formula_as_conditional_limit(self):
        n,C,D,w=s.symbols("n C D w",positive=True)
        rho=C*n**(1+w);q=D*n*n
        eps=rho-q;P=w*rho-q
        self.zero(s.diff(P,n)/s.diff(eps,n)-(w*(1+w)*rho-2*q)/((1+w)*rho-2*q))


if __name__=="__main__":
    unittest.main(verbosity=2)
