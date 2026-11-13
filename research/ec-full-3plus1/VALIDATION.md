# What is verified, and what is not

## Independent operator checks

The tests verify the Clifford algebra; metric/tetrad compatibility for arbitrary lapse, shift, off-diagonal spatial metric and metric derivatives; the full Clifford covariant derivative; the reduced Ricci wave principal coefficient; an exact curved-coordinate flat harmonic gauge wave; arbitrary four-component local Dirac-current conservation; independent finite-difference local stress conservation for generic spinor first/second jets satisfying the nonlinear Dirac equation; full boosted nonlinear Dirac plane-wave stress; the prior curved LRS solution and forbidden triaxial off-diagonal stress; and the geometric torsion sign/coefficient directly from affine curvature and gamma matrices.

These checks do not impose a homogeneous ansatz on the production engine. The homogeneous solutions are regression tests of its general tensor operations.

## Numerical method

Centered second-order first derivatives are used in all three Cartesian grid directions; second derivatives are compositions of the same first-derivative operators, including diagonal derivatives. Using a nearest-neighbor second derivative alongside independently centered first derivatives gave much larger linear constraint-propagation errors on coarse localized tests. The compatible composition reduces that inconsistency, while retaining second-order continuum accuracy. It has a wider stencil and weakly resolved high-frequency modes; odd grid sizes and smooth, resolved data do not replace a high-frequency stability analysis. There is no artificial matter interaction, Wilson term or numerical damping hidden in the action.

Classical RK4 evolves the coupled metric and spinor arrays at every stage. The step is bounded by the user step (at most 0.01) and a lapse/shift-aware coordinate characteristic bound: 0.25 dx divided by the sum of the three grid-maximal speeds |βⁱ| + N √γⁱⁱ. This is a conservative coordinate-speed bound, **not** a coupled nonlinear stability guarantee or local truncation-error estimator. The public experiment remains restricted to initially near-Minkowski, short-time data.

The explicit normal triad handles general geometry algebraically; loss of spatial positive definiteness or spacelike slicing rejects numerical evolution. No constraint projection is used during evolution. The initial nonlinear solve uses SciPy Newton–Krylov on all four interior residuals with fixed conformal boundary values. Absolute start tolerance is 2e-8 in the declared units. All diagnostics are recalculated from the evolved fields.

The report monitors the maximum absolute Hamiltonian/momentum residual and harmonic contracted connection. Hamiltonian error is also divided by twice the initial interior peak |E|, with a 1e-12 floor; it is a fixed scale, not a pointwise error norm or proof of accuracy. The demonstration stops at 5% of that scale. Number conservation is measured by the actual integral $\int\sqrt{-g}\,j^0d^3x$ using trapezoidal quadrature, rather than reconstructing density from a conserved formula. No constant matter-energy integral is imposed in a dynamic geometry.

## Numerical evidence

- Periodic harmonic gauge-wave evolution: second-order spatial convergence and fourth-order time self-convergence of the actual 3D evolution engine, including the complex spinor in a nonzero-matter operator test (the latter deliberately does not claim constrained initial data).
- Small general metric/spinor perturbations: bounded short-time numerical amplification. This is a limited noise test, not a nonlinear stability theorem.
- Localized ECD initial data: nonzero spatially varying spin/current, all four complex components, all gravitational constraints solved at interior nodes, harmonic gauge initialized.
- Short coupled ECD evolution: nontrivial metric change, spatial spinor evolution, measured constraint drift, and integrated Dirac-number drift.
- Explicit rejection of out-of-range or nonconvergent initial data. A zero-field run recovers GR vacuum and Minkowski exactly. A single coherent nonzero Dirac field has no independent spinless-dust switch.
- Desktop/mobile browser checks include a **new backend calculation**, invalid request rejection, field plots/slice and JSON export.

The [separate coupled refinement experiment](coupled-convergence-results.json) evolves the same compact, spatially varying ECD seed on 9³, 17³ and 33³ grids to t=0.01. On 27 exact shared physical nodes, successive state differences decrease by factors 5.92 (metric), 4.00 (metric velocity) and 4.54 (complex spinor). Hamiltonian error is nonmonotonic on the coarsest grid but falls by a factor 3.81 from 17³ to 33³ on these nodes. This is evidence consistent with second-order short weak-field convergence, **not** an error bound, global-norm study or general collapse theorem. Reproduce with `python research/ec-full-3plus1/coupled_convergence.py`; it takes longer than the unit suite.

The independent [effective-stress divergence experiment](stress-conservation-results.json) measures the numerical covariant divergence of the full stress at t=0.005, using centered time differences and spatial derivatives on the evolved metric. The shared-node RMS residuals are 1.82e-6, 3.53e-6 and 9.27e-7 at 9³, 17³ and 33³. The coarsest pair is nonmonotonic; the finer pair decreases by 3.80. This is limited second-order conservation evidence, not exact discrete conservation. Reproduce with `python research/ec-full-3plus1/conservation.py` (a heavier diagnostic).

The saved browser example reports its actual parameters and residuals. A flat-principal-block elliptic preconditioner reduced typical initial-solve field evaluations from 98 to 19 at 9³ and from 726 to 19 at 19³ in local experiments. These are performance observations, not proofs of elliptic existence or uniqueness. Strong-collapse, full-domain and boundary/domain-size convergence remain unestablished.

## Boundary, geometry and physics limits

The compact spinor has a smooth continuum initial collar. The finite cube prescribes constant outer metric velocity, linearly evolving outer metric values consistent with g_t=p, and fixed initial outer spinor values, not a constraint-preserving outgoing gravitational boundary. Two outer grid layers are excluded from displayed extrema; that does not establish exact causal insulation of numerical modes. The integrated number includes the full cube and is only a short-time check, not a global exterior construction. Periodic boundaries are used only for declared benchmarks.

No asymptotic ADM mass, followed material volume, full torsionful curvature regularity, trapped-surface finder, event horizon or global bounce is established. Coordinate time is harmonic time; local normal expansion is not a global material-volume rate. The experiment reports `bounce: not-assessed`. No conclusion follows merely from a local sign change, low initial residual, or finite displayed density.

Classical ECD here has no quantum statistics, dense nuclear EOS, gauge/strong/weak interactions or quantum-gravity completion. The weak-field numerical limits are operational choices, not a physical validity theorem. General coupled hyperbolicity/stability, improved boundaries, initial-data conditioning and strong-field spatial/time convergence remain required.
