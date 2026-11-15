"""Independent action, Clifford, field and exact-spacetime checks."""
import argparse,json,itertools
from pathlib import Path
import numpy as np
import sympy as s
from field_source import *


def verify():
    rng=np.random.default_rng(2115);torsion=[]
    for _ in range(8):
        q=rng.normal(size=4);psi=rng.normal(size=(6,4))+1j*rng.normal(size=(6,4));bar=psi.conj()@GAMMA[0]
        A=np.einsum('fi,aij,fj->a',bar,np.array([G5@g for g in GAMMA]),psi).real
        T=-np.einsum('abcd,d->abc',EPS,q)/6;C=T/2;Gamma=ETA[:,None,None]*C
        scalar=0.
        for r in range(4):
            for z in range(4):
                for l in range(4):scalar+=ETA[z]*(Gamma[r,r,l]*Gamma[l,z,z]-Gamma[r,z,l]*Gamma[l,r,z])
        omega=np.zeros((4,4,4),complex)
        for mu in range(4):
            for a in range(4):
                for b in range(4):omega[mu]-=Gamma[a,mu,b]*ETA[b]*(LOW[a]@LOW[b]-LOW[b]@LOW[a])/8
        linear=sum((.5j*np.einsum('fi,ij,fj->',bar,GAMMA[mu]@omega[mu]+omega[mu]@GAMMA[mu],psi)).real for mu in range(4))
        curvature_error=abs(scalar-np.sum(ETA*q*q)/24);coupling_error=abs(linear+np.sum(ETA*q*A)/8)
        assert curvature_error<1e-12 and coupling_error<1e-12
        torsion.append([curvature_error,coupling_error])
    field=[]
    for a,H,n0,p in [(1.3,-.12,.021,1.2),(.7,.04,.08,.9)]:
        n=n0/a**3;psi=np.sqrt(n/6)*modes();mom=p*DIRS;out=source(np.repeat(a,3),np.repeat(H,3),psi,mom)
        frequency=p/a-2*(3/16)*n;expected_dt=(-1.5*H-1j*frequency)*psi
        E=p*n/a-3/16*n*n;P=p*n/(3*a)-3/16*n*n
        assert np.max(abs(out['dt']-expected_dt))<1e-12
        assert np.max(abs(out['T']-np.diag([E,a*a*P,a*a*P,a*a*P])))<1e-12
        h=1e-5;axes=np.repeat(a,3);volume=a**3
        Ev=-(action_density(1+h,axes,psi,out['dt'],mom)-action_density(1-h,axes,psi,out['dt'],mom))/(2*h*volume)
        Pv=[]
        for i in range(3):
            ap=axes.copy();am=axes.copy();ap[i]+=h;am[i]-=h
            Pv.append(a*(action_density(1,ap,psi,out['dt'],mom)-action_density(1,am,psi,out['dt'],mom))/(2*h*volume))
        assert abs(Ev-E)<1e-10 and max(abs(np.array(Pv)-P))<1e-10
        field.append({'a':a,'n':n,'frequency':frequency,'E':E,'P':P,'Dirac_max_error':float(np.max(abs(out['dt']-expected_dt))),'lapse_variation_error':abs(Ev-E),'axis_variation_error':float(max(abs(np.array(Pv)-P))),'total_axial':out['axial'].tolist(),'single_axial_square_sum':float(sum(np.sum(ETA*A*A) for A in [np.einsum('i,aij,j->a',v.conj()@GAMMA[0],np.array([G5@g for g in GAMMA]),v).real for v in psi]))})
    eta=s.symbols('eta',real=True);b,q,k=s.symbols('b q k',positive=True);a=s.sqrt(b*b+q*q*eta*eta)
    Cr=3*q*q/k;Cs=Cr*b*b;H=s.diff(a,eta)/a**2;E=Cr/a**4-Cs/a**6;P=Cr/(3*a**4)-Cs/a**6
    Hamiltonian=s.simplify(3*H*H-k*E);spatial=s.simplify(s.diff(H,eta)/a+k*(E+P)/2)
    conservation=s.simplify(s.diff(E,eta)/a+3*H*(E+P))
    clock=(eta*a+b*b/q*s.asinh(q*eta/b))/2;null_clock=b*b*eta+q*q*eta**3/3
    assert Hamiltonian==spatial==conservation==0
    assert s.simplify(s.diff(clock,eta)-a)==0 and s.simplify(s.diff(null_clock,eta)-a*a)==0
    # Tetrahedral test: four fields can supply isotropic stress; six is not minimal.
    tetra=np.array([[1,1,1],[1,-1,-1],[-1,1,-1],[-1,-1,1]])/np.sqrt(3)
    four=source(np.ones(3),np.zeros(3),np.sqrt(.2/4)*modes(tetra),tetra)
    assert np.max(abs(four['P']-four['P'].mean()))<1e-13
    assert np.max(abs(four['T'][0,1:]))<1e-13
    return {'basis':'Explicit chiral/Weyl matrices; prior numerical engine and old symbolic tests not imported.','random_auxiliary_curvature_and_linear_coupling_errors':torsion,'independent_field_and_action_variation_checks':field,'exact_residuals':{'Hamiltonian':str(Hamiltonian),'spatial_Einstein':str(spatial),'stress_conservation':str(conservation)},'causal_clock_derivatives':'dt/deta=a>0; d(lambda_null)/deta=a²; both clocks extend to both infinities. Timelike clocks have a positive lower bound relative to t for each fixed comoving momentum.','tetrahedral_four_field_source':{'E':four['E'],'P':four['P'].tolist(),'axial2':four['axial2']},'classification':'Benchmark passes these independent checks; no quantum or perturbative validity conclusion.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();out=verify();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
