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
