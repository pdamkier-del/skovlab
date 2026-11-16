"""Read-only reference excerpt from PR2 full-field ECD; no evolution engine port."""
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


