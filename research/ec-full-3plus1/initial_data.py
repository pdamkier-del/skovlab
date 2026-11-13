"""Finite-cube conformal constraint solve. This is not asymptotic-flat gluing."""
import numpy as np
from scipy.optimize import newton_krylov,NoConvergence
from scipy.sparse import eye,kron,csr_matrix
from scipy.sparse.linalg import splu,LinearOperator
from ecd import ETA,minkowski,harmonic_initial_velocity,diagnostics


def seed_spinor(grid,amplitude=.025,radius=2.5,phase=0.):
    x,y,z=np.moveaxis(grid.xyz,-1,0);q=(x/radius)**2+(y/(.85*radius))**2+(z/(1.1*radius))**2
    bump=np.zeros_like(q);inside=q<1;bump[inside]=amplitude*np.exp(1-1/(1-q[inside]))
    spinor=np.stack([.12*(x+1j*y)/radius,.08j*z/radius,np.ones_like(x),.16*(z+1j*x)/radius],axis=-1)
    return bump[...,None]*spinor*np.exp(-1j*phase*(x*x+y*y+z*z))[...,None]


def construct(grid,unknown,seed,Ktrace):
    u=np.zeros((grid.n,)*3+(4,));u[grid.interior]=unknown.reshape((grid.n-2,)*3+(4,))
    # Overflow/nonpositive metric trials are invalid Newton steps, not new matter.
    if np.max(np.abs(u[...,0]))>2:raise ValueError('Conformal trial is outside supported weak-field range.')
    chi=np.exp(u[...,0]);W=u[...,1:];dW=grid.grad(W);div=np.trace(dW,axis1=-2,axis2=-1)
    LW=dW+np.swapaxes(dW,-1,-2)-2/3*np.eye(3)*div[...,None,None]
    g,_,_=minkowski(grid);g[...,1:,1:]=np.eye(3)*chi[...,None,None]**4
    K=LW/chi[...,None,None]**2+g[...,1:,1:]*Ktrace[...,None,None]/3
    p=harmonic_initial_velocity(grid,g,K)
    return g,p,seed/chi[...,None]**3


def solve_constraints(grid,seed=None,Ktrace=None,mass=.1,kappa=1.,tolerance=2e-8,maxiter=20):
    if grid.boundary!="dirichlet":raise ValueError("Constraint construction requires a finite Dirichlet cube.")
    if seed is None:seed=seed_spinor(grid)
    if Ktrace is None:
        r2=np.sum(grid.xyz**2,axis=-1);Ktrace=.002*np.exp(-r2/2)
    if seed.shape!=(grid.n,)*3+(4,) or Ktrace.shape!=(grid.n,)*3:raise ValueError('Initial field/grid shape mismatch.')
    evaluations=0
    def residual(u):
        nonlocal evaluations
        evaluations+=1
        d=diagnostics(grid,construct(grid,u,seed,Ktrace),mass,kappa)
        return np.concatenate([d['hamiltonian'][...,None],d['momentum']],axis=-1)[grid.interior].ravel()
    start=np.zeros((grid.n-2)**3*4)
    # Flat principal elliptic blocks, with exactly the grid's composed derivatives.
    N=grid.n-2;d1=np.gradient(np.eye(grid.n),grid.dx,axis=0,edge_order=2)
    d2=csr_matrix((d1@d1)[1:-1,1:-1]);identity=eye(N,format='csr')
    lap=kron(kron(d2,identity),identity)+kron(kron(identity,d2),identity)+kron(kron(identity,identity),d2)
    factor=splu(lap.tocsc())
    def precondition(v):
        r=np.asarray(v,dtype=float).reshape(-1,4).copy();r[:,0]/=-8
        return factor.solve(r).ravel()
    preconditioner=LinearOperator((len(start),len(start)),matvec=precondition,dtype=float)
    try: solution=newton_krylov(residual,start,f_tol=tolerance,maxiter=maxiter,inner_M=preconditioner)
    except NoConvergence as e:raise RuntimeError('Einstein constraint solve did not converge; initial data rejected.') from e
    error=float(np.max(np.abs(residual(solution))))
    if not np.isfinite(error) or error>tolerance:raise RuntimeError(f'Constraint residual {error} exceeds {tolerance}.')
    state=construct(grid,solution,seed,Ktrace)
    return state,{'converged':True,'max_absolute_residual':error,'evaluations':evaluations,'preconditioner':'flat principal scalar/vector Laplacian blocks','tolerance':tolerance,'boundary':'finite-cube chi=1, W=0; not an asymptotic exterior','seed_amplitude_max':float(np.max(np.abs(seed)))}
