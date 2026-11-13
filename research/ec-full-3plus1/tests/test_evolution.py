import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ecd import *
from initial_data import *
from benchmarks import run_wave,gauge_wave
from evolve import evolve

class Evolution(unittest.TestCase):
    def test_vacuum_spatial_convergence(self):
        ns=[7,11,15];err=[run_wave(n,steps=4)[0] for n in ns]
        orders=[np.log(err[i]/err[i+1])/np.log(ns[i+1]/ns[i]) for i in range(2)]
        self.assertTrue(all(1.7<o<2.3 for o in orders),(err,orders))

    def test_rk4_time_self_convergence(self):
        gr=Grid(5,2.,'periodic');states=[]
        for steps in [2,4,8]:
            st=gauge_wave(gr,amplitude=.2)
            st[2][:]=.01*np.array([.1+.1j,.05j,1.,.2])*np.exp(1j*np.pi*gr.xyz[...,0]/gr.half_width)[...,None]
            for _ in range(steps):st=rk4(gr,st,.4/steps)
            states.append(st)
        errs=[sum(np.linalg.norm(a-b) for a,b in zip(states[i],states[i+1])) for i in range(2)]
        self.assertTrue(13<errs[0]/errs[1]<19,errs)
        spin_errors=[np.linalg.norm(states[i][2]-states[i+1][2]) for i in range(2)]
        self.assertTrue(12<spin_errors[0]/spin_errors[1]<20,spin_errors)

    def test_general_matter_sources_all_metric_equations(self):
        gr=Grid(5);g,p,psi=minkowski(gr);rng=np.random.default_rng(41)
        psi[:]=(rng.normal(size=psi.shape)+1j*rng.normal(size=psi.shape))*.001
        acc=rhs(gr,(g,p,psi))[1]
        self.assertGreater(np.max(np.abs(acc[...,0,1:])),1e-8)
        self.assertGreater(np.max(np.abs(acc[...,1,2])),1e-8)
        np.testing.assert_allclose(acc,acc.swapaxes(-1,-2),atol=1e-15)

    def test_short_inhomogeneous_coupled_run_and_stops(self):
        result,state=evolve(n=7,duration=.01,dt=.005)
        self.assertEqual(result['status'],'requested-time-completed')
        self.assertEqual(result['bounce'],'not-assessed')
        self.assertLess(result['rows'][-1]['constraint_scaled'],.05)
        self.assertLess(abs(result['rows'][-1]['relative_number_change']),1e-7)
        self.assertGreater(np.ptp(state[0][...,0,0]),1e-8)
        self.assertGreater(np.ptp(state[2][...,2].real),1e-3)
        for values in [{'n':8},{'amplitude':-1},{'duration':1},{'radius':5},{'dt':0}]:
            with self.assertRaises(ValueError):evolve(**values)

    def test_small_unconstrained_noise_is_not_an_exponential_grid_instability(self):
        gr=Grid(5,2.,'periodic');g,p,psi=minkowski(gr);rng=np.random.default_rng(15)
        noise=rng.normal(size=g.shape)*1e-9;g+=(noise+noise.swapaxes(-1,-2))/2
        p[:]=rng.normal(size=p.shape)*1e-9;p[:]=(p+p.swapaxes(-1,-2))/2
        psi[:]=(rng.normal(size=psi.shape)+1j*rng.normal(size=psi.shape))*1e-9
        baseline=np.linalg.norm(g-np.diag(ETA))+np.linalg.norm(p)+np.linalg.norm(psi)
        state=g,p,psi
        for _ in range(12):state=rk4(gr,state,.005)
        final=np.linalg.norm(state[0]-np.diag(ETA))+np.linalg.norm(state[1])+np.linalg.norm(state[2])
        self.assertLess(final/baseline,4)

if __name__=='__main__':unittest.main()
