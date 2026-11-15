# Programme log

Date: 2026-11-15, Europe/Copenhagen. Stop condition is all B1–B7, not just a mathematical turn. The original master prompt takes precedence over issue #4's older directory suggestion; quantum-fermion documents are nested under `models/01_quantum_fermions/` in the new requested `ec-bounce-programme/`.

## Audit of starting state

Read issue #4 and the actual branch heads. Main=d069bfac8398cc71793c542ad93d650cc511794c; PR #2=a3421e7c06b89b2c6c4edc7412de1c6545092358; PR #3=47167c304c4c5bf8700066f2bfa94ba48864d3e0. Main and branch research records, single-spinor limitations, local analytical turn and six-field benchmark were reviewed. Five priority branch documents were refetched and compared byte-for-text with local copies; SHA256 provenance is recorded. No repository AGENTS.md was present in the main recursive tree. Existing numerical trajectories and benchmark audits were not repeated.

## P01 — Particle/antiparticle quantum correlator

Hypothesis: replacing a classical squared current by a genuine fermion correlator changes the thermal source. Derived the coincident Wick expression for arbitrary independent isotropic massless Weyl charges, retaining interspecies Hartree and same-species exchange. Built a fresh 256-dimensional sparse Fock operator with full quartic vacuum normal ordering and particle/antiparticle terms. Seventeen ensembles agree within 3.56e−15. A massless charge-symmetric thermal gas has zero order-G contact expectation in this prescription, despite nonzero particle density and contact noise. A general spin-variance-density closure cannot be assumed. Result 01 and correlator/state documents preserve scope and fluctuations caveats.

## P02 — Sharp occupation bound and conserved order-G stress

Hypothesis: temperature, charge imbalance or species may permit a small-contact controlled bounce. Derived the sharp continuum compact-support Pauli bound r≤(g+1)κΛ²/(24π²); verified 800 arbitrary shell spectra and saturation. Eight thermal quadratures match independent analytic expressions. Derived grand-canonical and fixed-entropy/charge stress from one potential; susceptibility inversion and adiabatic conservation pass symbolic checks. The formal source turns only at order-one correction, with unresolved higher-order control; this is a restricted no-bounce result where the explicit positive-energy/remainder inequality holds. No dynamics launched. Results 02–03 and stress/bound documents are the first milestone.


## P03 — Massive matter and rest-energy loophole

Derived the full unpolarized massive Wick trace using fresh SymPy gamma matrices. Verified massive thermal integrals and a Pauli low-momentum inequality, recovering the prior nonrelativistic coefficient only as a limit. Investigated a specific cold μ=m gas plus photons: an apparent radiation-only cancellation at m=0.1,T/m≈4.03579e−5 omits fermion positive energy ≈1.42739e10 times the radiation. With the full source the contact fraction is ≈7.00582e−11, so there is no turn at that point. This does not refute an unspecified nonequilibrium correlated state. Artifacts: result 04, cold-gas document, massive section in result 03. No expensive evolution justified.

## P04 — Matched spinfluid gate and published action triage

Compared the same microscopic massless symmetric ensemble against a universal spin-variance ∝n_total² fluid closure; the first-order mismatch prevents that identification from serving as a universal minimal-ECD derivation. Preserved prior conditional fluid mathematics without rerunning it. Motivated by the missing correlations, inspected Lucat–Prokopec's actual generalized action and 2PI/validity sections, translated coefficient magnitude, and recorded a printed parameter/cutoff hierarchy tension. Did not reproduce its dynamical solution or declare it refuted. Full minimal quantum-state question remains higher priority; Holst/extra actions were not scanned or fabricated.

## Final validation and handoff

The four small computation scripts and separate source-scale arithmetic completed with assertions passing. The integration validator reruns independent reference computations and checks the sharp bound, operator error, thermal symmetric cancellation, conservation, massive sign and positive-rest-energy result. No new spatial/time evolution occurred, so no checkpoints or spatial refinement are claimed. B1–B7 matrix, model registry, negative findings, Danish report and exact continuation are updated. Meaningful commits separate the quantum-source milestone from the cold-gas/matching/acceptance handoff. Stop classification is C; no accepted Level B or universal scientific obstruction is claimed.


## P05 — Full covariance dynamics before gravity

Continued from c4192f9 on the actual programme branch; main and PR #2/#3 remain at their reviewed heads. Read the saved status, registry, acceptance matrix and continuation. Revisited the actual local Hartree/Fock source equations. Derived a fixed-Minkowski vacuum-Wick Hamiltonian functional and its matrix variational self-energy; generic matrix directional differences check the gradient independently. Prepared the predeclared m=.1,T=.001,mu=m state and verified full covariance eigenvalues against FD occupations at 48/96/192 radial nodes and independent adaptive integrals.

Added one fixed coherent eigenvector rotation of amplitude .05 (no occupation retuning), then evolved both helicity Bloch vectors at fixed geometry. Independent DOP853 reference and RK4 64/128/256 give error ratios 15.9846/15.9970; charge, full energy and occupation drift are recorded separately. Momentum quadrature converges; finite cutoff dependence is preserved as a limitation, not called renormalized away. Initial and final mode arrays are retained in JSON. This is a finite-cutoff Gaussian matter validation, not full cosmological backreaction or a quantum bounce.

## P06 — Component generator and subtraction consistency

Independently differentiated the squared Bloch length of the printed local component equations. Found a nonzero generic polynomial defect if interpreted as full covariance Hartree–Fock. Verified it on admissible finite covariance data and derived the necessary cross-product completion only as a diagnostic. Because the paper's currents are subtracted/approximated, this does not prove a physical Pauli violation or refute its full 2PI theory. Derived the exact full-to-subtracted covariance identity, including reference commutator and projector time derivative. Decision: do not naively use the printed components as a physical source; resolve subtraction and approximation order first. Artifact: result 07 and component-consistency document.

## P07 — Pauli bound including particle–antiparticle coherence

Asked whether the newly admissible coherent sector evades the old no-pairing Gaussian occupation bound. Derived an amplitude-independent inequality B<=5 I rho_free/2 from positivity of the full covariance, with I<=Lambda^2/(2pi^2). It covers the specified isotropic parity-even Dirac Gaussian sector including arbitrary mode-dependent coherence, but not general non-Gaussian/curved-space sources. Checked 1200 admissible covariances plus independent integration. At m=Lambda=.1 the contact fraction is bounded by .000126534; the declared coherent example is about 2.08e-7. Hence this weak coherent Gaussian branch still supplies no controlled flat bounce. Artifact: result 08 and coherent-state proof.

## Continuation decision after P07

No Level B. Full quantum ECD remains INCONCLUSIVE, with narrower tested weak Gaussian/coherent branches excluded under their explicit source/remainder assumptions. The next scientific gate is a consistently subtracted, conserved dynamical stress and a controlled connected four-point/error estimate beyond local Hartree–Fock. Do not repeat the fixed-background trajectory or insert the diagnostic component repair into cosmological evolution. Source/state problems still precede any new gravitational evolution. No general inhomogeneous assessment, full curved-space renormalization, stress-noise computation or UV completion has been performed.
