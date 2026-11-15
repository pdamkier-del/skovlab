# Stress, ensembles and conservation at first order

A fixed free-state expectation and an equilibrium state at fixed temperature/chemical potentials are not the same comparison. This matters for both sign and equation of state.

For the specified massless gas Q=−B, the first interaction contribution to the grand potential is Ω1/V=⟨H_int⟩0/V=−G_A B. Thus

P(T,μ_i)=P0+G_A B+O(G_A²),
ρ(T,μ_i)=3P0+5G_A B+O(G_A²).

B is homogeneous of degree six in T and all μ_i. Applying ρ=−P+T∂_TP+Σμ_i∂_μiP gives the factor five. Holding the *free* occupations fixed while using this grand-canonical energy would be inconsistent.

At fixed **physical entropy and charge densities**, T and μ_i shift at order G_A. A Legendre transform, or equivalently susceptibility-matrix inversion, instead gives

ρ(s,d_i)=ρ0(s,d_i)−G_A B(d_i)+O(G_A²),
P(s,d_i)=ρ0(s,d_i)/3−G_A B(d_i)+O(G_A²).

`stress_and_mass.py` verifies both corrections symbolically for equally populated channels at arbitrary finite T and μ using the full 2×2 thermodynamic susceptibility matrix. The general result also follows from degree-four homogeneity of P0 and degree-six homogeneity of B. Both ensembles have the same trace correction −ρ+3P=−2G_A B; there is no physical sign contradiction.

On an assumed adiabatic homogeneous fluid trajectory, s,d_i∝a⁻³; the free massless energy is C_r a⁻⁴ and B=B0 a⁻⁶. Hence

ρ=C_r/a⁴−G_A B0/a⁶,
P=C_r/(3a⁴)−G_A B0/a⁶,
a dρ/da+3(ρ+P)=0.

The last identity is independently checked symbolically. It is an order-G conserved equilibrium closure, not a solved nonequilibrium quantum backreaction. Free conformal transport can preserve a free thermal spectrum, but collisions, relaxation, interaction-induced correlations, anomalies and higher orders must be controlled before continuing this closure to a bounce.

If extrapolated, flat FLRW would turn at r=G_AB/ρ0=1, with Ḣ=κρ0/3>0. This is a **formal** solution of the truncated source, not an accepted quantum-state solution. At fixed entropy-per-charge ratios its formal acoustic response is

c_s²=(4/9−2r)/(4/3−2r).

The numerator changes sign at r=2/9 and enthalpy vanishes at r=2/3, before the formal r=1 turn. This flags another reason not to certify robustness from a homogeneous negative-stiff-fluid equation. Because these corrections are no longer parametrically small, it is not a controlled proof that exact quantum ECD has this gradient instability. A real perturbation assessment must use the microscopic dynamical source in its validity region.

No new cosmological evolution is run: the validity gate fails before a controlled bounce source is available. A torsion-free order-G control is obtained by G_A=0 in the same potential and separately imposing H²=κρ0/3 on flat data. It has positive radiation energy/pressure and Ḣ=−2κρ0/3, so a contracting branch cannot turn. We do not reuse an interacting H that violates that constraint. The earlier classical torsion-free trajectory is provenance, not evidence for quantum closure.
