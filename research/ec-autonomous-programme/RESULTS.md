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
