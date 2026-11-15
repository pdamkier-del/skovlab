# Exact benchmark and its scope

Six independent massless fields have momenta ±p along the three axes, equal comoving numbers n0/6, common chirality, and positive **free** kinetic-energy eigenvectors u_f†u_f=1. Put ψ_f=a^(-3/2)√(n0/6)u_f exp(ip_f·x−iθ), n=n0/a³. The total vector current is at rest and Aᵃ=(−n,0,0,0). Its square is −n²; the sum of individual axial squares is zero.

Direct substitution into every Dirac equation and the full stress gives

θ̇=p/a−2G_A n,
E=pn0/a⁴−G_A n0²/a⁶,
P=pn0/(3a⁴)−G_A n0²/a⁶.

Write C_r=pn0, C_s=G_A n0², a_b²=C_s/C_r, q²=κC_r/3. In conformal time,

a(η)=√(a_b²+q²η²),
θ(η)=pη−(3/2)atan(qη/a_b),   q/a_b=4p/3.

Hamiltonian, spatial Einstein equation and Ė+3H(E+P)=0 reduce independently to zero in SymPy. The direct lapse/axis variation and explicit gamma source provide additional checks, not repetitions of that polynomial identity. `01_independent_benchmark.json` and `04_additional_checks.json` contain the evidence.

At the bounce define ρ_b=C_r/a_b⁴=C_s/a_b⁶ (the positive radiation contribution, **not** total E). E_b=0, P_b=−2ρ_b/3 and Ḣ_b=κρ_b/3>0. NEC violation is explicit. The interacting phase frequency becomes negative near the bounce; calling all phases positive energy throughout would be incorrect. This alone does not establish a quantum ghost or a stable vacuum.

## Regularity and completeness

R_b=2κρ_b, K_b=12Ḣ_b²=4κ²ρ_b²/3 and T_abcT^abc=−(3/2)κ²A²=8κρ_b at the bounce. All fields, a≥a_b>0, and their finite-order derivatives remain bounded along the exact solution. Thus the full metric-compatible connection and its curvature are regular there. The massless full scalar R̃=R+3κ²A²/8 vanishes; this single cancellation alone would not prove regularity. No global conclusion about arbitrary perturbations follows from it.

Proper cosmic time t(η)=[ηa+(a_b²/q)asinh(qη/a_b)]/2 extends to ±∞. For each timelike geodesic of fixed comoving momentum P, dτ/dt=(1+P²/a²)^(-1/2) has a positive lower bound. Null affine parameter is proportional to ∫a²dη and diverges in both directions. The exact FLRW spacetime is causally geodesically complete, also under the flat torus quotient. A torus is locally isotropic but lacks global continuous rotational symmetry.

## What actually differs from one field

For one commuting classical spinor the Fierz identities restrict its own axial current to spacelike or null; the six-field cross terms allow a timelike total current. This explains why a one-field localized packet is not a numerical reproduction of this homogeneous benchmark. Neither calculation proves a general collapse theorem. Two nonparallel chiral rays can already make total A timelike, but isotropic stress needs more structure.

At least four positive-weight massless rays are needed for zero net momentum and rank-three isotropic second moment: with at most three rays a positive weighted zero sum confines their span to dimension≤2. Four tetrahedral directions attain the bound and pass a direct source test. Six is convenient, not minimal. On a torus the tetrahedral momentum quantization must also be respected.

Within isotropic, balanced massless families, mixing opposite positive-free-energy chiral modes with fraction r gives χ=1−2r and A²=−χ²n². The formal bounce remains for χ≠0 with a_b²=G_Aχ²n0/p. For χ=0 this classical axial source vanishes and the solution is singular radiation. Reducing |χ| raises the formal bounce momentum by 1/|χ| and radiation density by 1/χ⁴. This is not a statement that an unpolarized quantum state has zero axial-current correlations.

Mass breaks exact chiral separation. Several massive, differently boosted polarized fields can still have timelike total A; there is no general massive no-bounce theorem here. The small-mass ODE experiment is a local classical continuity check, not a realistic massive matter state.

The exact acceleration lasts only Δln a=(ln2)/2≈0.347 after the turn. There is no demonstrated 50–60 e-fold inflation, finite cloud, exterior matching, ADM mass, black-hole interior or baby universe.
