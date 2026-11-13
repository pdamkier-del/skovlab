# General, spatially varying classical Einstein–Cartan–Dirac

This directory implements the **full local neutral single-species classical ECD field equations on a three-dimensional grid**. There is no homogeneous, spherical, axial, diagonal-metric or perfect-fluid restriction in the evolution engine. All four complex spinor components evolve. The metric has ten independent components and ten independent time derivatives; symmetry is stored redundantly as 4×4 arrays.

**Status: experimental full-field 3+1 implementation, not a validated strong-collapse simulator.** The short-time weak-field tests below pass. General nonlinear stability, strong-collapse convergence, asymptotic-flat exterior construction and bounce physics remain unresolved. A complete research claim needs those steps; the existence of code is not such a claim.

[Online viewer](https://pdamkier-del.github.io/skovlab/research/ec-full-3plus1/) · [Dansk rapport (PDF)](rapport.pdf) · [Field derivation](FORMULATION.md) · [Convention correction](CONVENTION_AUDIT.md) · [Validation](VALIDATION.md)

## Run an actual calculation in the browser

From the repository root, use an isolated environment:

~~~sh
python -m venv research/ec-full-3plus1/.venv
research/ec-full-3plus1/.venv/bin/python -m pip install -r research/ec-full-3plus1/requirements.txt
research/ec-full-3plus1/.venv/bin/python research/ec-full-3plus1/server.py
~~~

Open **http://127.0.0.1:8770/**. Changing the controls runs the Python constraint solver and coupled 3D evolution; the browser is the interface. The calculation can take seconds or minutes depending on resolution. The static GitHub Pages version displays a real saved calculation and exports it, but cannot run Python. It explicitly disables new calculations. No precomputed curve is passed off as a newly computed solution.

For a reproducible command-line run, using the same Python environment:

~~~sh
python research/ec-full-3plus1/evolve.py --n 9 --duration 0.02 --dt 0.005 --output solution.json --fields final-fields.npz
python -m unittest discover -s research/ec-full-3plus1/tests -v
node research/ec-full-3plus1/tests/browser.test.cjs
~~~

The browser test uses the existing repository Playwright installation. NumPy/SciPy are sufficient for the new field tests; the original research's SymPy dependency remains separate. The export contains parameters, actual diagnostics, xy slices, initial constraint report and explicit limits. The optional NPZ contains all final metric, metric-velocity and spinor arrays, not just observables.

## What is implemented

- Torsion-eliminated minimal ECD action; full nonlinear Hehl–Datta equation and its complete on-shell Hilbert stress.
- General Lorentzian metric, lapse/shift, Cholesky spatial triad and its derivatives, metric-compatible spin connection, including nonzero shift and off-diagonal geometry.
- Harmonic-coordinate reduced Einstein equations coupled to that stress at every RK4 stage. No imposed pressure or separate spin evolution law.
- A nonlinear conformal initial-data solve for the Hamiltonian and all three momentum constraints, with harmonic gauge initialization. Nonconvergent data are rejected.
- An initially compact, smooth, triaxially shaped complex spinor with spatial polarization rotation. It is merely a selectable family of data, not a restriction on the engine's allowed fields.
- Actual spatial evolution, Hamiltonian/momentum/gauge residuals, normal expansion, shear, energy, axial source, integrated Dirac number, and explicit validity/constraint stops.
- Two boundary modes: periodic analytic/numerical benchmarks, and prescribed finite-cube data for short localized experiments. The outer metric evolves linearly with its prescribed initial velocity, while that velocity and the zero outer spinor are fixed. This is **not** a constraint-preserving physical exterior.

The viewer does not show a fictitious global scale factor: the normal expansion is local, coordinate time is not proper time, and no material-volume tracking has been implemented. No global bounce is assessed.

## Important convention result

Checking the tetrad spin connection against Clifford covariance fixes its sign. With the explicitly declared geometric frame connection, this requires a correction to the previous literal axial-torsion orientation. The **effective quartic coefficient, Dirac equation and prior LRS evolution are unchanged**. Read [CONVENTION_AUDIT.md](CONVENTION_AUDIT.md) before transferring the geometric torsion tensor from earlier reports. Previous reports are preserved as historical artifacts.

## What is still required

A constraint-preserving, convergent outer treatment; domain-size/asymptotic tests; larger-domain initial-data solves; coupled matter/metric spatial convergence for the intended strong-collapse family beyond the checked short weak-field shared-node benchmark; longer nonlinear stability tests; curvature and effective-theory controls; tracked material volumes; asymptotic ADM mass; general horizon diagnostics; and a regular solution through any proposed bounce. Existing FLRW and LRS modules are unchanged.
