"""Periodic homogeneous Regge frusta, assembled as Lorentzian simplices."""
from functools import lru_cache
from itertools import product

import numpy as np
from scipy.optimize import least_squares, root

from mesh import Slab
from regge import GeometryError, Regge, potential


@lru_cache(maxsize=None)
def periodic_layer(n):
    """Three sites per direction distinguish each physical link on the torus."""
    from itertools import permutations
    space=[*product(range(3),repeat=n)]
    nodes=[(t,*x) for t in (0,1) for x in space]
    ids={q:i for i,q in enumerate(nodes)}
    simplices=[]
    axial=set()
    for x in space:
        for p in permutations(range(n+1)):
            u=[0,*x]
            vertices=[ids[tuple(u)]]
            for axis in p:
                u[axis]=1 if axis==0 else (u[axis]+1)%3
                vertices.append(ids[tuple(u)])
                axial.add(tuple(sorted(vertices[-2:])))
            simplices.append(vertices)
    slab=Slab(np.array(nodes),np.array(simplices),axial)
    engine=Regge(slab)
    time=slab.sites[:,0]
    ends=time[engine.edges]
    cross=ends[:,0]!=ends[:,1]
    same=np.count_nonzero(slab.sites[engine.edges[:,0],1:]!=slab.sites[engine.edges[:,1],1:],axis=1)
    return engine,time,cross,same,ends[:,0]


class Frusta:
    """One time-local Lagrangian from a periodic Regge slab per spatial cell."""
    def __init__(self,n,G=.08,model=None,matter="affine",cosmological=0.):
        if n<2:
            raise ValueError("Einstein gravity is topological at D=2")
        self.n=n
        self.G=G
        self.model=potential() if model is None else model
        self.matter=matter
        self.cosmological=cosmological
        self.engine,self.time,self.cross,self.offset,self.side=periodic_layer(n)
        hinge_times=self.time[np.asarray(self.engine.hinges)]
        self.lower=np.all(hinge_times==0,axis=1)&self.engine.exterior
        self.upper=np.all(hinge_times==1,axis=1)&self.engine.exterior

    def evaluate(self,left,right,h):
        a,u=left
        b,v=right
        n=self.n
        d=self.offset
        dt=self.cross
        if min(a,b,h)<=0 or h*h<=n*(b-a)**2/4:
            raise GeometryError("Nonpositive scale or duration")
        x=.25*((n-d)*(b-a)**2+d*(a+b)**2)
        s=np.where(dt,-h*h+x,d*np.where(self.side==0,a*a,b*b))
        p=np.where(self.time==0,u,v)
        A,ds,dp,k,vol=self.engine.evaluate(s,p,self.G,self.model,matter=self.matter,
                                          cosmological=self.cosmological)
        area=self.engine.geometry(self.engine.gram(self.engine.unpack(s,self.engine.h_slots)))[0]
        curvature=area*k/3**n
        ja=np.where(dt,.5*(-(n-d)*(b-a)+d*(a+b)),2*d*a*(self.side==0))
        jb=np.where(dt,.5*((n-d)*(b-a)+d*(a+b)),2*d*b*(self.side==1))
        result=np.array([ds@ja,dp[self.time==0].sum(),ds@jb,dp[self.time==1].sum(),
                         -2*h*ds[dt].sum()])/3**n
        core=~self.engine.exterior
        max_deficit=np.max(np.abs(k[core]),initial=0.)
        # The orthogonal separation h differs from vertex-strut proper time.
        strut=np.sqrt(h*h-n*(b-a)**2/4)
        return (A/3**n,result,max_deficit,vol.sum()/3**n,strut,
                curvature[self.lower].sum(),curvature[self.upper].sum(),curvature[core].sum())

    def start(self,left,velocity,h):
        a,phi=left
        rho=.5*velocity**2+self.model[0](phi)
        H=np.sqrt((16*np.pi*self.G*rho+2*self.cosmological)/(self.n*(self.n-1)))
        guess=np.array([a*(1+h*H),phi+h*velocity])
        momentum=a**self.n*velocity
        def objective(q):
            try:
                derivatives=self.evaluate(left,q,h)[1]
                return np.array([derivatives[-1],derivatives[1]+momentum])
            except GeometryError:
                return np.full(2,1.)
        solution=least_squares(objective,guess,diff_step=1e-5,max_nfev=42,
                               xtol=1e-12,ftol=1e-12,gtol=1e-12)
        error=np.max(abs(objective(solution.x)))
        if error>2e-9:
            raise GeometryError(f"Beginning lapse or momentum residual {error}")
        return solution.x

    def step(self,older,left,old_h):
        """Interior DEL + lapse. Solve new two endpoint coordinates and duration."""
        past=self.evaluate(older,left,old_h)[1][2:4]
        target=np.r_[(left-older)/old_h,1.]
        def unpack(z):
            return left+old_h*z[:2],old_h*z[2]
        def objective(z):
            q,h=unpack(z)
            try:
                d=self.evaluate(left,q,h)[1]
                return np.r_[d[:2]+past,d[-1]]
            except GeometryError:
                return np.full(3,1.)
        fit=least_squares(objective,target,jac="3-point",max_nfev=100,
                          xtol=2e-12,gtol=4e-14,ftol=2e-12,
                          bounds=([-np.inf,-np.inf,.45],[np.inf,np.inf,2.4]))
        err=np.max(abs(objective(fit.x)))
        q,h=unpack(fit.x)
        return q,h,err

    def step_fixed_time(self,older,left,h):
        """Solve only the endpoint DEL equations to audit lapse drift at prescribed h."""
        past=self.evaluate(older,left,h)[1][2:4]
        fit=root(lambda q:self.evaluate(left,q,h)[1][:2]+past,2*left-older,tol=2e-10)
        e=np.max(abs(self.evaluate(left,fit.x,h)[1][:2]+past))
        if e>2e-10:
            raise GeometryError(f"Fixed-time endpoint residual {e}")
        return fit.x,e
