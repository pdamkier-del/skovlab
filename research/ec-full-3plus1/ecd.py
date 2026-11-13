"""General neutral classical ECD operators. Signature -+++, kappa=1 by default.
No spatial symmetry or fluid EOS. Last axes carry tensor/spinor components.
"""
from dataclasses import dataclass
import numpy as np

ETA=np.array([-1.,1.,1.,1.])
I2=np.eye(2,dtype=complex); Z2=np.zeros((2,2),complex)
SIGMA=[np.array([[0,1],[1,0]]),np.array([[0,-1j],[1j,0]]),np.diag([1,-1])]
GAMMA=np.array([-np.block([[I2,Z2],[Z2,-I2]])]+[np.block([[Z2,s],[-s,Z2]]) for s in SIGMA])
LOW=ETA[:,None,None]*GAMMA
G5=-1j*GAMMA[0]@GAMMA[1]@GAMMA[2]@GAMMA[3]
COMM=np.array([[LOW[a]@LOW[b]-LOW[b]@LOW[a] for b in range(4)] for a in range(4)])


def christoffel(g,dg):
    inv=np.linalg.inv(g)
    c=np.einsum('...bdc->...dbc',dg)+np.einsum('...cdb->...dbc',dg)-dg
    return .5*np.einsum('...ad,...dbc->...abc',inv,c)


def ricci_reduced(g,dg,ddg):
    """R_ab - nabla_(a C_b), C^a=g^bc Gamma^a_bc. No damping."""
    inv=np.linalg.inv(g)
    di=-np.einsum('...ab,...lbc,...cd->...lad',inv,dg,inv)
    c=np.einsum('...bdc->...dbc',dg)+np.einsum('...cdb->...dbc',dg)-dg
    dc=np.einsum('...lbdc->...ldbc',ddg)+np.einsum('...lcdb->...ldbc',ddg)-ddg
    con=.5*np.einsum('...ad,...dbc->...abc',inv,c)
    dcon=.5*(np.einsum('...lad,...dbc->...labc',di,c)+np.einsum('...ad,...ldbc->...labc',inv,dc))
    r=(np.einsum('...aamn->...mn',dcon)-np.einsum('...nama->...mn',dcon)
       +np.einsum('...aal,...lmn->...mn',con,con)-np.einsum('...anl,...lma->...mn',con,con))
    gauge=np.einsum('...bc,...abc->...a',inv,con)
    dcup=np.einsum('...lbc,...abc->...la',di,con)+np.einsum('...bc,...labc->...la',inv,dcon)
    clow=np.einsum('...ab,...b->...a',g,gauge)
    dclow=np.einsum('...lab,...b->...la',dg,gauge)+np.einsum('...ab,...lb->...la',g,dcup)
    cov=dclow-np.einsum('...alm,...a->...lm',con,clow)
    return r-.5*(cov+np.swapaxes(cov,-1,-2)),r,gauge


def frame(g,dg):
    """Normal-adapted Cholesky triad; its derivative fixes rotation gauge."""
    inv=np.linalg.inv(g)
    if np.any(inv[...,0,0]>=0): raise ValueError('Time coordinate is not spacelike-sliced.')
    lapse=1/np.sqrt(-inv[...,0,0]); beta=lapse[...,None]**2*inv[...,0,1:]
    L=np.linalg.cholesky(g[...,1:,1:]); li=np.linalg.inv(L); B=np.swapaxes(li,-1,-2)
    shape=g.shape[:-2]; e=np.zeros(shape+(4,4)); e[...,0,0]=1/lapse
    e[...,1:,0]=-beta/lapse[...,None];e[...,1:,1:]=B
    di=-np.einsum('...ab,...lbc,...cd->...lad',inv,dg,inv)
    dn=.5*lapse[...,None]**3*di[..., :,0,0]
    db=2*lapse[...,None,None]*dn[..., :,None]*inv[...,None,0,1:]+lapse[...,None,None]**2*di[..., :,0,1:]
    de=np.zeros(shape+(4,4,4))
    de[..., :,0,0]=-dn/lapse[...,None]**2
    de[..., :,1:,0]=-db/lapse[...,None,None]+beta[...,None,:]*dn[..., :,None]/lapse[...,None,None]**2
    for mu in range(4):
        q=li@dg[...,mu,1:,1:]@B
        x=np.tril(q).copy()
        for a in range(3): x[...,a,a]*=.5
        de[...,mu,1:,1:]=-B@np.swapaxes(x,-1,-2)
    co=np.linalg.inv(e); con=christoffel(g,dg)
    w=np.einsum('...av,...mvb->...mab',co,de+np.einsum('...vml,...lb->...mvb',con,e))
    # W^a_b=e^a_nu nabla e_b^nu. Negative Clifford convention needs -W.
    omega=-.125*np.einsum('...mab,abij->...mij',w*ETA,COMM)
    curved=np.einsum('...ma,aij->...mij',e,GAMMA)
    return {'e':e,'de':de,'co':co,'omega':omega,'gamma':curved,'lapse':lapse,'beta':beta,'inv':inv,'connection':con}


