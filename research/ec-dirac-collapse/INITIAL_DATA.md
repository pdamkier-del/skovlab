# Initial data: independent choices and constraints

## General ECD, not implemented

On a spacelike slice supply six spatial metric components, six extrinsic-curvature components and four complex components per classical Dirac species. Choose topology, asymptotics, lapse/shift evolution, an orthonormal spatial triad and its rotation gauge. The four gravitational constraints couple geometry and spinor-derived stress. No separately chosen density, pressure or spin profile may contradict those fields. The spin connection/source must be evaluated consistently, including replacing time derivatives through the Dirac equation where necessary.

For an asymptotically flat slice, in an admissible asymptotically Cartesian chart,

$$M_{ADM}=\frac1{16\pi G}\lim_{r\to\infty}\int_{S_r}(\partial_j\gamma_{ij}-\partial_i\gamma_{jj})\,dS^i.$$

This requires falloff, constraints and the usual asymptotic hypotheses. It is not $\rho$ times coordinate volume, nor a Misner–Sharp mass. Prescribing a target ADM mass, cloud size and collapse profile means solving a nonlinear constrained inverse problem; no such algorithm is delivered here. A conformal constraint construction with actual Dirac source, positivity/existence analysis and asymptotically flat boundary treatment remains necessary.

## Implemented branch

| Input | Role / restriction |
|---|---|
| $m\geq0$ | Neutral classical field mass; UI uses positive $m$ to define rest content. |
| $n_0\geq0$ | Single-spinor current density; derived in the UI. |
| $L_0>0$ | Physical initial edge of a followed homogeneous coordinate cell; all initial scale factors normalized to one. |
| $D_0$ | Initial longitudinal-minus-transverse rate, signed. UI sets $D_0=r\sqrt{E_0}$. |
| Spin $\pm z$ | Uniform orientation only, allowed by the LRS stress equations. |
| Collapse branch | Negative Hamiltonian root; not an independent rate. |

The UI selects $M_{rest},L_0,m,r$ and sign, then computes

$$n_0=M_{rest}/(mL_0^3),\quad E_0=mn_0+G_A n_0^2,\quad D_0=r\sqrt{E_0},\quad H_0=-\sqrt{(\kappa E_0+D_0^2/3)/3}.$$

Initial phase is fixed to zero by the global U(1) symmetry. $a_0=b_0=1$ is a coordinate normalization. No additional spin transport or initial pressure data are needed. Hamiltonian is checked numerically; three momentum constraints vanish exactly. The Dirac equation fixes its time derivative. Initial off-diagonal stress is zero because transverse rates agree and the axial vector is longitudinal.

Negative density/mass, nonpositive length, nonfinite parameters, invalid spin sign, inconsistent supplied $H_0$, and data at/above the cutoff are rejected with explicit errors. The UI contains no independent $H_0$ slider. Large rest content or a small cell can thus be refused. Larger $L_0$ at fixed rest content reduces density and initial contraction; increasing $M_{rest}$ increases both. Initial shear also increases $|H_0|$. Spin sign alone does not change volume evolution.

The periodic homogeneous domain has no ADM mass or exterior. The conserved number $\mathcal N=n v L_0^3$ and rest content $m\mathcal N$ are valid here. The total matter energy in the cell, $E v L_0^3$, is **not** conserved: it satisfies $d(EV)=-P\,dV$. No general local gravitational energy density is introduced to force a constant total.
