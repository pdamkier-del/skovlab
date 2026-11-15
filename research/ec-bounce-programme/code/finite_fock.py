"""Independent explicit normal-ordering of particle+antiparticle operators.
Two Weyl channels, each two local spin components and four fermionic modes.
Sparse Fock matrices verify continuum coincident Wick algebra; not a closed QFT.
"""
import itertools,json
from pathlib import Path
import numpy as np
from scipy.sparse import csr_matrix,eye
from quantum_gas import correlator

SIGMA=np.array([[[0,1],[1,0]],[[0,-1j],[1j,0]],[[1,0],[0,-1]]],complex)

def annihilator(i,n):
 rows=[];cols=[];vals=[]
 for s in range(2**n):
  if s&(1<<i):rows.append(s^(1<<i));cols.append(s);vals.append((-1)**((s&((1<<i)-1)).bit_count()))
 return csr_matrix((vals,(rows,cols)),shape=(2**n,2**n),dtype=complex)

def normal_word(word,ops):
 # Fermionic Wick polynomial: move creators left WITHOUT CAR contraction terms.
 # This is not normal-ordering the already simplified product after contractions.
 sign=(-1)**sum((not word[i][1]) and word[j][1] for i in range(4) for j in range(i+1,4))
 ordered=[x for x in word if x[1]]+[x for x in word if not x[1]]
 creators=[i for i,d in ordered if d];ann=[i for i,d in ordered if not d]
 if len(set(creators))<len(creators) or len(set(ann))<len(ann):return None
 mat=eye(256,format='csr',dtype=complex)*sign
 for mode,dagger in ordered:mat=mat@(ops[mode].getH() if dagger else ops[mode])
 return mat

def operator():
 ops=[annihilator(i,8) for i in range(8)]
 for i in range(8):
  for j in range(8):
   err=ops[i]@ops[j].getH()+ops[j].getH()@ops[i]-(eye(256) if i==j else csr_matrix((256,256)))
   assert not err.nnz or np.max(abs(err.data))<1e-13
 # chi_spin=a_spin+b_spin^dagger at this point. Local wave functions are an
 # orthonormal +/- momentum pair; weights and volume set to one.
 fields=[[(4*c+i,False),(4*c+2+i,True)] for c in range(2) for i in range(2)]
 matrices=[]
 for a in range(4):
  upper=-np.eye(2) if a==0 else SIGMA[a-1]
  lower=np.eye(2) if a==0 else SIGMA[a-1]
  matrices.append(np.block([[upper,np.zeros((2,2))],[np.zeros((2,2)),lower]]))
 Q=csr_matrix((256,256),dtype=complex)
 for a,M in enumerate(matrices):
  for i,j,k,l in itertools.product(range(4),repeat=4):
   coeff=(-1 if a==0 else 1)*M[i,j]*M[k,l]
   if abs(coeff)<1e-15:continue
   for gi,gj,gk,gl in itertools.product(fields[i],fields[j],fields[k],fields[l]):
    w=[(gi[0],not gi[1]),gj,(gk[0],not gk[1]),gl]
    mat=normal_word(w,ops)
    if mat is not None:Q+=coeff*mat
 assert np.max(abs((Q-Q.getH()).data),initial=0)<1e-12
 return Q

def main():
 Q=operator();Q2=Q@Q;out=[];rng=np.random.default_rng(8321)
 choices=[(.3,.3,.3,.3),(.8,.1,.8,.1),(.8,.1,.1,.8),(1,0,0,0),(0,0,0,0)]
 choices+=list(map(tuple,rng.random((12,4))))
 maxerr=0
 for fp,fm,gp,gm in choices:
  f=np.repeat([fp,fm,gp,gm],2);weights=np.array([np.prod([f[i] if s&(1<<i) else 1-f[i] for i in range(8)]) for s in range(256)])
  mean=float(np.dot(weights,Q.diagonal()).real);d=[2*(fp-fm),2*(gp-gm)];wick=correlator(d,[1,-1]);maxerr=max(maxerr,abs(mean-wick))
  variance=float(np.dot(weights,Q2.diagonal()).real-mean**2)
  assert abs(mean-wick)<1e-12 and variance>-1e-12
  out.append({'occupations_by_channel_particle_antiparticle':[fp,fm,gp,gm],'net_charges':d,'Fock_A2':mean,'coincident_Wick_A2':wick,'finite_mode_Q_variance':variance})
 dest=Path(__file__).resolve().parents[1]/'results/01_particle_antiparticle_fock.json'
 dest.write_text(json.dumps({'normal_order':'Full quartic Wick polynomial relative to a,b vacuum; all pair creation/annihilation terms retained.','channels':2,'Fock_dimension':256,'max_independent_error':maxerr,'samples':out,'limitation':'Finite-mode variance does not certify spacetime-smeared renormalized stress noise or interacting evolution.'},indent=2)+'\n')
 print('PASS particle/antiparticle Fock vs Wick:',maxerr)
if __name__=='__main__':main()
