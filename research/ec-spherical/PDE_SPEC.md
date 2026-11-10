# Spherical PDE implementation specification — not an implementation

This specification accompanies `derivation.pdf` / `derivation.tex`. It does not authorize implementing the generic spherical Weyssenhoff proposal. The existing FLRW ODE, UI, exports and hosting route are unchanged.

## Readiness decisions

| Candidate | Status | Gate before code |
|---|---|---|
| GR dust | Supported pre-caustic equations | Select comoving monotone chart, center treatment, finite pressure-free boundary and Schwarzschild matching; benchmark against LTB. |
| GR, 0 < w ≤ 1 | Supported smooth causal material equations | Prove/choose a suitable gauge and initial-boundary formulation; choose an outer boundary compatible with constant-w matter. Do not assume a compact vacuum edge. |
| Averaged conserved-spin EC, constant w | Conditional effective equations | Check averaging assumptions, h = (1+w)ρ−2q and c_eff². Low-spin ordinary dust has c_eff² < 0; generic dust/bounce PDE implementation is blocked. |
| Full ideal coherent spherical Weyssenhoff branch | Formal SO(3) branch only | Select published constitutive formulation and normalization; enforce regular radial spin/parity conditions; same acoustic obstruction applies after specialization. |
| Full retained-correlation averaged spin matter | Not closed | Specify and derive the missing moments, EOS, transport and gravitational averaging terms. No generic implementation. |
| Spinful surface layers / radiating boundary | Not specified | Select EC junction formulation, surface action/source data and admissible distributional regularity. No guessed GR jump formula. |

Necessary acoustic conditions are not a proof that the entire constrained Einstein–matter initial-boundary system is strongly hyperbolic or stable. The gauge and boundary problem need their own analysis. In the dust limit, coincident characteristics require a dust/Lagrangian formulation instead of assuming a strictly hyperbolic acoustic eigensystem.

## 1. Variables and equations

Use the general comoving spherical metric with lapse A=exp(Φ), radial metric B=exp(Λ), areal radius R. Work in a patch with R'>0 and Γ = R'/B > 0 initially; this is a chart restriction, not a physical prohibition on throats.

For the first no-flux perfect-source scheme:

- Evolved: `R(t,r), U(t,r), rho(t,r)`; add `q(t,r)` only for a mathematically approved effective source. An equivalent number/composition representation is possible but must not duplicate matter degrees of freedom.
- Constraint/gauge: geometric `M=G m_MS`, `Gamma`, `B`, `Phi`.
- Derived: `epsilon=rho−q`, `P=w rho−q`, expansion Θ, shear σ², null expansions, curvature and local proper times.
- Model 1: q=0. Model 2: q=κ S_H²/4. Coherent model 3: q=κ b², not κ b²/4 in BHL spin units.

The precise equations and their undivided metric versions are numbered in the derivation. A constrained method would evolve R,U,ρ,(q), integrate M' = κ epsilon R² R'/2 with M(0)=0, derive Γ²=1+U²−2M/R, set B=R'/Γ and integrate Φ' = −P'/(epsilon+P), with one lapse normalization. It would monitor the unused mass-time equation, Γ-time equation, angular Einstein component and ADM residuals. This is a proposed split; a constraint-propagation/stability analysis of that discrete split is required before production use.

A free-evolution alternative may evolve M instead. Do not evolve and overwrite every redundant mass/metric variable independently. Do not solve U = ±sqrt(2M/R+Γ²−1) with a manual sign switch at a bounce.

If a supported full matter formulation actually produces radial energy flux Q or distinct pressures, use the general equations in the derivation, including

- D_r M = κ R²(epsilon Γ + Q U)/2;
- D_t M = −κ R²(P_r U + Q Γ)/2;
- D_t Γ = U D_r Φ + κ RQ/2;
- full projected energy and momentum conservation, including D_t Q.

Specifying symbols Q and P_r−P_perp is not a constitutive closure. Their evolution cannot be inferred from tidal stretching alone.

## 2. Initial data and center

After fixing R_i=r, select U_i and ordinary density ρ_i. An approved averaged model additionally needs a spin-composition/variance profile q_i; a coherent radial branch needs a signed b_i=O(r) instead. No spin profile is selected by this audit. Solve the mass, metric and lapse constraints as described above. Independent input of density, mass, radial metric and extrinsic curvature is inadmissible.

Check:

1. Real Γ_i² and positive B_i; R_i>0 for noncentral shells.
2. Smooth center series R=ℓ r+O(r³), M=O(r³), U=O(r), Γ=1+O(r²), even scalar density/variance profiles.
3. The selected EOS and source domain, including h and acoustic conditions.
4. Pressure/flux/spin compatibility at the chosen material boundary.
5. Hamiltonian, momentum, mass and source constraints with absolute and scaled residuals.

Use analytic center limits and parity-compatible stencils. Do not replace R or Γ by a small arbitrary denominator floor. A coherent radial spin magnitude must vanish at a regular center; ensemble spin variance can remain nonzero there.

## 3. Boundary and exterior problem

