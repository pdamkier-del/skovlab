"""Covariant diagnostics for the existing single-spinor classical ECD engine.
No changes to its action, initial-data solver or evolution equations.
"""
from pathlib import Path
import sys
import numpy as np
ENGINE=Path(__file__).resolve().parents[1]/'ec-full-3plus1'
if str(ENGINE) not in sys.path:sys.path.insert(0,str(ENGINE))
import ecd


def efolds_from_density(initial,final):
    a,b=np.asarray(initial,dtype=float),np.asarray(final,dtype=float)
    if np.any(~np.isfinite(a)) or np.any(~np.isfinite(b)) or np.any(a<=0) or np.any(b<=0):
        raise ValueError('Positive finite timelike-current densities are required.')
    return (np.log(a)-np.log(b))/3


@np.errstate(divide='ignore',invalid='ignore')
def kinematics(g,dg,psi,dpsi,mass=.1,kappa=1.,dt_psi=None,relative_floor=1e-12):
    """All derivatives are coordinate derivatives; dg[...,mu,a,b].
    dt_psi optionally describes an interpolated numerical solution, in which
    case current_divergence measures its continuity defect rather than zeroing it.
    No acceleration divergence / material bounce is inferred from first jets.
    The source focusing estimate assumes Einstein equations; it is not an
    independent measurement of metric Ricci from second derivatives.
    """
    src=ecd.matter(g,dg,psi,dpsi,mass,kappa);f=src['frame'];e=f['e'];inv=f['inv']
    jt=np.einsum('...am,...m->...a',f['co'],src['current'])
    partial=np.concatenate([(src['dt'] if dt_psi is None else dt_psi)[...,None,:],dpsi],axis=-2)
    bar=psi.conj()@ecd.GAMMA[0];dbar=partial.conj()@ecd.GAMMA[0]
    djt=(np.einsum('...mi,aij,...j->...ma',dbar,ecd.GAMMA,psi)
         +np.einsum('...i,aij,...mj->...ma',bar,ecd.GAMMA,partial)).real
    current=src['current'];dj=np.einsum('...mva,...a->...mv',f['de'],jt)+np.einsum('...va,...ma->...mv',e,djt)
    n2=-np.einsum('...a,...ab,...b->...',current,g,current)
    valid=(jt[...,0]>0)&(n2>relative_floor*jt[...,0]**2)
    n=np.sqrt(np.where(valid,n2,np.nan))
    dn=-(np.einsum('...mab,...a,...b->...m',dg,current,current)+2*np.einsum('...ab,...ma,...b->...m',g,dj,current))/(2*n[...,None])
    u=current/n[...,None];ul=np.einsum('...ab,...b->...a',g,u)
    du=dj/n[...,None,None]-current[...,None,:]*dn[..., :,None]/n[...,None,None]**2
    covdu=du+np.einsum('...vml,...l->...mv',f['connection'],u)
    theta=np.trace(covdu,axis1=-2,axis2=-1)
    projector=np.eye(4)+ul[..., :,None]*u[...,None,:]
    lower=np.einsum('...av,...bv->...ba',g,covdu)
    B=projector@np.swapaxes(lower,-1,-2)@np.swapaxes(projector,-1,-2)
    h=g+ul[..., :,None]*ul[...,None,:]
    shear=(B+np.swapaxes(B,-1,-2))/2-theta[...,None,None]*h/3
    rotation=(B-np.swapaxes(B,-1,-2))/2
    sigma2=np.einsum('...ab,...cd,...ac,...bd->...',inv,inv,shear,shear)
    omega2=np.einsum('...ab,...cd,...ac,...bd->...',inv,inv,rotation,rotation)
    acceleration=np.einsum('...m,...mv->...v',u,covdu)
    divj=np.trace(dj,axis1=-2,axis2=-1)+np.einsum('...mml,...l->...',f['connection'],current)
    velocity=current[...,1:]/current[...,0,None]
    dv=(dj[...,1:,1:]*current[...,0,None,None]-dj[...,1:,0,None]*current[...,None,1:])/current[...,0,None,None]**2
    # dv[...,derivative_i,velocity_j], transpose for separation-Jacobian ODE.
    velocity_gradient=np.swapaxes(dv,-1,-2)
    W=f['lapse']*current[...,0]/n
    norm=normal_kinematics(g,dg,f)
    spatial=norm['spatial_metric'];normal_theta=norm['normal_theta']
    rest_metric=spatial+ul[...,1:,None]*ul[...,None,1:]
    E=np.einsum('...a,...ab,...b->...',u,src['stress'],u)
    trace=np.einsum('...ab,...ab->...',inv,src['stress'])
    return {'valid':valid,'density':n,'density_derivative':dn,'u':u,'theta':theta,'shear_norm':sigma2,'vorticity_norm':omega2,
            'acceleration':acceleration,'current_divergence':divj,'W':W,'lapse':f['lapse'],'beta':f['beta'],
            'velocity':velocity,'velocity_gradient':velocity_gradient,'rest_metric':rest_metric,'spatial_metric':spatial,
            'normal_theta':normal_theta,'matter_efold_coordinate_rate':theta/(3*u[...,0]),
            'normal_efold_coordinate_rate':f['lapse']*normal_theta/3,
            'continuity_efold_coordinate_defect':divj/(3*n*u[...,0]),
            'energy_current_frame':E,'mean_stress':(trace+E)/3,
            'einstein_source_focusing_estimate_excluding_acceleration_divergence':-theta*theta/3-sigma2+omega2-kappa*(E+trace/2)}


