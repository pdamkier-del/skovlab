# Massive thermal gas: test of a low-temperature loophole

**Question:** Could the contact energy of cold fermions cancel a radiation background at a temperature well below the interaction scale, and thereby evade the relativistic Pauli obstruction?

Specify unpolarized free Dirac matter, μ=m, T≪m, plus photons; negligible antiparticles are suppressed by exp(−2m/T). Use the independently derived Q=−D²/2−S² and include ρ_f=2∫d³p E f/(2π)³≥mn, rather than only photons. The gas remains Pauli-compatible. No coherent particle-antiparticle condensate or non-Gaussian state is assumed.

At μ=m, n≈0.0972(mT)^(3/2), S≈D≈n. The contact scales as G_A m³T³ while photons scale as T⁴. Equating these two alone suggests T/m∼G_A m²≪1. But positive fermion rest energy scales as m^(5/2)T^(3/2), and dominates the radiation at that alleged turn by a factor of order (G_A m²)^(-5/2). Thus keeping radiation and discarding the very fermions producing the contact is inconsistent for this state.

A scaled, stable quadrature avoids subtracting nearly equal √(m²+p²) and m. Nine cold examples confirm the density scaling and positive energy. One deliberately false radiation-only balance uses fixed minimal G_A=3/16, m=0.1M̄P (G_Am²=0.001875). It occurs at T/m=4.03579e−5, where contact/radiation=1 to numerical precision. Including the fermions gives

ρ_f/ρ_radiation≈1.42739e10,
|Δρ|/(ρ_f+ρ_radiation)≈7.00582e−11.

There is no bounce at this point. This is a small controlled-state diagnostic, not a time-evolved solution and not a physical assertion about these photons equilibrating with neutral fermions. A product of specified thermal reference states suffices for the energy accounting test.

The stronger low-momentum inequality in `VALIDITY_AND_BOUNCE_BOUNDS.md` explains this result without choosing a temperature. It also shows why arbitrarily many unpolarized independent species cannot enhance an absent interspecies axial Hartree term. Out-of-equilibrium coherence, a different conserved charge or a connected four-point function can invalidate the free-gas closure; those cases are unresolved, not excluded.

Artifacts: `code/nonrelativistic_loophole.py`, `results/04_nonrelativistic_loophole.json`. This test is new; it does not repeat the older nonrelativistic cold-sea coefficient calculation.
