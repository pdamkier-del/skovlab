import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from kinematics import *
from track import interpolate,coupled_step,run

class Kinematics(unittest.TestCase):
    def test_density_efolds_and_invalid_frames(self):
        self.assertAlmostEqual(float(efolds_from_density(8,1)),np.log(2))
        self.assertAlmostEqual(float(efolds_from_density(1,np.exp(-180))),60)
        for a,b in [(0,1),(1,-1),(1,np.nan)]:
            with self.assertRaises(ValueError):efolds_from_density(a,b)
        g=np.diag(ecd.ETA);dg=np.zeros((4,4,4));ds=np.zeros((3,4),complex)
        for psi in [np.zeros(4,complex),np.array([1,0,1,0],complex)]:
            k=kinematics(g,dg,psi,ds);self.assertFalse(k['valid']);self.assertTrue(np.isnan(k['theta']))
        self.assertAlmostEqual(normal_kinematics(g,dg)['normal_theta'],0)

    def test_anisotropic_expansion_and_proper_clock(self):
        N=1.7;a=np.array([1.2,.9,1.1]);H=np.array([-.02,.01,-.04]);g=np.diag(np.r_[-N*N,a*a]);dg=np.zeros((4,4,4));dg[0,1:,1:]=np.diag(2*N*H*a*a)
        psi=np.array([0,0,.1,0],complex);k=kinematics(g,dg,psi,np.zeros((3,4),complex))
        self.assertAlmostEqual(k['theta'],sum(H));self.assertAlmostEqual(k['normal_theta'],sum(H))
        self.assertAlmostEqual(k['shear_norm'],sum((H-H.mean())**2));self.assertAlmostEqual(k['vorticity_norm'],0)
        self.assertAlmostEqual(k['matter_efold_coordinate_rate'],N*sum(H)/3)
        self.assertAlmostEqual(k['current_divergence'],0)

    def test_tilted_spatially_varying_manufactured_conserved_current(self):
        # Pure kinematic manufactured field, not an asserted ECD solution.
        b=.4;slope=.13;n=1/np.sinh(b);alpha=ecd.GAMMA[0]@ecd.GAMMA[1]
        psi=np.sqrt(n)*(np.cosh(b/2)*np.eye(4)+np.sinh(b/2)*alpha)@np.array([0,0,1,0],complex)
        ds=np.zeros((3,4),complex);ds[0]=(-slope/(2*np.tanh(b))*np.eye(4)+slope/2*alpha)@psi
        k=kinematics(np.diag(ecd.ETA),np.zeros((4,4,4)),psi,ds,dt_psi=np.zeros(4,complex))
        self.assertAlmostEqual(k['density'],n);self.assertAlmostEqual(k['W'],np.cosh(b))
        self.assertAlmostEqual(k['theta'],slope*np.cosh(b));self.assertAlmostEqual(k['matter_efold_coordinate_rate'],slope/3)
        self.assertAlmostEqual(k['current_divergence'],0);self.assertAlmostEqual(k['velocity_gradient'][0,0],slope/np.cosh(b)**2)
        self.assertAlmostEqual(k['shear_norm'],2*k['theta']**2/3);self.assertAlmostEqual(k['vorticity_norm'],0)
        self.assertAlmostEqual(k['acceleration']@np.diag(ecd.ETA)@k['acceleration'],slope*slope*np.sinh(b)**2)

    def test_generic_metric_and_spinor_current_identities(self):
        rng=np.random.default_rng(33);L=np.tril(rng.normal(size=(3,3))*.1)+np.eye(3);sp=L@L.T;N=.9;beta=np.array([.1,-.03,.02])
        g=np.zeros((4,4));g[1:,1:]=sp;g[0,1:]=sp@beta;g[1:,0]=g[0,1:];g[0,0]=-N*N+beta@sp@beta
        dg=rng.normal(size=(4,4,4))*.02;dg=(dg+dg.swapaxes(-1,-2))/2
        psi=(rng.normal(size=4)+1j*rng.normal(size=4))*.2;ds=(rng.normal(size=(3,4))+1j*rng.normal(size=(3,4)))*.1
        k=kinematics(g,dg,psi,ds)
        self.assertTrue(k['valid']);self.assertAlmostEqual(k['u']@g@k['u'],-1)
        self.assertAlmostEqual(k['current_divergence'],0);self.assertAlmostEqual(k['u']@k['density_derivative']/k['density'],-k['theta'])
        self.assertAlmostEqual(k['u']@g@k['acceleration'],0)
        self.assertGreaterEqual(k['shear_norm'],-1e-13);self.assertGreaterEqual(k['vorticity_norm'],-1e-13)

    def test_primitive_interpolation_gradient(self):
        gr=ecd.Grid(5);x,y,z=np.moveaxis(gr.xyz,-1,0);f=2*x+3*y*z
        point=np.array([[.2,-.3,.4]]);v,d=interpolate(gr,f,point)
        np.testing.assert_allclose(v,[2*.2+3*(-.3)*.4]);np.testing.assert_allclose(d,[[2,1.2,-.9]])
        with self.assertRaises(ValueError):interpolate(gr,f,[[9,0,0]])

    def test_passive_tracker_does_not_change_field_step(self):
        gr=ecd.Grid(5);state=ecd.minkowski(gr);state[2][...,2]=.01
        p=np.zeros((1,17));p[0,:3]=[.2,.3,.1];p[:,8:]=np.eye(3).reshape(1,9)
        normal=np.zeros((1,5));normal[:,:3]=p[:,:3]
        got,_,_=coupled_step(gr,state,p,normal,.001)
        expected=ecd.rk4(gr,state,.001)
        for a,b in zip(got,expected):np.testing.assert_array_equal(a,b)

    def test_tracked_weak_field_run_reports_independent_consistency_errors(self):
        r=run(n=7,duration=.01,dt=.005);self.assertEqual(r['status'],'requested-time-completed')
        self.assertEqual(r['bounce'],'not-assessed');last=r['rows'][-1]
        for name in ['volume_integral_error','density_continuity_balance_error','tilt_volume_identity_error']:
            self.assertLess(np.max(np.abs(last[name])),1e-9)
        np.testing.assert_allclose(np.array(last['N_expansion'])-last['N_contraction_magnitude'],last['N_material_integral'],atol=1e-12)
        np.testing.assert_allclose(np.mean(last['N_directional_principal_stretches'],axis=1),last['N_geometric_rest_volume'],atol=1e-12)
        self.assertGreater(np.max(np.abs(last['continuity_integral_defect'])),1e-9)
        self.assertTrue(all(x<0 for x in last['N_normal']))

    def test_tilted_slice_volume_relation(self):
        gamma=np.array([[1.2,.1,0],[.1,.9,.05],[0,.05,1.1]]);v=np.array([.1,-.2,.03]);W=1/np.sqrt(1-v@gamma@v)
        ui=W*gamma@v;rest=gamma+np.outer(ui,ui)
        self.assertAlmostEqual(np.linalg.det(rest),W*W*np.linalg.det(gamma))

if __name__=='__main__':unittest.main()
