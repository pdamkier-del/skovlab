# Minimal multi-field action: independent reconstruction

Units c=ℏ=1; κ=8πG=1/M̄P². Signature η=(-,+,+,+), {γᵃ,γᵇ}=-2ηᵃᵇ, ψ̄=ψ†γ⁰, γ⁵=-iγ⁰γ¹γ²γ³. Define Aᵃ=Σ_f ψ̄_f γ⁵γᵃψ_f. Coordinate/tetrad indices must not be interchanged. The independent Weyl matrices are in `code/field_source.py`; no old engine is imported.

## Eliminate the auxiliary connection before solving the fields

Start with e[ R̃/(2κ)+Σ_f (i/2)(ψ̄γD̃ψ−D̃ψ̄γψ)−Σ_f m_f ψ̄_fψ_f ]. Take W_abμ=e_aν∇̃_μe_bν and Ω_μ=−W_abμ[γᵃ,γᵇ]/8. With ε_0123=+1, parameterize the sourced totally antisymmetric torsion T_abc=−ε_abcd qᵈ/6. The unsourced irreducible pieces vanish by their algebraic equations. Up to the connection divergence,

R̃=R+q²/24, ΔL_D=−q·A/8,

L_aux=q²/(48κ)−q·A/8.

Hence q=3κA, T_abc=−κ ε_abcd Aᵈ/2 and

S_eff=∫e[R/(2κ)+Σ_f L_D,f−G_A A²],   G_A=3κ/16.

This sign follows both direct affine-curvature contraction and explicit spin-connection matrices for eight generic q and generic spinors (`01_independent_benchmark.json`). It agrees with the minimal limit in [Shaposhnikov et al., Eq. 2](https://arxiv.org/html/2008.11686v2). The old repository's literal geometric-sign presentation must be read with its later convention audit; it is not independent evidence for this calculation.

A²=Σ_f A_f²+2Σ_{f<g} A_f·A_g. **Keep every cross term.** Each pure chiral classical ray can have A_f²=0 while their sum is timelike. Removing the cross terms changes the action and destroys this benchmark.

## Equations and complete stress

With the Levi-Civita spin derivative D,

iγ^μD_μψ_f−m_fψ_f−2G_A A_aγ⁵γᵃψ_f=0,

G_μν=κT_μν,

T_μν=−(i/4)Σ_f[ψ̄_fγ_μD_νψ_f+ψ̄_fγ_νD_μψ_f−(D_νψ̄_f)γ_μψ_f−(D_μψ̄_f)γ_νψ_f]+G_A g_μν A².

The displayed stress is **on shell**. Its kinetic part already contains the nonlinear phase shift. Adding a fluid interaction term to the free kinetic stress double counts or miscounts it. We independently vary the off-shell diagonal-tetrad action with respect to lapse N and each a_i, holding ψ and its jets fixed, and only then insert the Dirac equation. This reproduces energy and all pressures, including a negative-frequency bounce point. A reduced on-shell action must not be varied instead.

Constraints on a spatially flat diagonal Bianchi I slice: H_xH_y+H_yH_z+H_zH_x=κE; homogeneous momentum constraints require T_0i=0. Off-diagonal spatial Einstein equations additionally require T_ij=0 for i≠j. Evolution is Ḣ_i=−ΘH_i+κ[P_i+(E−Σ_jP_j)/2], Θ=ΣH_i. Lapse=1, shift=0. Full Dirac sources are recomputed at every step.

The field equations imply ∇_μT^μν=0 and separate vector U(1) current conservation for each species. Numerical directional derivatives of E verify Ė+Σ_iH_i(E+P_i)=0 outside the exact isotropic trajectory. Constraints are monitored without projection. There is no effective-fluid replacement of the dynamical fields.
