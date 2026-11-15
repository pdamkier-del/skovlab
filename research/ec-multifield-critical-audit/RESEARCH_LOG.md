# Critical programme research log

Date: 2026-11-15 UTC. New programme, separate from the earlier one-field autonomous work. Baseline main d069bfac8398cc71793c542ad93d650cc511794c. Old result inventories were read to avoid rerunning completed one-field studies. New code imports no old evolution engine.

## C01 — Independent action, equations and exact benchmark

Rebuilt gamma/connection/affine contractions in a Weyl basis; retained total-current cross terms; derived complete source. Eight generic auxiliary-connection cases passed. Checked lapse and axis variation before on-shell substitution, all field equations and symbolic Einstein/conservation residuals. Proved exact causal geodesic completeness and bounded curvature/torsion. Found no material error in the benchmark under the corrected convention. Found four tetrahedral fields suffice for isotropic stress. Artifacts: `field_source.py`, `verify_benchmark.py`, result 01, action/analytical documents.

## C02 — Physical fermion-state audit and gate decision

Built finite six-mode fermion operators independently, compared exact matrices and Wick traces for distinct species versus one species. Found the classical negative contact can match a specific distinct-species reference expectation, while same-species exchange changes its coefficient. Imposed Pauli fundamental-mode normalization; derived p_b≥14.8489 M̄P, ρ_b≥1175.94 M̄P⁴ and strong contact/curvature. Added six-species Fermi-sea estimate: formal cancellation also outside the controlled weak-coupling regime. Conclusion: no controlled physical bounce supplied. General multi-field 3D build is not justified. Artifacts: `fermion_state.py`, result 02, fermion validity document.

## C03 — Small classical robustness cycle after the physical audit

Permitted only a bounded homogeneous full-field ODE. Solved initial Hamiltonian separately for each perturbation and for the torsion-free action. Exact 64/128/256 RK4 refinement gives fourth-order convergence. Five perturbations at 128/256 steps retained a local volume turn with small constraint and charge residuals. Torsion-free control follows separate singular radiation solution. Derived paired massless volume convexity; repeated regular volume oscillations are excluded within this ansatz. No general spatial robustness or physical-state claim. Artifacts: `robustness.py`, result 03, robustness/numerical documents.

## C04 — Adversarial source/conservation checks and handoff

Independently checked anisotropic paired source and volume convexity; deliberately unbalanced one pair and detected nonzero momentum constraint. Checked energy conservation by directional finite differences, and off-shell energy at negative-phase-frequency bounce. Preserved all negative physical findings. Artifacts: `additional_checks.py`, result 04, falsification inventory, final status and precise next action. All four computation scripts completed with assertions passing. The programme stops at a clear quantum-state/EFT question, not at an unfinished expensive 3D infrastructure project.
