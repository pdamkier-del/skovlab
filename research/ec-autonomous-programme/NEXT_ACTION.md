# Exact continuation after nine completed cycles

Branch codex/ec-autonomous-programme; current PR #2 remains stacked on the audit branch and is not merged into main. Read MASTER_STATUS.md and the end of RESEARCH_LOG.md. C01–C09 are complete. Do not repeat the old audits, exact reference branches, density sweeps or theta=.2 trajectories as new research.

## Available data

C08 contains15 raw NPZ checkpoints (29.3MB) and checkpoints/cycle08/index.json with whole-file SHA256 and Git blob IDs. They cover n9/17/33 spatial runs and the separate17³ temporal runs, at initial/midpoint/final times. All g,p,psi arrays are preserved. Use checkpoints.load_checkpoint() with hash/status validation; do not treat rejected states as restart data or replace raw fields by resampled comparisons.

C09 reads these fields without re-evolution and separately validates the material-current Raychaudhuri identity and effective Einstein-source replacement. Its geometric/source residuals improve with refinement; the final state is strongly focusing, with a well-conditioned current frame. The contact splitting is an on-shell same-state identity, not a torsion-free attribution.

## Highest-priority new experiment: one larger spin orientation

Hypothesis: the resolved focusing trajectory is or is not robust to a finite nonlinear change in orientation amplitude while density, species, action and wavelength remain fixed.

Predeclare exactly spin_amplitude=1.0, theta=sin(kx), k=2 pi/8, n_seed=4[1+.1 cos(kx)cos(ky)cos(kz)], L8,m0,kappa1. Do not scan until a desired bounce appears. The C07 source identities hold for arbitrary real theta/first jets; use them as regressions, not a new derivation. Do not add a scalar phase or complex spin rotation without deriving its extra momentum source.

1. Call spin_texture_data.construct(spin_amplitude=1.0) at9/17/33. Check all source projections, vector zero-mode compatibility, harmonic initialization, independent FD constraints and oversampled continuum residuals. Tighten nonlinear tolerance if it competes with truncation. Classify coarse alias error honestly. If33³ does not resolve the initial family, stop the dynamical inference and select a controlled refinement/reduction rather than assuming a successful Newton solve suffices.
2. Reuse spin_texture_evolution.run(spin_amplitude=1.0,...) in an explicit new driver or add a clear CLI amplitude parameter. Keep the original ECD equations, all complex components, guards, and source-provenance hashes. Start with t_end=.2, n9/17/33,40steps and separate17³20/40/80-step refinement. Store outputs as cycle10_* and checkpoints/cycle10; do not overwrite C08. Resolve constraints for every new state.
3. Persist raw initial/midpoint/final and safe rejected-state checkpoints. Record Git/raw/field hashes. Apply full-affine curvature probes at two diagnostic difference steps and the C09 geometric/source focusing balance to the new states. Current frames and material-volume signs must remain distinguishable from normal expansion, coordinate stops and numerical error.
4. Compare with C08 at matched density/charge and separately constrained geometry. Report field/expansion/volume differences against their convergence uncertainty. Harmonic-slice volume is slicing-dependent; a small difference is not a universal physical effect or a stability exponent.

Success can be convergent continued contraction, a resolved local turn, or an explicit numerical/model-domain stop. A candidate turn requires actual current-flow continuation and regularity through it; sampled sign changes or oscillating spinor phases do not establish a global bounce or physical oscillation. No counterfactual torsion attribution is justified without a separate constrained Einstein–Dirac comparison.

If longer evolution is the better next question after this test, restart from retained fields rather than repeating completed intervals, and retain code/parameter/time metadata. Full33³ runs cost several hundred seconds here; choose a controlled symmetry reduction only with a documented question and validation of its source/constraints.

Update all seven research records after each completed cycle, commit a meaningful milestone, and leave exact continuation parameters and unresolved failures. High-curvature classical torus calculations remain mathematical benchmarks, not controlled dense quantum fermion clouds or finite black-hole interiors.
