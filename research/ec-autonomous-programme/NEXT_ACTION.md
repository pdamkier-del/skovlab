# Exact next action

Latest completed: cycle 01 strong homogeneous harmonic benchmark and diagnostic charge fix. Do not rerun the old audit or rederive the known proper-time branch as new research.

Next: cycle 02 periodic planar constrained perturbation. Use a real lower-component seed aligned along z, mass zero, n_seed(z)=4[1+.02 cos(2 pi z/8)], psi=chi^-3 sqrt(n_seed) (0,0,1,0), spatial metric chi⁴ delta, Kij=gammaij K/3 with unknown positive constant K. Momentum vanishes for variation along the polarization. Derive and independently solve the periodic Hamiltonian BVP with mean(log chi)=0:

chi''=K² chi⁵/12 - GA n_seed² chi^-7/4 (kappa=1).

Use an integral variable to impose the mean condition, solve K as a BVP parameter, then sample onto odd periodic grids. Verify the full tensor engine constraints and their spatial convergence; do not hide continuum error by only solving the monitored discrete residual. Set initial harmonic p0mu using harmonic_initial_velocity().

Evolve with PlanarGrid and the existing RK4/RHS, compare at common physical locations, refine time separately, measure charge and full stress divergence. Check at least one lifted full 3D RHS/RK step for spatially varying data. Record all failures as outcomes rather than changing the equations. Boundaries are a periodic torus, not a vacuum exterior.

Update every status file after the completed cycle, commit meaningful progress, and leave the next unresolved question precisely specified.
