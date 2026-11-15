# Autonomous ECD programme — master status

Updated 2026-11-15. Starting research baseline: d069bfac8398cc71793c542ad93d650cc511794c; inherited audit: 770122a9d1e69bbea123a132e98e717a300a9699. No previous ec-autonomous-programme files existed on either accessible branch. This is programme initialization from verified research, not a claim that missing cycles were completed.

## Completed cycles: 01, 02 and 03

The unchanged ECD evolution equations pass a new strong-curvature homogeneous harmonic-time benchmark. All tensor components, spinor, constraints and metric curvature are evaluated through the existing engine. The periodic number quadrature defect identified in the audit is corrected; no physical interaction has been added.

For n0=4, D0=.15, mass=0, kappa=1, volume falls to 1/8. Exact metric R=-384 and Kretschmann=246303.1910 at the endpoint. RK4 errors decrease toward fourth order. At 160 steps, relative metric, metric-velocity and spinor errors are 3.86e-10, 6.45e-10, 2.74e-10. Full 5³ and compressed homogeneous evaluations agree. This verifies a restricted mathematical high-curvature trajectory, not general spatial stability or physically controlled fermion matter.

## Programme limits

No finite-cloud bounce, multi-species evolution, nonlinear 3D stability or oscillation is established. The old weak-field frontend limits remain unchanged. Large curvature in reduced Planck units deliberately lies outside a controlled physical EFT interpretation.

## Cycle 02 — spatially varying high-curvature contraction

A continuum periodic Hamiltonian BVP supplies planar constrained initial data, with K=2.999732467797363 and mean(log chi)=0. Independent finite-difference constraints converge; no discrete projection hides the continuum initial error. At t=.45 the field differences show spatial orders 1.98–2.00. At n=129 the final relative Hamiltonian residual is 1.04e-6, normal H remains below -3.84 and current expansion remains negative. Metric R is approximately -89.55 to -88.91. Charge drift is about 5e-12. A full 9³ RHS and RK step agrees with the compressed planar implementation exactly at the printed precision.

The evolved-snapshot stress divergence is time-difference limited and falls by about four under dt halving. A separate local tangent derivative reduces that floor but itself shows finite-difference-step sensitivity. Metric-velocity time self-convergence is not yet cleanly fourth order (ratio 9.85 in one pair); report this limitation rather than calling every test a pass.

## Cycle 03 — finite planar perturbations and deeper contraction

Four cases (epsilon=.1,.3; seed modes1,4) were evolved to t=.8 at n=65,129,257 with 400 steps. Observed spatial orders are 1.94–2.03. Both normal and current expansion remained negative at every sampled node/time. Proper slice volume ends at 9.09–9.52% of its initial value. Density contrast amplification is mode-dependent: about 1.93/1.85 for mode1 and .97/.90 for mode4. This is not decay of every perturbation or a nonlinear stability theorem.

Finest-grid max relative Hamiltonian errors range from 3.06e-6 to 8.11e-4. The coarse epsilon=.3, mode4 run exceeds 1% constraint error and is not accepted as quantitatively resolved by itself. A separate n=129 temporal test at 200/400/800 steps yields field ratios 16.07,16.06,15.82, supporting RK4 order in this longer case. No bounce or physical oscillation was established.

## Immediate next investigation

Cycle 04: construct and validate genuinely x/y/z-dependent periodic constrained data before any transverse dynamical-stability claim. Use the real polarized spinor's momentum-curl identity to solve the vector conformal constraint, then the nonlinear scalar constraint, and check the full tensor source and independent FD constraints. Read NEXT_ACTION.md.
