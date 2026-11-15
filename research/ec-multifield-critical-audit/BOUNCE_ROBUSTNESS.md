# Bounded classical robustness investigation

The physical audit does not justify an expensive general six-field 3D solver. A small homogeneous full-spinor experiment is useful for testing whether the exact classical turn is an isolated cancellation. This gate was applied before the ODE runs.

In the massless paired Bianchi I family let N_i denote the total number in the opposite pair along axis i, v=a_xa_ya_z, r_i=p_iN_i/(a_i v), ρ_s=G_A(ΣN_i)²/v². Direct full-spinor evaluation gives E=Σr_i−ρ_s and P_i=r_i−ρ_s, with vanishing momentum and off-diagonal stress. Einstein evolution implies

Ḣ_i=−ΘH_i+κr_i,  v̈=κvΣr_i>0.

Consequently this restricted family has at most one regular volume minimum and no regular volume maximum or repeated volume oscillation. This does not guarantee a turn before directional singularity and does not constrain all inhomogeneous ECD solutions. Anisotropic pressure drives shear; assuming σ²v² constant would be unjustified.

The exact turn is nondegenerate, Ḣ_b>0. Smooth finite-time ODE dependence and continuity of the separately solved constraints ensure sufficiently small admissible perturbations retain a nearby local volume turn. This is a local open set inside the ansatz, not generic stability in 3D or global perturbed geodesic completeness.

Actual full six-spinor runs tested: 2% reduction of one balanced pair's density; 2% increase of its |p|; small initial shear; m=0.01p_b; 1% opposite-chirality admixture. Every case completed the finite reference interval and crossed mean H from negative to positive at both 128 and 256 steps. Numerical details are in `NUMERICAL_VALIDATION.md`.

Important restrictions:

- Pair balance is preserved. Changing only one member gives nonzero homogeneous momentum and violates the diagonal Bianchi I momentum constraint; the independent test detects this invalid datum. It is not evidence for instability.
- Continuous p changes are interpreted on the R³ cover or on a rectangular torus with L_i=2π/p_i. They are not continuous momentum perturbations on the unchanged fixed cubic torus. This experiment is classical and not a separately occupation-matched physical state.
- The mass perturbation starts with the original pure chiral field and subsequently evolves all components. It is not a positive-free-energy massive eigenstate preparation.
- Opposite-chirality massless initial modes individually have positive free kinetic energy. Coherent phase information is retained; no spin-fluid average is imposed.
- The exact and amplitude/shear/chirality runs can use the original periodic torus. There is no artificial outer boundary or finite cloud surface.

Survival in these cases supports nearby homogeneous mathematical robustness. It does not repair the Planck-scale state problem or establish inhomogeneous stability. Large anisotropy, correlations, massive state preparation, finite clouds and spatial perturbations remain unresolved.
