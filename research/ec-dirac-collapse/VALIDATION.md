# Validation scope and numerical method

## Independent mathematics

The SymPy tests construct explicit Clifford matrices, the curved spin connection, nonlinear Dirac residual and all sixteen stress components. They detect the forbidden generic triaxial off-diagonal stress before restricting to LRS. A separate coordinate metric calculation builds Christoffel symbols, Ricci and Einstein tensors directly, checking independent temporal/transverse/longitudinal and mixed components. Algebra then verifies current and energy conservation, the normal Friedmann identity, exact volume acceleration and constraint propagation.

These are independent checks of the documented derivation, not computer expressions substituted for it. The older action/torsion checks are retained in the previous research directories.

## Numerical algorithm

Classical fourth-order Runge–Kutta advances six ODEs in proper time. Logarithms keep volume and scale factors positive while finite. Number density is reconstructed from the analytically integrated Dirac amplitude/current law; phase is evolved numerically. This enforces number conservation by construction, so a measured zero number residual is **not** an independent numerical spinor test. The curved matrix residual independently checks that this reconstruction obeys Dirac. JSON gives density and phase (and initial spin sign) sufficient to reconstruct every spinor component.

Each step obeys $\Delta\tau\leq\min(T/600,0.012/\max(|H|,|D|,m+2G_A n,0.001))$, with a resolution divisor for refinement. This is a scale-based step bound, not an embedded error estimator or a CFL theorem for PDEs. $T=2/\max(|H_0|,0.01)$. A hard step budget prevents browser hangs. Every proposed point is checked for finite diagnostics, cutoff and constraint/volume error. No constraint projection is used.

The relative Hamiltonian residual is $|6H^2-2E-2D^2/3|/\max(6H^2,2E+2D^2/3,10^{-30})$. Stop thresholds are $10^{-6}$ for it and $10^{-7}$ for $|\log v-2\log a-\log b|$. Momentum constraints vanish by the exact ansatz; no spatial residual experiment is claimed. Constraint errors grow under contraction as predicted by $\dot C=-6HC$.

The metric curvature diagnostic is independently obtained for diagonal Bianchi I:

$$\mathcal K=4[2(\dot A+A^2)^2+(\dot B+B^2)^2+A^4+2A^2B^2],\qquad R=E-3P\quad(\kappa=1).$$

The curvature monitor uses the evolved rates; $R=E-3P$ is an Einstein on-constraint identity, not an independent off-constraint curvature calculation.

## Automated checks

- Nine Node numerical tests: inadmissible initial data, constraint solving, fourth-order convergence to exact coupled volume/expansion, conserved number and shear integral, geometric volume, generalized Friedmann/focusing identity, nontrivial vacuum Kasner and Minkowski, massless/isotropic limits, proper absence of an independent spinless-matter switch, operational cutoff, spin reversal, refinement and step exhaustion.
- Four independent Python symbolic tests covering the items above.
- Playwright: desktop/mobile layout, finite plotted data, successful compute/export, reported cutoff, invalid input handling and recovery, no browser errors.
- Existing 24 application tests and 67 previous mathematical tests retained. New results do not supersede their stated scope.

At nonzero density a single coherent spinor has nonzero axial magnitude. The spinless limit tested here is removal of the field (vacuum), not dust with arbitrarily suppressed spin. A formally torsion-free interacting-matter comparison would be a separately specified action, not a checkbox silently changing $G_A$ in ECD.

No ADM mass conservation test, spatial convergence test, general exterior matching test or nonlinear 3+1 stability proof is claimed. Work balance replaces constancy of cell matter energy. The UI distinguishes operational/numerical/step/time stops; analytical monotonicity excludes a volume bounce only within this branch.
