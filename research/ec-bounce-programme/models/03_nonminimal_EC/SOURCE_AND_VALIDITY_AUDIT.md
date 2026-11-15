# Model 3 — preliminary action/validity audit, not accepted candidate

**INCONCLUSIVE; literature triage and independent restricted-state checks only.** The full 2PI equations, renormalization and perturbations have not been reproduced.

[Lucat and Prokopec, arXiv:1512.06074v1](https://arxiv.org/html/1512.06074v1) is the inspected primary source. Eq. (7) has arbitrary axial torsion coupling ξ (and a vector coefficient set to zero in their main treatment); Eq. (9) gives an effective contact of magnitude 3πG_Nξ²/2. Their signature differs: in our conventions the corresponding magnitude is G_eff=3κξ²/16. It is a separate model when ξ≠1. They use nonequilibrium 2PI/Hartree–Fock backreaction and discuss its perturbative renormalization. Sec. VI acknowledges loss of control for relativistic near-equilibrium bounces and proposes a cold nonequilibrium route.

Independent consequences of the declared coefficient: increasing |ξ| lowers a formal contact momentum scale and also its interaction validity scale. In our Gaussian cutoff class, replace G_A by G_eff in the proven bound r≤2(g+1)G_effΛ²/(9π²); lowering the formal turn scale alone does not create a small contact expansion. A controlled resummation or ultraviolet matching could alter this conclusion, but must be exhibited rather than inferred from a sub-Planckian temperature.

The cold free-gas check in Model 1 gives a precise question for that proposed route: does its source retain the fermion rest/kinetic energy and an admissible Pauli covariance while the nonequilibrium correlator grows enough to cause a turn? Equating a density-squared term with radiation alone fails in our equilibrium reference state by a factor ≈1.43e10. This is **not** a reproduction or disproof of the paper's dynamical 2PI solution.

A separate parameter consistency check: the printed Figure 5 values ξ≈1000, m/T0≈100, T0≈0.001M_P imply m≈0.1M_P and ξm/M_P≈100. That does not satisfy the small-mass hierarchy invoked alongside the quoted scale M_P/|ξ| in Sec. VI. Different Planck normalizations cannot produce a parametric hierarchy here. This diagnostic does not prove a heavy-particle EFT is impossible: a separately matched nonrelativistic EFT could have a different domain, but its matching/control is not established by this figure. Curvature below a quoted scale alone cannot settle the matter.

Next gate: translate the actual action and renormalized covariance/stress consistently, then audit Pauli eigenvalues, energy bookkeeping, masses, cutoff, omitted diagrams and noise before numerical reproduction. Ghost/gradient spectra, full torsionful regularity, independently constrained attribution and genuine inhomogeneous robustness remain unchecked. No acceptance by citation and no tuning ξ until a bounce appears.

Arithmetic provenance: `code/source_scale_check.py` and `results/05_nonminimal_source_scale.json`; this records approximate printed parameters, not an exact unitarity bound.

P06 adds `COMPONENT_CONSISTENCY.md`: the printed component generator has a generic norm defect under a full-covariance interpretation. Regular/subtracted currents require their own reference map, so this is not a refutation of the physical 2PI solution. The full theory remains INCONCLUSIVE.
