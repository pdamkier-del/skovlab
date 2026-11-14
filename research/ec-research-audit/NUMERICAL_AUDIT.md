# Numerical audit

Baseline: d069bfac8398cc71793c542ad93d650cc511794c. Existing simulation sources were not modified. All executions used an isolated downloaded snapshot. No new simulation was built. Extra checks used algebra, direct action variation and existing functions.

## Reproduced evidence

Environment: Python 3.12; NumPy 2.3.5; SciPy 1.17.0; SymPy 1.14.0. This is not the repository's fully pinned historical environment.

| Existing test suite | Reproduced result | Interpretation |
|---|---:|---|
| ec-full-3plus1/tests, Python | 16/16 pass | Operator checks and short weak-field evolution |
| ec-analytical-bounce/tests | 14/14 pass | Planar identities, stress, local coefficients and comparison |
| ec-general-investigation/tests | 29/29 pass | Kinematics, trace relations and chiral benchmark |
| ec-matter-models/validation | 13/13 pass | Algebra, state-specific exchange and scale arithmetic |
| ec-two-matter-models/validation | 10/10 pass | Declared field/kinetic distinctions and identities |
| ec-spherical/validation | 23/23 pass | Symbolic geometry, analytical reductions and FLRW bridge |
| ec-spherical/full-weyssenhoff/validation | 21/21 pass | Selected source, radial characteristics and symmetry |
| ec-dirac-collapse/validation/model.test.mjs | 9/9 pass | LRS ODE, exact volume, constraints and cutoffs |

Total: **126 Python tests and 9 Node model tests passed**. The first spherical run failed because the isolated snapshot initially omitted its imported ec-flrw modules; fetching those baseline dependencies resolved the environment error without code edits. This is not a solver defect.

Browser/Playwright tests, PDF builds, root-wide web application tests and CI job history were not rerun. Saved browser/CI assertions are therefore repository evidence, not independent executions in this audit.

Commands, from a complete snapshot root:

~~~sh
python -m unittest discover -s research/ec-full-3plus1/tests -p 'test_*.py'
python -m unittest discover -s research/ec-analytical-bounce/tests -p 'test_*.py'
python -m unittest discover -s research/ec-general-investigation/tests -p 'test_*.py'
python -m unittest discover -s research/ec-matter-models/validation -p 'test_*.py'
python -m unittest discover -s research/ec-two-matter-models/validation -p 'test_*.py'
python -m unittest discover -s research/ec-spherical/validation -p 'test_*.py'
python -m unittest discover -s research/ec-spherical/full-weyssenhoff/validation -p 'test_*.py'
node --test research/ec-dirac-collapse/validation/model.test.mjs
python research/ec-full-3plus1/coupled_convergence.py --output /tmp/ecd-audit-refinement.json
python research/ec-full-3plus1/conservation.py --output /tmp/ecd-audit-conservation.json
~~~

These output paths avoid overwriting the repository's saved research records.

## Coupled refinement: independently rerun

The existing experiment uses half-width 4, mass .1, \(\kappa=1\), duration .01 and two RK4 steps of .005, with default compact seed and constraints solved separately at each resolution. Comparison is on 27 exact shared nodes, not a whole-domain norm.

| n | Initial max constraint residual | Final common-node max Hamiltonian residual |
|---:|---:|---:|
| 9 | \(1.30824\times10^{-13}\) | \(1.50653\times10^{-7}\) |
| 17 | \(1.22163\times10^{-12}\) | \(2.68469\times10^{-7}\) |
| 33 | \(1.19493\times10^{-11}\) | \(7.05328\times10^{-8}\) |

Successive state-difference ratios reproduce the saved values:
metric 5.92137, metric velocity 4.00221, spinor 4.53671. The corresponding apparent orders for exact factor-two refinement are about 2.57, 2.00 and 2.18. The metric is not yet displaying a clean asymptotic ratio of four. Initial elliptic errors, coarse resolution and temporal errors all enter this comparison.

This is positive evidence for approximately second-order short weak-field behavior. The first Hamiltonian pair gets worse; only the finer pair improves by 3.81. A broad acceptance interval of ratios between three and eight is useful regression logic, not proof of a convergence theorem or an error bound.

The same fixed temporal step at each spatial resolution does not independently establish the coupled spatial asymptotic regime. The separate RK4 self-convergence test establishes the expected order for its chosen semidiscrete case, whose nonzero matter data are intentionally unconstrained. Neither test certifies a constrained strong-collapse trajectory.

## Stress conservation and tracer evidence

The stored finite-difference full-stress divergence experiment has shared-node RMS residuals \(1.82283\times10^{-6}\), \(3.52599\times10^{-6}\), \(9.26974\times10^{-7}\) for 9³, 17³, 33³. The audit reran this experiment and reproduced all six stored RMS/maximum residual values exactly at the printed precision. The coarse pair is nonmonotonic; the finer ratio is about 3.80. Its centered time difference keeps \(h=.005\), so both temporal and spatial errors enter. There is no source-normalized full-domain conservation error budget.

