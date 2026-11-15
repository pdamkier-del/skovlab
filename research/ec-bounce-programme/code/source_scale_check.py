"""Arithmetic diagnostic of printed nonminimal-theory parameters.
Not a reproduction or refutation of the paper's 2PI dynamics.
"""
import json
from pathlib import Path

def main():
 xi=1000.;T_over_MP=.001;m_over_T=100.
 m_over_MP=T_over_MP*m_over_T;cutoff_over_MP=1/xi
 ratio=m_over_MP/cutoff_over_MP
 assert ratio==100.
 result={'primary_source':'https://arxiv.org/html/1512.06074v1','location':'Figure 5 caption and Section VI','printed_approximate_parameters':{'xi':xi,'T0_over_printed_MP':T_over_MP,'mass_over_T0':m_over_T},'derived_mass_over_printed_MP':m_over_MP,'quoted_relativistic_scale_over_same_MP':cutoff_over_MP,'mass_over_quoted_scale':ratio,'precision':'Order-of-magnitude parameters and cutoff estimate; not an exact unitarity calculation.','conclusion':'Printed parameters do not demonstrate m << MP/xi. A separately matched heavy-particle EFT or different stated regime must be audited; no universal heavy-state exclusion is inferred.'}
 (Path(__file__).resolve().parents[1]/'results/05_nonminimal_source_scale.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS printed-parameter scale arithmetic; full 2PI validity remains unresolved')
if __name__=='__main__':main()
