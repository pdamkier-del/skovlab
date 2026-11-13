# Established results and remaining work

| Requirement | Status |
|---|---|
| Action, algebraic torsion, complete on-shell source | Existing audit retained; curved aligned-spinor substitution checked independently here. |
| General ADM constraints/evolution and normal-volume identity | Documented with fixed conventions; compact projections, not a full gauge-specific 3+1 numerical derivation. |
| Stable general 3+1 ECD evolution | **Not delivered.** Raw ADM is insufficient justification. |
| Inhomogeneous spin, arbitrary shear/tidal structure | **Not implemented.** Homogeneous LRS only. |
| Coupled reduced classical ECD evolution | Implemented and benchmarked against exact volume solution. |
| Constraint-solving initial data | Algebraic in LRS only; no general elliptic field-data solver. |
| Bounded cloud and exterior | **Not delivered.** Periodic/cell homogeneous geometry has no exterior. |
| Volume bounce | Analytically excluded for implemented positive-density branch; no universal ECD no-bounce theorem. |
| Regularity | Finite Levi–Civita curvature over accepted numerical interval; no global extension or full torsionful curvature invariant check. |
| Quantum/many-body validity | No quantum fermion gas, QCD, degeneracy or SM interactions included. Classical field applicability unresolved. |
| Existing FLRW / stable URL | Preserved; separate nested static app. |

## What is needed for the requested full collapse experiment

1. Choose and derive a strongly hyperbolic gravitational evolution with compatible tetrad rotation gauge; couple all spinor components and the full Hilbert source. Verify characteristics and conservation, including first-order/reduction constraints if introduced.
2. Build smooth compact classical spinor initial fields and solve the Einstein Hamiltonian/momentum constraints on an asymptotically flat slice. Establish existence for the selected family, convergence and the actual ADM mass rather than accepting arbitrary mass/radius/speed triples.
3. Derive constraint-preserving outer gravitational boundaries, causal spinor treatment, vacuum radiation and consistent finite-domain errors. Test long-time nonlinear stability and spatial/time convergence; ODE convergence is not PDE convergence.
4. Track the full field stress, current frame where timelike, local normal expansion, followed matter volumes, tidal curvature, full torsionful regularity and loss of validity. General tilted matter needs a declared volume/time prescription. No automatic spherical shell mass or coordinate-radius proxy is valid.
5. Construct and validate the exterior transition, then test trapped surfaces with the appropriate general spatial surface machinery; event horizons require global causal analysis.

## Vacuum matching audit

Minimal algebraic EC has $T_{abc}=\kappa\epsilon_{abcd}J_5^d/2$. In an open source-free region $\psi=0$ its classical stress and torsion vanish, leaving $G_{\mu\nu}=0$. This exterior can have Weyl curvature and gravitational waves and need not be Schwarzschild. Smooth compact classical initial fields and a regular causal hyperbolic solution provide a plausible local support construction, but they do not solve the gravitational constraints or prove a global matched spacetime.

For a non-null interface without a metric surface layer, continuity of induced metric and Levi–Civita extrinsic curvature plus the appropriate traction/flux conditions is necessary. Smoothly vanishing spinors in an open collar also remove contortion jumps; arbitrary discontinuous torsion or a reflecting artificial matter wall does not establish action-consistent matching. Null fronts need their own junction formalism. The previous [vacuum audit](../ec-two-matter-models/VACUUM_MATCHING.md) details the stronger full-curvature jump condition and quantum qualifications. None is implemented by truncating a Bianchi I cell.

These gaps are specific missing deliverables, not evidence that inhomogeneous ECD collapse is impossible or that torsion invariably reverses it.