def matter(g,dg,psi,spatial_derivatives,mass=.1,kappa=1.):
    """All 4 complex spinor components. spatial_derivatives[...,i,component]."""
    f=frame(g,dg); gam=f['gamma']; om=f['omega']; GA=3*kappa/16
    bar=np.einsum('...a,ab->...b',psi.conj(),GAMMA[0])
    axial=np.einsum('...i,aij,...j->...a',bar,np.array([G5@x for x in GAMMA]),psi).real
    jframe=np.einsum('...i,aij,...j->...a',bar,GAMMA,psi).real
    J2=np.sum(ETA*axial*axial,axis=-1)
    interaction=mass*np.eye(4)+2*GA*np.einsum('...a,aij->...ij',axial*ETA,np.array([G5@x for x in GAMMA]))
    Ds=spatial_derivatives+np.einsum('...iab,...b->...ia',om[...,1:,:,:],psi)
    contracted=np.einsum('...iab,...ib->...a',gam[...,1:,:,:],Ds)
    inv_gt=f['lapse'][...,None,None]**2*gam[...,0,:,:]
    dt=-np.einsum('...ab,...b->...a',om[...,0,:,:],psi)-np.einsum('...ab,...b->...a',inv_gt,contracted+1j*np.einsum('...ab,...b->...a',interaction,psi))
    D=np.concatenate([(dt+np.einsum('...ab,...b->...a',om[...,0,:,:],psi))[...,None,:],Ds],axis=-2)
    Dbar=np.einsum('...mi,ij->...mj',D.conj(),GAMMA[0])
    gamlow=np.einsum('...mn,...nab->...mab',g,gam)
    Q=np.einsum('...a,...mab,...nb->...mn',bar,gamlow,D)-np.einsum('...na,...mab,...b->...mn',Dbar,gamlow,psi)
    stress=(-.25j*(Q+np.swapaxes(Q,-1,-2))+GA*g*J2[...,None,None]).real
    normal=f['e'][..., :,0]
    E=np.einsum('...a,...ab,...b->...',normal,stress,normal)
    momentum=-np.einsum('...ia,...a->...i',stress[...,1:,:],normal)
    current=np.einsum('...ma,...a->...m',f['e'],jframe)
    return {'dt':dt,'stress':stress,'E':E,'momentum':momentum,'axial':axial,'axial2':J2,'current':current,'frame':f}


@dataclass
class Grid:
    n:int=9
    half_width:float=4.
    boundary:str="dirichlet"
    def __post_init__(self):
        if self.n<5 or self.n%2!=1 or self.half_width<=0: raise ValueError('Use odd n>=5 and positive half width.')
        if self.boundary not in ['dirichlet','periodic']:raise ValueError('Unsupported boundary.')
        self.dx=2*self.half_width/(self.n if self.boundary=='periodic' else self.n-1)
        self.xyz=np.stack(np.meshgrid(*[np.linspace(-self.half_width,self.half_width,self.n,endpoint=self.boundary!='periodic')]*3,indexing='ij'),axis=-1)
        self.interior=((slice(None),)*3 if self.boundary=='periodic' else (slice(1,-1),)*3)
    def derivative(self,a,i):
        if self.boundary=='periodic':return (np.roll(a,-1,i)-np.roll(a,1,i))/(2*self.dx)
        return np.gradient(a,self.dx,axis=i,edge_order=2)
    def grad(self,a):
        return np.stack([self.derivative(a,i) for i in range(3)],axis=3)
    def hessian(self,a):
        out=np.empty(a.shape[:3]+(3,3)+a.shape[3:])
        for i in range(3):
            for j in range(3):out[:,:,:,i,j]=self.derivative(self.derivative(a,i),j)
        return out



def derivatives(grid,g,p):
    dg=np.concatenate([p[...,None,:,:],grid.grad(g)],axis=3)
    dd=np.zeros(g.shape[:3]+(4,4,4,4))
    mixed=grid.grad(p);dd[...,0,1:,:,:]=mixed;dd[...,1:,0,:,:]=mixed
    dd[...,1:,1:,:,:]=grid.hessian(g)
    return dg,dd


def rhs(grid,state,mass=.1,kappa=1.):
    g,p,psi=state;dg,dd=derivatives(grid,g,p)
    source=matter(g,dg,psi,grid.grad(psi),mass,kappa)
    red,_,_=ricci_reduced(g,dg,dd); inv=source['frame']['inv']
    T=source['stress'];trace=np.einsum('...ab,...ab->...',inv,T)
    acc=2*(red-kappa*(T-.5*g*trace[...,None,None]))/inv[...,0,0,None,None]
    return p,acc,source['dt']


