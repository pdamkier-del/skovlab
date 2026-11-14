# Independent scientific audit of ECD collapse

Audit date: 14 November 2026. Repository: pdamkier-del/skovlab. Reviewed baseline: [d069bfac8398cc71793c542ad93d650cc511794c](https://github.com/pdamkier-del/skovlab/tree/d069bfac8398cc71793c542ad93d650cc511794c). All statements about existing code refer to that snapshot.

## Judgment

The project has established useful classical-field mathematics, exposed failures of an earlier fluid closure, and implemented a genuinely spatially varying ECD prototype with reproducible short weak-field convergence. It has **not** established a regular torsion-induced bounce of a finite collapsing body, a black-hole interior continuation, or a realistic fermionic collapse prediction.

The strongest next direction is **B: a bounded analytical investigation of the existing six-field benchmark's admissibility and robustness**, beginning with its physical state and scale assumptions. Keep the current solver as a benchmark instrument. Expanding it into a strong-collapse code before resolving the matter interpretation would be a costly way to obtain results of uncertain meaning.

## Evidence standard and review coverage

“Established” below means supported within specified equations and assumptions; it does not mean experimentally validated. “Reproduced” means executed in this audit. “Missing” means no sufficient evidence in the reviewed material, rather than a demonstrated impossibility.

The review followed all nine research commits from the spherical audit (3efc961, 10 November) through the two Weyssenhoff models (e5e8aa6), matter-model comparison (7e1fc4a), Dirac/kinetic comparison (efeb67c), LRS implementation and refinement (793a935, fabd0ee), general solver (84a9756), planar construction (183bd20), and general/chiral investigation (d069bfa). The seven requested research directories, their theoretical reports, relevant LaTeX source, implementation, test source, and saved numerical records were examined. Compiled PDFs were not separately compared against their editable sources; browser workflows were not rerun. This is an independent targeted audit, not a line-by-line formal verification or exhaustive literature/priority search.

### What each stage actually contributes

| Research stage | Supported contribution | Essential limitation |
|---|---|---|
| ec-spherical, including full-weyssenhoff | Spherical geometry, conditional effective-source equations, material characteristic analysis, symmetry and boundary restrictions | Neither a general closed spin-correlation theory nor a finite-cloud evolution |
| ec-matter-models | Minimal axial contact and state-dependent exchange example; useful scale audit | No renormalized dense interacting EOS or transport closure |
| ec-two-matter-models | Distinguishes classical fields from quantum spin kinetics; ADM and matching requirements | Listed kinetic literature does not supply a ready dense curved-EC solver |
| ec-dirac-collapse | Exact aligned LRS field branch, full source, exact volume benchmark and no-volume-bounce result | Homogeneous, positive-density branch only |
| ec-full-3plus1 | General local field components, constrained finite-box data, harmonic evolution, weak-field tests | One species, short times, artificial outer data, no physical exterior |
| ec-analytical-bounce | Constrained analytic planar data with a regular local current-volume minimum | Not finite, not a trapped collapse, and not caused by torsion |
| ec-general-investigation | Current/volume identities, conditional compression obstruction, passive tracers, exact six-field cosmological bounce | Single-field identities cannot be transferred to several fields or quantum expectations |

The earlier torsion-orientation error is explicitly superseded by [CONVENTION_AUDIT.md](../ec-full-3plus1/CONVENTION_AUDIT.md). Older wording must not be used as an independent confirmation of the corrected convention.

## Is classical minimal ECD meaningful?

Yes, as an action-defined nonlinear classical field theory and a mathematical benchmark. It tests spinor geometry, self-gravitating wave evolution, constraints and the consequences of algebraic torsion without guessing a pressure law.

A complex commuting spinor is not automatically a gas of fermions. A one-particle wave function can give useful bilinears on a prescribed background in a controlled one-particle regime. Feeding those bilinears back into classical gravity introduces an additional semiclassical approximation; the nonlinear self-interaction does not thereby become an exact one-particle quantum evolution. A finite collection of modes can be a mean-field ansatz only after its state, occupations and neglected correlations are justified.

In a fermion-parity invariant quantum state the expectation of a single fermionic field vanishes. Useful macroscopic observables are even operators, such as stress, currents and correlation functions. Fermions have no unrestricted bosonic coherent occupation of a single mode. Classical amplitudes in this project have no built-in Pauli bound.

The present model can describe coherent field gradients, polarization bilinears, anisotropic stress, classical wave transport and their gravitational backreaction. It does not itself provide Fermi pressure, exchange, pairing, nuclear/QCD interactions, composition changes, collisions, realistic particle production or a renormalized quantum stress. Negative-frequency content in an unrestricted classical solution cannot simply be renamed an occupied antiparticle state while retaining the same classical stress.

### The state is part of the physics

For quantum matter the effective contact involves

\[
G_A\langle[A_\mu A^\mu]_{\rm ren}\rangle,\qquad
A^\mu=\sum_f\bar\psi_f\gamma_5\gamma^\mu\psi_f,
\]

rather than a universally interchangeable square of the mean axial current. An unpolarized state can have zero mean axial current and nonzero exchange/correlations. Conversely, cancellation of classical species currents can remove the classical interaction. The distinction is discussed explicitly by [Dolan (2009/2010)](https://arxiv.org/html/0911.1636v2); it is not resolved by more grid points.

The repository's normal-ordered nonrelativistic free-sea example gives
\(\Delta\epsilon=\Delta P=-3G_A n^2(1-\zeta^2)/2\).
Its sign and coefficient can be checked by Wick contraction. It is a first-order result for that reference state, not a universal fermion EOS, a nuclear result, or a high-density stability theorem.

## Physical scales and restrictions on bounce claims

Minimal torsion is auxiliary, with no independent propagating torsion field. Eliminating it gives a fixed dimension-six axial interaction; the minimal coefficient agrees with Eq. (2), at zero nonminimal couplings, of [Shaposhnikov et al.](https://arxiv.org/html/2008.11686v2). The mechanism is state-dependent, not universal repulsion.

With \(\kappa=\bar M_P^{-2}\), \(G_A=3\kappa/16\), a relativistic gas has schematically \(\epsilon_0\sim p_F^4\), \(n\sim p_F^3\) and \(|\Delta\epsilon|/\epsilon_0\sim\kappa p_F^2\), subject to calculated species/correlation factors. For fixed ordinary species without a justified enhancement, dominance is at an uncontrolled Planckian scale. At nuclear density the repository's order-of-magnitude ratio \(G_A n/m_n\simeq4.1\times10^{-41}\) is consistent. Extrapolating a nonrelativistic \(mn\) balance to enormous density misses the earlier onset of relativistic momenta and nucleon compositeness.

A controlled interpretation needs microscopic momenta and inverse gradient lengths below a declared cutoff, small relevant curvature scales in cutoff units, a controlled quantum state and sufficiently small omitted corrections. Small curvature alone does not establish occupation admissibility. Conversely, weak fields in reduced Planck units can be a numerical benchmark without corresponding to an astrophysical star.

There is no general classical ECD no-bounce theorem here. The single-field Fierz identity, conditional focusing bounds and fluid hyperbolicity failure have restricted hypotheses. The multi-field cosmological counterexample genuinely matters mathematically. It does not evade the physical validity questions by being an exact solution.

## What is the largest obstacle?

The missing bridge from freely chosen commuting spinor data to a physically specified fermionic state in a controlled regime is the central scientific obstacle. Independent numerical obstacles—boundaries, strong-field convergence, regularity diagnostics and global geometry—remain substantial even if that bridge is built.

The prior recommendation to begin with full EC–Standard-Model/QCD-matched matter identifies a long-term realistic target. It is too broad as this student's immediate project. A sharply delimited state/scale calculation and analytical robustness study are more feasible and more diagnostic. The next three tasks and decision gates are in [NEXT_STEPS.md](NEXT_STEPS.md).

## Primary-source checks and their scope

| Source inspected | What it supports | What is not imported |
|---|---|---|
| [Hehl–Datta, 1971, DOI](https://doi.org/10.1063/1.1665738) | Original nonlinear spinor/torsion identification; bibliographic record checked | Original full text was not independently available for complete reproduction |
| [Shaposhnikov et al., 2008.11686v2, Eqs. 1–2](https://arxiv.org/html/2008.11686v2) | Total-current contact, minimal coefficient and Planck suppression | Their dark-matter scenario or nonminimal parameter choices |
| [Bréchet–Hobson–Lasenby, 0706.2367v2, Eqs. 24–29](https://arxiv.org/html/0706.2367v2) | Selected Weyssenhoff source and spin transport | A universal microscopic EOS or full perturbed-cloud stability |
| [Hashemi–Jalalzadeh–Ziaie, 1407.4103v2](https://arxiv.org/html/1407.4103v2) | Homogeneous spin-fluid bounce under its assumptions | A vacuum exterior: the paper itself discusses generalized Vaidya matching |
| [Müller–Nowaczyk, 1504.01034v3, Lemma 3.20](https://arxiv.org/html/1504.01034v3) | Torsion-free Einstein–Dirac–Maxwell local Cauchy framework | A theorem for the present nonlinear discrete ECD scheme |
| [Lindblom et al., gr-qc/0512093v3](https://arxiv.org/html/gr-qc/0512093v3) | GH constraints and a specific hyperbolic formulation/boundary treatment | Its damping and boundary guarantees for this different implementation |
| [Liu–Mameda–Huang, 2002.03753v4](https://arxiv.org/abs/2002.03753v4) | Corrected curved-spacetime semiclassical collisionless spin kinetics | A ready dense collisional EC closure |

The numerical evidence, exact mathematical hypotheses and individual bounce classifications are documented separately in the companion files.
