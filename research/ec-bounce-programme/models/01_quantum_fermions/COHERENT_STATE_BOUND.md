# P07 — coherence does not evade the bound in this larger Gaussian sector

## Assumptions

One Dirac species; isotropic, parity-even Gaussian state, with full covariance 0≤R_h(p)≤I and arbitrary momentum-dependent charge-neutral particle–antiparticle coherence. Fixed physical cutoff p≤Λ. The vacuum reference is the free Minkowski projector at the same mass. The angular/helicity symmetries ensure C=(DI+Sγ⁰)/4, hence the Wick contact source Q=−D²/2−S². No non-Gaussian connected quartic, parity-breaking axial Hartree source, extra force or curved-space counterterm is included. The old occupation-only theorem did not cover this coherent sector.

## Proof without a small-coherence assumption

Use R=[(1+q)I+r·σ]/2. Pauli positivity gives |r|≤1−|q| and |q|≤1. Let n=b/E be the free unit Hamiltonian vector, δ=r+n and e=1+n·r. The negative-energy vacuum is r=−n. Then

q²≤|q|≤e,
|δ|²=|r|²+1+2n·r≤2e.

With the sum over helicities and measure dμ=d³p/(2π)³,

ρ_free=Σ_h∫dμ E e≥0,
D=Σ_h∫dμ q,
S=Σ_h∫dμ δ₁,
I=Σ_h∫dμ/E.

Weighted Cauchy–Schwarz therefore implies

D²≤Iρ_free,
S²≤2Iρ_free,
B=D²/2+S²≤(5/2)Iρ_free.

For two helicities,

I=[Λ√(Λ²+m²)−m² asinh(Λ/m)]/(2π²)≤Λ²/(2π²).

Thus

**G_AB/ρ_free≤(5/2)G_AI≤5G_AΛ²/(4π²)=15κΛ²/(64π²).**

This is a sufficient bound; sharpness is **not** claimed. It is independent of coherence amplitude and holds for every admissible covariance in the declared sector. At zero free excitation energy the same inequalities force D=S=0, so no division-by-zero exception supplies a finite negative source.

At m=Λ=0.1M̄P, the finite-mass bound is 0.0001265343. The predeclared coherent covariance has actual contact/free-energy fraction ≈2.08172e−7. Testing 1200 arbitrary admissible momentum-dependent covariances at m=0,0.1,0.5 independently verifies both mode inequalities and the integrated bound; adaptive integration checks I. These tests complement the analytical proof rather than replacing it.

## Interpretation

This extends the restricted negative result to a genuine coherent Gaussian sector. It closes the suggestion that adding an arbitrarily chosen small coherent pair rotation, while keeping this weak fixed-cutoff source, necessarily produces a bounce. It does not rely on equilibrium or adiabatic pressure.

If the same local source were the complete flat-FLRW energy up to remainder δρ, then (5/2)G_AI+|δρ|/ρ_free<1 would imply positive total energy and prevent H=0. We have not calculated that curved-space remainder. The theorem is a state/source bound in the declared reference scheme, not a proof that all cosmological quantum ECD sources are positive.

All-orders interactions, non-Gaussian cumulants, parity-breaking polarized multi-species states, dynamical vacuum polarization/curvature terms and controlled resummations remain outside this theorem. A large nonminimal coupling simply replaces G_A by its own coefficient in the bound; a smaller formal bounce scale is not an error estimate for the omitted physics.

Artifacts: `code/coherent_pauli_bound.py`, `results/08_coherent_pauli_bound.json`.
