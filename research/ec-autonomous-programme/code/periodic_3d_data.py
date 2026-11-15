"""Continuum conformal construction of genuinely 3D periodic ECD initial data.
Real aligned seed: momentum source is a curl, solved by Fourier vector Poisson.
The scalar nonlinear constraint is solved pseudospectrally with mean(log chi)=0.
Evolution and full FD constraints are always those of the existing ECD engine.
"""
import argparse,json,time
from pathlib import Path
import numpy as np
from scipy.optimize import newton_krylov
from scipy.sparse.linalg import LinearOperator
from scipy.signal import resample
from strong_benchmark import ecd


def spectral_geometry(n,length):
    k=2*np.pi*np.fft.fftfreq(n,d=length/n)
    wave=np.array(np.meshgrid(k,k,k,indexing='ij'));ksq=np.sum(wave*wave,axis=0)
    def grad(a):return np.array([np.fft.ifftn(1j*q*np.fft.fftn(a)).real for q in wave])
    def lap(a):return np.fft.ifftn(-ksq*np.fft.fftn(a)).real
    return wave,ksq,grad,lap


def construct(n=17,n0=4.,epsilon=.1,length=8.,tolerance=1e-11):
    if n<5 or n%2!=1 or not 0<=abs(epsilon)<1:raise ValueError('Odd n>=5, |epsilon|<1 required.')
    start=time.monotonic();grid=ecd.Grid(n,length/2,'periodic');x,y,z=np.moveaxis(grid.xyz,-1,0);k=2*np.pi/length
    seed=n0*(1+epsilon*np.cos(k*x)*np.cos(k*y)*np.cos(k*z))
    dseed=np.array([-n0*epsilon*k*np.sin(k*x)*np.cos(k*y)*np.cos(k*z),-n0*epsilon*k*np.cos(k*x)*np.sin(k*y)*np.cos(k*z),-n0*epsilon*k*np.cos(k*x)*np.cos(k*y)*np.sin(k*z)])
    # j_i = 1/4 (partial_y n_seed,-partial_x n_seed,0), with kappa=1.
    j=np.array([dseed[1]/4,-dseed[0]/4,np.zeros_like(seed)])
    wave,ksq,grad,lap=spectral_geometry(n,length)
    safe=np.where(ksq>0,ksq,1.)
    W=np.array([np.fft.ifftn(np.where(ksq>0,-np.fft.fftn(a)/safe,0.)).real for a in j])
    dW=np.array([grad(a) for a in W]);div=sum(dW[i,i] for i in range(3))
    LW=np.moveaxis(dW+dW.swapaxes(0,1)-2/3*np.eye(3)[:,:,None,None,None]*div,(0,1),(-2,-1))
    Q=np.sum(LW*LW,axis=(-2,-1))+2*(3/16)*seed*seed
    counter=0
    def evaluate(flat,details=False):
        nonlocal counter
        counter+=1;u=np.asarray(flat).reshape((n,)*3);chi=np.exp(u)
        Ksq=1.5*np.mean(Q*chi**-7)/np.mean(chi**5)
        residual=lap(u)+np.sum(grad(u)**2,axis=0)-Ksq/12*chi**4+Q/8*chi**-8+np.mean(u)
        return (residual,Ksq) if details else residual.ravel()
    symbol=-ksq-9.;symbol[0,0,0]=1.
    def precondition(v):return np.fft.ifftn(np.fft.fftn(v.reshape((n,)*3))/symbol).real.ravel()
    M=LinearOperator((n**3,n**3),matvec=precondition,dtype=float)
    u=newton_krylov(evaluate,np.zeros(n**3),f_tol=tolerance,maxiter=20,inner_M=M).reshape((n,)*3)
    residual,Ksq=evaluate(u,True);chi=np.exp(u);K=np.sqrt(Ksq)
    if np.max(abs(residual))>tolerance:raise RuntimeError('Scalar spectral constraint solve failed final tolerance.')
    g,_,_=ecd.minkowski(grid);g[...,1:,1:]=np.eye(3)*chi[...,None,None]**4
    Kij=LW/chi[...,None,None]**2+g[...,1:,1:]*K/3
    p=ecd.harmonic_initial_velocity(grid,g,Kij)
    psi=np.zeros((n,)*3+(4,),complex);psi[...,2]=np.sqrt(seed)*chi**-3
    state=g,p,psi;d=ecd.diagnostics(grid,state,mass=0.)
    # Dealiased continuum residual on a finer grid, independent of monitored FD H.
    fine=2*n+1
    def prolong(a):
        for axis in range(3):a=resample(a,fine,axis=axis)
        return a.real
    uf=prolong(u);Qf=prolong(Q);_,_,gf,lf=spectral_geometry(fine,length);chif=np.exp(uf)
    constraint_fine=-8*chif**-4*(lf(uf)+np.sum(gf(uf)**2,axis=0))+2*Ksq/3-Qf*chif**-12
    momentum_spectral=np.array([lap(W[i])+grad(div)[i]/3-j[i] for i in range(3)])
    Eexpected=(3/16)*seed*seed*chi**-12
    report={'n':n,'parameters':{'n0':n0,'epsilon':epsilon,'length':length,'mass':0.,'kappa':1.,'tolerance':tolerance},'Ktrace':float(K),'mean_log_chi':float(np.mean(u)),'scalar_spectral_residual_max':float(np.max(abs(residual))),'vector_spectral_residual_max':float(np.max(abs(momentum_spectral))),'oversampled_continuum_Hamiltonian_max':float(np.max(abs(constraint_fine))),'oversample_n':fine,'FD_Hamiltonian_max':float(np.max(abs(d['hamiltonian']))),'FD_Hamiltonian_relative':float(np.max(abs(d['hamiltonian']))/(2*np.max(abs(d['E'])))),'FD_momentum_max':float(np.max(abs(d['momentum']))),'harmonic_max':float(np.max(abs(d['harmonic']))),'energy_formula_max_error':float(np.max(abs(d['E']-Eexpected))),'seed_momentum_mean':np.mean(j,axis=(1,2,3)).tolist(),'initial_H_min':float(np.min(d['H'])),'initial_H_max':float(np.max(d['H'])),'source_variation_each_axis':[float(np.max(np.ptp(seed,axis=i))) for i in range(3)],'chi_range':[float(np.min(chi)),float(np.max(chi))],'field_evaluations':counter,'seconds':time.monotonic()-start,'scope':'Genuinely x/y/z-varying constrained data on a torus, not a finite body; only initial data, not a validated evolution.'}
    return grid,state,report


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    records=[]
    for n in [9,17,33]:
        _,_,r=construct(n=n);records.append(r);print('completed 3D initial n',n,'H',r['FD_Hamiltonian_max'],'M',r['FD_momentum_max'],flush=True)
    tolerance_records=[]
    for tol in [1e-9,1e-11,1e-12]:
        _,_,q=construct(n=17,tolerance=tol);tolerance_records.append(q)
    report={'tolerance_study':tolerance_records,'hypothesis':'A real polarized seed with variation in all three coordinates admits a periodic conformal constraint solution in this small-amplitude family.','records':records,'classification':'Numerically supported initial-data existence for these seeds; no general existence/uniqueness or dynamical stability theorem.'}
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2,allow_nan=False)+'\n');print('wrote',args.output)
if __name__=='__main__':main()