def rk4(grid,state,dt,mass=.1,kappa=1.):
    """Prescribed outer metric velocity, fixed outer spinor; no CP boundary claim."""
    interior=grid.interior
    def stage(base,k,h):
        vals=[]
        for index,(a,b) in enumerate(zip(base,k)):
            if index==0:
                # g_t=p must hold also at the prescribed outer boundary.
                v=a+h*b
            else:
                v=a.copy();v[interior]=a[interior]+h*b[interior]
            vals.append(v)
        return tuple(vals)
    a=rhs(grid,state,mass,kappa);b=rhs(grid,stage(state,a,dt/2),mass,kappa)
    c=rhs(grid,stage(state,b,dt/2),mass,kappa);d=rhs(grid,stage(state,c,dt),mass,kappa)
    return stage(state,tuple((aa+2*bb+2*cc+dd)/6 for aa,bb,cc,dd in zip(a,b,c,d)),dt)


def minkowski(grid):
    g=np.broadcast_to(np.diag(ETA), (grid.n,)*3+(4,4)).copy()
    return g,np.zeros_like(g),np.zeros((grid.n,)*3+(4,),complex)


def harmonic_initial_velocity(grid,g,K):
    """N=1, beta=0 initially. Solve all four contracted-connection equations."""
    p=np.zeros_like(g);p[...,1:,1:]=-2*K
    def gauge(v):
        dg=np.concatenate([v[...,None,:,:],grid.grad(g)],axis=3)
        return np.einsum('...bc,...abc->...a',np.linalg.inv(g),christoffel(g,dg))
    base=gauge(p);cols=[]
    for a in range(4):
        q=p.copy();q[...,0,a]+=1
        if a: q[...,a,0]+=1
        cols.append(gauge(q)-base)
    M=np.stack(cols,axis=-1);sol=np.linalg.solve(M,-base[...,None])[...,0]
    for a in range(4):p[...,0,a]=sol[...,a];p[...,a,0]=sol[...,a]
    return p


def diagnostics(grid,state,mass=.1,kappa=1.):
    g,p,psi=state;dg,_=derivatives(grid,g,p)
    src=matter(g,dg,psi,grid.grad(psi),mass,kappa);f=src['frame'];N=f['lapse'];beta=f['beta']
    spatial=g[...,1:,1:];inv=np.linalg.inv(spatial);ds=grid.grad(spatial)
    con=christoffel(spatial,ds);_,ric,_=ricci_reduced(spatial,ds,grid.hessian(spatial))
    R=np.einsum('...ij,...ij->...',inv,ric);db=grid.grad(beta)
    lie=(np.einsum('...k,...kij->...ij',beta,ds)+np.einsum('...ik,...jk->...ij',spatial,db)+np.einsum('...jk,...ik->...ij',spatial,db))
    K=-(p[...,1:,1:]-lie)/(2*N[...,None,None]);mixed=inv@K
    trace=np.trace(mixed,axis1=-2,axis2=-1);norm=np.einsum('...ij,...ji->...',mixed,mixed)
    dm=grid.grad(mixed)
    momentum=(np.einsum('...jji->...i',dm)+np.einsum('...jjl,...li->...i',con,mixed)-np.einsum('...lji,...jl->...i',con,mixed)-grid.grad(trace)-kappa*src['momentum'])
    ham=R+trace*trace-norm-2*kappa*src['E']
    gauge=np.einsum('...bc,...abc->...a',f['inv'],f['connection'])
    H=-trace/3;shear=norm-trace*trace/3
    friedmann=6*H*H-2*kappa*src['E']+R-shear
    weight=np.sqrt(-np.linalg.det(g))*src['current'][...,0]
    number=weight
    for axis in [2,1,0]: number=np.trapezoid(number,dx=grid.dx,axis=axis)
    det=np.linalg.det(spatial)
    return {'hamiltonian':ham,'momentum':momentum,'harmonic':gauge,'H':H,'shear2':shear,'R3':R,'E':src['E'],'axial2':src['axial2'],'current':src['current'],'number':float(number),'lapse':N,'det_spatial':det,'friedmann_residual':friedmann,'K':K}


def characteristic_step(grid,g,safety=.25):
    """Conservative coordinate null-speed bound; not a coupled stability theorem."""
    inv=np.linalg.inv(g);N=1/np.sqrt(-inv[...,0,0]);beta=N[...,None]**2*inv[...,0,1:]
    spatial_inv=np.linalg.inv(g[...,1:,1:])
    speeds=np.abs(beta)+N[...,None]*np.sqrt(np.diagonal(spatial_inv,axis1=-2,axis2=-1))
    return float(safety*grid.dx/np.sum(np.max(speeds,axis=(0,1,2))))