Continuum U(1)/diffeomorphism identities and generic local spinor-jet checks are valuable independent of these residuals. Re-evaluating every local temporal derivative from Dirac can make a *local operator* continuity test hold algebraically. That is weaker than demonstrating conservation of the integrated evolved numerical state.

The later general investigation does add passive material/normal tracers; the older full-solver document's “no tracking” description is not the final project status. Inspection of track.py confirms that field RK4 stages duplicate the existing engine while tracers are passive. Its trilinear reconstruction differentiates its own piecewise reconstructed primitives and reports a continuity defect. This is a sound distinction.

Saved tracer rest-volume and expansion-integral identities agree near roundoff, while density-based e-folds differ substantially relative to their tiny values. For example, at 9³ the first marker gives \(N_u=.000181575\), the density estimate .000117563, and a measured continuity contribution .0000640115. An identity closing to \(10^{-15}\) has not made the observable accurate to \(10^{-15}\). The later finer outputs still do not provide a certified physical e-fold count or a detected bounce.

## Confirmed current defect: periodic number integral

Location: [ecd.py, diagnostics(), lines 186–188 at the audited commit](https://github.com/pdamkier-del/skovlab/blob/d069bfac8398cc71793c542ad93d650cc511794c/research/ec-full-3plus1/ecd.py#L186).

Grid(boundary="periodic") omits the duplicate endpoint and uses \(dx=2L/n\). diagnostics() nevertheless applies open-interval trapezoids along all axes. It misses the final periodic cell and gives unequal effective weights.

A uniform Minkowski spinor with component \(\psi_2=.1\), half-width 4, n=9 has \(j^0=.01\). The correct torus charge is \(Q=.01\times8^3=5.12\); the implementation returns **3.5959396433470516**, a ratio \((8/9)^3=.7023319616\).

Minimal reproduction, from research/ec-full-3plus1:

~~~python
from ecd import Grid, minkowski, diagnostics
grid = Grid(9, 4., "periodic")
state = minkowski(grid)
state[2][..., 2] = .1
print(diagnostics(grid, state)["number"])  # 3.5959396433470516
print(.01 * 8**3)                       # 5.12
~~~

A periodic sum times \(dx^3\), or explicit wrapped-cell integration, is the appropriate future correction. No fix was applied under the instruction to preserve existing simulations. This affects absolute charge and can bias relative charge measurements for translating periodic profiles. It does not automatically invalidate the Dirichlet localized charge check or the analytical cosmological result.

## Other independent targeted checks

- Finite differencing the algebraic Cholesky frame independently of its implemented derivative gave max error \(8.66\times10^{-12}\).
- Direct lapse/spatial-scale variation of the constant-tetrad rest-wave action recovered \(E=mn+G_A n^2\), \(P=G_A n^2\).
- Fresh symbolic substitution of the six-field scale factor in both FLRW equations gave identically zero residuals. The metric Kretschmann scalar at the bounce is \(12q^4/a_b^8\), finite.
- A fresh Pauli-matrix exchange contraction with \(n_\uparrow=.7,n_\downarrow=.3\) gave \(-1.26=-6n_\uparrow n_\downarrow\).
- The exact accelerating e-fold count is .3465735903; the one-occupation six-mode scale is \(1175.94175\,\bar M_P^4\).

These are targeted verification, not a new simulator or a new many-body theory.

## Numerical risks that remain missing evidence

1. **Outer boundary.** Fixed spinor and metric velocity, with linearly updated boundary metric, are not outgoing constraint-preserving data. Excluding two displayed layers does not prove insulation. Initial data are obtained from a global finite-box elliptic solve; boundary influence is not solely a later wave-propagation issue.
2. **High-frequency modes.** The composed centered operator has periodic symbol \(D_0^2=-\sin^2(kdx)/dx^2\). Even-grid Nyquist modes would be invisible; odd grids remove the exact alternating null mode but retain poorly resolved near-Nyquist modes. The first-order Dirac derivative has the same resolution issue. Smooth low-frequency convergence and a brief noise test do not settle uniform high-frequency stability. This is a documented risk, not a demonstrated instability in every tested run.
3. **Constraints.** Solving the same discrete residual later monitored is useful but can conceal a consistent discretization bias. Independent derivatives, continuum/manufactured solutions and full-domain norms remain necessary.
4. **Scale controls.** CFL control based on null speeds is sensible; it is not a nonlinear error estimator. Fixed weak-field thresholds are operational stops, not physical validity bounds.
5. **Geometry and outcomes.** No asymptotic mass, complete exterior, trapped-surface history, whole-body bounce or strong-field curvature regularity test is established.
6. **Long times and parameter families.** No convincing boundary/domain-size convergence, long contraction, robustness under general constrained perturbations or completed strong-field collapse has been shown.

Continuum GH guidance is available in [Lindblom et al.](https://arxiv.org/html/gr-qc/0512093v3), but their first-order reduction and boundary conditions differ. Numerical convergence would establish approximation to selected classical equations, not the physical appropriateness of those equations or their state.
