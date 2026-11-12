# Implementation readiness

**Decision: do not implement a spherical EC collapse prototype at this stage.** The selected ideal radial system is formally closed, but the requested physically justified high-density finite initial-boundary problem has not passed all six gates. The existing averaged FLRW simulator remains unchanged.

| Required gate | Status | Evidence / missing requirement |
|---|---|---|
| 1. Closed equations | **Conditional pass for coherent SO(3) ideal branch; fail for generic correlations** | Explicit metric, spin, conservation and constraint equations with a declared ordinary EOS. General retained correlations lack moment closure. |
| 2. Physically justified spin-fluid model | **Partial** | Established BHL/Obukhov–Korotky field formulation selected. Full original constrained action not independently reconstructed; dense-matter EOS, polarization preparation and validity scale unresolved. |
| 3. Viable initial-value formulation | **Partial locally; fail as requested collapse problem** | Explicit constrained initial data and continuum equations. No coupled gauge/free-boundary existence result or continuation through \(h=0\); generic low-spin dust already has nonreal material roots. |
| 4. Acceptable characteristics | **Fail for generic dust/bounce path; conditional local pass for positive-pressure low-spin patches** | Full reduced pencil derived. \(c^2<0\) on the dust low-spin branch; zero-speed defect; enthalpy singularity; superluminal negative-enthalpy branch for \(w<1\). Stiff exception separately documented. |
| 5. Consistent center and boundary | **Center conditions derived; finite boundary not established** | Coherent spin must be \(O(r)\). Stronger regular vacuum matching forces surface spin to zero; constant positive-\(w\) compact edge and general surface-layer problem remain unresolved. |
| 6. Independent checks | **Algebraic/analytical checks pass, with stated limits** | New principal-symbol, spin, center, mixed-component and full-curvature jump tests; prior geometry/constraint/FLRW/GR tests rerun. These do not prove microscopic validity or nonlinear well-posedness. |

A local causal ideal fluid patch is a legitimate restricted mathematical candidate. It is insufficient to justify a finite spinning-star collapse experiment continuing into torsion dominance. No favorable patch is advertised as a validated bounce solver.

## What could be simulated after the missing gates are met

Use the existing Stage 1 [PDE specification](../PDE_SPEC.md), augmented by this stage's **signed** spin variable, polarization/contact characteristics, center parity and full-connection interface checks. A selected GR dust benchmark remains a reference target; this task adds no GR or EC evolution solver.

For any accepted system record:

- Shell \(R,U\), neighboring material labels and particle-volume Jacobian; distinguish focusing, caustics and chart necks.
- Areal and volume extrema separately, with proper-time derivatives and refinement-confirmed continuation.
- Metric and torsionful curvature, spin/ordinary density, shear and expansion; a turning point alone is insufficient.
- Complete recollapse/oscillation extrema sequences with valid equations and boundary data throughout.
- Misner–Sharp mass, both null expansions, future trapping versus anti-trapping, constraint and pressure-work residuals.
- Local \(N_R=\ln(R/R_i)\), \(N_V=\frac13\ln(BR^2/B_iR_i^2)\), and accelerated-volume expansion only with an explicit shell proper clock.
- Metric/spin junction residuals. Until an exterior is constructed, report matching as **not computed**.

No interior-only experiment can establish an event horizon, a complete black-hole spacetime or a baby universe.

## Justified next research

Choose between a controlled microscopic spin kinetic/fluid completion and an explicit Einstein–Cartan–Dirac comparison. EC–Dirac fixes a different, axial spin current from an action; its algebraic torsion interaction does not change the Dirac principal cone. It still requires spinor/bilinear spherical compatibility, gravitational constraints, initial data, quantum-state interpretation and boundary analysis.

A paired spinor ansatz giving spherical stress must have its **total axial current** checked: cancellation can remove the classical torsion interaction. Zero mean quantum spin with nonzero correlations is a separate semiclassical problem. EC–Dirac is a justified investigation, not a promised bounce or an already approved solver.