def curvature_density_bound(mass,kappa,scalar_curvature_limit):
    if not all(np.isfinite(x) for x in [mass,kappa,scalar_curvature_limit]) or mass<0 or kappa<=0 or scalar_curvature_limit<0:
        raise ValueError('Require m>=0, kappa>0 and a nonnegative scalar-curvature bound.')
    GA=3*kappa/16
    return (mass+np.sqrt(mass*mass+8*GA*scalar_curvature_limit/kappa))/(4*GA)


def normal_kinematics(g,dg,frame=None):
    """Geometric normal congruence, defined also in matter-free vacuum."""
    f=ecd.frame(g,dg) if frame is None else frame
    inv=f['inv']
    dinv=-np.einsum('...ab,...mbc,...cd->...mad',inv,dg,inv)
    dN=.5*f['lapse'][...,None]**3*dinv[..., :,0,0]
    dbeta=2*f['lapse'][...,None,None]*dN[..., :,None]*inv[...,None,0,1:]+f['lapse'][...,None,None]**2*dinv[..., :,0,1:]
    spatial=g[...,1:,1:];si=np.linalg.inv(spatial)
    lie=(np.einsum('...k,...kij->...ij',f['beta'],dg[...,1:,1:,1:])
         +np.einsum('...ik,...jk->...ij',spatial,dbeta[...,1:,:])+np.einsum('...jk,...ik->...ij',spatial,dbeta[...,1:,:]))
    K=-(dg[...,0,1:,1:]-lie)/(2*f['lapse'][...,None,None])
    normal_theta=-np.einsum('...ij,...ij->...',si,K)
    return {'lapse':f['lapse'],'beta':f['beta'],'normal_theta':normal_theta,'spatial_metric':spatial,'normal_efold_coordinate_rate':f['lapse']*normal_theta/3}


def positive_ricci_efold_bound(mass,kappa,ricci_min):
    """Necessary net-fold bound for one classical field while R>=ricci_min>0.
    This is not a sufficient inflation/bounce condition or a lifetime prediction.
    """
    if not all(np.isfinite(v) for v in [mass,kappa,ricci_min]) or mass<=0 or kappa<=0 or ricci_min<=0:
        raise ValueError('Require m>0, kappa>0 and R_min>0 for this single-field bound.')
    GA=3*kappa/16;disc=mass*mass-8*GA*ricci_min/kappa
    if disc<0:raise ValueError('The requested positive Ricci floor exceeds the single-field trace bound.')
    high=(mass+np.sqrt(disc))/(4*GA)
    low=2*ricci_min/(kappa*(mass+np.sqrt(disc)))
    return {'density_min':low,'density_max':high,'necessary_net_efold_bound':float((np.log(high)-np.log(low))/3)}
