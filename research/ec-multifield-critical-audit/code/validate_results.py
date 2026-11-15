"""Acceptance checks for the recorded full-field ODE runs, not a physical-validity test."""
import json
from pathlib import Path
r=Path(__file__).resolve().parents[1]/'results'
d=json.loads((r/'03_classical_robustness.json').read_text())
e=d['exact_refinement']
for x in e:
 assert x['status']=='completed' and x['event']['mean_Hdot']>0
 assert x['max_constraint_over_fixed_rho_b']<2e-7
for a,b in zip(e,e[1:]):
 assert 12<a['exact_endpoint_errors'][2]/b['exact_endpoint_errors'][2]<20
for p in d['perturbations']:
 for x in p['records']:
  assert x['status']=='completed' and x['event']['mean_Hdot']>0
  assert x['max_constraint_over_fixed_rho_b']<2e-8
  assert x['max_momentum']<1e-10 and x['max_offdiagonal_stress']<1e-10
 assert abs(p['records'][0]['event']['t']-p['records'][1]['event']['t'])<3e-10
assert d['torsion_free']['endpoint']['Hmean']<0
assert d['torsion_free']['max_constraint_over_reference_rho_b']<2e-8
print('PASS: exact fourth-order refinement, five constrained local turns, and separate torsion-free control')
