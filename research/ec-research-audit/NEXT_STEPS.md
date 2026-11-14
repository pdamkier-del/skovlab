# Prioritized next three research tasks

These are proposed future tasks. This audit neither modifies existing simulations nor implements a new one. The primary direction is analytical B; a narrowly supervised quantum-state calculation supports the first task. Each result must remain useful if the answer is negative.

## 1. Establish a state and validity map for the six-field benchmark

**Exact question.** Can the classical six-species chiral solution be associated with any specified fermionic state in a regime where the contact stress is controlled, or is its bounce only a classical mathematical benchmark? First answer this for independent fundamental torus modes with occupations \(0\le f_f\le1\); do not claim an answer for all possible correlated states.

**Equations/components.**
\[
A=\sum_f\bar\psi_f\gamma_5\gamma\psi_f,\quad
\Delta S=-\int e\,G_AA^2,\quad G_A=3\kappa/16,
\]
\[
\langle[A^2]_{\rm ren}\rangle,\quad
\epsilon_{\rm cl}=pn_0a^{-4}-G_An_0^2a^{-6}.
\]
The free reference state fixes species, mode functions, chirality, particle/antiparticle content, torus spin structure and occupations. A classical field label is not automatically an independently available physical species or an independently occupiable mode of one species.

**Derive or implement.**

- Write a one-page dictionary between classical amplitudes, conserved charges and normalized quantum modes. Begin with the already known \(n_0=6/L^3,p=2\pi/L\) case and generalize only to explicitly specified fractional occupations or extra modes.
- Compute the vacuum-subtracted leading contact expectation by Wick contraction, separating direct, exchange and cross-species terms. Specify operator ordering/renormalization and finite-volume mode normalization. Evaluate the corresponding stress or energy/pressure derivatives; do not infer it only from the classical mean-current square.
- Quantify \(|\Delta\epsilon|/\epsilon_0\), physical momenta \(p/a\), \(G_A(p/a)^2\), curvature in cutoff units and the scale of neglected terms. For a quantum interpretation also assess suitably smeared stress fluctuations relative to the mean; declare the smearing scale.
- Explain explicitly why first-order perturbation theory cannot validate a bounce at which the first-order correction cancels the leading energy. Identify a controlled interval away from that cancellation, if one exists.
- Deliver a short “validity map” with separate columns for exact classical solution, candidate quantum state and controlled approximation. Have a QFT mentor review the contact calculation.

