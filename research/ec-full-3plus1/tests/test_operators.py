import sys,unittest
from pathlib import Path
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from ecd import *
from initial_data import solve_constraints,seed_spinor

class Operators(unittest.TestCase):
    def test_clifford(self):
        for a in range(4):
            for b in range(4):np.testing.assert_allclose(GAMMA[a]@GAMMA[b]+GAMMA[b]@GAMMA[a],-2*ETA[a]*np.eye(4) if a==b else np.zeros((4,4)))

    def test_general_tetrad_metricity_and_spin_connection(self):
        rng=np.random.default_rng(4);L=np.tril(rng.normal(size=(3,3))*.1)+np.eye(3);gamma=L@L.T
        N=.87;beta=np.array([.11,-.04,.02]);g=np.empty((4,4));g[1:,1:]=gamma;g[0,1:]=gamma@beta;g[1:,0]=g[0,1:];g[0,0]=-N*N+beta@gamma@beta
        dg=rng.normal(size=(4,4,4))*.03;dg=(dg+dg.swapaxes(-1,-2))/2
        f=frame(g,dg);np.testing.assert_allclose(f['e'].T@g@f['e'],np.diag(ETA),atol=1e-14)
        for mu in range(4):
            np.testing.assert_allclose(f['de'][mu].T@g@f['e']+f['e'].T@dg[mu]@f['e']+f['e'].T@g@f['de'][mu],0,atol=1e-14)
            for nu in range(4):
                derivative=np.einsum('a,aij->ij',f['de'][mu,nu],GAMMA)
                connection=np.einsum('l,lij->ij',f['connection'][nu,mu],f['gamma'])
                comm=f['omega'][mu]@f['gamma'][nu]-f['gamma'][nu]@f['omega'][mu]
                np.testing.assert_allclose(derivative+connection+comm,0,atol=1e-14)

    def test_reduced_ricci_wave_principal_part(self):
        rng=np.random.default_rng(8);g=np.diag(ETA).copy();g[0,1]=g[1,0]=.1
        dg=rng.normal(size=(4,4,4))*.02;dg=(dg+dg.swapaxes(-1,-2))/2
        dd=np.zeros((4,4,4,4));pert=rng.normal(size=(4,4));pert=(pert+pert.T)/2
        r0=ricci_reduced(g,dg,dd)[0];dd[0,0]=pert
        np.testing.assert_allclose(ricci_reduced(g,dg,dd)[0]-r0,-.5*np.linalg.inv(g)[0,0]*pert,atol=1e-13)

    def test_exact_harmonic_gauge_wave_is_flat(self):
        x=.37;t=.14;A=.08;k=1.3;phase=k*(x-t);F=A*np.sin(phase);v=np.exp(F)
        dF=np.array([-A*k*np.cos(phase),A*k*np.cos(phase),0,0]);ddF=np.zeros((4,4));ddF[:2,:2]=-A*k*k*np.sin(phase)*np.array([[1,-1],[-1,1]])
        g=np.diag([-v,v,1,1]);dg=np.zeros((4,4,4));dd=np.zeros((4,4,4,4))
        for mu in range(4):
            dg[mu,0,0]=-v*dF[mu];dg[mu,1,1]=v*dF[mu]
            for nu in range(4):
                val=v*(ddF[mu,nu]+dF[mu]*dF[nu]);dd[mu,nu,0,0]=-val;dd[mu,nu,1,1]=val
        for a in ricci_reduced(g,dg,dd):np.testing.assert_allclose(a,0,atol=2e-15)

    def test_arbitrary_spinor_local_current_conservation(self):
        rng=np.random.default_rng(5);psi=(rng.normal(size=4)+1j*rng.normal(size=4))*.2;ds=(rng.normal(size=(3,4))+1j*rng.normal(size=(3,4)))*.1
        src=matter(np.diag(ETA),np.zeros((4,4,4)),psi,ds,mass=.31)
        partial=np.vstack([src['dt'],ds]);div=0j
        for mu in range(4):
            div+=partial[mu].conj()@GAMMA[0]@GAMMA[mu]@psi+psi.conj()@GAMMA[0]@GAMMA[mu]@partial[mu]
        self.assertLess(abs(div),1e-14)
        self.assertGreater(np.linalg.norm(src['axial']),0)
        np.testing.assert_allclose(src['stress'],src['stress'].T,atol=1e-14)

    def test_curved_lrs_matches_prior_ecd_field(self):
        grid=Grid(5);g,p,psi=minkowski(grid);rates=np.array([.02,.02,-.01]);p[...,1:,1:]=np.diag(2*rates);psi[...,2]=np.sqrt(.01)
        dg,_=derivatives(grid,g,p);src=matter(g,dg,psi,grid.grad(psi))
        P=3/16*.01**2;np.testing.assert_allclose(src['stress'][2,2,2],np.diag([.1*.01+P,P,P,P]),atol=1e-15)
        expected=-np.sum(rates)/2*.1-1j*(.1+2*3/16*.01)*.1
        self.assertAlmostEqual(src['dt'][2,2,2,2],expected)
        p[...,2,2]=.06;dg,_=derivatives(grid,g,p)
        self.assertAlmostEqual(matter(g,dg,psi,grid.grad(psi))['stress'][2,2,2,1,2],.01*(.03-.02)/4)

    def test_minkowski_and_vacuum_evolution(self):
        grid=Grid(5);state=minkowski(grid)
        self.assertAlmostEqual(characteristic_step(grid,state[0]),grid.dx/12)
        for a in rhs(grid,state):np.testing.assert_array_equal(a,0)
        for a,b in zip(state,rk4(grid,state,.01)):np.testing.assert_array_equal(a,b)
        moving=minkowski(grid);moving[1][...,0,0]=.001
        updated=rk4(grid,moving,.01)
        np.testing.assert_allclose(updated[0][0],moving[0][0]+.01*moving[1][0],atol=1e-15)
        np.testing.assert_array_equal(updated[1][0],moving[1][0])
        d=diagnostics(grid,state)
        for key in ['hamiltonian','momentum','harmonic','friedmann_residual']:np.testing.assert_array_equal(d[key],0)

    def test_inhomogeneous_constraints_and_harmonic_initialization(self):
        grid=Grid(7);state,report=solve_constraints(grid)
        self.assertTrue(report['converged']);self.assertLess(report['max_absolute_residual'],2e-8)
        d=diagnostics(grid,state);self.assertLess(np.max(np.abs(d['harmonic'])),1e-14)
        np.testing.assert_allclose(d['friedmann_residual'], d['hamiltonian'],atol=1e-14)
        self.assertGreater(np.ptp(d['E']),1e-5);self.assertGreater(np.max(d['axial2']),1e-8)
        self.assertTrue(np.all(np.max(np.abs(state[2]),axis=(0,1,2))>0))
        self.assertLess(np.min(d['H']),0)
        with self.assertRaises(RuntimeError):solve_constraints(grid,tolerance=1e-15,maxiter=1)


