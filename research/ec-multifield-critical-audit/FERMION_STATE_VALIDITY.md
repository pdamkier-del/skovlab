# Fermion-state and effective-theory audit

## Classical field versus fermion state

An ordinary commuting spinor amplitude is not an arbitrarily occupied fermionic coherent state. Fermion parity normally gives ⟨ψ⟩=0; even bilinears and their fluctuations carry the physical data. Six independent classical fields may represent six species or an approximation to several modes, but those interpretations have different exchange terms. The total-current square is a composite operator: ⟨A²⟩ is not generally ⟨A⟩². A quantum calculation must specify the state, normal ordering/renormalization, masses, species, vacuum, and evolution of correlations.

We evaluated an explicitly normal-ordered reference-state operator, not just a c-number factorization. Jordan–Wigner matrices for six fermionic modes (64-dimensional Fock space) and an independent Wick trace agree exactly. For a filled six-mode reference state with nV=6:

| Interpretation | V²⟨:A²:⟩ | Classical total-current estimate |
|---|---:|---:|
| Six distinguishable chiral species, one mode each | −36 | −36 |
| Six momentum modes of one Weyl species | −72 | −36 |

Thus quantization does **not** automatically remove a negative contact energy. It also does not validate the classical evolution. Same-species exchange doubles this particular coefficient; treating six modes as six distinguishable species is a material assumption. These finite reference-state expectations omit the other momentum modes produced by scattering and do not establish an interacting eigenstate, a closed quantum truncation, curved-space renormalized stress or small stress fluctuations. See `code/fermion_state.py` and `02_fermion_state.json`.

## Pauli normalization exposes the scale problem

For the literal six fundamental modes on a cubic torus of comoving side L, p=2π/L and each species occupation f≤1. Then n0=6f/L³. The classical formula gives

ρ_b=p³/(G_A² n0)≥1024π³/(27κ²)=1175.94175 M̄P⁴,

p_b=p/a_b≥(8π^(3/2)/3) M̄P=14.84887 M̄P,

G_A p_b²≥4π³/3=41.34170,
R_b≥2351.88351 M̄P².

Lower f raises the required scales. Rescaling L does not lower these physical thresholds. Taking arbitrarily large classical n0 for those same six modes would violate their proposed occupations. These bounds apply to this normalization and state interpretation; they are not universal no-bounce theorems for every correlated state.

As a second reference estimate, six equal isotropic free chiral Fermi seas have n=g p_F³/(6π²), ρ0=g p_F⁴/(8π²), and Hartree plus same-species exchange gives ⟨:A²:⟩=−C n² with C=1+1/g=7/6. Therefore |Δρ|/ρ0=gCκp_F²/(24π²). Formal equality requires p_F≈5.8171 M̄P; at p_F=0.1 M̄P the correction is only 2.9552×10⁻⁴. Extrapolating this weak-coupling reference estimate to equality is uncontrolled. Large species changes gravitational cutoff assumptions and is not a demonstrated rescue.

Minimal torsion elimination produces a dimension-six contact interaction. Higher-curvature and other higher-dimension operators, quantum gravity, vacuum polarization and backreaction cannot be assumed negligible at the displayed momenta and curvature. No ultraviolet completion or controlled cancellation is supplied. The exact background's smoothness does not establish effective-theory validity. Quantum-state fluctuations, Casimir terms on a small torus, conformal anomaly and renormalization counterterms remain uncomputed. Missing gauge interactions and the actual chiral/massive Standard Model species prevent identifying this model with realistic collapsing matter.

## Four distinct claims

A. **Exact classical solution:** supported by independent equations, action variation and convergence.

B. **Plausible semiclassical state:** negative contact expectation is possible in specified free reference states, but a state whose renormalized stress tracks the full bounce with controlled fluctuations has not been constructed.

C. **Controlled dense-matter effective theory:** not established; both the six-mode normalization and free Fermi-sea estimate put formal cancellation beyond their controlled regime.

D. **Realistic collapse:** unestablished. No finite cloud, realistic forces, collapse constraints, exterior or quantum-state evolution is supplied.

This audit rejects a claim of demonstrated physical bounce, not every conceivable ultraviolet completion. Relevant distinctions about averaging are discussed by [Dolan](https://arxiv.org/html/0911.1636v2); its model assumptions are not used as a substitute for our operator calculation. Published [Fermi-bounce models](https://arxiv.org/abs/1402.5880) include nonminimal ingredients and cannot validate the fixed minimal action here.