**Independent validation.** Reproduce the coefficient from the minimal specialization of [Shaposhnikov et al., Eq. (2)](https://arxiv.org/html/2008.11686v2); compare Wick algebra to an independent finite-mode creation/annihilation calculation. Recover the repository's nonrelativistic unpolarized exchange example in its own limit, without transferring its coefficient to a chiral relativistic state. Check dimensions and recover \(\rho_b=1024\pi^3/(27\kappa^2)\) for the existing illustrative normalization. Vary L: those normalized bounce scales must remain unchanged.

**Success.** A reproducible state-specific correlator and explicit controlled interval, or a clear demonstration that the proposed correspondence does not furnish a controlled bounce. Either answer is a useful result.

**Failure.** Treating amplitude as unrestricted fermion occupation; neglecting exchange without justification; calling a first-order cancellation a controlled prediction; or silently changing species/couplings to obtain a bounce. A calculation that cannot define its state or error budget leaves the question unresolved.

**Decision enabled.** Decide whether to retain a purely classical benchmark objective or pursue a physical matter model. If no controlled torsion-dominant state is supplied, do not advertise realistic collapse prevention. This gate comes before expensive solver expansion.

**Preparation.** Dirac free modes and bilinears; Fermi occupation and anticommutation; Wick's theorem; dimensions of EFT operators; basic semiclassical stress. Expert supervision is needed for the composite operator and fluctuations.

## 2. Test the exact classical bounce against homogeneous anisotropy

**Exact question.** Within the *same* six-field minimal classical action, does the regular FLRW bounce survive a specified small homogeneous anisotropy of the geometry and balanced opposite momentum pairs? This is a finite-dimensional perturbation question, not general nonlinear spatial stability.

**Equations/components.**
\[
ds^2=-dt^2+\sum_i a_i(t)^2(dx^i)^2,\quad
v=a_xa_ya_z,\quad H=\dot v/(3v),\quad
\sigma_i=\dot a_i/a_i-H,
\]
\[
3H^2=\kappa E+\tfrac12\sum_i\sigma_i^2,\qquad
\dot\sigma_i+3H\sigma_i=\kappa(P_i-\bar P).
\]
Use all six Dirac equations, the full summed Hilbert stress, total \(A\), and conserved species charges. No barotropic replacement is allowed.

**Derive or implement.**

- First establish that the proposed opposite-pair field ansatz is invariant under the field equations on a diagonal Bianchi I metric. Keep off-diagonal Einstein/source equations as checks; do not assume they vanish merely because the background did.
- Permit the three paired populations or physical axis momenta to differ slightly while maintaining zero net momentum; distinguish these perturbations from a gauge rescaling of torus coordinates.
- Derive \(E,P_i,A^2\) and the phase equations before linearization. Spatial gradients and anisotropic momentum pressures remain; shear cannot be treated as a separately conserved \(v^{-2}\) term unless the derived anisotropic stress actually vanishes.
- Linearize around the exact bounce and use variables regular at H=0. Avoid dividing by H or defining a “stability” variable that diverges only because H vanishes.
- Seek an explicit sufficient/necessary condition for positive minimum v and finite fields/curvature over a declared interval around the bounce. If only a finite-time transfer bound can be shown, state that scope. No new PDE solver is required for this analytical task.

**Independent validation.** Check the isotropic limit against every nonlinear phase and stress component in CHIRAL_MULTIFIELD_BENCHMARK.md. Differentiate the Hamiltonian residual using the derived evolution to verify constraint propagation. Verify \(\dot E+\sum_iH_i(E+P_i)=0\). Have a second derivation or a GR mentor check the off-diagonal source and shear equations. Compare the zero-contact action with separately solved constraints.

**Success.** A precise open perturbation class with a regular turn, a counterexample/instability in that class, or a sharp threshold delimiting it. Explicitly identify the norm, time interval and whether the result is linear or nonlinear.

**Failure.** Studying only the unperturbed Friedmann equation; retaining isotropic pressure after momenta become anisotropic; ignoring constraints; declaring a bounded homogeneous perturbation proof of general spatial stability. An unclosed ansatz must be rejected rather than numerically evolved.

**Decision enabled.** Determine whether the exact construction is robust enough to justify further classical study. Even a stable answer does not settle Task 1 or a finite-cloud question. If the restricted family is already fragile, document that result before contemplating full 3+1 multi-species work.

**Preparation.** Bianchi I geometry, ADM Hamiltonian, shear, linear perturbations of constrained ODEs, tetrads and the complete Dirac stress. A mathematical-relativity reviewer is advisable.

## 3. Produce a bounded acceptance specification for the existing one-field solver

**Exact question.** What limited continuum initial-boundary problem does the present discretization demonstrably approximate, and what evidence would justify using it to test a specified analytical result?

This task follows the scientific choice in Task 1; it is a verification gate, not a request to build a collapse simulator.

**Equations/components.** Existing ecd.py, initial_data.py, harmonic reduction, \(\mathcal H,\mathcal M_i,\mathcal C^\mu\), current and stress conservation, characteristic speeds, and kinematics.py/track.py. Benchmark inputs are one-field LRS and local planar data, whose species content matches the current engine.

**Derive or implement.**

- Write a continuum reduction and boundary specification with the actual evolved variables. Derive a frozen-coefficient coupled principal-symbol/energy estimate in its declared regular regime, or identify precisely why a different reduction is required. Do not import a theorem for another GH formulation.
- Specify gauge conversion of the LRS proper-time solution to harmonic coordinates, or use coordinate-invariant stress/current/expansion observables with analytically specified boundary data. For planar data, restrict comparison to initial jets and a controlled local interval; their Taylor coefficients are not a global exact solution.
- Pre-register a validation matrix: independent space/time refinement; full-domain and fixed interior L2/L∞ norms; constraint/source scaling; domain-size tests including the elliptic initial solve; charge flux and stress divergence; high-frequency mode checks.
- Record the periodic-charge fix as a future isolated code correction with the uniform-field counterexample as acceptance criterion. During the current audit no fix is made.
- Set prospective numerical tolerances relative to the observable: a sign change is unresolved unless error bounds exclude zero, constraints converge and the result is insensitive to boundary/domain changes.
- State that the six-field solution requires a future multi-species engine with cross terms. Do not simulate it by a one-field sum or a fitted fluid.

**Independent validation.** Compare with continuum exact solutions, independent derivative operators and a second source derivation where practical. Compare the proposed GH boundary treatment with its actual continuum assumptions, using [Lindblom et al.](https://arxiv.org/html/gr-qc/0512093v3) as guidance rather than a transferred guarantee. Have a numerical-relativity mentor review the specification before implementation. Preserve the present rerun numbers as regression evidence.

**Success.** A reviewable specification naming one defensible finite-domain benchmark problem, required error measurements, and explicit pass/fail criteria. A proof that the present boundary/discretization is inadequate for that target is also an actionable outcome.

**Failure.** More resolution on the same 27 sampled nodes without boundary/time studies; treating residual identities as independent checks; or evaluating a physical bounce before selecting its matter state and geometric observable.

**Decision enabled.** Authorize a narrowly scoped later verification effort in A only if the continuum target is justified. Otherwise retain the prototype as exploratory code and choose C for a physically meaningful collapse baseline. No multi-species or strong-collapse implementation should be inferred as already authorized by this research plan.

**Preparation.** Consistency/stability/convergence, centered-difference symbols, RK4, constrained elliptic data, hyperbolic characteristic boundaries and current-flux balance.

## Suggested practical sequence

Begin with the state dictionary and scale arithmetic, which the student can understand before advanced GR. Obtain QFT review for the limited correlator calculation. Then decide whether the classical robustness question remains the project's objective. Derive its anisotropic equations before commissioning numerical work. The solver specification can be developed once the benchmark and physical interpretation are explicit.

No outcome of these three tasks alone proves finite-cloud or black-hole singularity avoidance. The immediate product is a defensible research question and an evidence standard, with clear reasons to continue, narrow or redirect the work.
