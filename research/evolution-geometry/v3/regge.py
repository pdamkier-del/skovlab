"""Pure Lorentzian Regge slabs with Schläfli gradients and scalar matter."""
from collections import defaultdict
from itertools import combinations
from math import factorial

import numpy as np

from mesh import boundary_facets


class GeometryError(ValueError):
    pass


def potential(mass=0.,quartic=0.,constant=0.):
    return (lambda x:.5*mass**2*x*x+quartic*x**4/4+constant,
            lambda x:mass**2*x+quartic*x**3)


class Regge:
    """Topological dimension D follows from the supplied pure top simplices.

    Use causally regular, non-null codimension-two faces and their link wedges.
    Signed squared intervals are independent. A single edge variable is shared.
    """
    def __init__(self,slab):
        top=slab.simplices
        self.D=D=top.shape[1]-1
        self.nv=len(slab.sites)
        if len({tuple(sorted(s)) for s in top})!=len(top):
            raise GeometryError("Duplicate simplices")
        self.edges=np.array(sorted({tuple(sorted(p)) for cell in top for p in combinations(cell,2)}))
        index={tuple(e):i for i,e in enumerate(self.edges)}
        boundary=boundary_facets(top)
        self.fixed_edges=np.array([index[p] for p in sorted({p for f in boundary for p in combinations(f,2)})],int)
        self.fixed_vertices=np.array(sorted({v for f in boundary for v in f}),int)
        self.free_edges=np.setdiff1d(np.arange(len(self.edges)),self.fixed_edges)
        self.free_vertices=np.setdiff1d(np.arange(self.nv),self.fixed_vertices)
        self.top=top
        self.slots=np.zeros((len(top),D+1,D+1),int)
        self.leg_ids=np.empty((len(top),D),int)
        for cell in range(len(top)):
            for i,j in combinations(range(D+1),2):
                self.slots[cell,i,j]=self.slots[cell,j,i]=index[tuple(sorted((top[cell,i],top[cell,j])))]
            self.leg_ids[cell]=self.slots[cell,np.arange(D),np.arange(1,D+1)]
        self.axial=all(tuple(self.edges[i]) in slab.axial_edges for i in self.leg_ids.ravel())
        # Edge derivative of each Gram entry. Both references use the first vertex.
        self.maps=np.zeros((D+1,D+1,D,D))
        for i,j in combinations(range(D+1),2):
            b=np.zeros((D+1,D+1))
            b[i,j]=b[j,i]=1.
            self.maps[i,j]=.5*(b[1:,0,None]+b[0,None,1:]-b[1:,1:])
        star=defaultdict(list)
        for i,cell in enumerate(top):
            for local in combinations(range(D+1),D-1):
                key=tuple(sorted(cell[list(local)]))
                other=tuple(j for j in range(D+1) if j not in local)
                star[key].append((i,local,other))
        self.hinges=list(sorted(star))
        self.h_edge_ids=np.empty((len(star),(D-1)*(D-2)//2),int)
        self.h_maps=[]
        k=D-2
        for i,j in combinations(range(k+1),2):
            b=np.zeros((k+1,k+1))
            b[i,j]=b[j,i]=1.
            self.h_maps.append(.5*(b[1:,0,None]+b[0,None,1:]-b[1:,1:]))
        self.h_positions=list(combinations(range(k+1),2))
        exterior={tuple(h) for f in boundary for h in combinations(f,D-1)}
        self.exterior=np.array([h in exterior for h in self.hinges])
        self.wedges=[]
        for i,h in enumerate(self.hinges):
            self.h_edge_ids[i]=[index[p] for p in combinations(h,2)]
            link=defaultdict(set)
            for cell,local,other in star[h]:
                u,v=top[cell,list(other)]
                link[u].add(v)
                link[v].add(u)
                self.wedges.append((i,cell,local+other))
            reached=set()
            todo=[next(iter(link))]
            while todo:
                u=todo.pop()
                if u not in reached:
                    reached.add(u)
                    todo.extend(link[u]-reached)
            degrees=sorted(len(x) for x in link.values())
            expected=([1,1]+[2]*(len(link)-2)) if self.exterior[i] else [2]*len(link)
            if len(reached)!=len(link) or degrees!=expected:
                raise GeometryError("Hinge link must be a single path or circle")
        self.hid,self.sid,order=zip(*self.wedges)
        self.hid=np.asarray(self.hid)
        self.sid=np.asarray(self.sid)
        self.order=np.asarray(order)
        self.h_slots=np.zeros((len(star),k+1,k+1),int)
        for c,(i,j) in enumerate(self.h_positions):
            self.h_slots[:,i,j]=self.h_slots[:,j,i]=self.h_edge_ids[:,c]

    @staticmethod
    def gram(s):
        return .5*(s[:,1:,0,None]+s[:,0,None,1:]-s[:,1:,1:])

    @staticmethod
    def unpack(s,slots):
        out=s[slots].copy()
        i=np.arange(slots.shape[1])
        out[:,i,i]=0.
        return out

    @staticmethod
    def geometry(G,require=None):
        order=G.shape[-1]
        if order==0:
            return np.ones(len(G)),np.zeros(len(G),bool),G
        eig=np.linalg.eigvalsh(G)
        if np.any(np.min(abs(eig),axis=1)<=1e-11*np.max(abs(eig),axis=1)):
            raise GeometryError("Null or degenerate Gram matrix")
        neg=np.sum(eig<0,axis=1)
        if np.any(neg>1) or (require is not None and np.any(neg!=require)):
            raise GeometryError("Unexpected Lorentz signature")
        return np.sqrt(abs(np.linalg.det(G)))/factorial(order),neg==1,np.linalg.inv(G)

    def temporal_norm(self,s,clock):
        values=np.asarray(clock)[self.top]
        difference=values[:,1:]-values[:,[0]]
        inverse=self.geometry(self.gram(self.unpack(s,self.slots)),require=1)[2]
        return np.einsum("bi,bij,bj->b",difference,inverse,difference)

    def evaluate(self,s,phi,Gnewton=1.,model=None,coupled=True,matter="axial",cosmological=0.):
        s=np.asarray(s,float)
        phi=np.asarray(phi,float)
        if len(s)!=len(self.edges) or len(phi)!=self.nv or not np.isfinite(s).all() or not np.isfinite(phi).all():
            raise ValueError("Invalid edge or field arrays")
        if Gnewton<=0:
            raise ValueError("Use coupled=False for a fixed geometry")
        Vpot,dVpot=potential() if model is None else model
        Ghat=self.gram(self.unpack(s,self.slots))
        volume,_,inverse=self.geometry(Ghat,require=1)
        hG=self.gram(self.unpack(s,self.h_slots))
        area,timelike,hinv=self.geometry(hG)
        S=self.unpack(s,self.slots[self.sid])
        S=S[np.arange(len(S))[:,None,None],self.order[:,:,None],self.order[:,None,:]]
        Q=self.gram(S)
        D=self.D
        k=D-2
        C=Q[:,k:,k:]
        if k:
            off=Q[:,:k,k:]
            C=C-off.transpose(0,2,1)@np.linalg.solve(Q[:,:k,:k],off)
        a,b,d=C[:,0,0],C[:,1,1],C[:,0,1]
        scale=np.max(abs(C),axis=(1,2))
        if np.any(np.minimum(abs(a),abs(b))<1e-11*scale):
            raise GeometryError("Null wedge ray")
        time=timelike[self.hid]
        angle=np.zeros(len(C),complex)
        x=time
        if np.any(a[x]<=0) or np.any(b[x]<=0):
            raise GeometryError("Timelike hinge must have a Euclidean normal plane")
        angle[x]=np.arccos(np.clip(d[x]/np.sqrt(a[x]*b[x]),-1.,1.))
        x=~time
        rad=np.sqrt(d[x]**2-a[x]*b[x])
        numerator=d[x]-rad
        # Rationalize for nearly coincident rays on the positive branch.
        numerator=np.where(d[x]>0,a[x]*b[x]/(d[x]+rad),numerator)
        phase=np.where(a[x]*b[x]<0,np.pi/2,np.where(numerator*np.sign(a[x])<0,np.pi,0.))
        angle[x]=phase-1j*np.log(abs(numerator)/np.sqrt(abs(a[x]*b[x])))
        delta=np.where(self.exterior,np.pi,2*np.pi).astype(complex)
        np.add.at(delta,self.hid,-angle)
        interior=~self.exterior
        if np.any(abs(delta[interior&~timelike].real)>1e-8):
            raise GeometryError("Causally irregular spacelike hinge (incorrect null-ray count)")
        deficit=np.where(timelike,delta.real,delta.imag)
        normalized=1/(8*np.pi*Gnewton)
        action_g=normalized*(area@deficit-cosmological*volume.sum())
        d_geom=np.zeros(len(s))
        local_phi=phi[self.top]
        onsite=np.asarray(Vpot(local_phi))
        if onsite.shape!=local_phi.shape:
            raise ValueError("Potential must be vectorized")
        potential_mean=onsite.mean(axis=1)
        d_field=-volume[:,None]*dVpot(local_phi)/(D+1)
        if matter=="axial":
            if not self.axial:
                raise GeometryError("An axial scalar stencil requires actual staircase legs")
            legs=s[self.leg_ids]
            if np.any(abs(legs)<1e-11*np.max(abs(legs),axis=1)[:,None]):
                raise GeometryError("Null scalar leg")
            jump=np.diff(local_phi,axis=1)
            kernel=jump/legs
            kinetic=np.sum(jump*kernel,axis=1)
            d_field[:,:-1]+=volume[:,None]*kernel
            d_field[:,1:]-=volume[:,None]*kernel
            if coupled:
                np.add.at(d_geom,self.leg_ids.ravel(),(.5*volume[:,None]*kernel**2).ravel())
        elif matter=="affine":
            jump=local_phi[:,1:]-local_phi[:,[0]]
            kernel=np.einsum("bij,bj->bi",inverse,jump)
            kinetic=np.sum(jump*kernel,axis=1)
            extra=.5*volume[:,None,None]*kernel[:,:,None]*kernel[:,None,:]
            d_field[:,1:]-=volume[:,None]*kernel
            d_field[:,0]+=volume*kernel.sum(axis=1)
        else:
            raise ValueError("Unknown matter scheme")
        density=-.5*kinetic-potential_mean
        scalar_action=volume@density
        if coupled:
            jac=.5*(density-cosmological*normalized)[:,None,None]*volume[:,None,None]*inverse
            if matter=="affine":
                jac+=extra
            for i,j in combinations(range(D+1),2):
                np.add.at(d_geom,self.slots[:,i,j],np.einsum("bij,ij->b",jac,self.maps[i,j]))
            if k:
                hjac=.5*normalized*(area*deficit)[:,None,None]*hinv
                for p,derivative in enumerate(self.h_maps):
                    np.add.at(d_geom,self.h_edge_ids[:,p],np.einsum("bij,ij->b",hjac,derivative))
        d_phi=np.zeros(self.nv)
        np.add.at(d_phi,self.top.ravel(),d_field.ravel())
        return action_g+scalar_action,d_geom,d_phi,deficit,volume
