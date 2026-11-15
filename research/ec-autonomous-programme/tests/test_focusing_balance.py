import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from spin_texture_focusing import measure
from strong_benchmark import exact,PlanarGrid

class CurrentFocusing(unittest.TestCase):
    def test_independent_homogeneous_raychaudhuri_and_contact_split(self):
        grid=PlanarGrid(5);volume=.5;t=-np.log(volume)/3;state,_=exact(grid,t,D0=0.)
        r=measure(grid,state,1e-4)['terms']
        self.assertAlmostEqual(r['material_theta_dot']['mean'],-9/volume**2,places=4)
        self.assertAlmostEqual(r['volume_focusing']['mean'],-3/volume**2,places=10)
        self.assertAlmostEqual(r['explicit_contact_source_identity']['mean'],-6/volume**2,places=10)
        self.assertLess(r['other_source_identity']['RMS'],1e-11)
        self.assertLess(r['acceleration_divergence']['RMS'],1e-11)
        self.assertLess(r['shear_focusing']['RMS'],1e-11)
        self.assertLess(r['vorticity_defocusing']['RMS'],1e-11)
        self.assertLess(r['Einstein_Ricci_source_mismatch']['RMS'],1e-10)
    def test_tangent_step_error_decreases_on_exact_trajectory(self):
        grid=PlanarGrid(5);state,_=exact(grid,.2,D0=0.)
        a=measure(grid,state,1e-3)['terms']['geometric_identity_residual']['RMS']
        b=measure(grid,state,5e-4)['terms']['geometric_identity_residual']['RMS']
        self.assertTrue(3.9<a/b<4.1,(a,b))

if __name__=='__main__':unittest.main()
