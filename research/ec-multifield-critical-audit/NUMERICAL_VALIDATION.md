# Reproduction and numerical validation

From this directory, with Python 3 and NumPy, SciPy, SymPy installed:

```bash
OPENBLAS_NUM_THREADS=1 python code/verify_benchmark.py --output results/01_independent_benchmark.json
OPENBLAS_NUM_THREADS=1 python code/fermion_state.py --output results/02_fermion_state.json
OPENBLAS_NUM_THREADS=1 python code/robustness.py --output results/03_classical_robustness.json
OPENBLAS_NUM_THREADS=1 python code/additional_checks.py
MPLCONFIGDIR=/tmp/ec-mpl python code/plot_results.py
python code/validate_results.py
```

Scripts assert their algebraic/operator checks and write deterministic JSON, except wall-clock metadata. `results/environment.json` records versions. No external one-field solver or checkpoint is required. Full complex six-spinor amplitudes, three logarithmic scale factors and three H_i form 54 real ODE variables. Spatial derivatives are exact plane-wave derivatives; this is **not a spatial discretization or a 3D convergence test**. Proper-time lapse=1, shift=0, diagonal Bianchi I, periodic or cover boundaries as specified in `BOUNCE_ROBUSTNESS.md`. RK4 evolves the Einstein equations without constraint projection, clipping, or replacing the source with an equation of state.

Reference units κ=1, p=1, L=2π, n0=6/L³, a_b=0.06734517. Start at η=−a_b/q=−0.75 and end at +0.75 (t≈±0.05797377). Amplitudes are Pauli-normalized for the six distinct fundamental reference modes; the calculation is explicitly outside controlled physical EFT, not a physical simulation.

## Exact refinement

| Steps | Hamiltonian max / fixed ρ_b | Species-number max relative drift | Endpoint spinor norm error |
|---:|---:|---:|---:|
| 64 | 1.3162e−7 | 1.2460e−7 | 1.2254e−6 |
| 128 | 8.4629e−9 | 7.8244e−9 | 7.8769e−8 |
| 256 | 5.3623e−10 | approximately 4.9e−10 | 4.9940e−9 |

Spinor errors decrease by factors 15.56 and 15.77, consistent with fourth order. At 256 steps the volume turn is at t=1.14e−11, v=0.000305435404 and Ḣ_mean≈391.980584. The source trace R and geometric Kretschmann remain finite over this interval. R is computed using the Einstein trace, so is not an independent geometric-curvature check; K uses evolved H_i and their derivatives.

All five perturbations completed at both resolutions. At 256 steps the worst Hamiltonian residual / fixed ρ_b is 7.20e−10. Momentum and off-diagonal stress are zero or ≤2.4e−15 in these units. Turn volumes range from 0.000287473359 to 0.000305414567. Each has positive mean-H derivative; the coarse/fine event shifts are ≤2.1e−10 proper-time units. No global future or inhomogeneous claim follows.

The Hamiltonian residual uses the fixed positive reference radiation scale ρ_b≈1175.94, rather than dividing by total E which vanishes at the exact bounce. Independent finite directional differences of the complete energy give conservation residuals /ρ_b below 1.5e−10 at the finer difference step in tested initial states. Separate U(1) drifts, momentum and off-diagonal stress are recorded. Conditioning/symmetry/constraint stops would be reported inconclusive, not singularity or bounce evidence.

## Matched torsion-free control

Set the contact coefficient to zero in the action/source. Retain initial metric a_i, spinors, momenta and charges; **solve its own Hamiltonian constraint**. Initial H_ECD=−6.99982664 versus H_free=−9.89924977. Keeping the same H would violate one theory's constraints.

The separate isotropic massless control is exactly radiation, a²(t)=a_i²−2q(t−t_i). Its crunch is at Δt=0.0505088781. Integrating only 80% of that interval gives H_mean=−49.4962487, no bounce, K≈1.44046e8 and Hamiltonian residual / reference ρ_b=9.94e−9. Finite-time singularity follows from the analytical radiation solution, not from a solver failure or this finite endpoint. Initial total energies differ because these are different actions with separately consistent constraints.

The independent tests additionally verify generic auxiliary curvature/coupling, all benchmark field equations, off-shell stress variation including a bounce point, four-field tetrahedral isotropy, anisotropic paired sources, volume convexity, finite Fock/Wick agreement, and rejection of an unbalanced pair's momentum constraint. No general 3+1 Hamiltonian, harmonic-gauge or spatial-boundary verification is claimed.
