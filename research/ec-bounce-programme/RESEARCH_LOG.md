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
