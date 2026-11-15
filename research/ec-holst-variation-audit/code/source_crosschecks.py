"""Convention conversion of independently derived nonminimal coupling algebra.
Source typography issues are recorded with exact references, not silently fixed.
"""
import json
from pathlib import Path
import sympy as s

def main():
 Y,a,nu,A,V,dphi,M=s.symbols('Y a nu A V dphi M',real=True)
 B=Y/4;J=-(a*V+nu*A)/2;four=3*J**2/(4*M**2)-12*(A/8+B*J)**2/(M**2*(1+Y**2))
 expected=3*(a*a*V*V+2*a*(nu+Y)*V*A+(nu*nu+2*nu*Y-1)*A*A)/(16*M**2*(1+Y**2))
 assert s.simplify(four-expected)==0
 # Map the 2024 formula through R'_p=-R', phi_p=-phi, A_p=-A,
 # alpha_p=a, beta_nonminimal_p=-nu. V_p=V. Gravity c_p=4c/M^2.
 paperY=-Y;paperA=-A;paperNu=-nu
 paper_four=3*(a*a*V*V+2*a*(paperNu+paperY)*V*paperA+(paperNu**2+2*paperNu*paperY-1)*paperA**2)/(16*M*M*(1+paperY**2))
 assert s.simplify(paper_four-four)==0
 own_derivative=s.sqrt(s.Rational(3,8))*dphi/M*(-A/s.sqrt(1+Y*Y)+(nu*A+a*V)*Y/s.sqrt(1+Y*Y))
 paper_derivative=s.sqrt(s.Rational(3,8))*(-dphi)/M*((-1/s.sqrt(1+paperY**2)+paperNu*paperY/s.sqrt(1+paperY**2))*paperA+a*paperY/s.sqrt(1+paperY**2)*V)
 assert s.simplify(own_derivative-paper_derivative)==0
 result={'2022_reference':'https://arxiv.org/html/2206.15041v3','2022_verified_equations':['4.19','4.20-4.22','4.25-4.31'],'2024_reference':'https://arxiv.org/html/2406.14982v2','2024_verified_structure':['12-14 scalar normalization','35-37 effective-formula algebra'],'2024_effective_formula_map':'b_p=-4 beta/M^2, c_p=4c/M^2, chi_p=-z, phi_p=-omega; alpha_N,p=a, beta_N,p=-nu, A_p=-A, V_p=V. This is a map matching effective formulas; the independent microscopic trace-source sign dictionary of Eq29 is not certified by this algebra alone.','2024_nonminimal_residuals':{'AA_AV_VV':'0','scalar_derivative_currents':'0'},'2026_reference':'https://arxiv.org/html/2605.09571v2','2026_printed_consistency_flags':[{'equations':'14-18','flag':'K in Eq15 multiplies (partial B)^2. Canonical integration over z in Eq17 requires B_z; Eq18 has the correct universal asinh relation. Do not identify this K_B with 2022 K_z.'},{'equations':'38-39,41','flag':'Eq38 uses C_phi/M_P, so C_phi is dimensionless; Eq39 as printed has derivative dB/dphi of dimension inverse mass and requires M_P or a declared dimensionless phi. Eq41 is dimensionless.'},{'equations':'40 and 42','flag':'For real gamma and B(0)=1/(4gamma), substitution into positive Eq40 stays positive, while Eq42 is negative. A signature change cannot reconcile two formulas within the same convention. Independent elimination fixes the effective-action sign here.'}],'limits':'Flags are local algebra/dimension checks, not a reproduction or refutation of reheating/leptogenesis phenomenology. Separate literal typography from physical model.'}
 (Path(__file__).resolve().parents[1]/'results/06_source_crosschecks.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS nonminimal convention mapping; source equation/dimension flags preserved')
if __name__=='__main__':main()
