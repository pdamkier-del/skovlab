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
