import unittest
import sympy as s
from geometry import t,r,theta,phi,x,Phi,Lam,R,A,B,g,connection,coordinate_curvature,hand_components,clean,substitute,covariant_divergence,full_spin_derivative,spatial_spin_transport

class SymbolicAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ric,cls.scalar,cls.G=coordinate_curvature()

    def zero(self,expr): self.assertEqual(clean(expr),0)

    def test_01_independent_einstein_components(self):
        e00,e11,e01,e22=hand_components()
        for actual,expected in [(self.G[0,0]/A**2,e00),(self.G[1,1]/B**2,e11),(self.G[0,1],e01),(self.G[2,2]/R**2,e22),(self.G[3,3],s.sin(theta)**2*self.G[2,2])]: self.zero(actual-expected)
        for a,b in [(0,2),(0,3),(1,2),(1,3),(2,3)]: self.zero(self.G[a,b])

    def test_02_warped_product_derivation(self):
        C=connection(); inv=g.inv(); hess=lambda a,b:s.diff(R,x[a],x[b])-sum(C[c,a,b]*s.diff(R,x[c]) for c in range(2))
        box=sum(inv[a,b]*hess(a,b) for a in range(2) for b in range(2)); norm=-s.diff(R,t)**2/A**2+s.diff(R,r)**2/B**2
        for a in range(2):
            for b in range(2): self.zero(self.G[a,b]-(-2*hess(a,b)/R+(2*box/R+(norm-1)/R**2)*g[a,b]))
        rh=clean(self.scalar-2*(1-norm)/R**2+4*box/R)
        self.zero(self.G[2,2]/R**2-(box/R-rh/2))

    def test_03_FLRW_limit_all_curvatures(self):
        a=s.Function('a')(t); k=s.symbols('k',real=True); mapping={Phi:0,Lam:s.log(a)-s.log(1-k*r*r)/2,R:a*r}
        self.zero(substitute(self.G[0,0],mapping)-3*(s.diff(a,t)**2+k)/a**2)
        pressure=-2*s.diff(a,t,2)/a-(s.diff(a,t)**2+k)/a**2
        self.zero(substitute(self.G[1,1]/B**2,mapping)-pressure)
        self.zero(substitute(self.G[2,2]/R**2,mapping)-pressure)
        self.zero(substitute(self.G[0,1],mapping))

    def test_04_vacuum_Schwarzschild_and_Minkowski(self):
        m=s.symbols('m',positive=True); F=1-2*m/r
        for mapping in [{Phi:0,Lam:0,R:r},{Phi:s.log(F)/2,Lam:-s.log(F)/2,R:r}]:
            for a,b in [(0,0),(0,1),(1,1),(2,2)]: self.zero(substitute(self.G[a,b],mapping))

    def test_05_general_spherical_conservation_including_flux(self):
        e=s.Function('epsilon')(t,r); pr=s.Function('Pr')(t,r); pt=s.Function('Pt')(t,r); q=s.Function('Q')(t,r)
        T=s.diag(e/A**2,pr/B**2,pt/R**2,pt/(R**2*s.sin(theta)**2)); T[0,1]=T[1,0]=q/(A*B)
        div=covariant_divergence(T); Hr=s.diff(Lam,t)/A; Ht=s.diff(R,t)/(A*R); accel=s.diff(Phi,r)/B; Gamma=s.diff(R,r)/B
        energy=s.diff(e,t)/A+(e+pr)*Hr+2*(e+pt)*Ht+s.diff(q,r)/B+2*q*(Gamma/R+accel)
        momentum=s.diff(q,t)/A+2*q*(Hr+Ht)+s.diff(pr,r)/B+(e+pr)*accel+2*Gamma*(pr-pt)/R
        self.zero(A*div[0]-energy); self.zero(B*div[1]-momentum);self.zero(div[2]);self.zero(div[3])

    def test_06_Misner_Sharp_mass_identities_with_flux(self):
        U=s.diff(R,t)/A; Gamma=s.diff(R,r)/B; mass=R*(1+U**2-Gamma**2)/2
        epsilon=self.G[0,0]/A**2; Pr=self.G[1,1]/B**2; Q=-self.G[0,1]/(A*B) # these are kappa times physical sources
        self.zero(s.diff(mass,r)/B-R**2*(epsilon*Gamma+Q*U)/2)
        self.zero(s.diff(mass,t)/A+R**2*(Pr*U+Q*Gamma)/2)
        self.zero((2*(U+Gamma)/R)*(2*(U-Gamma)/R)-4*(2*mass/R-1)/R**2)

    def test_07_ADM_and_radial_evolution(self):
        U=s.diff(R,t)/A; Gamma=s.diff(R,r)/B; Hr=s.diff(Lam,t)/A; Ht=U/R; acc=s.diff(Phi,r)/B
        r3=2*(1-Gamma**2)/R**2-4*s.diff(Gamma,r)/(B*R)
        self.zero(r3+4*Hr*Ht+2*Ht**2-2*self.G[0,0]/A**2)
        self.zero(s.diff(U,r)/B-Gamma*Hr+R*self.G[0,1]/(2*A*B))
        m=R*(1+U**2-Gamma**2)/2
        self.zero(s.diff(U,t)/A-(Gamma*acc-m/R**2-R*self.G[1,1]/(2*B**2)))
        self.zero(s.diff(Gamma,t)/A-(U*acc-R*self.G[0,1]/(2*A*B)))

    def test_08_spherical_polarized_spin_derivative_vanishes(self):
        b=s.Function('b')(t,r); spin=s.zeros(4);spin[2,3]=R**2*s.sin(theta)*b;spin[3,2]=-spin[2,3]
        D=full_spin_derivative(spin)
        for item in D: self.zero(item)
        transport=spatial_spin_transport(spin)
        expected=R**2*s.sin(theta)*(s.diff(b,t)+(s.diff(Lam,t)+2*s.diff(R,t)/R)*b)/A
        self.zero(transport[2,3]-expected)
        self.zero(transport[1,2]);self.zero(transport[1,3])

    def test_09_unpolarized_covariance_and_effective_action(self):
        # Spatial SO(3) spin covariance: <s_ij s_kl> = S²/3(delta_ik delta_jl - delta_il delta_jk).
        S2=s.symbols('S2'); delta=lambda i,j:int(i==j)
        self.zero(sum(S2*(delta(i,i)*delta(j,j)-delta(i,j)*delta(j,i))/3 for i in range(3) for j in range(3))/2-S2)
        for i in range(3):
            for j in range(3): self.zero(sum(S2*(delta(i,j)*delta(k,k)-delta(i,k)*delta(k,j))/3 for k in range(3))-2*S2*delta(i,j)/3)
        n,C,D,w=s.symbols('n C D w',positive=True); rho=C*n**(1+w);q=D*n*n;epsilon=rho-q
        self.zero(n*s.diff(epsilon,n)-epsilon-(w*rho-q))
        cs=clean(s.diff(w*rho-q,n)/s.diff(epsilon,n));self.zero(cs-(w*(1+w)*rho-2*q)/((1+w)*rho-2*q))

    def test_10_Cartan_contortion_and_elimination_coefficient(self):
        k=s.symbols('kappa',positive=True); b1,b2,b3=s.symbols('b1 b2 b3',real=True);eta=[-1,1,1,1];sp=s.zeros(4);sp[1,2]=b3;sp[2,3]=b1;sp[3,1]=b2;sp=sp-sp.T
        torsion=lambda a,i,j:k*int(a==0)*sp[i,j]
        low=lambda a,i,j:eta[a]*torsion(a,i,j)
        K=lambda a,i,j:eta[a]*(low(a,i,j)-low(i,j,a)+low(j,a,i))/2
        for a in range(4):
            self.zero(sum(torsion(i,a,i) for i in range(4)))
            for i in range(4):
                for j in range(4):
                    self.zero(K(a,i,j)-K(a,j,i)-torsion(a,i,j))
                    self.zero(eta[a]*K(a,i,j)+eta[j]*K(j,i,a))
        # Independently verify the variational Cartan 3-form equation in the rest frame.
        from itertools import combinations
        for c in range(4):
            for d in range(c+1,4):
                for e,f,h in combinations(range(4),3):
                    wedge=sum(s.LeviCivita(a,b,c,d)*(torsion(a,e,f)*int(b==h)+torsion(a,f,h)*int(b==e)+torsion(a,h,e)*int(b==f)) for a in range(4) for b in range(4))
                    self.zero(wedge-k*sp[c,d]*s.LeviCivita(0,e,f,h))
        deltaR=sum(eta[j]*(sum(K(i,i,m)*K(m,j,j)-K(i,j,m)*K(m,i,j) for i in range(4) for m in range(4))) for j in range(4))
        S2=b1*b1+b2*b2+b3*b3
        self.zero(deltaR+k*k*S2/2)
        linear=-sum(sp[a,b]*eta[b]*K(a,0,b) for a in range(4) for b in range(4))/2
        self.zero(deltaR/(2*k)+linear-k*S2/4)

    def test_18_contracted_Bianchi_identity(self):
        inv=g.inv(); Tup=inv*self.G*inv
        for value in covariant_divergence(Tup): self.zero(value)

    def test_19_nonradial_spin_terms_are_not_identically_discarded(self):
        spin=s.zeros(4); spin[1,2]=r*r;spin[2,1]=-r*r
        D=full_spin_derivative(spin)
        values=[clean(substitute(v,{Phi:0,Lam:0,R:r})) for v in D]
        self.assertTrue(any(v!=0 for v in values))

    def test_20_rotation_invariance_of_radial_spin(self):
        b=s.Function('b')(t,r); spin=s.zeros(4);spin[2,3]=R**2*s.sin(theta)*b;spin[3,2]=-spin[2,3]
        generators=[[0,0,0,1],[0,0,-s.sin(phi),-s.cot(theta)*s.cos(phi)],[0,0,s.cos(phi),-s.cot(theta)*s.sin(phi)]]
        for xi in generators:
            for a in range(4):
                for c in range(4):
                    value=sum(xi[d]*s.diff(spin[a,c],x[d])+spin[d,c]*s.diff(xi[d],x[a])+spin[a,d]*s.diff(xi[d],x[c]) for d in range(4))
                    self.zero(value)

    def test_21_Raychaudhuri_acceleration_divergence(self):
        Hr=s.diff(Lam,t)/A; Ht=s.diff(R,t)/(A*R); expansion=Hr+2*Ht; shear=(Hr-Ht)**2/3
        acceleration=s.diff(Phi,r)/B; Gamma=s.diff(R,r)/B
        div=s.diff(acceleration,r)/B+2*Gamma*acceleration/R+acceleration**2
        rhs=-expansion**2/3-2*shear-(self.G[0,0]/A**2+self.G[1,1]/B**2+2*self.G[2,2]/R**2)/2+div
        self.zero(s.diff(expansion,t)/A-rhs)

    def test_22_warped_Kretschmann_FLRW_limit(self):
        C=connection(); inv=g.inv(); hess=lambda a,b:s.diff(R,x[a],x[b])-sum(C[c,a,b]*s.diff(R,x[c]) for c in range(2))
        box=sum(inv[a,b]*hess(a,b) for a in range(2) for b in range(2)); norm=-s.diff(R,t)**2/A**2+s.diff(R,r)**2/B**2
        Rh=clean(self.scalar-2*(1-norm)/R**2+4*box/R)
        hnorm=sum(inv[a,a]*inv[b,b]*hess(a,b)**2 for a in range(2) for b in range(2))
        K=Rh**2+8*hnorm/R**2+4*(1-norm)**2/R**4
        a=s.Function('a')(t); k=s.symbols('k'); mapping={Phi:0,Lam:s.log(a)-s.log(1-k*r*r)/2,R:a*r}
        expected=12*((s.diff(a,t,2)/a)**2+((s.diff(a,t)**2+k)/a**2)**2)
        self.zero(substitute(K,mapping)-expected)

    def test_23_metric_FLRW_with_noninheriting_aligned_spin(self):
        a=s.Function('a')(t); b=s.Function('beta')(t)
        # Cartesian homogeneous axial spin along z, pulled back to spherical coordinates.
        spin=s.zeros(4);spin[1,3]=a**2*b*r*s.sin(theta)**2;spin[2,3]=a**2*b*r*r*s.sin(theta)*s.cos(theta);spin=spin-spin.T
        mapping={Phi:0,Lam:s.log(a),R:a*r}
        for item in full_spin_derivative(spin):self.zero(substitute(item,mapping))
        inv=g.inv();norm=sum(inv[i,i]*inv[j,j]*spin[i,j]**2 for i in range(4) for j in range(4))/2
        self.zero(substitute(norm,mapping)-b**2)
        for (i,j),item in spatial_spin_transport(spin).items():
            self.zero(substitute(item,mapping)-spin[i,j]/b*(s.diff(b,t)+3*s.diff(a,t)*b/a))
        # This is metric-only FLRW, not an SO(3)-invariant spin configuration.
        xi=[0,0,-s.sin(phi),-s.cot(theta)*s.cos(phi)]
        lie=sum(xi[d]*s.diff(spin[1,3],x[d])+spin[d,3]*s.diff(xi[d],x[1])+spin[1,d]*s.diff(xi[d],x[3]) for d in range(4))
        self.assertNotEqual(clean(lie),0)

if __name__=='__main__': unittest.main(verbosity=2)
