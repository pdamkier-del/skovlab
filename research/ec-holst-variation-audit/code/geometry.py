"""Direct metric-compatible affine curvature, no torsion formula imported."""
import itertools
import numpy as np
ETA=np.array([-1.,1.,1.,1.]);E=np.zeros((4,4,4,4))
for p in itertools.permutations(range(4)):E[p]=(-1)**sum(p[i]>p[j] for i in range(4) for j in range(i+1,4))

def torsion(t,q):
 T=np.zeros((4,4,4))
 for a,b,c in itertools.product(range(4),repeat=3):
  T[a,b,c]=((ETA[a] if a==c else 0)*t[b]-(ETA[a] if a==b else 0)*t[c])/3-np.dot(E[a,b,c],q)/6
 return T

def contortion(T):return np.array([[[(T[a,b,c]-T[b,c,a]+T[c,a,b])/2 for c in range(4)]for b in range(4)]for a in range(4)])
def contractions(C,dC=None):
 if dC is None:dC=np.zeros((4,4,4,4)) # derivative,lowered first, derivative-index, vector-index
 G=ETA[:,None,None]*C;dG=ETA[None,:,None,None]*dC
 R=np.zeros((4,4,4,4))
 for a,b,c,d in itertools.product(range(4),repeat=4):R[a,b,c,d]=dG[c,a,d,b]-dG[d,a,c,b]+sum(G[a,c,e]*G[e,d,b]-G[a,d,e]*G[e,c,b] for e in range(4))
 scalar=sum(ETA[b]*R[a,b,a,b] for a,b in itertools.product(range(4),repeat=2))
 holst=np.einsum('abcd,a,abcd',-E,ETA,R)
 return float(scalar),float(holst),R
