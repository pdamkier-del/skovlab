"""One fixed minimal Einstein-Cartan-Holst-Dirac action, local 3+1 kernels.
No homogeneous ansatz. Geometry/spin-frame algorithm adapted read-only from PR2;
Weyl matrices, scalar interaction and complete stress are independently checked.
"""
from dataclasses import dataclass
import numpy as np
ETA=np.array([-1.,1.,1.,1.]);I=np.eye(2,dtype=complex);Z=np.zeros((2,2),complex)
SIGMA=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
GAMMA=np.array([np.block([[Z,I],[I,Z]])]+[np.block([[Z,s],[-s,Z]])for s in SIGMA])
LOW=ETA[:,None,None]*GAMMA;G5=-1j*GAMMA[0]@GAMMA[1]@GAMMA[2]@GAMMA[3]
AX=np.array([G5@g for g in GAMMA]);COMM=np.array([[LOW[a]@LOW[b]-LOW[b]@LOW[a]for b in range(4)]for a in range(4)])
@dataclass(frozen=True)
class Parameters:
 M:float=1.
 beta:float=.25
 c:float=1e4
 mass:float=.1

def couplings(phi,p=Parameters()):
 X=np.sqrt(2/3)*phi/p.M+np.arcsinh(4*p.beta/p.M**2);v=np.sinh(X)/4-p.beta/p.M**2;sech=1/np.cosh(X)
 V=p.M**4*v*v/(4*p.c);Vp=p.M**3*v*np.cosh(X)*np.sqrt(2/3)/(8*p.c)
 h=np.sqrt(3/8)/p.M*sech;g=3/(16*p.M**2)*sech**2
 gp=-2*np.sqrt(2/3)/p.M*np.tanh(X)*g
 return {'X':X,'V':V,'Vp':Vp,'h':h,'g':g,'gp':gp,'f':p.M**2*np.sinh(X)/4,'fphi':p.M*np.sqrt(2/3)*np.cosh(X)/4,'z':p.M**2*v/(2*p.c)}

def christoffel(g,dg):
 inv=np.linalg.inv(g);c=np.einsum('...bdc->...dbc',dg)+np.einsum('...cdb->...dbc',dg)-dg
 return .5*np.einsum('...ad,...dbc->...abc',inv,c)

def frame(g,dg):
 inv=np.linalg.inv(g);N=1/np.sqrt(-inv[...,0,0]);shift=N[...,None]**2*inv[...,0,1:]
 L=np.linalg.cholesky(g[...,1:,1:]);li=np.linalg.inv(L);B=np.swapaxes(li,-1,-2);shape=g.shape[:-2]
 e=np.zeros(shape+(4,4));e[...,0,0]=1/N;e[...,1:,0]=-shift/N[...,None];e[...,1:,1:]=B
 di=-np.einsum('...ab,...lbc,...cd->...lad',inv,dg,inv);dN=.5*N[...,None]**3*di[..., :,0,0]
 db=2*N[...,None,None]*dN[..., :,None]*inv[...,None,0,1:]+N[...,None,None]**2*di[..., :,0,1:]
 de=np.zeros(shape+(4,4,4));de[..., :,0,0]=-dN/N[...,None]**2
 de[..., :,1:,0]=-db/N[...,None,None]+shift[...,None,:]*dN[..., :,None]/N[...,None,None]**2
 for mu in range(4):
  Q=li@dg[...,mu,1:,1:]@B;A=np.tril(Q).copy()
  for i in range(3):A[...,i,i]*=.5
  de[...,mu,1:,1:]=-B@np.swapaxes(A,-1,-2)
 co=np.linalg.inv(e);con=christoffel(g,dg)
 W=np.einsum('...av,...mvb->...mab',co,de+np.einsum('...vml,...lb->...mvb',con,e))
 om=-.125*np.einsum('...mab,abij->...mij',W*ETA,COMM)
 gam=np.einsum('...ma,aij->...mij',e,GAMMA)
 return {'e':e,'co':co,'de':de,'omega':om,'gamma':gam,'inv':inv,'connection':con,'N':N,'shift':shift}

