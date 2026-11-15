# Results and assumptions

## C01 — exact high-curvature benchmark (analytically established; implementation numerically supported)

Keep the minimal neutral one-field action with GA=3 kappa/16. For mass zero and n0>0, let H0=-sqrt(kappa GA n0²/3+D0²/9), rates=(H0-D0/3,H0-D0/3,H0+2D0/3). In harmonic time t,

v=exp(3 H0 t), N=v, a_i=exp(rates_i t), psi=sqrt(n0/v) exp(-2 i GA n0 t) (0,0,1,0).

The diagonal metric is (-v²,a_x²,a_y²,a_z²). Its p00=6 H0 g00 and pii=2 rates_i gii. Derivation: start from the already verified proper-time LRS equations, use d tau=v dt, n=n0/v, D=D0/v. Mass zero makes v linear in proper time and the harmonic-time rates constant. This transforms the prior exact branch into a test of the general harmonic tensor engine; it does not claim a new matter solution.

R=-2 kappa GA n²; torsion contraction T_abc T^abc=-3 kappa² n²/2. With r_i=rates_i, metric Kretschmann=4/v⁴ [sum_i(r_i²-3 H0 r_i)²+sum_(i<j)r_i² r_j²]. H=H0/v stays negative. No volume bounce exists on this branch. Proper time is (v-1)/(3 H0), reaching a finite limiting collapse time as t tends to infinity. The endpoint of any finite benchmark run is before that limit.

C01 reaches v=.125 from n0=4,D0=.15, giving R=-384 and K=246303.19100165. At 160 steps the scaled Hamiltonian maximum is 1.09e-8; charge drift is 2.31e-10. Curvature errors fall with refinement. See machine-readable records for all values.

Physical restriction: these are deliberately high reduced-Planck curvatures of a commuting classical field. They are mathematical stress tests, not reliable dense-fermion predictions. A numerical non-bounce on this already known branch does not exclude other ECD bounces.

## Diagnostic correction

Periodic grids omit the repeated endpoint, so charge must be the periodic sum times dx³. Open-interval trapezoids undercounted a uniform n=9 torus by (8/9)³. The correction changes diagnostics only and is regression-tested for uniform charge and translated nonuniform data. Dirichlet quadrature is unchanged.

## C02 — constrained periodic planar perturbation (conditional/numerically supported)

Take gamma_ij=chi(z)^4 delta_ij, Kij=gamma_ij K/3, psi=chi^-3 sqrt(n_seed(z)) (0,0,1,0), m=0, kappa=1. The polarization is along z, the only varying direction. Direct substitution in the full field source gives zero momentum and E=GA n_seed² chi^-12. The momentum constraint vanishes because K is constant. R3=-8 chi^-5 chi'', so the Hamiltonian constraint is exactly

chi''=K² chi⁵/12-GA n_seed² chi^-7/4.

