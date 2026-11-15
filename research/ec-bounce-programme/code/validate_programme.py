"""Run the bounded research calculations and verify their independent evidence.
No cosmological bounce or all-orders QFT validity is certified by this script.
"""
import hashlib,json,platform,subprocess,sys
from pathlib import Path
import numpy,scipy,sympy

def main():
 root=Path(__file__).resolve().parents[1]
 scripts=['finite_fock.py','thermal_bounds.py','stress_and_mass.py','nonrelativistic_loophole.py','source_scale_check.py']
 for name in scripts:subprocess.run([sys.executable,str(root/'code'/name)],cwd=root,check=True)
 read=lambda f:json.loads((root/'results'/f).read_text())
 a=read('01_particle_antiparticle_fock.json');b=read('02_thermal_and_pauli_bounds.json');c=read('03_stress_and_mass.json');d=read('04_nonrelativistic_loophole.json')
 assert a['Fock_dimension']==256 and len(a['samples'])==17 and a['max_independent_error']<1e-12
 assert abs(a['samples'][0]['Fock_A2'])<1e-12 and a['samples'][0]['finite_mode_Q_variance']>0
 assert b['random_distributions_tested']==800
 assert all(z['species_loop_proxy_at_formal_equality']>=.75-1e-12 for z in b['cutoff_checks'])
 assert all(z['unpolarized_Dirac_A2']==0 for z in b['thermal_checks'] if z['mu']==0)
 assert c['symbolic_checks']['adiabatic_conservation']=='0' and c['symbolic_checks']['grand_energy_minus_5GB']=='0'
 assert c['formal_gradient_sign_change_r']<c['formal_enthalpy_zero_r']<c['formal_flat_bounce_r']
 assert all(z['A2']<0 and z['rho0']>0 for z in c['massive_thermal_examples'])
 assert d['false_radiation_only_turn']['omitted_fermion_energy_over_radiation']>1e10
 assert d['false_radiation_only_turn']['contact_over_full_positive_energy']<1e-9
 assert read('05_nonminimal_source_scale.json')['mass_over_quoted_scale']==100.
 files=sorted((root/'code').glob('*.py'))+sorted((root/'results').glob('0*.json'))
 digest={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in files}
 result={'status':'PASS within explicitly declared source/state assumptions','python':sys.version,'numpy':numpy.__version__,'scipy':scipy.__version__,'sympy':sympy.__version__,'platform':platform.platform(),'scripts_completed':scripts,'evidence_sha256':digest,'new_spacetime_evolutions':0,'level_B_accepted':False,'limitation':'No complete covariant interacting stress/noise, actual quantum bounce, or inhomogeneous robustness demonstrated.'}
 (root/'results/validation.json').write_text(json.dumps(result,indent=2)+'\n')
 print('PASS programme integration checks. Level B remains unachieved.')
if __name__=='__main__':main()
