# Scalar–fermion interactions and complete effective stress

For the declared minimal symmetric Dirac action, expansion of the single eliminated square gives

L_eff=M²R/2−(∂φ)²/2−V+ΣL_D,f°−h(φ)∂_μφ A^μ−g(φ)A²,

h=√(3/8)/[M cosh X],
g=3/[16M²cosh²X].

All currents are total currents, so the contact includes interspecies cross terms. There is **one** contact term; no further EC term is appended. The classical field equations include

iγ^μD°_μψ_f−m_fψ_f−[h∂_μφ+2gA_μ]γ⁵γ^μψ_f=0,
□φ−V′+h∇_μA^μ−g′A²=0.

The h′ terms cancel in the scalar Euler equation. For homogeneous φ, φ̈+3Hφ̇+V′=h∇A−g′A². This is not a closed cosmological model until the actual fermion dynamics/state is supplied.

The complete on-shell effective Hilbert source is

T_μν=∂_μφ∂_νφ−g_μν[(∂φ)²/2+V]
+K_D,μν+h A_(μ∂_ν)φ+g g_μν A²,

where K_D,μν=−(i/4)Σψ̄[γ_μ↔D°_ν+γ_ν↔D°_μ]ψ and parentheses include 1/2. Dirac time derivatives in K_D already contain both interactions. The explicit h term cannot be dropped, nor may the free kinetic tensor be used unchanged. `fermion_stress.py` varies lapse and each scale factor **off shell**, holding field jets fixed, and only then substitutes the Dirac equation. Five generic massive field-jet tests confirm energy/pressure including the derivative coupling.

Total diffeomorphism conservation follows from the coupled scalar/Dirac equations; scalar and fermion stress need not be separately conserved. A massless anomaly-free axial current can make the h coupling a classical boundary/rephasing term, but g(φ)A² still contributes. Massive axial nonconservation permits pseudoscalar interactions and particle production. Quantum anomalies, normal ordering, state correlations and stress noise must be included before a semiclassical bounce claim.

## Explicit nonminimal extension and source comparison

If the action also has a declared trace source J=−(a_N V+ν_N A)/2, the same auxiliary elimination gives

L_4ψ=3[a_N²V²+2a_N(ν_N+Y)V·A+(ν_N²+2ν_NY−1)A²]/[16M²(1+Y²)],
L_der=√(3/8)∂_μφ/M{−sech X A^μ+tanh X(a_NV^μ+ν_NA^μ)},
Y=4B=sinh X.

These algebraic formulas follow from the specified +t·J source, not freely chosen pressures. `source_crosschecks.py` matches the **effective** 2024 Eq. (35)–(37) structure under its recorded orientation/current/field map. The microscopic trace-source sign dictionary back to that paper's Eq. (29) is not certified by that effective-formula algebra alone; no full nonminimal source-convention equivalence is claimed. The minimal sector and the declared J extension are independently fixed here.

The 2026 paper uses mostly-minus signature and a Dirac/Majorana normalization ζ=1/1/2. This audit uses canonically normalized Dirac fields, so Majorana factors must not be copied without the kinetic normalization. Local printed coefficient/dimension inconsistencies are recorded in `SOURCES.md` and result 06. They do not replace our derived interaction or constitute a refutation of the paper's phenomenology.

No specified renormalized fermion state, scattering hierarchy or covariant quantum stress has been solved in this new action. The source is exact at tree level in the stated classical action; identifying c-number spinors with physical occupied fermions is not assumed. For real B, g is no larger than minimal ECD, so scalar-dependent suppression alone does not rescue the previously uncontrolled minimal-contact quantum bounce estimates.

Additional action-level check: `nonminimal_source.py` directly varies the Hermitian 2024 Eq.27 spin term in all 24 connection directions, using gamma_p=−i gamma_here and the explicit row adjoint. It gives −q·A/8+t·(−alpha_p V+beta_N,p A)/2, fixing a_N=alpha_p and nu_N=−beta_N,p in our action. This agrees with the effective-formula map independently. Only the dictionary for its intermediate printed trace symbol in Eq.29 remains separate; the declared microscopic source is no longer inferred only from the effective polynomial. Result 07 preserves this distinction.
