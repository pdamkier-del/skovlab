import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from planar_contraction import periodic_data,sample_data,lift_check,run,PlanarGrid,diagnostic

class PeriodicPlanarData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.solution,cls.parameters=periodic_data()
    def test_continuum_constraints_converge_under_independent_differences(self):
        errors=[]
        for n in [17,33,65]:
            grid=PlanarGrid(n);state=sample_data(grid,self.solution,self.parameters);d=diagnostic(grid,state)
            errors.append(np.max(abs(d['hamiltonian'])))
            self.assertLess(np.max(abs(d['momentum'])),1e-12)
            self.assertLess(np.max(abs(d['harmonic'])),1e-12)
        for a,b in zip(errors,errors[1:]):self.assertGreater(a/b,3.5)
    def test_full_tensor_lift_of_spatially_varying_fields(self):
        out=lift_check(self.solution,self.parameters)
        self.assertLess(max(out['RHS_and_RK_step_max_absolute_differences']),1e-12)
    def test_homogeneous_limit_is_the_known_constrained_branch(self):
        s,p=periodic_data(epsilon=0.)
        np.testing.assert_allclose(s.sol(np.linspace(-4,4,23))[0],0,atol=1e-13)
        self.assertAlmostEqual(p['Ktrace'],3.,places=12)
    def test_time_control_and_current_frame_in_small_nonuniform_run(self):
        r,_=run(n=17,steps=10,duration=.01,solution=self.solution,parameters=self.parameters)
        self.assertLess(r['max_dt_over_characteristic_bound'],1.)
        self.assertLess(r['max_Theta_current_over_time'],0.)
        self.assertLess(r['max_charge_drift'],1e-8)

if __name__=='__main__':unittest.main()
