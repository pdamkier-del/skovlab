import sys,tempfile,unittest,json
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from spin_texture_data import construct,ecd
from checkpoints import save_checkpoint,load_checkpoint

class SpinTexture(unittest.TestCase):
    def test_texture_constraints_and_all_initial_stress_projections(self):
        reports=[]
        for n in [9,17]:
            _,_,r=construct(n=n);reports.append(r)
            self.assertLess(r['axial_formula_max_error'],1e-12)
            self.assertLess(r['energy_formula_max_error'],1e-12)
            self.assertLess(r['spatial_stress_formula_max_error'],1e-12)
            self.assertLess(r['harmonic_max'],1e-12)
        self.assertLess(reports[1]['FD_Hamiltonian_max'],reports[0]['FD_Hamiltonian_max']/3)
        self.assertLess(reports[1]['FD_momentum_max'],reports[0]['FD_momentum_max']/3)
    def test_fixed_polarization_limit_recovers_prior_data(self):
        from periodic_3d_data import construct as old
        _,a,_=old(n=9);_,b,_=construct(n=9,spin_amplitude=0.)
        for x,y in zip(a,b):np.testing.assert_allclose(x,y,atol=2e-11,rtol=2e-11)
    def test_arbitrary_conformal_jets_obey_momentum_scaling(self):
        rng=np.random.default_rng(7)
        for _ in range(5):
            n=2+rng.random();theta=rng.normal();dn=rng.normal(size=3)*.1;dt=rng.normal(size=3)*.1;chi=.8+.4*rng.random();dc=rng.normal(size=3)*.03
            v=np.array([0,0,np.cos(theta/2),np.sin(theta/2)],complex);dv=np.array([0,0,-np.sin(theta/2),np.cos(theta/2)],complex)/2
            seed=np.sqrt(n)*v;ds=dn[:,None]*v/(2*np.sqrt(n))+np.sqrt(n)*dt[:,None]*dv
            dS=np.array([dn*np.sin(theta)+n*np.cos(theta)*dt,np.zeros(3),dn*np.cos(theta)-n*np.sin(theta)*dt])
            expected=np.array([dS[2,1]-dS[1,2],dS[0,2]-dS[2,0],dS[1,0]-dS[0,1]])/4
            g=np.diag([-1.,chi**4,chi**4,chi**4]);dg=np.zeros((4,4,4));dg[1:,1:,1:]=np.einsum('i,jk->ijk',4*chi**3*dc,np.eye(3))
            src=ecd.matter(g,dg,chi**-3*seed,chi**-3*ds-3*chi**-4*dc[:,None]*seed,mass=0.)
            np.testing.assert_allclose(src['momentum']*chi**6,expected,atol=2e-14)
            self.assertAlmostEqual(src['E'],3/16*n*n*chi**-12,places=12)
    def test_lossless_restart_and_rejected_state_policy(self):
        gr=ecd.Grid(5,4.,'periodic');state=ecd.minkowski(gr);state[2][...,2]=.1
        config={'mass':0.,'kappa':1.,'dt':.001}
        a=ecd.rk4(gr,state,.001,mass=0.)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'checkpoint.npz';meta=save_checkpoint(p,gr,a,time=.001,step=1,config=config)
            grid,b,m=load_checkpoint(p);self.assertEqual(meta,m)
            for x,y in zip(a,b):np.testing.assert_array_equal(x,y)
            for x,y in zip(ecd.rk4(gr,a,.001,mass=0.),ecd.rk4(grid,b,.001,mass=0.)):np.testing.assert_array_equal(x,y)
            rejected=Path(folder)/'rejected.npz';save_checkpoint(rejected,gr,a,time=.001,step=1,config=config,status='rejected',reason='test')
            with self.assertRaises(ValueError):load_checkpoint(rejected)
            load_checkpoint(rejected,allow_rejected=True)
    def test_checkpoint_corruption_is_detected(self):
        gr=ecd.Grid(5,4.,'periodic');state=ecd.minkowski(gr)
        with tempfile.TemporaryDirectory() as folder:
            p=Path(folder)/'checkpoint.npz';save_checkpoint(p,gr,state,time=0,step=0,config={})
            with np.load(p,allow_pickle=False) as f:arrays={k:f[k] for k in f.files}
            arrays['psi']=arrays['psi'].copy();arrays['psi'][0,0,0,0]=1
            np.savez_compressed(p,**arrays)
            with self.assertRaises(ValueError):load_checkpoint(p)

if __name__=='__main__':unittest.main()
