"""Independent gamma algebra, coordinate geometry and constraint checks."""
import unittest
import sympy as s
from sympy.physics.matrices import mgamma

class Derivation(unittest.TestCase):
    def test_curved_spinor_and_complete_stress(self):
        eta=[-1,1,1,1]; g=[eta[i]*mgamma(i) for i in range(4)]; low=[eta[i]*g[i] for i in range(4)]
        g5=-s.I*g[0]*g[1]*g[2]*g[3]
        n,m,G,A,B,C=s.symbols('n m G A B C',positive=True,real=True)
        p=s.Matrix([0,0,s.sqrt(n),0]); bar=s.conjugate(p).T*g[0]
        J=[(bar*g5*x*p)[0] for x in g]; self.assertEqual(J,[0,0,0,n])
        opposite=s.Matrix([0,0,0,s.sqrt(n)]); opposite_bar=s.conjugate(opposite).T*g[0]
        opposite_J=[(opposite_bar*g5*x*opposite)[0] for x in g]
        self.assertEqual(opposite_J,[0,0,0,-n])
        th=A+B+C; w=m+2*G*n
        Dp=[(-th/2-s.I*w)*p]+[H/2*g[0]*g[i]*p for i,H in enumerate([A,B,C],1)]
        Db=[(-th/2+s.I*w)*bar]+[-bar*(H/2*g[0]*g[i]) for i,H in enumerate([A,B,C],1)]
        eq=s.I*sum((g[i]*Dp[i] for i in range(4)),s.zeros(4,1))-m*p-2*G*sum((eta[i]*J[i]*g5*g[i]*p for i in range(4)),s.zeros(4,1))
        self.assertEqual(s.simplify(eq),s.zeros(4,1))
        opposite_D=[(-th/2-s.I*w)*opposite]+[H/2*g[0]*g[i]*opposite for i,H in enumerate([A,B,C],1)]
        opposite_eq=s.I*sum((g[i]*opposite_D[i] for i in range(4)),s.zeros(4,1))-m*opposite-2*G*sum((eta[i]*opposite_J[i]*g5*g[i]*opposite for i in range(4)),s.zeros(4,1))
        self.assertEqual(s.simplify(opposite_eq),s.zeros(4,1))
        T=s.Matrix(4,4,lambda i,j:s.simplify(-s.I/4*((bar*low[i]*Dp[j]-Db[j]*low[i]*p)[0]+(bar*low[j]*Dp[i]-Db[i]*low[j]*p)[0])+(G*eta[i]*n*n if i==j else 0)))
        self.assertEqual(s.simplify(T.subs(B,A)-s.diag(m*n+G*n*n,G*n*n,G*n*n,G*n*n)),s.zeros(4))
        self.assertEqual(T[1,2],n*(B-A)/4)  # Generic diagonal Bianchi I is inconsistent.
        self.assertEqual(s.simplify((bar*g[0]*Dp[0]+Db[0]*g[0]*p)[0]+th*n),0)

    def test_coordinate_einstein_tensor(self):
        t,x,y,z=s.symbols('t x y z'); coords=[t,x,y,z]
        a,b=s.Function('a')(t),s.Function('b')(t)
        metric=s.diag(-1,a*a,a*a,b*b); inv=metric.inv()
        gamma=[[[s.simplify(sum(inv[i,l]*(s.diff(metric[l,k],coords[j])+s.diff(metric[l,j],coords[k])-s.diff(metric[j,k],coords[l])) for l in range(4))/2) for k in range(4)] for j in range(4)] for i in range(4)]
        ric=s.Matrix(4,4,lambda i,j:s.simplify(sum(s.diff(gamma[k][i][j],coords[k])-s.diff(gamma[k][i][k],coords[j])+sum(gamma[k][k][l]*gamma[l][i][j]-gamma[k][j][l]*gamma[l][i][k] for l in range(4)) for k in range(4))))
        scalar=s.simplify(s.trace(inv*ric)); ein=s.simplify(ric-metric*scalar/2)
        A=s.diff(a,t)/a; B=s.diff(b,t)/b
        self.assertEqual(s.simplify(ein[0,0]-(A*A+2*A*B)),0)
        self.assertEqual(s.simplify(ein[1,1]/a**2+s.diff(A,t)+s.diff(B,t)+A*A+B*B+A*B),0)
        self.assertEqual(s.simplify(ein[3,3]/b**2+2*s.diff(A,t)+3*A*A),0)
        for i in range(4):
            for j in range(i): self.assertEqual(ein[i,j],0)

    def test_constraint_propagation_and_exact_volume(self):
        H,D,n,m,G=s.symbols('H D n m G',real=True)
        E=m*n+G*n*n; P=G*n*n
        f=[-3*H*H+(E-P)/2,-3*H*D,-3*H*n]
        C=6*H*H-2*E-2*D*D/3
        self.assertEqual(s.expand(sum(s.diff(C,q)*v for q,v in zip([H,D,n],f))+6*H*C),0)
        self.assertEqual(s.expand(3*f[0]+9*H*H-s.Rational(3,2)*m*n),0)
        self.assertEqual(s.expand(s.diff(E,n)*f[2]+3*H*(E+P)),0)

    def test_generalized_friedmann_and_normal_focusing(self):
        H,d1,d2,d3,R,E=s.symbols('H d1 d2 d3 R E')
        K=s.diag(-H-d1,-H-d2,-H+d1+d2)
        norm=d1*d1+d2*d2+(d1+d2)**2
        self.assertEqual(s.expand(R+s.trace(K)**2-s.trace(K*K)-2*E-(R+6*H*H-norm-2*E)),0)

if __name__=='__main__': unittest.main()