Set u=log chi; u''=K² exp(4u)/12-GA n_seed² exp(-8u)/4-(u')². Solve for periodic u,u' and unknown positive K with mean(u)=0 (an integral auxiliary variable enforces the mean). This fixes the global conformal normalization and scalar compatibility; no finite-box exterior is asserted. Numerical convergence of a BVP is evidence for this local branch, not uniqueness for all seeds. Harmonic p0mu is then solved using the existing geometric routine.

For n_seed=4[1+.02 cos(2 pi z/8)], K=2.999732467797363. The independent grid Hamiltonian residual at initial time is .00071418, .00019217, .0000497165, .0000126347 at n=17,33,65,129. Initial momentum/gauge residuals are near roundoff. The continuum data are deliberately not reprojected onto each monitored discrete constraint.

At t=.45 the final relative Hamiltonian residual decreases from 5.88e-5 to 1.04e-6, while state differences give near-second-order spatial convergence. R remains finite at the endpoint, around -89.55 to -88.91. Both sampled current and normal expansion stay negative throughout; this is no local material-volume turn within the sampled resolved interval for this family. It does not prove no later turn, global regularity or stability against arbitrary perturbations. No finite-body or exterior conclusion follows.

Stress-divergence accuracy is limited by the centered temporal diagnostic at fixed dt. A tangent-source derivative provides a complementary check but has an additional chosen-delta error. Full torsionful Riemann regularity is not established by the algebraic torsion contraction or metric scalar/Kretschmann alone.

## C03 — bounded-amplitude planar continuation (numerically supported, restricted)

| Seed epsilon | Mode | Finest final volume ratio | Finest density-contrast amplification | Finest max relative Hamiltonian |
|---:|---:|---:|---:|---:|
| .1 | 1 | .09120468 | 1.92892 | 3.06e-6 |
| .3 | 1 | .09524739 | 1.84502 | 1.35e-5 |
| .1 | 4 | .09089638 | .96993 | 3.10e-4 |
| .3 | 4 | .09229357 | .90247 | 8.11e-4 |

Density contrast is (max n-min n)/(max n+min n) on the declared slices. It is not identical to the seed amplitude because solving the constraints changes the conformal factor and physical density. Amplification compares the same observable at endpoints; it is not a Lyapunov exponent, trajectory perturbation norm or proof of oscillation. The low modes increase and the high modes decrease over this interval, so uniform decay is not supported.

Normal/current expansion remain negative throughout the sampled evolution to t=.8. State errors converge with order 1.94–2.03 in space, and a separate high-mode time test has near-16 ratios. Finite endpoint metric/torsion contractions and positive spatial metric do not establish global regularity or all torsionful curvature bounds. This is a classical high-curvature torus calculation outside a demonstrated physical EFT regime.

## C04 — three-coordinate periodic constrained initial data (derived identities; numerical solution)

Let n_s=4[1+.1 cos(kx)cos(ky)cos(kz)], k=2 pi/8, gamma=chi⁴ delta, psi=chi^-3 sqrt(n_s)(0,0,1,0), m=0, kappa=1. The full initial source gives E=GA n_s² chi^-12 and

j_i=chi^-6 jtilde_i, jtilde=(partial_y n_s,-partial_x n_s,0)/4.

This is spin-induced stress momentum; a zero spatial particle current does not imply zero stress momentum. jtilde has zero mean and zero divergence. Thus solve Delta W=jtilde with meanW=0; divW=0, and L W is symmetric tracefree. With Kij=chi^-2(LW)ij+gammaij K/3, the conformal momentum constraint is satisfied. No stress component is discarded in the subsequent full tensor check.

Set Q=|LW|²+2 GA n_s². The scalar Hamiltonian is

Delta chi=K² chi⁵/12-Q chi^-7/8.

Periodicity implies K²=(3/2) integral(Q chi^-7)/integral(chi⁵). Use u=log chi and meanu=0 to fix normalization. The Newton residual is Delta u+|grad u|²-K² exp(4u)/12+Q exp(-8u)/8+meanu. Integrating this residual against chi shows that its zero also enforces meanu=0. This is a conformal constraint construction, not a new matter EOS or modification of ECD.

K=2.99909273989 for the tested family. Exact conformal scaling keeps initial total classical Dirac charge integral(n_s)=n0 L³ while geometry is solved; total charge and a chosen free collapse rate were not assigned independently. Numerical positivity, spectral/oversampled constraints, full-source matching and FD convergence support these data. Uniqueness and existence for arbitrary amplitudes are not established.

All three axes have nonzero source variation. Therefore these are genuinely 3D initial data, unlike a transverse lift of the planar test. Their evolution and stability require separate validation.

## C05 — full 3D strong-curvature trajectory (numerically supported within one finite family)

The C04 seed is evolved without spatial symmetry reduction. All metric components, metric velocities and complex spinor components remain active. State differences on common physical points converge with spatial orders 1.92–1.96; separate temporal ratios are near16. This validates a finite high-curvature contraction interval with truly x/y/z-dependent fields, extending the earlier weak-field prototype evidence.

At 33³ and t=.2: volume ratio .5489090168; relative Hamiltonian .0003830955; metric R range [-20.55495,-19.08540]. Normal and material expansion are negative at all sampled points/times. No resolved local volume bounce is found in this interval. This is not a universal no-bounce theorem or an assertion about untested later evolution.

The topology is a 3-torus, there is no finite cloud or exterior. The seed is deliberately a mathematically specified commuting field at uncontrolled reduced-Planck scales. A numerical bound over a finite interval does not establish geodesic completeness, and metric curvature tests do not yet monitor every torsionful component. These restrictions remain even though spatial/time refinement works.

## C06 — full-affine curvature benchmark (analytically established; diagnostic numerically validated)

For n0=4,D0=0,kappa1,m0, v=exp(-3t) and a_i=exp(-t). The independent Levi–Civita connection has Gamma^0_00=-3, Gamma^i_0i=Gamma^i_i0=-1 and Gamma^0_ii=-exp(4t). Corrected axial contortion adds C^0_12=exp(4t), C^0_21=-exp(4t), C^1_02=1, C^1_20=-1, C^2_01=-1, C^2_10=1; other components vanish.

Direct symbolic Riemann construction yields full scalar R_tilde=0 and full K_tilde=128 exp(12t)=128/v⁴. Metric R=-6/v², metric K=60/v⁴, and torsion contraction=-24/v². Thus a vanishing full scalar does not make the connection regular at unlimited compression. This is an explicit benchmark of the prior conditional invariant obstruction, not a new claim that all clouds reach that limit.

At v=.125, K_tilde=524288 and metric K=245760, both finite at this chosen endpoint and unbounded only in the limiting exact collapse. The full normal-tetrad component maximum is 3/v² (192 at this endpoint); its value depends on the specified frame, unlike a scalar contraction. The new numerical diagnostic approaches the exact values with its declared O(delta²) time-difference error. Scalar cancellation error must not be reclassified as physical nonzero R_tilde.

The same diagnostic is sampled on C04 three-coordinate initial data. Its smaller-step full scalar residual falls from about .03484 to .01022 to .00275 under spatial refinement. The massless zero-scalar continuum identity is approached; the nonzero full K remains. This initial-slice check does not certify the complete evolving 3D full connection or general regularity.

## Current classification of the programme's central questions

- **Analytically established:** exact reference branch has no volume bounce; its full scalar vanishes despite divergent full curvature under unlimited compression. The minimal action and corrected conventions are unchanged.
- **Numerically supported/conditional:** resolved finite-time planar contractions and one genuinely 3D high-curvature trajectory; periodic constrained initial data for specified seeds; the implemented convergence and curvature diagnostics.
- **Falsified as a blanket description of the measured tests:** every planar density contrast decays. Some tested contrasts increase over the interval. This is not an asymptotic instability theorem.
- **Unresolved:** regular bounce for a new admissible state, torsion attribution of such a bounce, its perturbative/nonlinear stability, post-bounce recollapse/oscillations, arbitrary 3D stability, finite-body matching and controlled quantum interpretation.

The numerical examples constrain specific finite families. They neither demonstrate singularity avoidance nor a universal absence of bounces.

## C07 — real spin-texture source identities and constrained data

For a real lower two-component spinor, in a local orthonormal Fermi frame,

A=(0,n sin theta,0,n cos theta), E=GA n², j=(curl S)/4,
S_ij=GA n² delta_ij+[K,E_spin]_ij/4, (E_spin)_ij=epsilon_ijk S_k.

All first density and angle derivatives and symmetric extrinsic-curvature components are arbitrary in the independent symbolic check. This is a restricted source identity, not an EOS for arbitrary Dirac fields. The commutator is symmetric and tracefree and must be kept in evolution. A zero spatial particle current does not imply zero stress momentum.

For the conformal seed Psi and psi=chi^-3 Psi, momentum scales as chi^-6 j_seed and E=GA n_seed² chi^-12. Hence the periodic conformal vector/scalar constraint construction remains valid after the source is changed consistently. The vector Fourier inverse is W_i=-j_i/k²+k_i(k dot j)/(4 k⁴) at nonzero wave number; its zero mode is fixed by meanW=0 after checking source compatibility.

The selected smooth periodic theta=.2 sin(kx) has been independently checked at 9³/17³/33³. Initial source projections agree to roundoff, FD constraints converge, and oversampled scalar residuals expose the coarse-grid alias error rather than hiding it. The zero-texture limit reproduces C04. Numerical existence for this family is supported; arbitrary-spin initial-data existence and dynamical stability are not proved.

Checkpoint persistence preserves the full metric, metric velocity and complex spinor without resampling or lossy packing, and distinguishes harmonic time from proper time. Hash and restart tests establish reproducible storage, not physical correctness of a trajectory.
