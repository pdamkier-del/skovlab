"""Independent finite-Fock and Wick checks, plus Pauli/EFT scale calculations.
This computes reference-state contact expectations, not an interacting quantum bounce.
"""
import argparse,json
from pathlib import Path
import numpy as np
from field_source import SIGMA,modes,ETA


def annihilators(number):
    out=[];dim=2**number
    for i in range(number):
        a=np.zeros((dim,dim),complex)
        for state in range(dim):
            if state&(1<<i):a[state^(1<<i),state]=(-1)**((state&((1<<i)-1)).bit_count())
        out.append(a)
    return out


def contact_expectation(same_species=False):
    u=modes()[:,:2].T;ops=[-np.eye(2),*SIGMA]
    M=np.array([u.conj().T@q@u for q in ops])
    if not same_species:M=np.array([np.diag(np.diag(q)) for q in M])
    annih=annihilators(6);dim=64
    def bilinear(matrix):
        value=np.zeros((dim,dim),complex)
        for i in range(6):
            for j in range(6):
                if abs(matrix[i,j])>1e-15:value+=matrix[i,j]*(annih[i].conj().T@annih[j])
        return value
    Q=np.zeros((dim,dim),complex)
    for sign,mat in zip(ETA,M):
        J=bilinear(mat);Q+=sign*(J@J-bilinear(mat@mat))
    exact=float(Q[-1,-1].real);wick=float(sum(sign*(np.trace(mat)**2-np.trace(mat@mat)) for sign,mat in zip(ETA,M)).real)
    assert abs(exact-wick)<1e-11 and np.max(abs(Q-Q.conj().T))<1e-12
    target=-72. if same_species else -36.
    assert abs(exact-target)<1e-11
    return {'species_assignment':'one Weyl species, six occupied momentum modes' if same_species else 'six independent Weyl species, one occupied mode each','occupations':[1]*6,'normal_ordered_A2_times_V2':exact,'independent_Wick_result':wick,'mean_A2_times_V2':-36.,'coefficient_C_in_minus_C_n2':-exact/36,'qualification':'Exact reference-state finite-occupation Wick polynomial; not an interacting state, renormalized curved-space stress, or closed scattering truncation.'}


def verify():
    GA=3/16;scale=[]
    for occupation in [1.,.5,.1]:
        L=2*np.pi;p=2*np.pi/L;n0=6*occupation/L**3;ab=np.sqrt(GA*n0/p);rho=p**3/(GA*GA*n0);pb=p/ab
        scale.append({'per_mode_occupation':occupation,'a_b':ab,'rho_b_in_reduced_Planck4':rho,'p_b_in_reduced_Planck':pb,'GA_p_b_squared':GA*pb*pb,'R_b_in_reduced_Planck2':2*rho,'torsion_norm_b_in_reduced_Planck2':8*rho})
    classical=1024*np.pi**3/27
    assert abs(scale[0]['rho_b_in_reduced_Planck4']-classical)<1e-10
    # Six equally populated free chiral Fermi seas: C=1+1/g, not guessed from a mean current.
    g=6;C=1+1/g;prefactor=g*C/(24*np.pi**2)
    return {'six_distinct_species':contact_expectation(False),'same_species_six_modes':contact_expectation(True),'Pauli_normalized_benchmark':scale,'bounds':'For the six fundamental modes with f<=1: rho_b>=1024 pi³/(27 kappa²), p_b>=8 pi^(3/2)/(3 sqrt(kappa)), GA p_b²>=4 pi³/3. Changing L does not lower these physical bounce scales.','free_chiral_gas':{'g':g,'C':C,'ratio_prefactor_in_kappa_pF2':prefactor,'formal_equal_correction_pF_in_reduced_Planck':1/np.sqrt(prefactor),'ratio_at_pF_point1_Mbar':prefactor*.1**2,'scope':'Leading vacuum-normal-ordered free-state estimate, no strong correlations or medium response; not a universal bound for every quantum state.'},'classification':'Pauli/exchange algebra mathematically checked. A controlled quantum bounce does not follow; the benchmark cancellation is outside the small EFT/interaction expansion.'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();out=verify();args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
