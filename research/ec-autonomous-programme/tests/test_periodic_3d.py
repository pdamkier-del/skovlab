import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'code'))
from periodic_3d_data import construct,ecd

class Periodic3DConstraints(unittest.TestCase):
    def test_full_constraints_source_and_continuum_oversampling(self):
        reports=[]
        for n in [9,17]:
            gr,st,r=construct(n=n);reports.append(r)
            self.assertTrue(all(v>0 for v in r['source_variation_each_axis']))
            self.assertLess(r['energy_formula_max_error'],1e-12)
            self.assertLess(r['harmonic_max'],1e-12)
            self.assertLess(r['vector_spectral_residual_max'],1e-12)
            self.assertLess(abs(r['mean_log_chi']),1e-10)
        self.assertLess(reports[1]['oversampled_continuum_Hamiltonian_max'],1e-9)
        self.assertLess(reports[1]['FD_Hamiltonian_max'],reports[0]['FD_Hamiltonian_max']/3)
        self.assertLess(reports[1]['FD_momentum_max'],reports[0]['FD_momentum_max']/3)
    def test_spin_momentum_conformal_identity_for_arbitrary_first_jets(self):
        seed=np.array([0,0,.7,0],complex);ds=np.zeros((3,4),complex);ds[:,2]=[.1,.2,.3]
        flat=ecd.matter(np.diag(ecd.ETA),np.zeros((4,4,4)),seed,ds,mass=0.)
        expected=np.array([.7*.2/2,-.7*.1/2,0.])
        np.testing.assert_allclose(flat['momentum'],expected,atol=1e-15)
        for chi in [.8,1.2]:
            dchi=np.array([.03,.05,-.02]);g=np.diag([-1.,chi**4,chi**4,chi**4]);dg=np.zeros((4,4,4));dg[1:,1:,1:]=np.einsum('i,jk->ijk',4*chi**3*dchi,np.eye(3))
            psi=chi**-3*seed;dpsi=chi**-3*ds-3*chi**-4*dchi[:,None]*seed
            src=ecd.matter(g,dg,psi,dpsi,mass=0.)
            np.testing.assert_allclose(src['momentum']*chi**6,expected,atol=1e-14)
    def test_uniform_limit_and_invalid_density(self):
        _,_,r=construct(n=5,epsilon=0.)
        self.assertAlmostEqual(r['Ktrace'],3.,places=11)
        self.assertLess(r['FD_Hamiltonian_max'],1e-11)
        with self.assertRaises(ValueError):construct(n=5,epsilon=1.1)

if __name__=='__main__':unittest.main()
