# Choice of research direction

## Recommendation

Choose **B: analytical solutions and restricted bounce/no-bounce conditions**, focused on the existing six-field construction's state/scale interpretation and sensitivity to anisotropy. Use a small, supervised piece of D to test physical admissibility. Do not begin a broad quantum-statistical collapse program or enlarge the full solver now.

This is a research project with possible negative results. Showing that a classical bounce has no demonstrated controlled fermionic realization, or finding a precisely stated instability, is scientifically useful. Neither outcome is a reason to tune the action or initial state until a desired bounce appears.

The comparison below is relative to this repository and a third-semester physics student's position. It is a judgment, not a quantitative measure of novelty. No exhaustive priority search has established that any result is publishably new.

| Direction | Scientific value / potential novelty | Mathematical difficulty | Numerical feasibility | Physical realism | Risk of inconclusive work | Background and external expertise |
|---|---|---|---|---|---|---|
| A. Improve full 3+1 ECD | Valuable verification infrastructure; feature growth alone has limited novelty. A rigorous coupled/boundary analysis could be significant | Very high for full constrained gauge/boundary and strong-field control | Short benchmarks feasible; reliable collapse expensive | Remains low for real fermion matter unless state problem is solved | High: gauge, boundary, resolution and state errors can obscure every outcome | Numerical relativity, hyperbolic/elliptic PDE, spin geometry, convergence analysis; numerical-relativity mentor |
| B. Analytical conditions and solutions | High diagnostic value; narrow robustness/admissibility results could be new after literature review | Moderate for background identities; high for general theorems. Finite homogeneous perturbations are a bounded first target | Symbolic work and existing-operator checks feasible; no new simulation required initially | Explicitly limited, but cleanly exposes what a physical interpretation would require | Lower if question and hypotheses are fixed; universal classification would have high risk | GR, tetrads, Dirac bilinears, constrained dynamics, linear perturbations; GR/mathematical-physics reviewer |
| C. Simpler physically justified collapse | Strong learning value and a route to meaningful baseline observables; ordinary GR reproduction has limited novelty | Moderate for spherical GR dust; higher for Euler/free boundaries or kinetic matter | Most feasible if a known well-posed model and boundary problem are chosen | Good within its declared regime; a realistic ordinary model need not contain a significant torsion effect | Moderate; lower with known benchmarks and explicit stop criteria | GR, thermodynamics or kinetic theory, numerical analysis; collapse-model mentor |
| D. Quantum-statistical fermions | Addresses the core physical gap; a state-specific torsion correlator could be valuable | Very high in dense interacting curved matter; a free-state leading-order calculation is bounded | Equilibrium integrals feasible; full nonequilibrium quantum gravity/matter evolution unsuitable here | Best direction in principle, conditional on approximations and state | Very high if expanded to QCD/SM collapse; manageable for one explicitly limited correlator question | Second quantization, Wick contraction, renormalization, EFT, finite-density QFT; mandatory QFT/finite-density guidance |

## Why B should lead now

1. **The classical model already gives opposite outcomes in distinct states.** The aligned one-field branch focuses, the planar gradient state turns without torsion, and the six-field chiral state bounces because of torsion. This is evidence that state restrictions and source structure are the decisive variables.
2. **The exact six-field background removes many numerical ambiguities.** Its full field equations and stress can be checked, and perturbations can be restricted explicitly. Failure of robustness would be informative without first solving a three-dimensional boundary problem.
3. **The scale warning can be tested before an expensive evolution.** In the simple one-occupation normalization the bounce is far above reduced-Planck energy density. A free-state correlator and validity map can determine what, if anything, the classical amplitudes mean.
4. **The current solver is not yet an appropriate arbiter of this question.** It evolves one species, whereas the positive torsion-attributed example uses six. Adding fields, boundaries, strong gravity and horizon finding at once would confound interpretation.
5. **The project owner can learn the core geometry while working on a finite question.** Advanced quantum calculations should be supervised and delimited rather than presented as independent undergraduate prerequisites for a complete EC–SM theory.

Do not overstate B's physical promise: the exact background may remain only a mathematical benchmark. That is a valid endpoint.

## What to keep, defer and reject

**Keep:** corrected conventions, full stress, operator checks, exact LRS and six-field backgrounds, the planar counterexample, and weak-field engine/tracer work with its uncertainty labels.

**Defer:** new strong-collapse features, multi-species production code, horizon finders and realistic nuclear/QCD coupling until a specific scientific question survives the state/scale review.

**Reject as a shortcut:** using the old ill-behaved dust-plus-spin fluid merely because its ODE bounces; identifying convergence with physical validity; assuming “positive frequency” means a pointwise positive gradient trace; interpreting total cosmological expansion as inflation; prescribing a vacuum exterior by fixing outer metric values.

The earlier preference for full EC–SM/QCD-matched matter describes the most realistic eventual framework. It does not identify the best next executable task. A broad microscopic action without a controlled state can be less useful than a narrow benchmark whose limits are explicitly known.

## When C or D should become primary

If the owner principally wants **realistic finite-body collapse**, and Task 1 finds no controlled torsion-dominant regime in the selected matter state, switch to C: a standard spherical GR collapse baseline with known initial/exterior data, adding only a perturbatively justified torsion estimate if one is available. Dust/LTB is useful before caustics; a degenerate fermion system may require an occupation-limited kinetic distribution or a justified fluid EOS. Choose collisions versus collisionless transport by mean-free-path/time scales, rather than assuming either.

This would be a different scoped project, not a claim that realistic torsion collapse has been solved. It should not be built during this audit.

D should become primary only with a finite-density/QFT collaborator and one defined species/state/density regime. Start with the correlator and stress, not a full quantum collapse solver. A Wigner or spin-kinetic description is promising, but the [corrected collisionless curved-spacetime framework](https://arxiv.org/abs/2002.03753v4) is not an automatic dense collisional EC completion.

A should become primary only if the goal is explicitly classical numerical relativity and an external reviewer accepts the continuum formulation and finite-domain target. Fixing the periodic charge diagnostic is a small future correction; it does not solve the wider scientific gap.

## Research question to use as a title

**“Admissibility and anisotropic robustness of a minimal Einstein–Cartan six-field bounce.”**

This title states what can be investigated. It does not promise a realistic bounce, singularity resolution or a baby universe. The three tasks and explicit decisions are in [NEXT_STEPS.md](NEXT_STEPS.md).