def source(metric,dmetric,psi,dpsi_sp,phi,dphi,p=Parameters(),interactions=True):
 f=frame(metric,dmetric);C=couplings(phi,p)
 if not interactions:
  C=dict(C);C['h']=np.zeros_like(phi);C['g']=np.zeros_like(phi);C['gp']=np.zeros_like(phi)
 e=f['e'];gam=f['gamma'];om=f['omega']
 bar=np.einsum('...a,ab->...b',psi.conj(),GAMMA[0]);A=np.einsum('...i,aij,...j->...a',bar,AX,psi).real
 jf=np.einsum('...i,aij,...j->...a',bar,GAMMA,psi).real;S=np.sum(bar*psi,axis=-1).real;P=(1j*np.einsum('...i,ij,...j->...',bar,G5,psi)).real
 Q=np.einsum('...ma,...m->...a',e,dphi)
 b=C['h'][...,None]*Q+2*C['g'][...,None]*ETA*A
 interaction=p.mass*np.eye(4)+np.einsum('...a,aij->...ij',b,AX)
 Ds=dpsi_sp+np.einsum('...iab,...b->...ia',om[...,1:,:,:],psi)
 inv_gt=f['N'][...,None,None]**2*gam[...,0,:,:]
 dt=-np.einsum('...ab,...b->...a',om[...,0,:,:],psi)-np.einsum('...ab,...b->...a',inv_gt,np.einsum('...iab,...ib->...a',gam[...,1:,:,:],Ds)+1j*np.einsum('...ab,...b->...a',interaction,psi))
 D=np.concatenate([(dt+np.einsum('...ab,...b->...a',om[...,0,:,:],psi))[...,None,:],Ds],axis=-2)
 Dbar=np.einsum('...mi,ij->...mj',D.conj(),GAMMA[0]);gl=np.einsum('...mn,...nij->...mij',metric,gam)
 raw=np.einsum('...i,...mij,...nj->...mn',bar,gl,D)-np.einsum('...ni,...mij,...j->...mn',Dbar,gl,psi)
 KD=(-.25j*(raw+np.swapaxes(raw,-1,-2))).real
 Ac=np.einsum('...ma,...a->...m',e,A);Al=np.einsum('...mn,...n->...m',metric,Ac);A2=np.sum(ETA*A*A,axis=-1)
 grad2=np.einsum('...mn,...m,...n->...',f['inv'],dphi,dphi)
 scalar=dphi[..., :,None]*dphi[...,None,:]-metric*(.5*grad2+C['V'])[...,None,None]
 mixed=C['h'][...,None,None]*(Al[..., :,None]*dphi[...,None,:]+dphi[..., :,None]*Al[...,None,:])/2
 T=scalar+KD+mixed+C['g'][...,None,None]*metric*A2[...,None,None]
 normal=e[..., :,0];rho=np.einsum('...a,...ab,...b->...',normal,T,normal);J=-np.einsum('...ia,...a->...i',T[...,1:,:],normal)
 ward=(np.einsum('...mi,...mij,...j->...',Dbar,np.einsum('ij,...mjk->...mik',G5,gam),psi)+np.einsum('...i,...mij,...mj->...',bar,np.einsum('ij,...mjk->...mik',G5,gam),D)).real
 return {'dtpsi':dt,'Dpsi':D,'T':T,'KD':KD,'rho':rho,'J':J,'Sij':T[...,1:,1:],'axial':A,'Acoord':Ac,'A2':A2,'current':np.einsum('...ma,...a->...m',e,jf),'scalar_bilinear':S,'pseudoscalar_bilinear':P,'axial_divergence':ward,'scalar_force':-C['Vp']-2*C['h']*p.mass*P-C['gp']*A2,'frame':f,'couplings':C}

def adm_rhs(gamma,K,N,shift,gradN,hessN,ricci3,lie_gamma,lie_K,rho,J,Sij,M=1.):
 inv=np.linalg.inv(gamma);tr=np.einsum('...ij,...ij->...',inv,K);norm=np.einsum('...ij,...jk,...kl,...li->...',inv,K,inv,K);S=np.einsum('...ij,...ij->...',inv,Sij)
 dgamma=lie_gamma-2*N[...,None,None]*K
 dK=lie_K-hessN+N[...,None,None]*(ricci3+tr[...,None,None]*K-2*K@inv@K-(Sij-.5*gamma*(S-rho)[...,None,None])/M**2)
 Hamilton=np.einsum('...ij,...ij->...',inv,ricci3)+tr*tr-norm-2*rho/M**2
 return dgamma,dK,Hamilton
