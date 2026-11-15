# Chronological research log

## 2026-11-15 — bootstrap and cycle 01

Checked main and all accessible repository branches. MASTER_STATUS.md, RESEARCH_LOG.md and NEXT_ACTION.md did not exist. Existing audit remains the prior verified assessment; no invented autonomous history is imported.

Priority: distinguish strong-curvature solver behavior from physical blow-up before searching for bounces. Derived a massless LRS solution in harmonic time with N=v, and evaluated it using the full existing tensor engine on a periodic torus. Added a compressed translation-invariant grid and cross-checked against the actual full 5³ grid. Corrected periodic charge quadrature (a diagnostic-only bug already proven by the audit).

Hypothesis: the engine approximates the exact collapsing branch with fourth-order time convergence up to v=1/8. Result: supported; metric/velocity ratios tend to 16, spinor ratios approach 16 from above. The exact solution has no volume turn and its invariants diverge only in the limiting collapse, not at the finite endpoint used. The finite run is regular. This is not a perturbative-stability test.

Artifacts: code/strong_benchmark.py; tests/test_strong_benchmark.py; results/cycle01_homogeneous.json. Analytical derivation and validation scope are in RESULTS.md and VALIDATION.md.

Decision: proceed to constraint-consistent spatial perturbations. Periodic boundaries remove an artificial outer edge but impose torus topology; do not describe this as a finite body or causally isolated asymptotically flat region.

## 2026-11-15 — cycle 02: continuum constrained periodic planar data

Solved the periodic positive conformal-factor BVP independently with SciPy solve_bvp (tolerance 1e-11; 961 adaptive nodes). Initial seed density is 4[1+.02 cos(2 pi z/8)], mass zero, real lower spinor component, constant positive mean curvature determined by the BVP. All momentum constraints and harmonic initial gauge hold to roundoff on sampled data. Hamiltonian residuals fall with independently chosen grid spacing. This is a 1+1 symmetry reduction of the full tensor equations, not unrestricted 3D.

Evolved to harmonic t=.45 at n=17,33,65,129, 240 RK steps. Final state RMS differences on shared physical points give observed spatial orders 1.98–2.00. Constraints improve consistently; charge drift remains about 5e-12. Neither normal nor current expansion becomes positive on the sampled evolution. This numerically supports continued contraction of this particular perturbed branch, not a universal no-bounce result.

A deliberately independent stress-divergence test exposed a diagnostic time-difference floor: at fixed dt its residual scarcely changes with spatial refinement. Separate dt refinement gives second-order reduction of that diagnostic, as expected for centered time differencing. A local directional derivative of full stress along the semidiscrete RHS provides a separate spatial-sensitive check, with its own delta dependence explicitly recorded. The metric-velocity temporal ratio 9.85 is below the asymptotic RK4 value and remains a limitation. No instability/singularity/oscillation is inferred from an error floor.

Validation: seven new research tests pass; the existing 16 full-field tests also pass after the periodic charge fix. The inhomogeneous compressed RHS and one RK step equal a lifted full 9³ calculation. Results/code: cycle02_planar.json and planar_contraction.py.

Decision: investigate finite perturbation amplitudes/modes and deeper contraction next; preserve the diagnostic-floor caveat and the absence of transverse stability evidence.
