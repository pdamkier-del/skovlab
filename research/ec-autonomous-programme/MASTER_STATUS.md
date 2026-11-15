# Autonomous ECD programme — master status

Updated 2026-11-15. Starting research baseline: d069bfac8398cc71793c542ad93d650cc511794c; inherited audit: 770122a9d1e69bbea123a132e98e717a300a9699. No previous ec-autonomous-programme files existed on either accessible branch. This is programme initialization from verified research, not a claim that missing cycles were completed.

## Completed cycles: 01–08

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

This establishes more than a planar lift: the evolving data vary along all axes. It still does not establish stability against arbitrary perturbations, long-time collapse, a bounce, or physical ultra-dense fermion applicability. The largest run took about 317 seconds in this environment. C06 below adds a validated full torsionful curvature diagnostic.

## Cycle 06 — full torsionful curvature and scalar cancellation

An independent component-level symbolic calculation gives full scalar R_tilde=0 but full Kretschmann=128/v⁴ on the exact n0=4,D0=0,m=0 branch. The metric counterparts are R=-6/v² and K=60/v⁴. At v=1/8 the full Kretschmann is 524288 despite the identically zero full scalar. The corrected geometric torsion orientation is checked against the complete independent connection components.

The new full-affine diagnostic converges at second order in its tangent time-difference step on this reference. Applying it to C04 initial spatially varying data at 9³/17³/33³ also exposes decreasing spatial scalar residuals; this is not a test of full torsion curvature throughout the evolved C05 trajectory. Thirteen new research tests and the 16 existing full-field tests pass in this session. No frontend/browser suite was run.

## Cycle 07 — constrained spatial spin texture

Verified the proposed real lower-pair texture theta=.2 sin(kx), with the same density seed and charge as C04. An independent symbolic derivation checks all four axial components and all 16 stress components: E=GA n², j=curl(S)/4, and spatial stress GA n² I+[K,E_spin]/4. Conformal momentum scaling is independently checked for arbitrary first jets. Thus the anisotropic stress is retained rather than replaced by a perfect fluid.

The full vector conformal operator and scalar constraint have been solved at 9³/17³/33³. At 33³, initial relative FD Hamiltonian is 4.53e-4 and momentum max 2.55e-4, both decreasing with refinement. Energy/axial/spatial-stress formula errors are below 7e-15. The coarse 9³ oversampled scalar residual is 1.47e-5; at 17³/33³ it is below 5e-11. This is an initial-data result, not a dynamical stability claim.

Lossless NPZ checkpoints now carry full fields, grid/units/harmonic-time metadata and per-field hashes. Reload/restart, corruption detection and rejected-state policy are tested. Eighteen programme tests pass in this continuation session. Expensive spin-texture evolution is the next cycle.

## Cycle 08 — evolved spin texture with full persisted fields

The validated theta=.2 sin(kx) family was evolved on 9³/17³/33³ to t=.2. Spatial state orders are 1.937,1.892,1.962; separate 17³ temporal ratios are 14.83,17.25,16.58. All runs complete within the predeclared constraints/current/coordinate/CFL guards. At 33³, final relative Hamiltonian=3.82e-4, charge drift<3.8e-10, volume ratio=.5489084664, and current expansion is negative at all sampled points/times.

Fifteen lossless full-field checkpoints (29,275,156 bytes) cover initial/midpoint/final states across the spatial/time tests. Every published Git blob is verified against its raw file Git SHA and SHA256; the report/index include retrievable blob IDs. No resampled comparison field replaces a raw checkpoint.

The full affine curvature was measured from reloaded states at t=0,.1,.2 with two tangent difference steps. At 33³ the final full Kretschmann maximum is about1480.76. The small massless full-scalar residual decreases with spatial refinement; it is not interpreted as a physical nonzero trace. These are sampled finite-time checks, not a regularity/completeness theorem.

## Exact continuation

Next C09: use the persisted C08 fields to resolve the material-current Raychaudhuri balance. Validate the kinematic identity independently of the effective Einstein-source substitution, distinguish geometric and constraint errors, and quantify whether acceleration/rotation oppose the measured focusing. No re-evolution is needed. See NEXT_ACTION.md.

No global bounce, oscillation, arbitrary-perturbation stability or physical fermion-cloud interpretation has been established.

## Record entry points

- [Chronological decisions and findings](RESEARCH_LOG.md)
- [Equations, results and limitations](RESULTS.md)
- [Reproduction and validation](VALIDATION.md)
- [Prioritized open questions](OPEN_QUESTIONS.md)
- [Exact next investigation](NEXT_ACTION.md)
- [Short Danish explanation](SUMMARY_DA.md)
- [Recorded convergence figure](figures/validation.svg)

The engine's only production change is periodic charge quadrature; all field equations, the weak-field frontend and its limits are preserved. Research drivers, initial-data construction and additional diagnostics live in this programme directory.
