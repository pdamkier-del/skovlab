import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from strong_benchmark import ecd,PlanarGrid,exact,curvature,run_homogeneous

class StrongBenchmark(unittest.TestCase):
    def test_exact_harmonic_field_rhs_and_invariants(self):
        grid=PlanarGrid(7)
        for t in [0.,.31,.69]:
            st,truth=exact(grid,t);h=1e-5
            plus,_=exact(grid,t+h);minus,_=exact(grid,t-h)
            numerical=ecd.rhs(grid,st,mass=0.)
            for a,b,c in zip(numerical,plus,minus):
                np.testing.assert_allclose(a,(b-c)/(2*h),rtol=2e-8,atol=2e-8)
            R,K=curvature(grid,st)
            np.testing.assert_allclose(R,truth['R'],rtol=2e-13)
            np.testing.assert_allclose(K,truth['Kretschmann'],rtol=2e-13)
            d=ecd.diagnostics(grid,st,mass=0.)
            self.assertLess(np.max(abs(d['hamiltonian'])),1e-10)
            self.assertLess(np.max(abs(d['momentum'])),1e-12)
            self.assertLess(np.max(abs(d['harmonic'])),1e-11)
    def test_refinement_reduces_strong_curvature_error(self):
        a=run_homogeneous(20);b=run_homogeneous(40)
        self.assertTrue(all(x/y>10 for x,y in zip(a['state_relative_errors'],b['state_relative_errors'])))
        self.assertLess(b['Kretschmann_relative_error'],a['Kretschmann_relative_error']/10)
    def test_periodic_number_includes_wrapped_cell_and_translation(self):
        grid=ecd.Grid(9,4.,'periodic');g,p,psi=ecd.minkowski(grid)
        psi[...,2]=.1
        self.assertAlmostEqual(ecd.diagnostics(grid,(g,p,psi),mass=0.)['number'],5.12,places=12)
        psi[...,2]=np.sqrt(.01*(1+.2*np.cos(2*np.pi*grid.xyz[...,2]/8)))
        Q=ecd.diagnostics(grid,(g,p,psi),mass=0.)['number']
        for axis in range(3):
            moved=np.roll(psi,3,axis=axis)
            self.assertAlmostEqual(ecd.diagnostics(grid,(g,p,moved),mass=0.)['number'],Q,places=12)

if __name__=='__main__':unittest.main()
