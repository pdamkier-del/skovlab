"""Reproduce the independent issue #6 audit; no Level B certification inferred."""
import json,hashlib,platform,subprocess,sys
from pathlib import Path
import numpy,scipy,sympy

def main():
 root=Path(__file__).resolve().parents[1]
 scripts=['verify_connection.py','scalar_identities.py','fermion_stress.py','source_crosschecks.py','nonminimal_source.py','closed_turn.py','inhomogeneous_constraints.py']
 for name in scripts:subprocess.run([sys.executable,str(root/'code'/name)],cwd=root,check=True)
 read=lambda f:json.loads((root/'results'/f).read_text())
 a=read('01_connection_variation.json');assert len(a['full_24_component_variations'])==8
 assert all(x['hessian_rank']==24 and x['max_Euler_residual']<1e-11 for x in a['full_24_component_variations'])
 b=read('02_scalar_and_fermions.json');assert set(b['residuals'].values())=={'0'}
 d=read('03_closed_turns.json')
 for case in d['cases']:
  assert case['samples'][0]['H_over_mu']<0<case['samples'][-1]['H_over_mu'] and case['Hdot_over_mu2_at_turn']>0
  err=[x['endpoint_error']for x in case['refinement']];assert all(12<err[i]/err[i+1]<20 for i in range(2))
  assert max(x['original_tetrad_variation_max']for x in case['samples'])<1e-8
 e=read('05_inhomogeneous_constraints.json')
 assert all(x['independent_refinement'][-1]['conformal_factor_min']>0 for x in e['cases'])
 assert 3.5<e['cases'][1]['linearized_solution_error']/e['cases'][0]['linearized_solution_error']<4.5
 for case in e['cases']:
  assert len(case['raw_BVP_angles'])==case['BVP_nodes']==len(case['raw_BVP_chi'])==len(case['raw_BVP_dchi'])
  assert case['independent_refinement'][-1]['normal_Theta_dot_min_in_mu2']>0
 files=sorted((root/'code').glob('*.py'))+sorted((root/'results').glob('0*.json'))+[root/'results/provenance.json']
 result={'status':'PASS stated classical/regulated algebra and finite local geometry checks','python':sys.version,'numpy':numpy.__version__,'scipy':scipy.__version__,'sympy':sympy.__version__,'platform':platform.platform(),'completed_scripts':scripts,'Level_B_accepted':False,'source_and_evidence_sha256':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()for p in files},'limitations':'No complete physical fermion state/quantum stress-noise, exact microscopic nonminimal dictionary, global completeness or Level B torsion-caused bounce.'}
 (root/'results/validation.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS issue #6 audit. Healthy pseudoscalaron verified; no Level B torsion-bounce accepted.')
if __name__=='__main__':main()
