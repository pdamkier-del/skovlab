"""Validate only P05-P07; old completed cycles are not rerun here."""
import hashlib,json,subprocess,sys
from pathlib import Path
import numpy as np

def main():
 root=Path(__file__).resolve().parents[1]
 scripts=['covariance_hf.py','component_consistency.py','coherent_pauli_bound.py']
 for name in scripts:subprocess.run([sys.executable,str(root/'code'/name)],check=True,cwd=root)
 read=lambda f:json.loads((root/'results'/f).read_text())
 d=read('06_covariance_hf.json');m=read('06_covariance_modes.json');p=read('07_component_consistency.json');b=read('08_coherent_pauli_bound.json')
 assert all(15<x<17 for x in d['observed_time_error_ratios'])
 assert d['coherent_time_refinement'][-1]['max_occupation_eigenvalue_drift']<1e-9
 assert max(abs(x) for x in d['energy_tangent_derivatives'])<1e-15
 assert all(x['occupation_spectrum_error']<1e-14 for x in d['thermal_state_checks'])
 # Recover the full mode spectrum directly from retained trace and Bloch arrays.
 q=np.asarray(m['trace_charge_mode']);ri=np.asarray(m['initial_full_bloch']);rf=np.asarray(m['final_DOP853_full_bloch'])
 assert ri.shape==rf.shape==(2,96,3) and len(m['momentum'])==96
 ei=np.stack([(1+q-np.linalg.norm(ri,axis=-1))/2,(1+q+np.linalg.norm(ri,axis=-1))/2],axis=-1)
 ef=np.stack([(1+q-np.linalg.norm(rf,axis=-1))/2,(1+q+np.linalg.norm(rf,axis=-1))/2],axis=-1)
 assert ei.min()>-1e-14 and ei.max()<1+1e-14 and np.max(abs(ef-ei))<1e-11
 assert np.max(abs(np.asarray(p['printed_generator_length_derivative'])))>1e-7
 assert np.max(abs(np.asarray(p['cross_product_completion_residual'])))<1e-15
 assert b['random_admissible_covariances_tested']==1200
 assert b['predeclared_coherent_state']['actual_contact_fraction']<b['predeclared_coherent_state']['bound']<.001
 paths=[root/'code'/x for x in scripts]+[root/'code/validate_covariance_cycles.py']+sorted((root/'results').glob('0[678]*.json'))
 report={'status':'PASS P05-P07 within declared finite-cutoff Gaussian assumptions','parent_programme_head':'c4192f955e579ba67058b0e3375e38ec8e18c4f4','new_gravitational_evolutions':0,'new_fixed_background_matter_evolution':True,'Level_B_accepted':False,'checkpoint_spectral_error':float(np.max(abs(ef-ei))),'sha256':{str(x.relative_to(root)):hashlib.sha256(x.read_bytes()).hexdigest() for x in paths}}
 (root/'results/covariance_validation.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS P05-P07, including retained covariance checkpoint. No Level B candidate.')
if __name__=='__main__':main()
