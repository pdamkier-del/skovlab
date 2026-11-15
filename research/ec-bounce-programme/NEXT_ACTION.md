# Exact continuation after P07

Latest verified programme head before this continuation was c4192f955e579ba67058b0e3375e38ec8e18c4f4 (PR #5). P05–P07 extend that same draft PR by new commits; main, PR #2 and PR #3 are untouched. Read MASTER_STATUS, the final log entries, and the three new derivations. No Level B candidate; STOP C remains a bounded handoff, not universal STOP B.

## Do not repeat completed work

P01–P04 operator/gas bounds and old classical trajectories are complete. P05 fixed-Minkowski covariance validation, P06 component algebra and P07 coherent-state bound are also complete. Do not run more weak coherent HF trajectories as a supposed search for a bounce: the declared sector already has an amplitude-independent conditional energy bound. Do not insert the diagnostic component completion into a cosmological solver as though it were the derived renormalized theory.

## Highest-priority next cycle: connected source and subtraction control

Keep minimal ξ=1 ECD primary. The local Gaussian HF dynamics preserves covariance spectra and energy, but does not generate an independently controlled connected four-point cumulant. The old occupation bound has now been extended to arbitrary particle–antiparticle coherence in one isotropic parity-even Gaussian sector. To evade it requires a specifically identified term or a genuinely different state class, not a larger coherent amplitude.

1. Derive the full equal-time covariance and stress from a declared renormalized dynamical approximation. Explicitly account for i Cdot=[h0+Sigma,C]+[Sigma,Pminus]−i Pminus_dot. Test the exact free limit, full Pauli spectrum and the metric variation of the same effective functional. In a changing geometry the reference projector is time-dependent. A finite fixed-Minkowski subtraction or a conserving truncation alone does not certify covariant renormalization or its remainder.
2. Smallest feasible independent test: compare exact finite-mode quartic quantum evolution to its Gaussian HF approximation for a declared particle/antiparticle state. Use a cutoff/volume and mode-complete Hamiltonian whose contractions are derived, not a postulated negative pressure. Calculate the connected axial four-point function Q_exact−Q_Wick(C_exact), energy, occupations and their leading coupling dependence. Include vacuum dressing/reference energy consistently. Such a finite-mode test estimates truncation effects in that regulator; it is not a closed continuum QFT or a physical bounce. Do not silently treat the old local-mode Fock operator as a complete scattering theory.
3. If a controlled connected-source candidate emerges, derive a continuum error/matching bound and spacetime-smeared stress noise. Only then formulate constrained semiclassical geometric evolution and its independent torsion-free control. No general 3D build is justified before this gate.

## Nonminimal source cross-check

For the inspected Lucat–Prokopec source, resolve exactly what the regular component currents mean and which approximations produced the printed equal-time system. Its generic squared-Bloch-length defect is a necessary consistency warning for a naive full-covariance interpretation, not a proof against the renormalized theory. Recover the subtraction/counterterm terms and their approximation order before claiming occupation violation or implementing it numerically. Preserve the earlier cold-rest-energy and printed mass/cutoff checks; do not rerun them as discoveries. No coupling scan as a substitute for validity.

## Data and reproduction

Run `OPENBLAS_NUM_THREADS=1 python code/validate_covariance_cycles.py` for the new cycles only. Results 06/07/08 record matrix HF validation, component consistency and the coherent-state bound. `results/06_covariance_modes.json` retains all initial/final full Bloch modes at 96 radial nodes, fixed vacuum, momenta/weights, trace charges and reconstruction formula. These can restart fixed-background matter evolution at t=100, although no longer trajectory is scientifically prioritized. Temporal tests are 64/128/256 against DOP853; momentum quadrature 48/96/192; cutoffs .08/.10/.12 preserve a measured unresolved matching dependence.

`results/covariance_validation.json` contains source/evidence hashes and a checkpoint spectral check. The old validator/results remain provenance and need not be rerun unless changed. No gravitational evolution, full stress/noise or B6 inhomogeneous assessment was performed in P05–P07.

Update the registry, B1–B7 table, falsification/log and exact next action after a completed cycle. Models 4–5 remain NOT YET INVESTIGATED until a specific justified action is selected. If connected-source/renormalization control is unavailable, state that explicitly rather than inventing a no-go or continuing costly geometry with an assumed source.
