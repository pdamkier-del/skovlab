# Autonomous ECD programme — master status

Updated 2026-11-15. Starting research baseline: d069bfac8398cc71793c542ad93d650cc511794c; inherited audit: 770122a9d1e69bbea123a132e98e717a300a9699. No previous ec-autonomous-programme files existed on either accessible branch. This is programme initialization from verified research, not a claim that missing cycles were completed.

## Completed cycles: 01–05

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

## Cycle 04 — genuinely three-dimensional periodic constrained data

Constructed n_seed=4[1+.1 cos(kx)cos(ky)cos(kz)] with variation along all axes. Spin-induced momentum is a nonzero curl. A Fourier vector solve supplies the conformal shear; a nonlinear scalar solve determines positive chi and constant K with mean(log chi)=0. The complete ECD source, harmonic initialization and independent FD constraints are checked.

At 33³: scalar spectral residual 4.78e-12, vector residual 4.88e-15, oversampled continuum Hamiltonian residual 4.91e-11. The engine's independent FD relative Hamiltonian is 4.55e-4 and momentum max 3.92e-5, both decreasing under refinement. Tightening the 17³ nonlinear tolerance to 1e-12 changes K by less than 1e-12 and leaves FD errors essentially unchanged. This distinguishes elliptic-solve tolerance from spatial discretization error. Ten research tests now pass.

## Cycle 05 — short full 3D high-curvature evolution

The original full-grid engine evolves the C04 three-coordinate seed to harmonic t=.2. Spatial refinement 9³/17³/33³ gives state orders 1.946,1.920,1.963 (metric/velocity/spinor). Separate 17³ time refinement 20/40/80 steps gives ratios 14.83,17.25,16.58, compatible with RK4 on this test. The 33³ endpoint relative Hamiltonian is 3.83e-4; charge drift remains below 8e-11 on that run. Current and normal expansion stay negative, volume ratio is .5489090, and metric R ranges from -20.55 to -19.09.

This establishes more than a planar lift: the evolving data vary along all axes. It still does not establish stability against arbitrary perturbations, long-time collapse, a bounce, or physical ultra-dense fermion applicability. The largest run took about 317 seconds in this environment. Full torsionful curvature remains the next regularity diagnostic.

## Immediate next investigation

Cycle 06: independently validate a full-affine-curvature diagnostic on the exact massless isotropic branch, where the full scalar vanishes but other full curvature components need not. Do not use vanishing scalar curvature to classify regularity. Then define the next spatially varying regularity test without repeating completed contraction sweeps.
