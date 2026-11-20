"""Metric and full Cartan curvature from arbitrary local jets, no FLRW formulas."""
import itertools
import numpy as np
from ech import *
EPS=np.zeros((4,4,4,4))
for pp in itertools.permutations(range(4)):EPS[pp]=(-1)**sum(pp[i]>pp[j]for i in range(4)for j in range(i+1,4))

def metric_curvature(g,dg,ddg):
 inv=np.linalg.inv(g);di=-np.einsum('...ab,...lbc,...cd->...lad',inv,dg,inv)
 c=np.einsum('...bdc->...dbc',dg)+np.einsum('...cdb->...dbc',dg)-dg
 dc=np.einsum('...lbdc->...ldbc',ddg)+np.einsum('...lcdb->...ldbc',ddg)-ddg
 con=.5*np.einsum('...ad,...dbc->...abc',inv,c)
 dcon=.5*(np.einsum('...lad,...dbc->...labc',di,c)+np.einsum('...ad,...ldbc->...labc',inv,dc))
 R=from_connection(con,dcon);Ric=np.einsum('...abad->...bd',R);scalar=np.einsum('...ab,...ab->...',inv,Ric)
 return {'Riemann':R,'Ricci':Ric,'scalar':scalar,'Gamma':con,'dGamma':dcon,'G':Ric-.5*g*scalar[...,None,None]}

def from_connection(con,dcon):
 return np.einsum('...manb->...abmn',dcon)-np.einsum('...namb->...abmn',dcon)+np.einsum('...ame,...enb->...abmn',con,con)-np.einsum('...ane,...emb->...abmn',con,con)

def contortion(g,phi,dphi,psi,p=Parameters()):
 inv=np.linalg.inv(g);vol=np.sqrt(-np.linalg.det(g));f=frame(g,np.zeros(g.shape[:-2]+(4,4,4)));bar=np.einsum('...i,ij->...j',psi.conj(),GAMMA[0]);A=np.einsum('...i,aij,...j->...a',bar,AX,psi).real;A=np.einsum('...ma,...a->...m',f['e'],A);cp=couplings(phi,p)
 q=24/(p.M**2*(1+16*cp['f']**2/p.M**4))[...,None]*(cp['fphi'][...,None]*np.einsum('...mn,...n->...m',inv,dphi)+A/8)
 tc=-cp['f'][...,None]/p.M**2*np.einsum('...mn,...n->...m',g,q)
 T=(np.einsum('...ac,...b->...abc',g,tc)-np.einsum('...ab,...c->...abc',g,tc))/3-vol[...,None,None,None]*np.einsum('abcd,...d->...abc',EPS,q)/6
 low=(T-np.einsum('...bca->...abc',T)+np.einsum('...cab->...abc',T))/2
 return np.einsum('...ar,...rbc->...abc',inv,low)

def full_curvature(g,dg,ddg,phi,dphi,ddphi,psi,dpsi,p=Parameters(),delta=1e-4,torsion=True):
 lc=metric_curvature(g,dg,ddg)
 if torsion:
  C=contortion(g,phi,dphi,psi,p);dC=[]
  for mu in range(4):
   plus=contortion(g+delta*dg[...,mu,:,:],phi+delta*dphi[...,mu],dphi+delta*ddphi[...,mu,:],psi+delta*dpsi[...,mu,:],p)
   minus=contortion(g-delta*dg[...,mu,:,:],phi-delta*dphi[...,mu],dphi-delta*ddphi[...,mu,:],psi-delta*dpsi[...,mu,:],p)
   dC.append((plus-minus)/(2*delta))
  full=from_connection(lc['Gamma']+C,lc['dGamma']+np.stack(dC,axis=-4))
 else:full=lc['Riemann']
 inv=np.linalg.inv(g);low=np.einsum('...ar,...rbcd->...abcd',g,full);Ric=np.einsum('...abad->...bd',full);scalar=np.einsum('...ab,...ab->...',inv,Ric)
 raised=np.einsum('...ae,...bf,...cg,...dh,...efgh->...abcd',inv,inv,inv,inv,low,optimize=True);K=np.sum(low*raised,axis=(-4,-3,-2,-1))
 H=-np.einsum('abcd,...abcd->...',EPS,low)/np.sqrt(-np.linalg.det(g))
 return {'metric':lc,'full_Riemann':full,'full_scalar':scalar,'full_K':K,'Holst':H}
