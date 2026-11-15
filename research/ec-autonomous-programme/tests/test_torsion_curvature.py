import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from torsion_curvature import connection,measure
from strong_benchmark import PlanarGrid,exact

class FullTorsionCurvature(unittest.TestCase):
    def test_complete_connection_matches_independent_components(self):
        grid=PlanarGrid(5)
        for t in [0.,.31]:
            state,_=exact(grid,t,D0=0.);actual=connection(grid,state)[0]
            ref=np.zeros((4,4,4));ref[0,0,0]=-3
            for i in [1,2,3]:ref[i,0,i]=-1;ref[i,i,0]=-1;ref[0,i,i]=-np.exp(4*t)
            ref[0,1,2]=np.exp(4*t);ref[0,2,1]=-np.exp(4*t)
            ref[1,0,2]=1;ref[1,2,0]=-1;ref[2,0,1]=-1;ref[2,1,0]=1
            np.testing.assert_allclose(actual,np.broadcast_to(ref,actual.shape),rtol=2e-14,atol=2e-14)
    def test_zero_full_scalar_does_not_hide_full_curvature(self):
        grid=PlanarGrid(5);volume=.125;t=-np.log(volume)/3;state,_=exact(grid,t,D0=0.)
        a=measure(grid,state,1e-3);b=measure(grid,state,5e-4)
        target=128/volume**4
        self.assertGreater(a['full_K_max'],500000)
        self.assertAlmostEqual(a['torsion2_min'],-24/volume**2,places=8)
        self.assertTrue(3.9<abs(a['full_R_max']/b['full_R_max'])<4.1)
        self.assertTrue(3.9<abs((a['full_K_max']-target)/(b['full_K_max']-target))<4.1)
    def test_symbolic_affine_contraction_is_independent_of_engine(self):
        import sympy as s
        from check_torsion_symbolic import scalar,kretsch,t
        self.assertEqual(scalar,0)
        self.assertEqual(s.simplify(kretsch-128*s.exp(12*t)),0)

if __name__=='__main__':unittest.main()
