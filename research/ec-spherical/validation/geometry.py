"""Independent coordinate calculation, not a numerical evolution solver.
Coordinates (t,r,theta,phi); Riemann uses derivative-index-first connection.
No hand-derived spherical Einstein components are used to construct the CAS tensor.
"""
from functools import lru_cache
import sympy as s

t,r,theta,phi=s.symbols('t r theta phi', real=True)
x=(t,r,theta,phi)
Phi=s.Function('Phi')(t,r); Lam=s.Function('Lambda')(t,r); R=s.Function('R')(t,r)
A=s.exp(Phi); B=s.exp(Lam)
g=s.diag(-A**2,B**2,R**2,R**2*s.sin(theta)**2)

def clean(v):
    return s.simplify(s.trigsimp(v))

@lru_cache(None)
def connection():
    inv=g.inv()
    return {(a,b,c):clean(sum(inv[a,d]*(s.diff(g[d,c],x[b])+s.diff(g[d,b],x[c])-s.diff(g[b,c],x[d])) for d in range(4))/2) for a in range(4) for b in range(4) for c in range(4)}

@lru_cache(None)
def coordinate_curvature():
    C=connection(); ric=s.zeros(4)
    for a in range(4):
        for b in range(a,4):
            value=sum(s.diff(C[c,a,b],x[c])-s.diff(C[c,a,c],x[b])+sum(C[c,a,b]*C[d,c,d]-C[d,a,c]*C[c,b,d] for d in range(4)) for c in range(4))
            ric[a,b]=ric[b,a]=clean(value)
    scalar=clean(sum(g.inv()[a,b]*ric[a,b] for a in range(4) for b in range(4)))
    ein=s.simplify(ric-g*scalar/2)
    return ric,scalar,ein

def hand_components():
    """The separately documented derivation, entered only for comparison."""
    dt=lambda y:s.diff(y,t); dr=lambda y:s.diff(y,r)
    E00=(2*dt(R)*dt(Lam)/R+dt(R)**2/R**2)/A**2-(2*dr(dr(R))/R+dr(R)**2/R**2-2*dr(Lam)*dr(R)/R)/B**2+1/R**2
    E11=-(2*dt(dt(R))/R+dt(R)**2/R**2-2*dt(Phi)*dt(R)/R)/A**2+(dr(R)**2/R**2+2*dr(Phi)*dr(R)/R)/B**2-1/R**2
    E01=-2*(dt(dr(R))-dr(Phi)*dt(R)-dt(Lam)*dr(R))/R
    E22=-(dt(dt(Lam))+dt(Lam)**2-dt(Phi)*dt(Lam)+(dt(dt(R))+(dt(Lam)-dt(Phi))*dt(R))/R)/A**2+(dr(dr(Phi))+dr(Phi)**2-dr(Phi)*dr(Lam)+(dr(dr(R))+(dr(Phi)-dr(Lam))*dr(R))/R)/B**2
    return E00,E11,E01,E22

def substitute(expr,mapping):
    # Substitute functions first; evaluate their derivatives afterward.
    return expr.subs(mapping, simultaneous=True).doit()

def covariant_divergence(Tup):
    C=connection()
    return [clean(sum(s.diff(Tup[a,b],x[a])+sum(C[a,a,c]*Tup[c,b]+C[b,a,c]*Tup[a,c] for c in range(4)) for a in range(4))) for b in range(4)]

def full_spin_derivative(spin):
    """BHL Eq.(24), transformed under Appendix B to (-+++), retaining BHL spin units.
    D_ab = -2 (g^{cd}-u^c u^d) nabla_c[u_(a spin_b)d].
    """
    C=connection(); up=s.Matrix([1/A,0,0,0]); low=g*up; inv=g.inv()
    tensor=lambda a,b,d:(low[a]*spin[b,d]+low[b]*spin[a,d])/2
    out=s.zeros(4)
    for a in range(4):
        for b in range(a,4):
            v=0
            for c in range(4):
                for d in range(4):
                    coeff=inv[c,d]-up[c]*up[d]
                    if coeff==0: continue
                    derivative=s.diff(tensor(a,b,d),x[c])-sum(C[e,c,a]*tensor(e,b,d)+C[e,c,b]*tensor(a,e,d)+C[e,c,d]*tensor(a,b,e) for e in range(4))
                    v+=coeff*derivative
            out[a,b]=out[b,a]=clean(-2*v)
    return out

def spatial_spin_transport(spin):
    C=connection(); up=s.Matrix([1/A,0,0,0]); theta_u=s.diff(Lam,t)/A+2*s.diff(R,t)/(A*R)
    return {(a,b):clean(sum(up[c]*(s.diff(spin[a,b],x[c])-sum(C[e,c,a]*spin[e,b]+C[e,c,b]*spin[a,e] for e in range(4))) for c in range(4))+theta_u*spin[a,b]) for a in range(1,4) for b in range(a+1,4)}
