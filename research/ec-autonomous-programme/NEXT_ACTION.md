# Exact next action after cycle 04

Completed: C01 harmonic homogeneous strong-field benchmark; C02 continuum planar data/evolution; C03 finite planar mode/amplitude continuation; C04 genuinely 3D periodic conformal constraint construction. Read their JSON records and do not repeat the completed parameter sweeps without a new uncertainty.

Next C05: use construct() from code/periodic_3d_data.py without changing the seed family (n0=4, epsilon=.1, L=8, mass0, kappa1). Evolve with the original full-grid ecd.rk4, not PlanarGrid, at n=9,17,33 to harmonic t=.2 with 40 steps. Refine time separately at n=17 with 20/40/80 steps. All timesteps must satisfy characteristic_step(). Reject >5% relative Hamiltonian or lapse<.1, and label coordinate/numerical exits as inconclusive.

Measure every-step constraints, normal/current expansion, current frame validity, charge, slice volume and source conservation. Compare the smooth final fields on shared physical points via documented interpolation, accounting for unequal odd-grid spacing ratios. Include metric curvature at the endpoint; state that g_tt comes from the evolution RHS and that metric invariants alone do not certify full torsionful regularity. Initial spectral/oversampled constraints from C04 are independent of the FD evolution residual.

If convergent, next investigate stronger/independent transverse seeds or a principled multi-species bounce benchmark. Do not interpret one resolved focusing family as a universal no-bounce or stability result. No finite-cloud or quantum applicability conclusion follows from these periodic high-curvature classical calculations.
