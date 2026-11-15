# P05 — full covariance and conserving Gaussian dynamics

## Question and model boundary

Can a concrete initial quantum state and its local Hartree–Fock dynamics preserve Pauli occupation and energy before attempting a semiclassical bounce? We derive a regulated fixed-Minkowski Hamiltonian closure from the same minimal contact action. This is not an independent reproduction of a fully renormalized cosmological 2PI solution. Geometry remains a=1; no gravitational initial constraints or bounce are evolved.

Let R_k,αβ=⟨ψ†_kβ ψ_kα⟩ be the full equal-time covariance, including the filled negative-energy free reference. A physical Gaussian state has 0≤R_k≤I. Write C=∫(R_k−P⁻_k)d³k/(2π)³, with P⁻ the fixed free-vacuum projector. For Mᵃ=γ⁰γ⁵γᵃ,

Q(C)=Σ_a η_aa{[tr(MᵃC)]²−tr(MᵃCMᵃC)},
Σ(C)=δ(G_AQ)/δC=2G_AΣ_aη_aa{tr(MᵃC)Mᵃ−MᵃCMᵃ}.

This keeps both contractions. Six generic Hermitian matrix directions independently check the gradient against a central difference of the complete quartic functional. For the isotropic parity-even unpolarized Dirac sector C=(DI+Sγ⁰)/4, explicit matrices give

Q=−D²/2−S²,  Σ=−G_AD I−2G_ASγ⁰.

The full-covariance equation is iṘ_k=[h0,k+Σ,R_k]. Its Hermitian generator preserves each mode's eigenvalues, charge and Pauli properties exactly in continuum time. The energy functional is

ρ=∫tr[h0,k(R_k−P⁻_k)]d³k/(2π)³+G_AQ(C).

Its derivative vanishes by the commutator and variational self-energy. This is not an EOS or an externally imposed negative pressure.

## Explicit helicity representation and preparation

For helicity h=±1, h0=b_h·σ, b_h=(m,0,hp). Define

R_h=[(1+q)I+r_h·σ]/2,
r_vac,h=−b_h/E_p,
q=f+−f−,
r_thermal,h=−(1−f+−f−)b_h/E_p.

Eigenvalues are f+ and 1−f−; subtracting vacuum afterwards does **not** make C an occupation matrix. The predeclared state m=0.1M̄P, T=0.001M̄P, μ=m has charge D≈9.92383711e−8, scalar S≈9.75755278e−8 and positive free energy ≈1.00945783e−8 in M̄P units. Spectra agree with the FD occupations to 1.12e−16. Independent adaptive radial integrals agree with 48/96/192-node Gauss integration. Antiparticles are retained via the stable FD expression; their occupation is exponentially small here.

For an actual nonstationary test, rotate the **full** Bloch eigenvectors by θ_h(p)=h×0.05 exp[−(p/0.03M̄P)²] about σ₂. This preserves eigenvalues exactly and introduces charge-neutral particle–antiparticle coherence rather than changing occupation by hand. It preserves the declared parity/isotropic sector. The dynamics are

ṙ_h=2[b_h−2G_AS e₁]×r_h.

The scalar identity shift −G_AD affects phases, not the equal-time commutator. All three Bloch components at both helicities are evolved.

## Numerical validation and its limits

Proper-time interval 0≤t≤100 M̄P⁻¹, fixed cutoff Λ=0.1M̄P. RK4 with 64/128/256 steps is compared against independent DOP853 integration. Endpoint covariance error ratios are 15.9846 and 15.9970. At 256 steps the maximum occupation-eigenvalue drift is 2.59e−10; total energy drift is about 5.84e−14 of initial energy. Energy conservation alone would be inadequate: it is much less sensitive than the covariance endpoint error.

Independent high-accuracy time solves at 48/96/192 radial nodes give final S agreement below 1.6e−20. This is momentum quadrature convergence, **not spatial refinement or B6**. Cutoffs 0.08/0.10/0.12 give final S≈1.07710994/1.07677015/1.07682736 e−7. The cutoff dependence is resolved and larger than the quadrature error; it is not hidden as rounding or claimed removed by renormalization. A regulator-independent curved-space source still requires matching and counterterms.

`results/06_covariance_modes.json` preserves every initial/final Bloch mode, momentum, quadrature weight, charge-mode trace, reference projector, units and reconstruction formula. These specify the retained Gaussian covariance, not an exact interacting quantum state. A tangent variation independently checks conservation of the full energy functional.

Hartree–Fock factorizes the four-point function with exchange throughout; self-consistency does not compute a connected four-point cumulant or bound its error. We have not computed pressure under time-dependent metric variation, covariant subtraction, omitted diagrams, stress noise, or a bounce. The calculation validates the finite-cutoff matter dynamics in its precise scope and supplies the next falsification gate.
