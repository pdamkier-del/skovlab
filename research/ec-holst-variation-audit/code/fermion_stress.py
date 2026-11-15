"""Off-shell lapse/axis variation versus the full on-shell scalar/Dirac stress.
Random classical jets test the tensor algebra, not a physical quantum state.
"""
import json
from pathlib import Path
import numpy as np

def main():
 I=np.eye(2);Z=np.zeros((2,2));S=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)
 G=np.array([np.block([[Z,I],[I,Z]])]+[np.block([[Z,s],[-s,Z]]) for s in S]);eta=np.array([-1,1,1,1]);G5=-1j*G[0]@G[1]@G[2]@G[3]
 rng=np.random.default_rng(603);out=[]
 for _ in range(5):
  a=rng.uniform(.8,1.4,3);p=rng.normal(size=(3,3));psi=(rng.normal(size=(3,4))+1j*rng.normal(size=(3,4)))/10;bar=psi.conj()@G[0];A=np.einsum('fi,aij,fj->a',bar,np.array([G5@g for g in G]),psi).real
  w=.3;wd=.07;mass=.2;X=np.sqrt(2/3)*w+np.arcsinh(1.);h=np.sqrt(3/8)/np.cosh(X);g=3/(16*np.cosh(X)**2);V=.001
  B=mass*np.eye(4)+sum((2*g*eta[b]*A[b]+(h*wd if b==0 else 0))*(G5@G[b]) for b in range(4));sp=1j*p[:,:,None]*psi[:,None,:]
  dt=-np.einsum('ab,fb->fa',G[0],np.einsum('iab,fib->fa',G[1:]/a[:,None,None],sp)+1j*np.einsum('ab,fb->fa',B,psi))
  D=np.concatenate([dt[:,None,:],sp],axis=1);db=D.conj()@G[0];gl=np.array([-G[0]]+[a[i]*G[i+1]for i in range(3)])
  Q=np.einsum('fi,mij,fnj->mn',bar,gl,D)-np.einsum('fni,mij,fj->mn',db,gl,psi);metric=np.diag(np.r_[-1.,a*a]);A2=np.sum(eta*A*A)
  K=(-.25j*(Q+Q.T)).real;Acov=eta*A*np.r_[1.,a];grad=np.array([wd,0,0,0]);T=K+h*(np.outer(Acov,grad)+np.outer(grad,Acov))/2+g*metric*A2
  T+=np.outer(grad,grad)-metric*(-wd*wd/2+V)
  def action(N,axes):
   time=.5j*np.sum(np.einsum('fi,ij,fj->f',bar,G[0],dt)-np.einsum('fi,ij,fj->f',dt.conj()@G[0],G[0],psi))/N
   kin=time
   for i in range(3):kin+=.5j*np.sum(np.einsum('fi,ij,fj->f',bar,G[i+1],sp[:,i])-np.einsum('fi,ij,fj->f',sp[:,i].conj()@G[0],G[i+1],psi))/axes[i]
   return float((N*np.prod(axes)*(kin-mass*np.sum(bar*psi)-h*wd/N*A[0]-g*A2+wd*wd/(2*N*N)-V)).real)
  eps=1e-5;energy=-(action(1+eps,a)-action(1-eps,a))/(2*eps*np.prod(a));press=[]
  for i in range(3):
   ap=a.copy();am=a.copy();ap[i]+=eps;am[i]-=eps;press.append(a[i]*(action(1,ap)-action(1,am))/(2*eps*np.prod(a)))
  err=max(abs(energy-T[0,0]),np.max(abs(np.array(press)-np.diag(T)[1:]/a**2)));assert err<1e-9
  out.append({'energy_error':float(abs(energy-T[0,0])),'max_pressure_error':float(np.max(abs(np.array(press)-np.diag(T)[1:]/a**2)))})
 (Path(__file__).resolve().parents[1]/'results/04_effective_stress.json').write_text(json.dumps({'off_shell_variations':out,'on_shell_stress':'T=scalar stress+K_D+h A_(mu partial_nu)omega +g g_munu A^2 for Lint=-h partial(omega).A-g A^2.','scope':'Independent variation before on-shell substitution; random classical jets, not quantized matter or an EOS.'},indent=2)+'\n');print('PASS independent off-shell energy/pressure variations including derivative axial coupling')
if __name__=='__main__':main()
