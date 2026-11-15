# Validation record

Cycle 01 commands from repository root:

```sh
python research/ec-autonomous-programme/code/strong_benchmark.py --output research/ec-autonomous-programme/results/cycle01_homogeneous.json
python -m unittest discover -s research/ec-autonomous-programme/tests -v
python -m unittest discover -s research/ec-full-3plus1/tests -v
```

Dependencies: existing ec-full-3plus1 NumPy/SciPy requirements; existing SymPy for older analytical suites. C01 JSON records actual Python/NumPy versions. No new dependency is needed.

Checks: exact-field temporal derivatives against full RHS; Hamiltonian, all momentum and harmonic constraints; metric Riemann contractions against independent LRS invariant formula; periodic charge; RK4 refinement 20/40/80/160 steps; compressed and full 5³ grid cross-check. All timesteps respect the engine's conservative characteristic bound in this test.

Limits: spatial derivatives vanish in C01, so there is no spatial-convergence or nonsymmetric stability evidence. Riemann time-second derivatives use the evolved metric RHS; comparison against exact analytic curvature tests its value, but is not an independent off-shell Einstein residual. Direct effective-stress divergence on evolved spatially varying data remains a next-cycle requirement. Full torsionful Riemann invariants are not computed by this metric-curvature routine.

## Cycle 02 reproduction and caveats

```sh
python research/ec-autonomous-programme/code/planar_contraction.py --output research/ec-autonomous-programme/results/cycle02_planar.json
```

Expected data family: n0=4, epsilon=.02, periodic length8, mode1, m=0, kappa=1, duration .45. Spatial runs use n=17,33,65,129 at 240 steps; temporal runs use n=65 and 60/120/240 steps. All pass the conservative timestep check. Comparisons Fourier-resample the smooth final fields onto 65 common physical positions; this interpolation does not evolve the solution and should not be confused with a spectral evolution method. Refinement orders account for the unequal spacing ratios of odd grids.

Seven research tests pass. Existing 16 full-field tests pass. Full 9³ spatially varying RHS/RK lift differences are zero at printed precision. Scalar BVP constraints are checked using independent finite differences; momentum and gauge constraints are checked through the full tensors.

The temporal state ratios are 16.10 (metric), 9.85 (metric velocity), 16.64 (spinor). The second ratio is not clean asymptotic fourth-order evidence. Centered evolved-snapshot stress divergence is assessed at the same final physical time with an extra diagnostic-only RK step; its relative error is dominated by O(dt²) time differencing (about 4.22e-5 at 240 steps). A tangent-state directional derivative is recorded separately for deltas 1e-5 and 5e-6, exposing its own truncation/roundoff sensitivity. Do not infer a spatial conservation failure from the fixed-dt floor, or exact conservation from a local operator identity.

Run-level results include endpoint metric curvature and algebraic torsion contraction, current timelike checks, all constraints, charge, normal/current expansion and CFL ratios. No convergent material trajectory/finite-volume bounce event or long-time oscillation is claimed.

## Cycle 03 reproduction

```sh
python research/ec-autonomous-programme/code/perturbation_sweep.py --output research/ec-autonomous-programme/results/cycle03_perturbations.json
```

12 spatial runs: epsilon=.1/.3, mode1/4, n=65/129/257, t_end=.8, 400 steps. Three separate time runs at n=129, epsilon=.3, mode4, 200/400/800 steps. The driver checkpoints after each completed seed family. Errors, stop reasons, BVP parameters, density contrasts, curvature, gauge/current/stress diagnostics and CFL ratios are stored; no visual classification of a curve is used.

Acceptance is refinement and an observable separated from zero, not a coarse run merely finishing. The strongest n65 case reaches .0123 Hamiltonian relative error and is only coarse evidence. Its finest error is .000811. No sampled current/normal turn is found; this says nothing about unsampled modes, transverse perturbations or unlimited evolution. All numeric states used the same action and the same existing RK engine without damping or altered matter forces.

## Cycle 04 reproduction

```sh
python research/ec-autonomous-programme/code/periodic_3d_data.py --output research/ec-autonomous-programme/results/cycle04_3d_initial.json
```

Grid sizes 9³,17³,33³; n0=4, epsilon=.1, length8, mass0, kappa1. The vector/scalar solve uses Fourier derivatives; the field engine checks independent second-order FD constraints. Evaluate scalar continuum residuals on 19³/35³/67³ oversampling grids. The latter higher grids are scalar-only validation and do not imply a full tensor evolution at those resolutions.

17³ tolerances 1e-9/1e-11/1e-12 give K values agreeing within 1e-12. The tightest spectral nonlinear residual is 2.22e-15, while FD relative Hamiltonian remains .00169023514. This explicitly rules out elliptic tolerance as the dominant observed FD error in this case. On 33³, energy-source formula agrees within 4.45e-15; initial gauge within 4.45e-16.

Ten programme tests pass, including arbitrary-jet source scaling, uniform limit, positivity/input rejection, nonzero three-axis variation, oversampling and independent constraint refinement. A spectral return flag alone is not the validation.

## Cycle 05 reproduction

```sh
python research/ec-autonomous-programme/code/full_3d_contraction.py --output research/ec-autonomous-programme/results/cycle05_full3d.json
```

Spatial runs: n=9,17,33, duration .2, 40 steps. Separate same-grid n17 temporal test: 20/40/80 steps; the 40-step result is reused rather than recomputed. Final fields are resampled to 17³ common physical points only for comparison; evolution remains second-order FD in the original engine. Data files are checkpointed after each resolution.

