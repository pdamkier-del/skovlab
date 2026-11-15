# Exact next action after cycle 03

Completed: C01 harmonic high-curvature reference, C02 continuum-constrained planar contraction, C03 finite planar amplitude/mode tests. Do not repeat those sweeps as new work.

Next C04: solve genuinely 3D periodic conformal initial data. Use n_seed=4[1+.1 cos(kx)cos(ky)cos(kz)], k=2 pi/8, real lower spinor seed polarized along z. With psi=chi^-3 sqrt(n_seed)(0,0,1,0), direct continuum source algebra gives j_i=chi^-6(derivative_y n_seed,-derivative_x n_seed,0)/4. This source is a zero-mean curl.

Solve Delta W_i+(1/3)derivative_i divW=j_tilde_i on the torus, with meanW=0. Then Aij=chi^-2(LW)ij and Kij=Aij+gammaij K/3. The scalar constraint is Delta chi=K² chi⁵/12-Q chi^-7/8, Q=|LW|²+2 GA n_seed², GA=3/16. Unknown positive constant K and mean(log chi)=0 fix scalar compatibility/normalization. Derive these identities from the full ECD source and check them independently rather than treating the effective energy as a fluid assumption.

Use Fourier derivatives for this continuum construction, oversample its residual and compare the existing independent FD Hamiltonian/momentum constraints at n=9,17,33. Inspect every component and verify variation in all axes. Check tolerance dependence before strong-field evolution.

A later dynamical C05 should first evolve these exact same families at 9³/17³/33³, with a short high-curvature interval and separate time refinement; include independent stress/current diagnostics and coordinate/constraint stops. No periodic constrained-data existence theorem or stability theorem is supplied by a Newton return flag.
