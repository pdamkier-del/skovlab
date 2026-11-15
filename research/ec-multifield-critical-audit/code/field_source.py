"""Independent Weyl-basis minimal ECD source for homogeneous plane-wave modes.
This is a source/ODE audit, not a spatial 3+1 evolution engine. No prior engine imports.
"""
import itertools
import numpy as np
I=np.eye(2,dtype=complex);Z=np.zeros((2,2),complex)
SIGMA=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
GAMMA=np.array([np.block([[Z,I],[I,Z]])]+[np.block([[Z,s],[-s,Z]]) for s in SIGMA])
ETA=np.array([-1.,1.,1.,1.]);LOW=ETA[:,None,None]*GAMMA
G5=-1j*GAMMA[0]@GAMMA[1]@GAMMA[2]@GAMMA[3]
EPS=np.zeros((4,4,4,4))
for p in itertools.permutations(range(4)):EPS[p]=(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))
DIRS=np.array([[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]],float)


def modes(directions=DIRS,chirality=1):
    fields=[]
    for d in directions:
        _,v=np.linalg.eigh(sum(d[i]*SIGMA[i] for i in range(3)))
        q=v[:,0 if chirality==1 else 1]
        fields.append(np.r_[q,[0j,0j]] if chirality==1 else np.r_[[0j,0j],q])
    return np.array(fields)


def source(a,H,psi,momenta,mass=0.,kappa=1.,contact=True):
    """Diagonal Bianchi I, nonrotating tetrad, proper time; every complex mode retained."""
    a=np.asarray(a);H=np.asarray(H);GA=3*kappa/16 if contact else 0.
    bar=psi.conj()@GAMMA[0]
    axial=np.einsum('fi,aij,fj->a',bar,np.array([G5@g for g in GAMMA]),psi).real
    currents=np.einsum('fi,aij,fj->fa',bar,GAMMA,psi).real
    B=mass*np.eye(4)+2*GA*np.einsum('a,aij->ij',axial*ETA,np.array([G5@g for g in GAMMA]))
    omega=np.array([a[i]*H[i]/2*GAMMA[0]@GAMMA[i+1] for i in range(3)])
    Ds=1j*momenta[:,:,None]*psi[:,None,:]+np.einsum('iab,fb->fia',omega,psi)
    dt=-np.einsum('ab,fb->fa',GAMMA[0],np.einsum('iab,fib->fa',GAMMA[1:]/a[:,None,None],Ds)+1j*np.einsum('ab,fb->fa',B,psi))
    D=np.concatenate([dt[:,None,:],Ds],axis=1);adj=D.conj()@GAMMA[0]
    gamlow=np.array([-GAMMA[0]]+[a[i]*GAMMA[i+1] for i in range(3)])
    Q=np.einsum('fi,mij,fnj->mn',bar,gamlow,D)-np.einsum('fni,mij,fj->mn',adj,gamlow,psi)
    A2=float(np.sum(ETA*axial*axial));metric=np.diag(np.r_[-1.,a*a])
    T=(-.25j*(Q+Q.T)+GA*metric*A2).real
    return {'dt':dt,'T':T,'E':float(T[0,0]),'P':np.diag(T)[1:]/a**2,'axial':axial,'axial2':A2,'currents':currents}


def action_density(N,a,psi,dt,momenta,mass=0.,kappa=1.):
    """Off-shell lapse/axis action density. Keep field jets fixed while varying tetrad.
    Symmetrized connection contribution vanishes for this diagonal nonrotating tetrad.
    """
    bar=psi.conj()@GAMMA[0];db=dt.conj()@GAMMA[0]
    kinetic=.5j*np.sum(np.einsum('fi,ij,fj->f',bar,GAMMA[0],dt)-np.einsum('fi,ij,fj->f',db,GAMMA[0],psi))/N
    for i in range(3):
        ds=1j*momenta[:,i,None]*psi;dsbar=ds.conj()@GAMMA[0]
        kinetic+=.5j*np.sum(np.einsum('fi,ij,fj->f',bar,GAMMA[i+1],ds)-np.einsum('fi,ij,fj->f',dsbar,GAMMA[i+1],psi))/a[i]
    A=np.einsum('fi,aij,fj->a',bar,np.array([G5@g for g in GAMMA]),psi).real
    scalar=np.sum(bar*psi).real
    return float((N*np.prod(a)*(kinetic-mass*scalar-3*kappa/16*np.sum(ETA*A*A))).real)