class MicroscopicChecks(unittest.TestCase):
    def test_geometric_contortion_coupling_sign_and_elimination(self):
        # Explicit affine C^a_{mu b}, no ambiguous spin-connection naming.
        import itertools
        p=np.array([0,0,1,0],complex);bar=p.conj()@GAMMA[0]
        C=np.zeros((4,4,4))
        for perm in itertools.permutations([0,1,2]):
            sign=(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3));C[perm]=sign/2
        affine=ETA[:,None,None]*C
        scalar=0.
        for sigma in range(4):
            for rho in range(4):
                for lam in range(4):scalar+=ETA[sigma]*(affine[rho,rho,lam]*affine[lam,sigma,sigma]-affine[rho,sigma,lam]*affine[lam,rho,sigma])
        self.assertAlmostEqual(scalar,1.5)
        omega=-.125*np.einsum('amb,a,b,abij->mij',C,ETA,ETA,COMM)
        linear=sum(.5j*bar@(GAMMA[mu]@omega[mu]+omega[mu]@GAMMA[mu])@p for mu in range(4))
        self.assertAlmostEqual(linear,.75) # q^3=-6, hence L_D=-q.J/8.
        kappa=.7;torsion012=-kappa/2
        effective=scalar*torsion012**2/(2*kappa)+linear*torsion012
        self.assertAlmostEqual(effective,-3*kappa/16)

    def test_local_nonlinear_stress_conservation_with_generic_spinor_jets(self):
        rng=np.random.default_rng(8)
        psi=(rng.normal(size=4)+1j*rng.normal(size=4))*.2
        A=(rng.normal(size=(3,4))+1j*rng.normal(size=(3,4)))*.1
        B=(rng.normal(size=(3,3,4))+1j*rng.normal(size=(3,3,4)))*.1;B=(B+B.swapaxes(0,1))/2
        g=np.diag(ETA);dg=np.zeros((4,4,4));h=1e-5;F=matter(g,dg,psi,A)['dt'];dF=[];spatial=[]
        for i in range(3):
            plus=matter(g,dg,psi+h*A[i]+.5*h*h*B[i,i],A+h*B[i])
            minus=matter(g,dg,psi-h*A[i]+.5*h*h*B[i,i],A-h*B[i])
            dF.append((plus['dt']-minus['dt'])/(2*h));spatial.append((plus['stress']-minus['stress'])/(2*h))
        dF=np.array(dF)
        dtT=(matter(g,dg,psi+h*F,A+h*dF)['stress']-matter(g,dg,psi-h*F,A-h*dF)['stress'])/(2*h)
        divergence=ETA*(-dtT[0,:]+sum(spatial[i][i+1,:] for i in range(3)))
        self.assertLess(np.max(np.abs(divergence)),1e-9)

    def test_boosted_nonlinear_plane_wave_and_full_stress(self):
        n=.013;m=.17;GA=3/16;r=.4;alpha=GAMMA[0]@GAMMA[1]
        psi=(np.cosh(r/2)*np.eye(4)+np.sinh(r/2)*alpha)@np.array([0,0,np.sqrt(n),0])
        M=m+2*GA*n;energy=M*np.cosh(r);momentum=M*np.sinh(r)
        ds=np.zeros((3,4),complex);ds[0]=1j*momentum*psi
        src=matter(np.diag(ETA),np.zeros((4,4,4)),psi,ds,mass=m)
        np.testing.assert_allclose(src['dt'],-1j*energy*psi,atol=1e-15)
        eps=m*n+GA*n*n;P=GA*n*n
        u=np.array([np.cosh(r),np.sinh(r),0,0]);ul=ETA*u
        expected=(eps+P)*np.outer(ul,ul)+P*np.diag(ETA)
        np.testing.assert_allclose(src['stress'],expected,atol=1e-15)

if __name__=='__main__':unittest.main()
