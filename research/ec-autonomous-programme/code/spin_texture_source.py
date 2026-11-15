"""Independent symbolic source identities for a real lower-component spin texture.
No numerical ECD engine imports. Gaussian/Fermi tetrad at a point, arbitrary Kij.
"""
import argparse,json
from pathlib import Path
import sympy as s
from sympy.physics.matrices import mgamma


def verify():
    n,G=s.symbols('n G',positive=True,real=True);theta=s.symbols('theta',real=True)
    dn=s.symbols('nx ny nz',real=True);dtheta=s.symbols('tx ty tz',real=True)
    xx,yy,zz,xy,xz,yz=s.symbols('Kxx Kyy Kzz Kxy Kxz Kyz',real=True)
    K=s.Matrix([[xx,xy,xz],[xy,yy,yz],[xz,yz,zz]])
    eta=[-1,1,1,1];gam=[eta[i]*mgamma(i) for i in range(4)];g5=-s.I*gam[0]*gam[1]*gam[2]*gam[3]
    v=s.Matrix([0,0,s.cos(theta/2),s.sin(theta/2)]);psi=s.sqrt(n)*v;bar=s.conjugate(psi).T*gam[0]
    A=s.Matrix([0,n*s.sin(theta),0,n*s.cos(theta)])
    actualA=s.Matrix([(bar*g5*q*psi)[0] for q in gam])
    spatial=[]
    for i in range(3):
        partial=dn[i]/(2*s.sqrt(n))*v+s.sqrt(n)*s.diff(v,theta)*dtheta[i]
        omega=-sum((K[i,j]*gam[0]*gam[j+1]/2 for j in range(3)),s.zeros(4))
        spatial.append(partial+omega*psi)
    B=2*G*sum((eta[i]*A[i]*g5*gam[i] for i in range(4)),s.zeros(4))
    D0=-gam[0]*(sum((gam[i+1]*spatial[i] for i in range(3)),s.zeros(4,1))+s.I*B*psi)
    D=[D0]+spatial;Dbar=[s.conjugate(q).T*gam[0] for q in D]
    lower=[eta[i]*gam[i] for i in range(4)]
    T=s.Matrix(4,4,lambda i,j:-s.I/4*((bar*lower[i]*D[j]-Dbar[j]*lower[i]*psi)[0]+(bar*lower[j]*D[i]-Dbar[i]*lower[j]*psi)[0])+(G*eta[i]*n*n if i==j else 0))
    S=A[1:4,0];dS=s.Matrix(3,3,lambda a,i:s.diff(S[a],n)*dn[i]+s.diff(S[a],theta)*dtheta[i])
    curl=s.Matrix([dS[2,1]-dS[1,2],dS[0,2]-dS[2,0],dS[1,0]-dS[0,1]])
    E=s.Matrix([[0,S[2],-S[1]],[-S[2],0,S[0]],[S[1],-S[0],0]])
    expected=s.zeros(4);expected[0,0]=G*n*n
    expected[0,1:4]=-curl.T/4;expected[1:4,0]=-curl/4
    expected[1:4,1:4]=G*n*n*s.eye(3)+(K*E-E*K)/4
    simplify=lambda q:s.simplify(s.trigsimp(s.expand_trig(q)))
    assert (actualA-A).applyfunc(simplify)==s.zeros(4,1)
    assert (T-expected).applyfunc(simplify)==s.zeros(4)
    return {'axial':'(0,n sin(theta),0,n cos(theta))','energy':'G_A n²','momentum':'curl(n sin(theta),0,n cos(theta))/4','spatial_stress':'G_A n² I + [K,E_spin]/4, E_spin_ij=epsilon_ijk S_k','restrictions':'m=0, real lower two-component spinor, Gaussian/Fermi tetrad point, arbitrary real symmetric K and first n/theta jets; conformal scaling independently tested numerically. Complex phases are outside this identity.','symbolic_residuals':'All 4 axial and all 16 full stress components vanish against the formulas.','sympy':s.__version__}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();out=verify();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(out)
