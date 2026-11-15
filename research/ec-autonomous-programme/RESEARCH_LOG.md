# Chronological research log

## 2026-11-15 — bootstrap and cycle 01

Checked main and all accessible repository branches. MASTER_STATUS.md, RESEARCH_LOG.md and NEXT_ACTION.md did not exist. Existing audit remains the prior verified assessment; no invented autonomous history is imported.

Priority: distinguish strong-curvature solver behavior from physical blow-up before searching for bounces. Derived a massless LRS solution in harmonic time with N=v, and evaluated it using the full existing tensor engine on a periodic torus. Added a compressed translation-invariant grid and cross-checked against the actual full 5³ grid. Corrected periodic charge quadrature (a diagnostic-only bug already proven by the audit).

Hypothesis: the engine approximates the exact collapsing branch with fourth-order time convergence up to v=1/8. Result: supported; metric/velocity ratios tend to 16, spinor ratios approach 16 from above. The exact solution has no volume turn and its invariants diverge only in the limiting collapse, not at the finite endpoint used. The finite run is regular. This is not a perturbative-stability test.

Artifacts: code/strong_benchmark.py; tests/test_strong_benchmark.py; results/cycle01_homogeneous.json. Analytical derivation and validation scope are in RESULTS.md and VALIDATION.md.

Decision: proceed to constraint-consistent spatial perturbations. Periodic boundaries remove an artificial outer edge but impose torus topology; do not describe this as a finite body or causally isolated asymptotically flat region.
