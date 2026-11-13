# Two matter models: decision and next derivation

Research date: 13 November 2026. The earlier [spherical](../ec-spherical/full-weyssenhoff/README.md) and [matter-model](../ec-matter-models/LITERATURE_REVIEW.md) audits were reviewed and are preserved. This stage performs a limited covariant/ADM compatibility comparison, not a full 3+1 expansion or simulation.

## Answers to the five questions

| Question | Assessment |
|---|---|
| **1. Which is more physically appropriate for a fermion cloud?** | **B's quantum statistical description**, once interactions, Pauli statistics and correlations are correctly included. The selected curved collisionless and flat dilute collisional papers do not together provide that complete dense model. One classical A spinor is not a many-body gas. |
| **2. Which has better-established equations for a first coupled EC calculation?** | **A, a specified minimal classical ECD action.** Its Cartan source, contact interaction, Dirac equations and variational stress are explicit. The dense quantum-state version still requires correlation/renormalization input. |
| **3. Which describes tidal deformation more realistically?** | **B at the many-particle level**, through a direction-dependent momentum/spin distribution and nonequilibrium stress, within its gradient/quasiparticle regime. A wave fields can deform too, but an individual field is not a kinetic distribution. |
| **4. Which has a credible vacuum-exterior route?** | **A has the clearer local mathematical route:** smooth compact neutral classical field data and a source-free collar, subject to Einstein constraints and regular evolution. B's leading moments can vanish outside a cloud, but its full spin/correlation/collision edge is not established. Neither has a global exterior solution here. |
| **5. Which first fully coupled derivation?** | **Primary A: neutral minimal ECD as an action-based mathematical benchmark. Backup B: a kinetic limit derived from the same microscopic action after closure/source matching.** This is a work-sequence choice, not a replacement of the prior physical goal of interacting EC–SM/QCD matter. |

## Exact equations to derive/check next

For **A**, use the already fixed action and derive the complete constrained initial-data/Cauchy system from this equation set:

$$
G_{\mu\nu}=\kappa T_{\mu\nu}^{\rm eff},\quad
T_{abc}=\frac{\kappa}{2}\epsilon_{abcd}J_5^d,\quad
C_{abc}=T_{abc}/2,
$$
$$
i\gamma^\mu D^\circ_\mu\psi_f-m_f\psi_f
-2G_AJ_{5\mu}\gamma_5\gamma^\mu\psi_f=0,\qquad G_A=3\kappa/16,
$$
$$
T_{\mu\nu}^{\rm eff}=-\frac2e\frac{\delta S_{m,\rm eff}}{\delta g^{\mu\nu}},
\qquad \nabla_\mu T_{\rm eff}^{\mu\nu}=0,\qquad\nabla_\mu j^\mu=0.
$$

The four ADM constraints and metric evolution are given in [ADM_COMPATIBILITY.md](ADM_COMPATIBILITY.md). The next calculation must explicitly project the field stress onto $E,j_i,S_{ij}$, choose a regular gauge/spin frame, solve gravitational constraints with smooth localized field data, and establish local support/continuation. It must not specify density, pressure, axial current and spinors independently. If charge is retained, Maxwell and Gauss constraints join the system; an exterior electromagnetic field would fail the requested GR-vacuum condition.

For **B**, start from the same ECD operator theory, not a replacement fluid:

$$
(i\gamma^\mu D_\mu^\circ-m)_x S^<(x,y)
=2G_A\gamma_5\gamma^\mu
\langle\bar\psi(y)J_{5\mu}(x)\psi(x)\rangle,
$$

together with the adjoint equation in $y$. Derive a chosen controlled self-energy/correlation approximation, its covariant Wigner transform, mass-shell constraints, spin transport, and the matching

$$
\langle J_5^\mu\rangle=\int_p\operatorname{tr}(\gamma_5\gamma^\mu W),\quad
T_{\mu\nu}^{\rm eff}=\langle T_{\mu\nu}[S_{\rm eff}]\rangle_{\rm ren}.
$$

The second relation includes the contact **four-point** contribution; it is not just $\int p_\mu p_\nu f$. Derive collision terms for the specified interactions at the same approximation order, including dense-medium statistics if needed, and check energy/spin Ward identities and exterior support. A Hartree closure with zero mean axial current would discard exchange/connected effects. No closure or collision coefficient is selected to obtain a bounce.

## What is established and what remains open?

- **Established / checked:** the prior ECD action and coefficient; classical Fierz/current identities; source-projection and focusing relations; a distribution's capacity for anisotropic stress; necessary local vacuum and contortion regularity conditions.
- **Conditional:** classical compact-support evolution assumes a regular hyperbolic solution with compatible metric data. Quantum kinetic moments assume a declared semiclassical/quasiparticle regime and source convention.
- **Open:** the complete dense curved-EC kinetic closure and its stability, quantum correlation support, full spinful interface formalism, realistic interaction matching and any actual regular bounce solution.

The identified classical kinetic EC paper, [Calogero 2410.20988v2](https://arxiv.org/pdf/2410.20988v2), prevents a blanket claim that no EC kinetic models exist. It does not supply the quantum, collisional, degenerate closure requested here. The distinction refines the scope without changing the prior validated Weyssenhoff or ECD conclusions.

## Files and reproduction

The six reports are [Dirac](DIRAC_MODEL.md), [kinetic](KINETIC_MODEL.md), [ADM](ADM_COMPATIBILITY.md), [vacuum](VACUUM_MATCHING.md), [bounce](BOUNCE_FEASIBILITY.md) and this comparison. Primary citations and access/reproduction limits are included where used.

With the existing pinned SymPy and Node environment, run:

~~~sh
python -m pip install -r research/ec-spherical/requirements.txt
python research/ec-two-matter-models/validation/run_checks.py
~~~

The [validation record](validation-results.json) separates new limited checks, earlier regressions, application tests and unchanged-file evidence. Symbolic success is not physical validation. No simulation, numerical time evolution, UI, forced Schwarzschild exterior or simulator modification is part of this stage.