All runs finish within their declared lapse, spacelike-metric, current-frame, CFL and 5%-constraint controls. Passing a 5% stop is not the accuracy criterion: independent refinement is the evidence. Charge drift is below 3e-10 across these runs but is nonmonotonic with spatial resolution. Source divergence uses evolved snapshots at the same final time, plus the separate tangent diagnostic; fixed-dt floors remain visible. Metric time-second jets in curvature come from the RHS, so the curvature trace check is not an independent off-shell Einstein test.

No browser/frontend tests were rerun; the weak-field public API limits are not raised. Strong-curvature research drivers bypass those operational frontend restrictions without changing the physical equations.

## Cycle 06 and final reproducibility

```sh
python -m pip install -r research/ec-autonomous-programme/requirements.txt
python research/ec-autonomous-programme/code/check_torsion_symbolic.py --output research/ec-autonomous-programme/results/cycle06_symbolic.json
python research/ec-autonomous-programme/code/torsion_curvature.py --output research/ec-autonomous-programme/results/cycle06_torsion_curvature.json
python -m unittest discover -s research/ec-autonomous-programme/tests -v
# Optional figure:
python -m pip install -r research/ec-autonomous-programme/requirements-plot.txt
python research/ec-autonomous-programme/code/plot_validation.py
```

The 13 new tests cover arbitrary-jet spin momentum, periodic scalar/vector data, independent FD/oversampled constraints, full-grid lifts, exact harmonic RHS/invariants, time refinement, charge quadrature, every independent reference affine-connection component, symbolic full curvature and O(delta²) cancellation error. The existing 16 full-field tests also passed after the sole production-file edit. These 29 relevant tests are the current session's unit/regression executions; the earlier audit's larger test inventory was not all rerun.

Full-affine numerical probes use delta=.001/.0005/.00025 on exact volumes1/.5/.125, plus delta=.0001/.00005 on 9³/17³/33³ constrained initial data. The symbolic checker imports only SymPy and the standard library. Numerical full Riemann lacks the usual torsion-free pair-exchange symmetries, so its contractions are formed without assuming them. Full scalar residual and full-K error both decrease by about four under delta halving on the exact branch. Small nonzero full-scalar residuals are truncation error, not a new physical stress.

The figure in figures/validation.svg is generated solely from committed JSON. It displays exact-reference temporal error, independent 3D constraint refinement and mode-dependent contrast response. The plot does not present a physical bounce or stability theorem.

Remaining evidence gap: full torsion curvature has not been measured throughout the evolved C05 trajectory. Complete endpoint fields were not saved in C05; its JSON contains diagnostics and common-grid state differences only. Future runs must add full NPZ checkpoint/output persistence before expensive extension, recording data/coordinate/matter validity stops separately. No plot or unit test compensates for that missing record.

## Cycle 07 reproduction

```sh
python research/ec-autonomous-programme/code/spin_texture_source.py --output research/ec-autonomous-programme/results/cycle07_source_symbolic.json
python research/ec-autonomous-programme/code/spin_texture_data.py --output research/ec-autonomous-programme/results/cycle07_spin_data.json
python -m unittest discover -s research/ec-autonomous-programme/tests -v
```

Source derivation uses SymPy only, fixed negative-Clifford conventions, arbitrary real first density/angle jets and arbitrary symmetric K. Numerical tests cover the independent conformal momentum scaling, all spatial stress components, theta=0 recovery, grid refinement, exact checkpoint/restart equivalence, corrupted field rejection and rejection-state access policy. Eighteen programme tests passed in this session; the earlier 16 engine tests were not rerun because no production engine code changed.

The 33³ initial energy/stress/axial formula errors are below 7e-15, scalar spectral residual 6.03e-12, vector spectral residual 6.03e-15, and oversampled scalar residual 4.87e-11. Initial FD relative Hamiltonian=.0004529730 and momentum max=.0002552764. Their finite values, rather than elliptic-solver tolerance, must be accounted for in the next evolution. The coarse oversampling error is 1.47e-5 and is not presented as continuum constraint satisfaction at machine precision.

Full checkpoint format is skovlab-ecd-fields-v1, allow_pickle=False, with g/p/psi arrays, units/grid/time/config/status metadata and SHA256 hashes. Rejected states cannot silently become restart data. The small smoke run tested this path but is not part of the scientific convergence evidence.

## Cycle 08 reproduction and raw data

```sh
python research/ec-autonomous-programme/code/spin_texture_evolution.py --output research/ec-autonomous-programme/results/cycle08_spin_evolution.json --checkpoints research/ec-autonomous-programme/checkpoints/cycle08
```

Three spatial runs at9³/17³/33³ and separate17³ time refinement use the unchanged original RK engine. Initial/midpoint/final checkpoints include full arrays, metadata, code SHA256 fingerprints, parameter/runtime versions, status and per-field hashes. Finite rejected states and the last accepted state are retained on a guard exit; no exit occurred in the reported scientific runs. A separate tiny smoke run tested the checkpoint/full-curvature integration path before expensive evolution.

Fifteen raw NPZ files are committed as binary blobs (29.3MB total). checkpoints/cycle08/index.json records relative paths, byte counts, SHA256 and Git blob SHA; cycle08_spin_evolution.json references each checkpoint. Publication added blob IDs after execution, without changing fields. Git checkout or the Git blob API can retrieve these exact binary files; raw-content tools restricted to UTF-8 should not reinterpret the NPZ as text. load_checkpoint() uses allow_pickle=False and validates each field hash and status.

Full torsionful curvature probes at t=0,.1,.2 use delta1e-4/5e-5 on reloaded fields. Spatial and diagnostic-step errors remain separate. Current/normal expansion and constraints are sampled every timestep. Stress divergence still has its documented centered-time diagnostic floor. No browser tests or new physical interactions were introduced.
