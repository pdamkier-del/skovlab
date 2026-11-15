"""Exact massless LRS ECD in harmonic time, using the existing tensor engine.
The compressed planar grid is a translation-invariant symmetry reduction only.
"""
from pathlib import Path
import sys,json,argparse,platform
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'ec-full-3plus1'))
import ecd

class PlanarGrid(ecd.Grid):
    """Torus fields independent of x,y; all metric/spinor components retained."""
    def __post_init__(self):
        if self.n<5 or self.n%2!=1 or self.half_width<=0:raise ValueError('Odd n>=5 required.')
        self.boundary='periodic';self.dx=2*self.half_width/self.n
        self.z=np.linspace(-self.half_width,self.half_width,self.n,endpoint=False)
        self.xyz=np.zeros((1,1,self.n,3));self.xyz[0,0,:,2]=self.z
        self.interior=(slice(None),)*3
    def derivative(self,a,i):
        return np.zeros_like(a) if i<2 else (np.roll(a,-1,2)-np.roll(a,1,2))/(2*self.dx)

def diagnostic(grid,state):
    d=ecd.diagnostics(grid,state,mass=0.)
    if isinstance(grid,PlanarGrid):
        # Lift the z quadrature to the full torus; ecd's dx³ assumes n³ nodes.
        dg,_=ecd.derivatives(grid,state[0],state[1])
        src=ecd.matter(state[0],dg,state[2],grid.grad(state[2]),mass=0.)
        d['number']=float(np.sum(np.sqrt(-np.linalg.det(state[0]))*src['current'][...,0])*grid.dx*(2*grid.half_width)**2)
    return d

def exact(grid,t,n0=4.,D0=.15,kappa=1.):
    GA=3*kappa/16;H0=-np.sqrt(kappa*GA*n0*n0/3+D0*D0/9)
    rates=np.array([H0-D0/3,H0-D0/3,H0+2*D0/3])
    v=np.exp(3*H0*t);scales=np.exp(rates*t)
    shape=grid.xyz.shape[:3];g=np.zeros(shape+(4,4));p=np.zeros_like(g)
    g[...,0,0]=-v*v;p[...,0,0]=6*H0*g[...,0,0]
    for i in range(3):g[...,i+1,i+1]=scales[i]**2;p[...,i+1,i+1]=2*rates[i]*g[...,i+1,i+1]
    psi=np.zeros(shape+(4,),complex);psi[...,2]=np.sqrt(n0/v)*np.exp(-2j*GA*n0*t)
    curvature=4*(np.sum((rates*rates-3*H0*rates)**2)+sum(rates[i]**2*rates[j]**2 for i in range(3) for j in range(i)))/v**4
    return (g,p,psi),{'v':v,'n':n0/v,'H':H0/v,'H0':H0,'R':-2*kappa*GA*(n0/v)**2,'torsion2':-1.5*kappa*kappa*(n0/v)**2,'Kretschmann':curvature,'proper_time':(v-1)/(3*H0)}

def curvature(grid,state):
    """Full metric Riemann contraction from metric jets, including evolved g_tt."""
    g,p,psi=state;dg,dd=ecd.derivatives(grid,g,p);dd[...,0,0,:,:]=ecd.rhs(grid,state,mass=0.)[1]
    inv=np.linalg.inv(g);Gamma=ecd.christoffel(g,dg)
    di=-np.einsum('...ab,...lbc,...cd->...lad',inv,dg,inv)
    C=np.einsum('...bdc->...dbc',dg)+np.einsum('...cdb->...dbc',dg)-dg
    dC=np.einsum('...lbdc->...ldbc',dd)+np.einsum('...lcdb->...ldbc',dd)-dd
    dGamma=.5*(np.einsum('...lad,...dbc->...labc',di,C)+np.einsum('...ad,...ldbc->...labc',inv,dC))
    Riem=np.zeros(g.shape[:-2]+(4,4,4,4))
    for mu in range(4):
        for nu in range(4):
            Riem[...,mu,nu]=dGamma[...,mu,:,nu,:]-dGamma[...,nu,:,mu,:]+Gamma[..., :,mu,:]@Gamma[..., :,nu,:]-Gamma[..., :,nu,:]@Gamma[..., :,mu,:]
    Ric=np.einsum('...rsrn->...sn',Riem);scalar=np.einsum('...ab,...ab->...',inv,Ric)
    low=np.einsum('...ar,...rsmn->...asmn',g,Riem)
    raised=np.einsum('...ab,...cd,...ef,...gh,...bdfh->...aceg',inv,inv,inv,inv,low,optimize=True)
    K=np.einsum('...abcd,...abcd->...',low,raised)
    return scalar,K

def run_homogeneous(steps=40,n0=4.,D0=.15,target_volume=.125,full_grid=False):
    grid=ecd.Grid(5,4.,'periodic') if full_grid else PlanarGrid(5,4.)
    state,initial=exact(grid,0,n0,D0);T=np.log(target_volume)/(3*initial['H0']);dt=T/steps
    Q0=diagnostic(grid,state)['number'];max_cfl=0.;max_constraint=0.;max_gauge=0.
    for step in range(steps):
        max_cfl=max(max_cfl,dt/ecd.characteristic_step(grid,state[0]))
        state=ecd.rk4(grid,state,dt,mass=0.)
        d=diagnostic(grid,state);max_constraint=max(max_constraint,float(np.max(abs(d['hamiltonian']))/max(2*np.max(abs(d['E'])),1e-30)))
        max_gauge=max(max_gauge,float(np.max(abs(d['harmonic']))))
    reference,truth=exact(grid,T,n0,D0);d=diagnostic(grid,state);R,K=curvature(grid,state)
    errors=[float(np.linalg.norm(a-b)/np.linalg.norm(b)) for a,b in zip(state,reference)]
    return {'steps':steps,'dt':dt,'harmonic_end_time':T,'exact':truth,'state_relative_errors':errors,'max_scaled_Hamiltonian':max_constraint,'momentum_max':float(np.max(abs(d['momentum']))),'max_harmonic':max_gauge,'relative_charge_drift':d['number']/Q0-1,'R_relative_error':float(np.max(abs(R/truth['R']-1))),'Kretschmann_relative_error':float(np.max(abs(K/truth['Kretschmann']-1))),'final_lapse':float(np.min(d['lapse'])),'max_dt_over_characteristic_bound':max_cfl,'compression':target_volume,'domain':'periodic 3-torus; homogeneous fields','storage':'full 5³' if full_grid else 'translation-invariant compressed grid'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    records=[run_homogeneous(steps=s) for s in [20,40,80,160]]
    ratios=[[records[i]['state_relative_errors'][j]/records[i+1]['state_relative_errors'][j] for j in range(3)] for i in range(3)]
    report={'hypothesis':'The existing harmonic ECD engine converges on a strong-curvature massless LRS solution, without a volume bounce.','environment':{'python':platform.python_version(),'numpy':np.__version__},'parameters':{'n0':4.,'D0':.15,'kappa':1.,'mass':0.,'target_volume':.125},'records':records,'time_refinement_ratios':ratios,'full_grid_crosscheck':run_homogeneous(steps=40,full_grid=True),'classification':'Restricted homogeneous verification; no spatial stability, physical EFT or general bounce conclusion.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
