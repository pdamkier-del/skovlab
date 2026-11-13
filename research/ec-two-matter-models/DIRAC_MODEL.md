# A. Einstein–Cartan–Dirac fields

## Physical meaning and scope

A Dirac field has a complex amplitude and a local spin orientation. Its derivatives respond to the spacetime geometry; no isotropic perfect-fluid equation of state is imposed. Several species or modes can describe more structure, but one commuting classical spinor is not a degenerate many-fermion gas. The realistic quantum-state/interaction recommendation in the [previous matter audit](../ec-matter-models/RECOMMENDATION.md) is unchanged.

Use **neutral minimal ECD** as the first closed mathematical benchmark. Masses and the torsion-induced contact interaction are included. Strong, electromagnetic and weak interactions, degeneracy statistics and collisions are not thereby supplied. A charged extension must include Maxwell consistently; its exterior need not be vacuum.

## Action and exact matter equations

Keep the [previous verified conventions](../ec-matter-models/ECD_DERIVATION.md): signature $(-+++)$, $\kappa=8\pi G$, full torsion $T^\rho{}_{\mu\nu}=2\widetilde\Gamma^\rho{}_{[\mu\nu]}$, derivative index first, $\epsilon_{0123}=1$, $\{\gamma^a,\gamma^b\}=-2\eta^{ab}$, $\gamma_5=-i\gamma^0\gamma^1\gamma^2\gamma^3$, $\bar\psi=\psi^\dagger\gamma^0$. Here contortion is denoted $C^\rho{}_{\mu\nu}$ to distinguish it from ADM extrinsic curvature $K_{ij}$.

$$
S=\int e\,d^4x\left[\frac{\widetilde R}{2\kappa}
+\sum_f\left\{\frac i2\bar\psi_f\gamma^\mu
\overleftrightarrow{\widetilde D}_\mu\psi_f-m_f\bar\psi_f\psi_f\right\}\right],
\quad
\widetilde D_\mu=\partial_\mu+\frac18\widetilde\omega_\mu{}^{ab}[\gamma_a,\gamma_b].
$$

With the operational definition $\delta S_m=-\frac12\int e\,s^\lambda{}_{ab}\delta\widetilde\omega_\lambda{}^{ab}+\cdots$, its spin current is

$$
s^\lambda{}_{ab}=-\frac i8\sum_f
\bar\psi_f\{\gamma^\lambda,[\gamma_a,\gamma_b]\}\psi_f.
$$

It is totally antisymmetric in Lorentz indices. It is not a convective Weyssenhoff/Frenkel ansatz. Define $J_5^a=\sum_f\bar\psi_f\gamma_5\gamma^a\psi_f$. The already independently checked Cartan solution and effective action are

$$
T_{abc}=\frac\kappa2\epsilon_{abcd}J_5^d,\qquad C_{abc}=\frac12T_{abc},
$$
$$
S_{\rm eff}=\int e\,d^4x\left[\frac{R}{2\kappa}
+\mathcal L_D^\circ-G_AJ_5^2\right],\qquad G_A=\frac{3\kappa}{16}.
$$

The square is of the **total** current, including cross-species terms. Varying the spinors gives

$$
\boxed{i\gamma^\mu D^\circ_\mu\psi_f-m_f\psi_f
-2G_AJ_{5\mu}\gamma_5\gamma^\mu\psi_f=0}
$$

and its adjoint. These are spatially varying nonlinear Dirac equations, with no imposed spatial symmetry.

## Energy-momentum and closure

The defining, symmetric effective source is the Hilbert tensor

$$
T^{\rm eff}_{\mu\nu}=-\frac2e
\frac{\delta S_{m,\rm eff}}{\delta g^{\mu\nu}}.
$$

The spinor/tetrad variation must accompany the metric variation. With the conventions above, a useful **classical on-shell** expression is

$$
T^{\rm eff}_{\mu\nu}
=-\frac i4\sum_f\left[
\bar\psi_f\gamma_\mu\overleftrightarrow D^\circ_\nu\psi_f+
\bar\psi_f\gamma_\nu\overleftrightarrow D^\circ_\mu\psi_f\right]
+G_Ag_{\mu\nu}J_5^2.
$$

The sign follows our negative Clifford convention. The Dirac equations imply $\mathcal L_D^\circ=2G_AJ_5^2$, so the total on-shell material Lagrangian is $G_AJ_5^2$; this explains the displayed metric term. It must not be isolated and interpreted as a fluid EOS: the derivative term also changes with the nonlinear solution. A homogeneous classical spinor check verifies positive free energy and the contact contribution; it does not represent a gas.

On the matter equations, diffeomorphism and local Lorentz identities give $\nabla_\mu T_{\rm eff}^{\mu\nu}=0$ and total spin/orbital balance. Spin need not be separately conserved, and massive/quantum axial currents are not generally conserved.

For specified species, the independent matter variables are four complex components per Dirac field. Neutral ECD has global phase symmetry, not freedom to discard an arbitrary spatial phase profile. Local Lorentz transformations change the spin frame and tetrad together; electromagnetic gauge freedom applies only when that gauge field is included. No extra density, pressure or spin-tensor profiles are independently prescribed once computed from the fields. Coupling this effective action to ADM gives a **formally closed classical system**, after gauge and gravitational constraints are supplied. A quantum ensemble instead needs its state and renormalized higher correlators.

## Compression and tidal deformation

The conserved vector current is $j^\mu=\sum_f\bar\psi_f\gamma^\mu\psi_f$. Where it is timelike, one possible material frame is $u^\mu=j^\mu/n$, $n=\sqrt{-j^2}$. Then

$$
\nabla_\mu j^\mu=0\quad\Longrightarrow\quad u^\mu\nabla_\mu n=-n\Theta.
$$

Thus contraction increases this number density. For a **single commuting regular spinor**, Fierz identities additionally give $j\cdot J_5=0$ and $J_5^2=-j^2$. Its coherent axial magnitude then grows with $n$. This identity does not apply to the total mean current of an arbitrary mixture: opposite spins can cancel, and quantum correlations can remain nonzero. At nodes or null current the chosen material velocity is undefined.

Spin orientation and stresses evolve through the Dirac equation and spin connection. Tidal curvature deforms wave packets and their spatial gradients; there is no rule that tidal stretching automatically makes a particular anisotropic pressure. A statistical/multimode state is needed for realistic multistream matter.

The axial contact is algebraic and leaves the Dirac principal cone metric-null. This avoids imposing the previous fluid sound-speed formula but proves neither nonlinear stability nor positive collective compressibility. Coupled classical Cauchy methods are established for torsion-free Einstein–Dirac–Maxwell; the contact term is a lower-derivative addition, but no dense quantum EC collapse theorem is claimed.

## Primary references

- [Hehl–Datta (1971), doi:10.1063/1.1665738](https://doi.org/10.1063/1.1665738): foundational nonlinear spinor formulation; original bibliographic record, with coefficients independently checked in the prior audit.
- [Shaposhnikov et al., 2008.11686v2](https://arxiv.org/pdf/2008.11686v2), Eq. (2), minimal limit; [Karananas et al., 2106.13811v2](https://arxiv.org/html/2106.13811v2): action and convention comparison.
- [Müller–Nowaczyk, 1504.01034v3](https://arxiv.org/pdf/1504.01034v3), Sec. 3.3: classical torsion-free Cauchy framework, with its stated hypotheses.
