# Classical Dirac collapse: verified reduced laboratory

[Open the app](https://pdamkier-del.github.io/skovlab/research/ec-dirac-collapse/) · [Dansk rapport](rapport.pdf) · [LaTeX](rapport.tex) · [Status and missing work](STATUS.md)

**Implemented:** a coupled classical ECD solution in homogeneous, locally rotationally symmetric (LRS) Bianchi I, with an aligned single commuting spinor. This is a genuine anisotropic Einstein–Dirac reduction, not a general inhomogeneous 3+1 solver or a finite cloud. The isotropic case is explicitly a metric FLRW limit. No existing FLRW files are modified.

The requested general 3+1 numerical solver is not established by this work. Plain ADM evolution is not automatically a strongly hyperbolic numerical formulation. Rather than introduce unsupported transport or a prescribed bounce, the app implements the closed reduction derived in [THEORY.md](THEORY.md). A 3+1 field theory being formally closed does not establish a stable discrete solver.

## What the app actually computes

- Synchronous proper time, diagonal LRS metric, two distinct material scale factors and shear.
- A homogeneous classical spinor amplitude, nonlinear phase and algebraic axial torsion.
- Six first-order ODE variables, RK4 integration without projection onto the Hamiltonian constraint.
- Three plots: material volume scale, expansion and its derivative. These are numerical solution values, not the analytical benchmark used by tests.
- Hamiltonian error, current/volume diagnostics, metric curvature, and explicit stop reasons. JSON exports include all rows, the reconstructed nonzero complex spinor component, and model/unit/method metadata. The torsion readout is the largest absolute orthonormal component, $|T_{012}|=n/2$, not a tensor norm.

For this branch, $E=mn+G_A n^2$, $P=G_A n^2$. These are derived from the field stress, not imposed phenomenological spin pressure. They imply $\dot H=-(E+P)/2-D^2/3\leq0$ on the constraint. There is **no volume bounce** for nonnegative mass and density. Changing the spin sign reverses torsion but leaves this branch's geometry unchanged. This conclusion does not cover other ECD states.

The spatially homogeneous domain can be taken as a periodic three-torus with a chosen compatible periodic spin structure. No boundary flux exists; this is not a vacuum-matched body. A comoving cell in its covering space gives the same diagnostics. $M_{rest}=mn_0 L_0^3$ is conserved rest energy content; it is **not ADM mass**. The cell size is not a cloud radius. ADM mass requires asymptotically flat constrained initial geometry and an asymptotic surface integral.

## Controls and validity

The UI chooses positive rest content, cell length, field mass, signed dimensionless initial anisotropy and a uniform axial spin orientation. The initial number density and negative expansion root are derived. Independent arbitrary collapse speed or spatial spin profiles are deliberately unavailable. See [INITIAL_DATA.md](INITIAL_DATA.md).

Units are $c=\hbar=\kappa=1$: mass in reduced Planck masses, length/time in inverse reduced Planck masses, number density in cubed and energy density in fourth powers of that mass. Approximately $\bar M_P=2.435\,10^{18}$ GeV, $1/\bar M_P=8.10\,10^{-35}$ m and $2.70\,10^{-43}$ s. This is a classical-field demonstrator, not neutron/quark matter or a quantum fermion gas.

A proposed step is rejected before any of $E$, $n$ or $\sqrt{R_{abcd}R^{abcd}}$ reaches 0.1 in these units. These dimensionful quantities are compared to their respective Planck-unit powers; they are not summed. This **chosen operational cutoff**, not an experimentally established validity surface, keeps the plotted solution away from formal divergence. It cannot certify quantum corrections are small. The cutoff is monitored at accepted/proposed endpoints; with step refinement its time changes by a step, not a claimed precise physical event. Full torsionful curvature is not separately bounded by an implemented invariant. No physical continuation beyond the cutoff is inferred.

## Reproduce

From the repository root:

~~~sh
node --test research/ec-dirac-collapse/validation/model.test.mjs
python research/ec-dirac-collapse/validation/test_symbolic.py
node research/ec-dirac-collapse/validation/browser.test.cjs
bash research/ec-dirac-collapse/build_pdf.sh
npm test
~~~

Python uses the existing pinned SymPy 1.14.0 requirement. Browser checks start their own local HTTP server and use the existing Playwright dependency. [VALIDATION.md](VALIDATION.md) describes exactly what is checked, including the analytical coupled-volume solution. No theorem of global regularity, inhomogeneous stability or exterior matching follows from these checks.
