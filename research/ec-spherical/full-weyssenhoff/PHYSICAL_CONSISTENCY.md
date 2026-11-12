# Physical consistency report

The selected full model is the neutral ideal convective Frenkel formulation reproduced in BHL 0706.2367v2, based on Obukhov–Korotky. It is not an unspecified “full-spin” switch. The original constrained microscopic action is identified but not independently reconstructed; the documented bulk EC variation and published effective field equations define this stage's scope.

| Formulation | Symmetry and equations | Scientific status |
|---|---|---|
| Model A: statistically unpolarized GSM | Zero mean spin, nonzero isotropic variance; Hashemi coefficient \(q=\kappa S_H^2/4\); explicitly conditional local averaging and variance transport. | Algebraically closed under stated assumptions, but shares the acoustic/enthalpy obstruction. Existing homogeneous FLRW reference preserved. |
| Model B: coherent SO(3) ideal fluid | Frenkel removes the invariant \(dt\wedge dr\) component; \(b_{\theta\phi}=R^2\sin\theta\,b(t,r)\) remains. \(q=\kappa b^2\), \(P=p-q\), \(\epsilon=\rho-q\). | Formal closed smooth radial branch with a declared EOS; material/gauge/boundary viability is a separate test. |
| Model B with parity as well as proper rotations | A radial axial mean changes sign under parity. | Nonzero coherent radial polarization excluded; variance can survive. |
| Full-field FLRW coherent convective spin | Spatial two-form selects an axial direction. | Nonzero coherent spin incompatible with full FLRW symmetry. A merely FLRW metric can have a non-inheriting spin configuration; Stage 1's aligned example remains distinct. |
| Common-congruence ensemble with independent radial/tangential spin second moments | Under commuting averaging/derivatives and no unresolved velocity/metric correlations, ideal moment transport closes as advection/dilution. | Conditional moment truncation; BHL quadratic source depends on the trace. It does not generate anisotropic pressure or remove the acoustic obstruction. |
| General ensemble retaining spin–velocity, spin–shear, acceleration and metric correlations | Spherical symmetry permits radial flux and anisotropic effective stress. Their values/evolution require a hierarchy and constitutive laws. | Not closed; no principal symbol or implementation justified. |

The retained derivative source is evaluated **before** symmetry reduction. In a vorticity-free orthonormal rest frame:

\[
\mathcal D_{00}=0,\qquad
\mathcal D_{0i}=\mathsf D^j b_{ij}+2b_{ij}a^j,\qquad
\mathcal D_{ij}=(H_i-H_j)b_{ij}\quad(i\ne j).
\]

For radial coherent spin, its spatial divergence vanishes as the curl of a radial axial vector; acceleration is radial and has zero contraction with the angular spin plane; the angular shear eigenvalues are equal. The cancellation holds for arbitrary radial spin/density/metric gradients. Nonspherical spin and unequal expansion-rate controls verify that the terms were not discarded globally.

The ideal spin equation gives \(D_t b=-\Theta b\). With conserved particles, \(b/n\) is advected. There is no additional propagating radial orientation degree of freedom in this exact symmetry class. Relaxation, spin exchange, nonconvective spin currents, spin-dependent internal energy or collisions could change the material theory, but none has been derived or inserted here.

For a fixed isentropic \(\rho=Cn^{1+w}\), equivalent independent matter choices are \((\rho,b)\) or \((n,\beta=b/n)\). With radial gauge \(R_i=r\), the free initial profiles are \(U_i,\rho_i,b_i\). Mass, radial metric, lapse and initial extrinsic curvature are constrained. Ensemble variance, signed coherent spin, torsion and Misner–Sharp mass are different quantities.

The closed ideal branch is a **conditional material model**. Its equations are compatible with proper spherical symmetry; compatibility does not establish high-density microscopic validity, a causal path to a bounce, or a finite star with a regular exterior.
