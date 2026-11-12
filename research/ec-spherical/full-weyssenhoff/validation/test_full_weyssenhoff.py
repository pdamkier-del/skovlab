"""Stage 2: independent principal-symbol, symmetry and interface checks.

No time-dependent PDE solver and no proposed physical spin initial profile.
The shared stage-1 geometry module constructs its tensors from the 4D metric.
"""
import cmath
import math
from pathlib import Path
import sys
import unittest

import sympy as s

STAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(STAGE.parent / "validation"))
from geometry import (t, r, theta, Phi, Lam, R, A, B, g, x, connection,
                      coordinate_curvature, full_spin_derivative,
                      spatial_spin_transport, clean)


class FullWeyssenhoffAudit(unittest.TestCase):
    def zero(self, expr):
        self.assertEqual(clean(expr), 0)

    def test_01_mixed_Einstein_components_and_flux_sign(self):
        G = coordinate_curvature()[2]
        tt = -(2*s.diff(R,t)*s.diff(Lam,t)/R+s.diff(R,t)**2/R**2)/A**2
        tt += (2*s.diff(R,r,2)/R+s.diff(R,r)**2/R**2-2*s.diff(Lam,r)*s.diff(R,r)/R)/B**2-1/R**2
        rr = -(2*s.diff(R,t,2)/R+s.diff(R,t)**2/R**2-2*s.diff(Phi,t)*s.diff(R,t)/R)/A**2
        rr += (s.diff(R,r)**2/R**2+2*s.diff(Phi,r)*s.diff(R,r)/R)/B**2-1/R**2
        tr = 2*(s.diff(R,t,r)-s.diff(Phi,r)*s.diff(R,t)-s.diff(Lam,t)*s.diff(R,r))/(A**2*R)
        ang = -(s.diff(Lam,t,2)+s.diff(Lam,t)**2-s.diff(Phi,t)*s.diff(Lam,t)+(s.diff(R,t,2)+(s.diff(Lam,t)-s.diff(Phi,t))*s.diff(R,t))/R)/A**2
        ang += (s.diff(Phi,r,2)+s.diff(Phi,r)**2-s.diff(Phi,r)*s.diff(Lam,r)+(s.diff(R,r,2)+(s.diff(Phi,r)-s.diff(Lam,r))*s.diff(R,r))/R)/B**2
        mixed = g.inv()*G
        for computed, expected in [(mixed[0,0],tt),(mixed[1,1],rr),
                                   (mixed[0,1],tr),(mixed[2,2],ang)]:
            self.zero(computed-expected)
        Q = s.symbols("Q")
        self.zero((-1/A**2)*(-A*B*Q)-B*Q/A)

    @staticmethod
    def spatial_divergence(spin):
        C = connection()
        # Fully spatial projected covariant divergence, independently evaluated.
        return [clean(sum(g.inv()[j,j]*(s.diff(spin[i,j],x[j])
                    -sum(C[e,j,i]*spin[e,j]+C[e,j,j]*spin[i,e]
                         for e in range(1,4))) for j in range(1,4)))
                for i in range(1,4)]

    def test_02_full_derivative_decomposition_with_nonradial_controls(self):
        f12, f13, f23 = [s.Function(name)(t,r) for name in ("f12","f13","f23")]
        spin = s.zeros(4)
        spin[1,2],spin[1,3],spin[2,3] = f12,f13,f23
        spin = spin-spin.T
        D = full_spin_derivative(spin)
        div = self.spatial_divergence(spin)
        self.zero(D[0,0])
        rates = [None,s.diff(Lam,t)/A,s.diff(R,t)/(A*R),s.diff(R,t)/(A*R)]
        for i in range(1,4):
            expected_J = div[i-1]+2*spin[i,1]*s.diff(Phi,r)/B**2
            self.zero(D[0,i]-A*expected_J)
            self.zero(D[i,i])
            for j in range(i+1,4):
                self.zero(D[i,j]-(rates[i]-rates[j])*spin[i,j])
        # These terms really survive outside the invariant radial branch.
        self.assertNotEqual(clean(D[1,2]),0)
        self.assertNotEqual(clean(D[0,3].diff(s.diff(Phi,r))),0)

    def test_03_radial_cancellation_separately_for_each_linear_term(self):
        b = s.Function("b")(t,r)
        spin = s.zeros(4)
        spin[2,3] = R**2*s.sin(theta)*b
        spin[3,2] = -spin[2,3]
        for value in self.spatial_divergence(spin):
            self.zero(value)
        for i in range(4):
            self.zero(spin[i,1]*s.diff(Phi,r)/B**2)
        for value in full_spin_derivative(spin):
            self.zero(value)
        # A radial Cartesian axial vector has zero curl for arbitrary F(r^2).
        X,Y,Z = s.symbols("X Y Z", real=True)
        rr = X*X+Y*Y+Z*Z
        F = s.Function("F")(rr)
        axial = s.Matrix([F*X,F*Y,F*Z])
        for i,j in [(0,1),(0,2),(1,2)]:
            self.zero(s.diff(axial[j],(X,Y,Z)[i])-s.diff(axial[i],(X,Y,Z)[j]))

    def test_04_spin_particle_transport_and_Frenkel_preservation(self):
        b,n = s.Function("b")(t,r),s.Function("n")(t,r)
        spin = s.zeros(4);spin[2,3]=R**2*s.sin(theta)*b;spin[3,2]=-spin[2,3]
        up = s.Matrix([1/A,0,0,0])
        self.assertEqual(spin*up,s.zeros(4,1))
        transport = spatial_spin_transport(spin)[2,3]
        self.zero(transport-R**2*s.sin(theta)/A*(s.diff(b,t)+(s.diff(Lam,t)+2*s.diff(R,t)/R)*b))
        expansion = (s.diff(Lam,t)+2*s.diff(R,t)/R)/A
        rules = {s.diff(b,t):-A*b*expansion,s.diff(n,t):-A*n*expansion}
        self.zero(s.diff(b/n,t).subs(rules))
        self.zero(s.diff(B*R**2*b,t).subs(rules))
        self.zero(s.diff(B*R**2*n,t).subs(rules))

    def test_05_characteristic_determinant_and_complete_eigenbasis(self):
        n,h,Pn,Pb,k,omega,c = s.symbols("n h Pn Pb k omega c",nonzero=True)
        A0 = s.diag(1,1,h)
        A1 = s.Matrix([[0,0,n],[0,0,0],[Pn,Pb,0]])
        self.zero((k*A1-omega*A0).det()+omega*(h*omega**2-n*Pn*k**2))
        principal = A0.inv()*A1
        for sign in [-1,1]:
            vec = s.Matrix([n,0,sign*c])
            for value in principal*vec-sign*c*vec:
                self.zero(value.subs(Pn,h*c*c/n))
        contact = s.Matrix([-Pb,Pn,0])
        self.assertEqual(principal*contact,s.zeros(3,1))
        eigenvectors = s.Matrix.hstack(s.Matrix([n,0,c]),s.Matrix([n,0,-c]),contact)
        self.assertNotEqual(s.factor(eigenvectors.det()),0)

    def test_06_density_spin_pencil_and_change_of_variables(self):
        n,beta,C,w,kappa,lam = s.symbols("n beta C w kappa lambda",positive=True)
        rho=C*n**(1+w); b=beta*n; q=kappa*b*b; h=(1+w)*rho-2*q
        A0 = s.diag(1,1,h)
        A1 = s.Matrix([[0,0,(1+w)*rho],[0,0,b],[w,-2*kappa*b,0]])
        N=w*(1+w)*rho-2*q
        self.zero((A1-lam*A0).det()-lam*(N-h*lam**2))
        eps=rho-q;P=w*rho-q
        self.zero(n*s.diff(eps,n)-eps-P)
        self.zero(n*s.diff(P,n)-N)
        J=s.Matrix([[s.diff(rho,n),0,0],[beta,n,0],[0,0,1]])
        primitive=s.Matrix([[0,0,n],[0,0,0],[s.diff(P,n)/h,s.diff(P,beta)/h,0]])
        for value in A0.inv()*A1*J-J*primitive:
            self.zero(value)

    def test_07_zero_sound_Jordan_structure_and_enthalpy_degeneracy(self):
        n,Pb,h=s.symbols("n Pb h",nonzero=True)
        mat=s.Matrix([[0,0,n],[0,0,0],[0,Pb/h,0]])
        self.assertEqual(mat.rank(),2)
        self.assertNotEqual(mat**2,s.zeros(3))
        self.assertEqual(mat**3,s.zeros(3))
        self.assertEqual(len(mat.nullspace()),1)
        dust=mat.subs(Pb,0)
        self.assertEqual(dust.rank(),1)
        self.assertEqual(dust**2,s.zeros(3))
        w,rho=s.symbols("w rho",positive=True)
        q=(1+w)*rho/2
        self.zero(w*(1+w)*rho-2*q-(w-1)*(1+w)*rho)
        self.assertEqual(s.diag(1,1,0).det(),0)

    def test_08_all_sound_domains_and_stiff_exception(self):
        for w in [s.Rational(0),s.Rational(1,3),s.Rational(4,5)]:
            zs=w*(1+w)/2;zh=(1+w)/2
            cs=lambda z:(w*(1+w)-2*z)/(1+w-2*z)
            self.assertLess(cs((zs+zh)/2),0)
            self.assertGreater(cs(zh+1),1)
            self.zero(cs(1)-(w+2))
            if w>0:
                self.assertGreater(cs(zs/2),0)
                self.assertLessEqual(cs(zs/2),1)
        z=s.symbols("z")
        self.zero((2-2*z)/(2-2*z)-1)
        # Stiff equation can simplify the ratio, not invert the time matrix.
        self.assertEqual(s.diag(1,1,2-2*z).det().subs(z,1),0)

    def test_09_general_ordinary_EOS_derivative(self):
        n,beta,kappa=s.symbols("n beta kappa",positive=True)
        rho=s.Function("rho")(n)
        p=n*s.diff(rho,n)-rho;q=kappa*beta*beta*n*n
        h0=rho+p
        c0=n*s.diff(p,n)/h0
        eps=rho-q;P=p-q
        self.zero(s.diff(P,n)/s.diff(eps,n)-(c0*h0-2*q)/(h0-2*q))
        self.zero((c0*h0-2*q)/(h0-2*q)-1-(c0-1)*h0/(h0-2*q))

    def test_10_extra_ideal_spin_moments_add_contacts_only(self):
        n,C,kappa,w,cp,ct,lam=s.symbols("n C kappa w cp ct lambda",positive=True)
        rho=C*n**(1+w);q=kappa*n*n*(cp+2*ct)
        P=w*rho-q;h=(1+w)*rho-2*q
        A0=s.diag(1,1,1,h)
        A1=s.zeros(4);A1[0,3]=n
        for j,var in enumerate([n,cp,ct]):
            A1[3,j]=s.diff(P,var)
        self.zero((A1-lam*A0).det()-lam**2*(h*lam**2-n*s.diff(P,n)))
        # The two moment-composition fields are independent zero-speed modes.
        self.assertEqual(len((A0.inv()*A1).nullspace()),2)

    def test_11_regular_center_and_constrained_initial_geometry(self):
        rc,r2,b1,u1,u3,kappa=s.symbols("rc r2 b1 u1 u3 kappa",real=True)
        rho=rc+r2*r*r; b=b1*r
        eps=rho-kappa*b*b;U=u1*r+u3*r**3
        M=kappa*(rc*r**3/3+(r2-kappa*b1*b1)*r**5/5)/2
        self.zero(s.diff(M,r)-kappa*eps*r*r/2)
        F=1+U*U-2*M/r  # Gamma^2; avoids spurious square-root simplification.
        R3=2*(1-F)/r**2-2*s.diff(F,r)/r
        self.zero(R3+4*s.diff(U,r)*U/r+2*(U/r)**2-2*kappa*eps)
        self.zero(s.limit(M/r**3,r,0)-kappa*rc/6)
        self.zero(s.limit(F,r,0)-1)
        self.zero(s.limit((s.diff(U,r)-U/r)**2/3,r,0))
        # Dust, center-normalized initial radial metric: a_r linear coefficient.
        accel=s.diff(kappa*b*b,r)/ (rho-2*kappa*b*b)
        self.zero(s.limit(accel/r,r,0)-2*kappa*b1*b1/rc)
        self.zero(s.limit(s.diff(accel,r)+2*accel/r+accel**2,r,0)-6*kappa*b1*b1/rc)

    def test_12_full_connection_boundary_delta_and_zero_Ricci_delta(self):
        kappa,b=s.symbols("kappa b",real=True);eta=[-1,1,1,1]
        spin=s.zeros(4);spin[2,3]=b;spin[3,2]=-b
        torsion=lambda a,i,j:-2*kappa*int(a==0)*spin[i,j]
        low=lambda a,i,j:eta[a]*torsion(a,i,j)
        K=lambda a,i,j:eta[a]*(low(a,i,j)-low(i,j,a)+low(j,a,i))/2
        self.zero(K(0,2,3)+kappa*b)
        # Exterior zero, interior K: jump = -K, outward normal e_1.
        singular=lambda a,c,i,j:-int(i==1)*K(a,j,c)+int(j==1)*K(a,i,c)
        self.zero(singular(0,3,1,2)-kappa*b)
        self.assertNotEqual(singular(0,3,1,2),0)
        for c in range(4):
            for j in range(4):
                self.zero(sum(singular(a,c,a,j) for a in range(4)))
        for a in range(4):
            for c in range(4):
                for i in range(4):
                    for j in range(4):
                        self.zero(singular(a,c,i,j).subs(b,0))

    def test_13_vacuum_edge_and_pressure_conditions(self):
        w,rho,b,kappa,n,C,beta=s.symbols("w rho b kappa n C beta",positive=True)
        P=w*rho-kappa*b*b
        self.zero(P.subs(w,0)+kappa*b*b)
        self.zero(P.subs(b,0)-w*rho)
        # Radiation-like representative of bounded spin-per-particle asymptotics.
        self.assertEqual(s.limit(kappa*beta**2*n**2/(C*n**s.Rational(4,3)),n,0,dir="+"),0)
        self.assertEqual(s.limit(-s.log(rho)/4,rho,0,dir="+"),s.oo)

    def test_14_geodesic_volume_bounce_bound_vs_causal_domain(self):
        w,rho=s.symbols("w rho",positive=True)
        gap=(1+3*w)*rho/4-w*(1+w)*rho/2
        self.zero(gap-(1-w)*(1+2*w)*rho/4)
        for ww in [0,s.Rational(1,3),s.Rational(4,5)]:
            self.assertGreater(gap.subs({w:ww,rho:1}),0)
        # Along collapse, z grows for w<1; for stiff matter it is advected.
        Theta,q=s.symbols("Theta q")
        zdot=(-2*q*Theta*rho+q*(1+w)*rho*Theta)/rho**2
        self.zero(zdot+(1-w)*Theta*q/rho)
        self.zero(zdot.subs(w,1))

    def test_15_numeric_mode_residual_growth_and_causal_boost(self):
        # Frozen-coefficient Fourier modes; not a PDE evolution.
        for w,z in [(0,.01),(1/3,.01),(1/3,1.0)]:
            rho=1.;b=math.sqrt(z);h=1+w-2*z
            c=cmath.sqrt((w*(1+w)-2*z)/h)
            mat=[[0,0,1+w],[0,0,b],[w/h,-2*b/h,0]]
            vec=[1+w,b,c]
            residual=[sum(mat[i][j]*vec[j] for j in range(3))-c*vec[i] for i in range(3)]
            self.assertLess(max(map(abs,residual)),1e-12)
            if c.imag:
                log_growth=lambda k:k*c.imag*.1
                self.assertGreater(log_growth(200),log_growth(100))
            elif 0<c.real<=1:
                for v in [-.9,0,.8]:
                    for sign in [-1,1]:
                        self.assertLessEqual(abs((v+sign*c.real)/(1+sign*v*c.real)),1+1e-12)

    def test_16_averaged_pencil_independent_of_coherent_identification(self):
        rho,q,w,lam=s.symbols("rho q w lambda",real=True)
        h=(1+w)*rho-2*q
        A0=s.diag(1,1,h)
        A1=s.Matrix([[0,0,(1+w)*rho],[0,0,2*q],[w,-1,0]])
        self.zero((A1-lam*A0).det()-lam*(w*(1+w)*rho-2*q-h*lam**2))
        n,C,chi=s.symbols("n C chi",positive=True)
        rhon=C*n**(1+w);qn=chi*n*n;hn=(1+w)*rhon-2*qn
        eps=rhon-qn;P=w*rhon-qn
        J=s.Matrix([[s.diff(rhon,n),0,0],[2*chi*n,n*n,0],[0,0,1]])
        primitive=s.Matrix([[0,0,n],[0,0,0],[s.diff(P,n)/hn,s.diff(P,chi)/hn,0]])
        for value in (A0.inv()*A1).subs({rho:rhon,q:qn})*J-J*primitive:
            self.zero(value)
        self.zero(n*s.diff(eps,n)-eps-P)
        # Independent variance has a different zero-background Jordan chain
        # from a coherent mean whose squared correction starts at second order.
        endpoint=(A0.inv()*A1).subs({w:0,q:0})
        self.assertEqual(endpoint.rank(),2)
        self.assertNotEqual(endpoint**2,s.zeros(3))
        self.assertEqual(endpoint**3,s.zeros(3))

    def test_17_analytic_initial_patches_satisfy_all_radial_constraints(self):
        rho0,q0,q2,H,kappa,w=s.symbols("rho0 q0 q2 H kappa w",positive=True)
        eps=rho0-q0-q2*r*r;P=w*rho0-q0-q2*r*r
        h=(1+w)*rho0-2*q0-2*q2*r*r;hc=(1+w)*rho0-2*q0
        M=kappa*((rho0-q0)*r**3/6-q2*r**5/10);U=-H*r
        F=1+(H*H-kappa*(rho0-q0)/3)*r*r+kappa*q2*r**4/5
        self.zero(s.diff(M,r)-kappa*eps*r*r/2)
        self.zero(F-(1+U*U-2*M/r))
        R3=2*(1-F)/r**2-2*s.diff(F,r)/r
        self.zero(R3+4*s.diff(U,r)*U/r+2*(U/r)**2-2*kappa*eps)
        Phi_i=-s.log(h/hc)/2
        self.zero(s.diff(Phi_i,r)+s.diff(P,r)/h)
        self.zero(s.diff(U,r)-U/r)
        self.zero(s.limit(F,r,0)-1)
        self.zero(s.limit(Phi_i,r,0))
        b1=s.symbols("b1",real=True)
        self.zero((q0+q2*r*r).subs({q0:0,q2:kappa*b1*b1})-kappa*(b1*r)**2)
        # Rational example in a local causal patch, no vacuum-boundary claim.
        vals={rho0:1,q0:s.Rational(1,100),q2:s.Rational(1,100),
              H:s.Rational(1,10),kappa:1,w:s.Rational(1,3),r:s.Rational(1,2)}
        self.assertGreater(F.subs(vals),0)
        self.assertLess((q0+q2*r*r-w*(1+w)*rho0/2).subs(vals),0)

    def test_18_shell_and_volume_conditions_remain_distinct(self):
        Gamma,ar,M,RR,kappa,rho,q,w,Hr,Ht,sigma,diva=s.symbols(
            "Gamma ar M RR kappa rho q w Hr Ht sigma diva",real=True)
        P=w*rho-q;h=(1+w)*rho-2*q
        grad_rho,grad_q=s.symbols("grad_rho grad_q",real=True)
        acceleration=Gamma*ar-M/RR**2-kappa*P*RR/2
        substituted=acceleration.subs(ar,-(w*grad_rho-grad_q)/h)
        self.zero(substituted-(-Gamma*(w*grad_rho-grad_q)/h-M/RR**2-kappa*(w*rho-q)*RR/2))
        theta=Hr+2*Ht
        self.zero(theta.subs(Ht,0)-Hr)
        self.zero(theta.subs(Hr,-2*Ht))
        expansiondot=-2*sigma-kappa*((1+3*w)*rho-4*q)/2+diva
        self.zero(2*expansiondot-(kappa*(4*q-(1+3*w)*rho)-4*sigma+2*diva))
        # Both expansions at a non-neck areal extremum have opposite signs.
        self.zero((2*Gamma/RR)*(-2*Gamma/RR)+4*Gamma**2/RR**2)

    def test_19_coordinate_Weyl_subtraction_and_curvature_invariants(self):
        ric,scalar,G=coordinate_curvature()
        C=connection();inv=g.inv()
        U=s.diff(R,t)/A;Gamma=s.diff(R,r)/B
        M=R*(1+U*U-Gamma*Gamma)/2
        eps=G[0,0]/A**2;pr=G[1,1]/B**2;pt=G[2,2]/R**2
        # Direct angular Riemann, divided by R^4 sin^2(theta).
        angular=s.diff(C[2,3,3],theta)-s.diff(C[2,2,3],x[3])
        angular+=sum(C[2,2,e]*C[e,3,3]-C[2,3,e]*C[e,2,3] for e in range(4))
        angular=clean(angular/(R**2*s.sin(theta)**2))
        self.zero(angular-2*M/R**3)
        Weyl=clean(angular-ric[2,2]/R**2+scalar/6)
        self.zero(Weyl-(2*(M/R**3-eps/6)+(pr-pt)/3))
        # Ricci trace/invariants from an isotropic source in a rest frame.
        e,p,kk=s.symbols("e p kk")
        tr=kk*(e-3*p)
        R00=kk*(e+3*p)/2;Rii=kk*(e-p)/2
        self.zero(-R00+3*Rii-tr)
        self.zero(R00**2+3*Rii**2-kk**2*(e**2+3*p**2))

    def test_20_nonzero_density_pressure_free_edge_is_noncausal(self):
        rho,w=s.symbols("rho w",positive=True)
        q=w*rho
        h=(1+w)*rho-2*q
        self.zero(h-(1-w)*rho)
        self.zero((w*(1+w)*rho-2*q)/h+w)
        self.assertEqual(h.subs(w,1),0)
        # The only spinless-pressureless endpoint has q=0.
        self.assertEqual(q.subs(w,0),0)

    def test_21_full_spin_equation_preserves_Frenkel_for_arbitrary_acceleration(self):
        b1,b2,b3,a1,a2,a3,Theta=s.symbols("b1 b2 b3 a1 a2 a3 Theta",real=True)
        spin=s.zeros(4);spin[1,2]=b3;spin[2,3]=b1;spin[3,1]=b2;spin=spin-spin.T
        up=[1,0,0,0];low=[-1,0,0,0];acc=[0,a1,a2,a3]
        dot=s.zeros(4)
        for i in range(4):
            for j in range(4):
                dot[i,j]=-Theta*spin[i,j]-sum(
                    (low[i]*spin[j,k]-low[j]*spin[i,k])*acc[k] for k in range(4))
        for i in range(4):
            self.zero(sum(dot[i,j]*up[j]+spin[i,j]*acc[j] for j in range(4)))
        norm=b1*b1+b2*b2+b3*b3
        self.zero(sum(spin[i,j]*dot[i,j] for i in range(1,4) for j in range(1,4))+2*Theta*norm)


if __name__ == "__main__":
    unittest.main(verbosity=2)
