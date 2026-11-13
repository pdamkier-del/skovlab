# Common ADM geometry and mathematical compatibility

## Physical interpretation

ADM separates a spacetime into spatial slices. Its normal observer is a coordinate/geometric choice, not necessarily the velocity of the particles or a bulk fluid. Both candidate matter models can carry energy across those slices and have direction-dependent stresses. We impose neither spherical symmetry nor homogeneity.

Use

$$
ds^2=-N^2dt^2+\gamma_{ij}(dx^i+\beta^i dt)(dx^j+\beta^jdt),
\quad n^\mu=N^{-1}(1,-\beta^i),\quad n_\mu=(-N,0).
$$

For a chosen timelike matter velocity, $u^\mu=W(n^\mu+v^\mu)$, $n\cdot v=0$, $W=(1-\gamma_{ij}v^iv^j)^{-1/2}$. For Dirac fields this choice can fail at null/zero current; for kinetic matter an Eckart or Landau frame must be declared rather than assumed.

## Compact gravitational equations

First eliminate algebraic torsion into the complete effective source. The following equations are then **Levi–Civita** ADM identities; they are not identities for the full torsionful connection. Set

$$
K_{ij}=-\frac1{2N}(\partial_t-\mathcal L_\beta)\gamma_{ij},\quad
E=T_{\mu\nu}n^\mu n^\nu,\quad
j_i=-\gamma_i{}^\mu T_{\mu\nu}n^\nu,\quad
S_{ij}=\gamma_i{}^\mu\gamma_j{}^\nu T_{\mu\nu}.
$$

The constraints and evolution equations are

$$
{}^{(3)}R+K^2-K_{ij}K^{ij}=2\kappa E,\qquad
D_j(K^j{}_i-\delta^j_iK)=\kappa j_i,
$$
$$
(\partial_t-\mathcal L_\beta)\gamma_{ij}=-2NK_{ij},
$$
$$
(\partial_t-\mathcal L_\beta)K_{ij}
=-D_iD_jN+
N({}^{(3)}R_{ij}+KK_{ij}-2K_{ik}K^k{}_j)
-\kappa N\left[S_{ij}-\frac12\gamma_{ij}(S-E)\right].
$$

Here $S=\gamma^{ij}S_{ij}$ and $D_i$ is the spatial metric derivative. These compact equations permit arbitrary spatial curvature and shear. Their signs follow the previous spherical convention $K^i{}_j=-\operatorname{diag}(H_r,H_\perp,H_\perp)$. Continuum constraint propagation requires the correctly derived $\nabla_\mu T_{\rm eff}^{\mu\nu}=0$. Inserting kinetic moments that fail this identity would make the coupled system inconsistent.

For the matter congruence define $h_{\mu\nu}=g_{\mu\nu}+u_\mu u_\nu$, $\Theta=\nabla_\mu u^\mu$, $a^\mu=u^\nu\nabla_\nu u^\mu$, $\sigma_{\mu\nu}=h_\mu{}^\alpha h_\nu{}^\beta\nabla_{(\alpha}u_{\beta)}-\Theta h_{\mu\nu}/3$, and $\omega_{\mu\nu}=h_\mu{}^\alpha h_\nu{}^\beta\nabla_{[\alpha}u_{\beta]}$. Only for $u=n$ are $\Theta=-K$ and $\omega=0$. Tidal shear of matter is not generally the trace-free ADM $K_{ij}$ alone.

## Inventory and closure

| Item | A. Classical minimal ECD | B. Selected quantum kinetic description |
|---|---|---|
| Geometry | Six $\gamma_{ij}$ and six $K_{ij}$; lapse/shift gauge and four Einstein constraints. A tetrad/spin frame also has local Lorentz gauge. | Same gravitational variables. |
| Independent matter | Four complex components per specified Dirac species; no independent perfect-fluid pressure/spin profile. | A Wigner matrix subject to its mass-shell/algebraic constraints; quasiparticle massive sector has four real occupation/polarization functions per momentum, plus antiparticles. Correlations/self-energies may require additional variables. |
| Evolution | Nonlinear Dirac equation and adjoint; Cartan relation is algebraic. | Published curved collisionless transport exists. A combined dense, collisional, self-consistent EC kinetic closure is not established here. |
| Source | Symmetric action-derived $T_{\rm eff}$ and total axial spin current. | Leading distribution moments plus quantum and interaction corrections; action matching and correlation contributions must be derived. |
| Closed coupled system? | Formally yes for the specified classical theory after gauge and constrained initial data. Quantum matter requires further state/renormalization data. | Not yet for the requested combined model. No arbitrary pressure, torque or collision term fills the gap. |
| Mathematical limit | Algebraic contact leaves the fixed-background null Dirac principal cone unchanged. This is not a global stability or bounce theorem. | Classical streaming has causal massive characteristics; higher spin-gradient/nonlocal approximations require their own analysis. Linear hydrodynamic equilibrium results do not prove coupled EC well-posedness. |

Minimal ECD's action and source are identified in [DIRAC_MODEL.md](DIRAC_MODEL.md); the kinetic gaps are in [KINETIC_MODEL.md](KINETIC_MODEL.md). Both admit general inhomogeneous/anisotropic kinematics. Neither is proved valid at arbitrarily strong tidal curvature or at the Planckian torsion-dominance estimates.

## References and limited checks

The ADM equations follow the Gauss–Codazzi projection of $G_{\mu\nu}=\kappa T_{\mu\nu}$, with the stated extrinsic-curvature sign; compare [Gourgoulhon, gr-qc/0703035](https://arxiv.org/abs/gr-qc/0703035). The [previous audit](../ec-spherical/derivation.pdf) independently checked their spherical limit. The new checks verify lapse/shift normality, source projection with tilted observers and the focusing trace, rather than claiming a complete unrestricted component proof.
