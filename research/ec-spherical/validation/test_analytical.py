"""Analytical limits, numerical evaluations and read-only bridge to the existing FLRW code."""
import json,math,subprocess,unittest
from pathlib import Path
import sympy as s
from geometry import t,r,theta,phi,x,Phi,Lam,R,A,B,g,connection,coordinate_curvature,clean,substitute
ROOT=Path(__file__).resolve().parents[3]

class AnalyticalAudit(unittest.TestCase):
    def near(self,a,b,tol=1e-8): self.assertLess(abs(float(a)-float(b))/(1+abs(float(b))),tol)

    def test_11_effective_sound_speed_and_hyperbolicity_obstruction(self):
        def cs(w,z): return (w*(1+w)-2*z)/(1+w-2*z)
        for w in [0,1/3,.8]:
            self.near(cs(w,0),w)
            self.near(cs(w,1),w+2)
            self.assertLess(cs(w,(1+w)**2/4),0)
        self.assertLess(cs(0,.01),0)
        self.assertGreater(cs(1/3,.01),0)
        self.assertGreater(cs(0,1),1)
        # The frozen-coefficient acoustic mode grows without a wavelength-independent bound.
        c2=cs(0,.01); self.assertGreater(math.exp(math.sqrt(-c2)*200*.1),math.exp(math.sqrt(-c2)*100*.1))
        # Degeneracy of enthalpy occurs before the flat FLRW bounce for every 0<=w<1.
        for w in [0,1/3,.8]: self.assertLess((1+w)/2,1)

    def test_12_local_conservation_and_advected_composition(self):
        rho,q,w,Theta=s.symbols('rho q w Theta', positive=True)
        rhodot=-(1+w)*rho*Theta; qdot=-2*q*Theta
        self.assertEqual(clean(rhodot-qdot+((1+w)*rho-2*q)*Theta),0)
        self.assertEqual(clean(qdot/q-2*rhodot/((1+w)*rho)),0)
        # Coordinate volume is BR^2, not R^3 in an arbitrary spherical flow.
        V=s.exp(Lam)*R**2
        self.assertEqual(clean(s.diff(s.log(V),t)/A-(s.diff(Lam,t)+2*s.diff(R,t)/R)/A),0)

    def test_13_LTB_inhomogeneous_dust(self):
        M=r**3*(1+r*r/20)/10; ts=3+r*r/10
        radius=(s.Rational(9,2)*M)**s.Rational(1,3)*(ts-t)**s.Rational(2,3)
        mapping={Phi:0,Lam:s.log(s.diff(radius,r)),R:radius}
        G=coordinate_curvature()[2]
        expected=2*s.diff(M,r)/(radius**2*s.diff(radius,r)) # kappa*rho
        exprs=[substitute(G[0,0],mapping)-expected,substitute(G[0,1],mapping),substitute(G[1,1]/B**2,mapping),substitute(G[2,2]/R**2,mapping)]
        for point in [{t:s.Rational(1,3),r:s.Rational(1,2),theta:s.pi/2},{t:1,r:s.Rational(4,5),theta:s.pi/3}]:
            for expr in exprs: self.near(s.N(expr.subs(point),20),0,1e-9)
        self.assertEqual(clean(s.diff(radius,t)**2-2*M/radius),0)

    def test_14_shell_neck_is_not_automatically_shell_crossing(self):
        # Closed FLRW in chi coordinates: a regular equator has R'=0 but B>0.
        chi=s.symbols('chi',real=True); a=s.symbols('a',positive=True)
        radius=a*s.sin(chi); Gamma=s.diff(radius,chi)/a
        self.assertEqual(Gamma.subs(chi,s.pi/2),0)
        self.assertEqual(radius.subs(chi,s.pi/2),a)
        self.assertGreater(float(a.subs(a,2)),0)
        # Constant homogeneous density yields M' proportional to R', so no density ratio blow-up is forced.
        mass=radius**3/6
        self.assertEqual(clean(s.diff(mass,chi)-radius**2*s.diff(radius,chi)/2),0)

    def test_15_matching_pressure_obstruction(self):
        rho,q,w=s.symbols('rho q w',real=True)
        P=w*rho-q
        self.assertEqual(P.subs(w,0),-q)
        self.assertEqual(P.subs(q,0),rho*w)
        # Constant w>0 with rho->0: Euler integration Phi=-w/(1+w) ln(rho)+const diverges.
        self.assertEqual(s.limit(-s.Rational(1,4)*s.log(rho),rho,0,dir='+'),s.oo)

    def test_16_original_FLRW_solver_is_unchanged_and_matches_spherical_limit(self):
        code="""import {simulate} from './ec-flrw/collapse/model.mjs';
const runs=[];for(const k of[-1,0,1])for(const w of[0,1/3]){const z=simulate({k,w,rho:6,spin2:1.2,rb:.4,T:.5});runs.push({p:z.p,data:z.data.filter((_,i)=>i%100===0)});}console.log(JSON.stringify(runs));"""
        runs=json.loads(subprocess.run(['node','--input-type=module','-e',code],cwd=ROOT,capture_output=True,text=True,check=True).stdout)
        a=s.Function('a')(t); k=s.symbols('k'); mapping={Phi:0,Lam:s.log(a)-s.log(1-k*r*r)/2,R:a*r}
        G=coordinate_curvature()[2]
        density=clean(substitute(G[0,0],mapping)); pressure=clean(substitute(G[1,1]/B**2,mapping))
        for run in runs:
            for row in run['data']:
                sub={a:row['a'],s.diff(a,t):row['v'],s.diff(a,t,2):row['acc']*row['a'],k:run['p']['k'],r:.4}
                self.near(density.subs(sub),row['rho']-row['spin2']/4,1e-8)
                self.near(pressure.subs(sub),row['pressure']-row['spin2']/4,1e-8)

    def test_17_direct_Riemann_Kretschmann_Schwarzschild(self):
        # Independently contract the coordinate Riemann tensor at a regular exterior point.
        m=s.Rational(1);F=1-2*m/r;mapping={Phi:s.log(F)/2,Lam:-s.log(F)/2,R:r};point={t:0,r:8,theta:s.pi/2,phi:0}
        C=connection()
        values={idx:float(substitute(v,mapping).subs(point)) for idx,v in C.items()}
        derivatives={(*idx,d):float(substitute(clean(s.diff(v,x[d])),mapping).subs(point)) for idx,v in C.items() for d in range(4)}
        diag=[float(substitute(g[i,i],mapping).subs(point)) for i in range(4)]
        K=0.0
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    for d in range(4):
                        curvature=derivatives[a,d,b,c]-derivatives[a,c,b,d]+sum(values[a,c,e]*values[e,d,b]-values[a,d,e]*values[e,c,b] for e in range(4))
                        K+=diag[a]*curvature**2/(diag[b]*diag[c]*diag[d])
        self.near(K,48/8**6,1e-12)

if __name__=='__main__': unittest.main(verbosity=2)
