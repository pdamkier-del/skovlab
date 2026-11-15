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

## 2026-11-15 — cycle 03: finite planar amplitudes and shorter wavelengths

Used the same independent periodic continuum BVP for epsilon=.1,.3 and mode1,4. Evolved each on 65/129/257 periodic z nodes to t=.8 with 400 RK steps. All timesteps satisfy the declared characteristic bound and lapse remains above .05. The finest-volume ratio is .09120,.09525,.09090,.09229 respectively. All sampled current and normal expansions stay negative. This excludes a resolved local volume turn only within these sampled, convergent finite-interval families, not generally or at later times.

RMS spatial orders are 1.94–2.03. A separate worst-seed (epsilon=.3,mode4) n=129 time sequence 200/400/800 steps gives ratios 16.074,16.059,15.817. This supplies clean temporal evidence for that case; it does not erase the earlier C02 cancellation/ratio limitation.

Density contrast grows by about 1.93 and 1.85 for the low mode, but changes by .970 and .902 for the higher mode. Thus “all perturbations decay” is falsified as a description of this observable over the tested interval, while continued contraction is numerically supported. No asymptotic instability rate or general stability classification follows from four finite cases. The coarse strongest run has Hamiltonian error .0123; finest error .000811 and refinement, rather than its coarse output alone, is the evidence.

Artifact: results/cycle03_perturbations.json and code/perturbation_sweep.py. Next priority is genuinely three-dimensional constrained data, since the planar lift cannot test transverse physics.

## 2026-11-15 — cycle 04: a full three-coordinate periodic constraint family

Highest unresolved obstruction after the planar tests was the absence of periodic high-curvature data with genuine transverse dependence. Derived the momentum-curl and energy identities for a real polarized conformal seed; verified the momentum identity for independent arbitrary first metric/spinor jets and checked the full source on the constructed data.

For n_seed=4[1+.1 cos(kx)cos(ky)cos(kz)], solved the zero-mean vector elliptic problem spectrally, then the scalar Hamiltonian with positive chi and unknown CMC K. Gauge initialization uses the existing full harmonic routine. Scalar residual is also evaluated on an oversampled grid; this avoids presenting a small monitored collocation residual as sufficient continuum evidence.

9³/17³/33³ independent FD Hamiltonian maxima are .0355067/.0104393/.00280839; momentum maxima .00046010/.00014408/.000039155. The 33³ oversampled scalar residual is 4.91e-11. Initial gauge is near roundoff. Tightening the 17³ scalar solve to 1e-12 reduces its nonlinear residual to 2.22e-15 without changing the finite-difference truncation error. Numerical initial-data existence is supported for this seed family, not proved for arbitrary data or for a finite isolated body.

Artifacts: code/periodic_3d_data.py, tests/test_periodic_3d.py, results/cycle04_3d_initial.json. Ten research tests pass. Decision: proceed to actual full 3D evolution of the same data, rather than identifying a planar lift with transverse stability.

## 2026-11-15 — cycle 05: actual full-grid three-dimensional evolution

Evolved the C04 data using the existing general 3+1 RHS and RK4, not the compressed planar adapter. Grid sizes 9³,17³,33³, harmonic duration .2, 40 time steps. Every-step current frame, constraints, lapse, positive spatial metric, charge and normal/current expansion were monitored. Explicit 5% relative-Hamiltonian and lapse .1 stops were not reached; timesteps obey the characteristic bound.

Spatial state orders are 1.9464,1.9204,1.9629. A separate 17³ 20/40/80-step sequence gives ratios 14.8297,17.2460,16.5839. The finest endpoint has relative Hamiltonian .00038310, slice-volume ratio .54890902 and metric R between -20.55495 and -19.08540. No sampled local normal/material turn occurs. Charge drift is small but not monotonically ordered by resolution; no spatial charge-convergence claim is made. Evolved stress divergence retains the documented centered-time diagnostic floor.

The full 33³ run took 316.9 seconds; continuing much deeper at comparable validation cost is a substantive computational task. This short result is a validated nonlinear trajectory for one high-curvature three-coordinate family, not arbitrary-perturbation stability. It establishes neither a finite body nor oscillations. Artifacts: code/full_3d_contraction.py and results/cycle05_full3d.json.

Decision: strengthen the regularity diagnostics by testing full torsionful Riemann contractions, rather than calling finite metric invariants or a vanishing full scalar a complete regularity check.

## 2026-11-15 — cycle 06: independent full-affine curvature validation

The remaining regularity gap was that metric invariants and the algebraic torsion norm do not themselves monitor the full torsionful Riemann tensor. Implemented Gamma_tilde=Gamma_LC+C from corrected T_abc=-epsilon_abcd A^d/2 at kappa1, transforming with the same frame/coframe. Time derivatives of the full connection are centered differences along the actual state RHS; spatial derivatives use the declared FD operator. No field equations were changed.

Independently specified the exact isotropic connection for n0=4,D0=0,m=0 and contracted it symbolically without importing the numerical engine. Result: full R=0, full K=128 exp(12t)=128/v⁴. The direct geometric numerical connection matches every reference component. Difference steps .001/.0005/.00025 give approximately factor-four reduction of full-scalar cancellation error and full-K error. At v=.125 the exact full K is 524288; the smallest-step relative K error is 1.44e-6.

Also evaluated C04 spatial initial data with n=9,17,33 and delta1e-4/5e-5. The 33³ full-scalar range at the smaller delta is [-.00274887,.00217763], decreasing under grid refinement toward the massless zero-scalar identity. Full K range is approximately [121.20046,133.18594]. These checks are at the initial slice, not a post hoc claim about all evolved C05 points. Finite Lorentzian contractions alone are not a global regularity theorem.

Artifacts: torsion_curvature.py, check_torsion_symbolic.py, cycle06_torsion_curvature.json, cycle06_symbolic.json, and independent connection/symbolic tests. Thirteen programme tests pass; the existing 16 full-field tests passed after the only production change (periodic diagnostic quadrature). Added reproducible requirements and a standalone SVG summarizing the recorded convergence/perturbation evidence.

Decision at execution handoff: preserve six validated cycles and their boundaries. The next distinct question is spin-orientation perturbations of constrained 3D data, not more fixed-polarization density scans. A genuine bounce or oscillation question still requires a new admissible state family, full diagnostics through a turn, matched-action constraints and long-time convergence.
