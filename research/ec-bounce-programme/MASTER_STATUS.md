# EC bounce programme — verified status

2026-11-15, Europe/Copenhagen. **No Level B candidate.** Seven completed bounded cycles extend the earlier audit without repeating old trajectories. The highest-priority unresolved issue remains controlled quantum backreaction in Model 1; cheap matching/source checks of Models 2–3 were justified by the specific Gaussian-source obstruction.

## New verified results

P01: for independent isotropic massless Weyl Gaussian channels, particles and antiparticles included,

⟨:A²:⟩=−[(Σs_i d_i)²+Σd_i²],

where d_i is net charge, not total particle density. An independent 256-dimensional full quartic Fock construction agrees to 3.56e−15. A massless charge-symmetric reference gas has zero first-order expectation, with nonzero noise/higher-order questions.

P02: sharp Pauli cutoff bound r≤(g+1)κΛ²/(24π²), tested on 800 spectra and saturated explicitly. At fixed physical entropy/charges, the thermodynamically derived first-order corrections are Δρ=ΔP=−G_A B. At fixed T,μ they are +5G_AB,+G_AB; susceptibility shifts reconcile them. Formal adiabatic conservation passes. No all-orders dynamical stress/remainder is established.

P03: unpolarized massive Dirac reference Q=−D²/2−S²; low-momentum bound |Δρ|/ρ0≤G_A P³/(2π²m) for the specified particle-dominated gas. Including the positive rest energy removes a specific false low-temperature radiation cancellation by a factor ≈1.43e10.

P04: the same-state comparison rejects a universal spinfluid identification q∝n_total² for the massless symmetric Gaussian ensemble. The published nonminimal 2PI mechanism has been read and triaged, with action/scale and parameter hierarchy concerns recorded; its dynamics, renormalization, noise and inhomogeneous stability were **not** independently validated.

## Continuation P05–P07

P05: derived a finite-cutoff full-covariance Hartree–Fock Hamiltonian and verified its variational self-energy, energy and Pauli occupation. The predeclared massive thermal state and one fixed coherent eigenvector rotation were tested. Fixed-Minkowski matter evolution has RK4 error ratios 15.9846/15.9970 against DOP853; 48/96/192 momentum quadratures agree. Raw covariance modes are preserved. Cutoff dependence is measured, not claimed renormalized away. This is not gravitational evolution or full quantum error control.

P06: the printed component system has a nonzero generic Bloch-length defect if interpreted as full covariance dynamics. Its regular/subtracted currents require a derived reference map; the result is not a demonstrated physical Pauli violation by the published theory. The exact subtraction identity and the missing consistency gate are documented.

P07: extended the state bound to arbitrary particle–antiparticle coherence in one isotropic parity-even Gaussian Dirac sector. Full covariance positivity gives B≤(5/2)Iρ_free, I≤Λ²/(2π²), hence G_AB/ρ_free≤15κΛ²/(64π²). At m=Λ=.1M̄P the finite-mass bound is .000126534. The declared coherent example has contact fraction about 2.08e−7. This is not a bound for every non-Gaussian/curved-space source.

## Classifications and stopping

Model 1 INCONCLUSIVE overall, tested weak Gaussian flat-bounce branch REJECTED WITHIN ASSUMPTIONS. Model 2 INCONCLUSIVE overall, universal closure fails the specified matching test. Model 3 INCONCLUSIVE preliminary source audit. Models 4–5 NOT YET INVESTIGATED. No broad theory is declared impossible.

STOP C: finite execution handoff with precise next source/state calculation. Not STOP A (no B1–B7-complete candidate) or STOP B (justified model classes not exhausted). No gravitational bounce evolution was attempted after the validity gate failed; the new short fixed-background covariance test addresses matter consistency only. A small Hubble rate or sub-Planckian temperature alone cannot certify the source.

## Evidence categories

- **Mathematically established:** conditional Gaussian correlators, occupation/coherent-covariance bounds, exact regulated commutator conservation and first-order thermodynamic identities.
- **Numerically supported:** independent finite operators/traces, continuum quadratures, random shell/saturation checks, cold positive-energy counterexample and convergent fixed-background covariance dynamics.
- **Physically conditional:** weak matched free-reference-state perturbation; any dynamical/2PI extension requires separate control.
- **Unresolved/speculative:** controlled bounce, microscopic spinfluid closure outside the tested state, full nonminimal mechanism, B6, realistic collapse or baby universe.

## Navigation and provenance

`MODEL_REGISTRY.md` records actions/scopes and transitions; `ACCEPTANCE_CRITERIA.md` maps B1–B7; `RESEARCH_LOG.md` and `FALSIFICATION_LOG.md` preserve decisions; `OPEN_QUESTIONS.md` and `NEXT_ACTION.md` define continuation; `SUMMARY_DA.md` answers all seven requested questions. Quantum source details and issue #4's requested document topics are under `models/01_quantum_fermions/` rather than a duplicate programme directory.

Baseline main d069bfac8398cc71793c542ad93d650cc511794c. PR #2 and PR #3 were inspected at their actual heads and remain untouched; five remotely refetched priority documents match local text and are hashed in provenance. No prior validated research is overwritten or merged. Reproduction and numerical integrity are in `VALIDATION.md`. No output claims indefinite background execution.

P05–P07 reproduce with `python code/validate_covariance_cycles.py`; new source/evidence hashes and checkpoint spectral checks are in `results/covariance_validation.json`. The earlier results/validator remain separate.