Choose one of the following *before* calling the domain an isolated collapsing star:

- Spinless, pressure-free, no-flux material boundary matched to a Schwarzschild exterior. Verify induced metric, extrinsic curvature, mass and boundary trajectory. Use horizon-regular exterior coordinates when necessary.
- A fluid patch with a specified non-vacuum exterior or analytic incoming characteristic data. Label this a patch, not an isolated star.
- A derived radiative/surface-layer model with its own material and EC junction equations.

A fixed-w positive-pressure fluid does not automatically have a regular compact vacuum edge in the comoving chart. Nonzero effective pressure at a comoving surface cannot be matched to vacuum by simply equating a mass. A Vaidya exterior is not an arbitrary time-varying Schwarzschild mass: radiation and interface flux conditions must be supplied.

If the spin source vanishes smoothly in a collar, ordinary GR matching is available there only after checking that such a collar solves the interior matter equations and all boundary conditions. A plotted spin zero is not a junction test. A nonzero spin surface layer is a separate unimplemented theory problem, with potential ill-defined products of distributions.

## 4. Spatial and temporal discretization acceptance plan

For an approved smooth system, compare a second-order convergent method of lines (regular center series, consistent radial constraint quadrature, controlled time stepping) with analytical and manufactured solutions. Select a conservative formulation or prove that the chosen primitive formulation preserves the relevant constraints. Establish the numerical characteristic structure before selecting a Riemann solver or SBP boundary treatment.

For a causal acoustic model, local coordinate sound speeds are ±A c_s/B in the fluid-comoving frame, plus material/contact modes. Require a documented CFL limit and independently controlled temporal error. Do not take sqrt(|c_eff²|) if the acoustic speed is imaginary. Negative acoustic speed squared is a model/principal-symbol failure, not a timestep adjustment.

The first smooth implementation need not claim shock resolution. If shocks develop, stop with a declared smooth-solution breakdown until a physical entropy condition, conservative variables and a suitable weak-solution scheme have been derived. Artificial viscosity may be a numerical scheme component only when its convergence and continuum target are established; it must not be sold as a physical EC bounce term.

## 5. Stop and classification policy

Maintain separate flags for:

- coordinate/chart failure (including Γ→0 in the divided monotone-chart system);
- loss of matter hyperbolicity or enthalpy inversion;
- particle/material shell-crossing candidate;
- noncentral shell focusing;
- curvature-growth candidate;
- a finite integration threshold;
- numerical failure or constraint violation;
- an ordinary bounce/recollapse;
- an unverified or failed exterior junction.

A regular closed-FLRW neck can have R'=0 without shell crossing. AH crossing 2M/R=1 is not a singularity and must not force a stop in an otherwise regular comoving formulation. No finite threshold is a computed spacetime singularity.

## 6. Required data products and outcome definitions

Record `t,r,Phi,Lambda,R,U,M,Gamma,rho,q,P_r,P_perp,Q`, the selected field-equation set, units, constraint residuals, cell-volume/particle Jacobian, and local proper time τ_r(t)=∫A dt. Explicitly mark absent/unmodelled fields instead of reporting zeros for uncomputed physics.

For each shell record areal extrema (U=0), local volume extrema (Θ=0), proper-time derivative signs, minima, curvature/source regularity and hyperbolicity-domain status. Initial imposed extrema do not count as collapse-generated bounces. A body-wide nonsingular bounce requires more than one shell or direction reversing. Counts of complete oscillations require complete extrema sequences, not an extrapolation from one bounce.

Export N_R=ln(R/R_i), N_V=(1/3)ln(BR²/B_iR_i²), and accelerated-expansion e-folds only with a declared local clock and volume-scale definition. These are not entropy or proof of inflation. Event horizons cannot be classified from an interior-only finite run.

For an implemented exterior, export induced-metric, extrinsic-curvature, mass/flux and spin-junction residuals, surface-layer assumptions and tolerances. Until then, `junction_status=not_computed`, not `satisfied`.

## 7. Acceptance tests before any EC PDE release

- Recover the exact FLRW equations for all three k values and reproduce existing trajectory exports unchanged.
- Recover flat/closed/open GR limits, vacuum Schwarzschild, analytic inhomogeneous LTB and a regular spherical neck.
- Demonstrate spatial and temporal convergence separately; test constraint propagation and center parity.
- Verify mass balance including pressure work and, where relevant, heat flux.
- Verify null-expansion signs and local trapping independent of compactness alone.
- Detect every model-domain exit before dividing by vanishing h or Γ.
- Supply a selected boundary/exterior problem and check its junction residuals.
- For a full spin system, verify spin transport, Frenkel preservation, symmetry of every source field and a closed characteristic/moment system.
- Compare against literature using identical EOS, spin normalization, averaging and boundary assumptions. Do not transfer effective-dust results to ordinary-dust-plus-negative-spin-pressure matter.

No simulator feature work is authorized by a passing symbolic geometry test alone. The audit currently blocks the generic spherical conserved-spin dust/bounce solver and the unclosed full-correlation model.
