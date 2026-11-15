# Coincident axial correlator, including antiparticles and exchange

Define the normal one-body matrix (C_i)_αβ=⟨:χ†_iβχ_iα:⟩. For isotropic independent massless Weyl channels C_i=(d_i/2)I₂. Particles enter with +f+ and antiparticles with −f−. It is a vacuum-subtracted matrix and need not be positive.

For the bilinear matrices M_iᵃ, the quartic Gaussian Wick polynomial is

⟨Q⟩=Σ_a η_aa{[Σ_i tr(M_iᵃ C_i)]²−Σ_i tr(M_iᵃ C_i M_iᵃ C_i)}.

In a Weyl basis M⁰=−s_iI₂ and M^j=σ_j (the spatial signs do not affect the contraction). Pauli traces give

**⟨Q⟩=−[(Σ_i s_i d_i)²+Σ_i d_i²]≡−B.**

The first square is Hartree and includes all interchannel terms. The sum of squares is the exchange contribution. It is not obtained by squaring a mean axial current.

Consequences:

- An unpolarized Dirac gas has two channels with d_R=d_L=D/2. Its mean axial current vanishes, but ⟨Q⟩=−D²/2.
- For equal same-chirality charge-asymmetric seas, B=g(g+1)d². The previous six-species sea is a special case, not repeated here as a new discovery.
- A massless charge-symmetric thermal gas has every d_i=0, so this **order-G vacuum-Wick expectation vanishes**, even though n_total and free energy are nonzero. This does not remove fluctuations, higher-order thermal interactions, mass corrections or general curved-space effects.

## Independent operator verification

`code/finite_fock.py` constructs a 256-dimensional Fock space of two Weyl channels, each with two particle and two antiparticle modes. The local ± momentum spinors form an orthonormal spin pair. It retains all pair-creation/annihilation terms and vacuum-normal-orders each quartic word before multiplying sparse matrices. It checks the canonical anticommutators and Hermiticity independently.

Seventeen product-occupation ensembles, including charge-symmetric, opposite-chirality and random occupations, agree with the coincident Wick trace to maximum absolute error 3.56e−15. A symmetric occupation 0.3 for all particle/antiparticle modes gives ⟨Q⟩≈0 and finite-mode Var(Q)=192 in the chosen mode/volume units; the vacuum also has nonzero noise. This is an operator check, not a closed eight-mode scattering theory or a continuum noise calculation.

## Massive unpolarized check

Independently constructed 4×4 SymPy gamma matrices give C=(DI₄+Sγ⁰)/4 after isotropic momentum integration. The same full Wick trace yields

**⟨Q⟩=−D²/2−S²** per independent unpolarized Dirac species. Interspecies axial Hartree terms vanish for this particular state; exchange is species-diagonal. At m→0, S→0 and the Dirac massless expression is recovered. At nonrelativistic particle dominance S≈D≈n, it tends to −3n²/2, consistent with the earlier restricted cold-sea calculation. The new result includes the thermal/antiparticle dependence rather than replacing this limit by a universal density law.

A relevant independent microscopic comparison is [Diakonov, Tumanov and Vladimirov, Sec. VIII](https://arxiv.org/html/1104.2432): they retain direct/exchange terms, distinguish charge from total density, and derive stress by variation of the averaged action. Their signature and vertex normalizations must be converted before comparing numerical coefficients. Our formulas above are derived and tested in this programme's conventions.
