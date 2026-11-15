# Reproduction and validation scope

From this directory run:

```bash
OPENBLAS_NUM_THREADS=1 python code/validate_audit.py
```

Pinned NumPy/SciPy/SymPy versions are in `requirements.txt`; Python/runtime and source/evidence SHA256 are recorded by the validator. No prior engine, fermion-fluid closure or branch code is imported.

1. `verify_connection.py`: direct affine curvature/derivative contractions and explicit gamma source; full 24-component Hessian and Euler solve at four real f values with/without trace-current source. No tensor component is projected away.
2. `scalar_identities.py`: derive the reduced functional, extract kinetic coefficient by differentiation, verify Legendre/canonical map, potential, vacuum mass and a declared nonminimal tuning algebra.
3. `fermion_stress.py`: six independent off-shell lapse/axis variations before inserting the Dirac equation, including minimal and nonminimal derivative/vector/axial/quartic terms.
4. `source_crosschecks.py`: exact effective nonminimal polynomial/current map and explicit source equation/dimension flags. It does not certify a fully resolved microscopic nonminimal convention map.
5. `closed_turn.py`: three separately constrained k=+1 data points; RK4 32/64/128 per half versus independent DOP853; full Cartan curvature, auxiliary equation, original tetrad trace and all 16 original coframe first variations. Time interpolation and coframe finite-difference errors are reported, not called exact zeros. It is not a flat-bounce or quantum simulation.
6. `inhomogeneous_constraints.py`: nonlinear reflection-even S³ BVP with pole/equator regularity, independent 65/129/257 finite-difference Hamiltonian checks and linear-harmonic comparison. Momentum constraints are identically zero on these time-symmetric scalar data. Raw collocation meshes/values/derivatives are retained. No inhomogeneous time evolution was run.

Connection algebraic errors are checked near machine precision. Scalar identities are exact symbolic residuals. Temporal convergence is fourth order and spatial constraint diagnostics second order within their documented ranges; the BVP's own tolerance is not substituted for independent discretization error. There is no universal residual cutoff certifying physical Level B. All numerical scales are recorded in M, m_phi and proper-time tau units; curvature and curvature-square factors differ.

The closed control is finite and time-local. Original full torsionful curvature is computed from the reconstructed Lorentz connection, not inferred from a single canceled scalar. The inhomogeneous regularity statement uses smooth constrained data and local canonical Einstein-scalar continuation; its full affine invariants were not independently evolved or numerically sampled in time. No global completeness, late singularity exclusion, exterior matching or quantum noise calculation is claimed.

7. `nonminimal_source.py` directly varies the original Hermitian nonminimal spin term with explicit gamma/adjoint transformations in all 24 directions; its source agrees with the independently derived effective-formula parameter map. The intermediate trace-label dictionary is not assumed. The analytic closed de Sitter control constraint/evolution is independently checked symbolically.
