# What the most general statement of this ECD model is

## Action and conventions

“General” refers to unrestricted spacetime dependence and all field components within a **specified action**. We retain neutral minimally coupled classical Dirac fields, no bare cosmological constant, Holst/nonminimal terms, quantum-state closure or extra interactions. Those additions define different models and require their own audit. The one-field implementation is the current numerical baseline; the finite-species equations below state its exact theoretical extension, not an implemented many-body solver.

Use the [corrected geometric connection conventions](../ec-full-3plus1/CONVENTION_AUDIT.md): $(-+++)$, derivative index first, $\epsilon_{0123}=1$, $\{\gamma^a,\gamma^b\}=-2\eta^{ab}$, $\bar\psi=\psi^\dagger\gamma^0$, $\gamma_5=-i\gamma^0\gamma^1\gamma^2\gamma^3$. For geometric frame connection $W_\mu{}^a{}_b=e^a{}_\nu\widetilde\nabla_\mu e_b{}^\nu$, spin differentiation is $\widetilde D=\partial-W^{ab}[\gamma_a,\gamma_b]/8$.

For finitely many species, the original action and algebraic elimination are

$$S=\int e\left[\frac{\widetilde R}{2\kappa}+\sum_f\left(\frac i2\bar\psi_f\gamma^\mu\overleftrightarrow{\widetilde D}_\mu\psi_f-m_f\bar\psi_f\psi_f\right)\right]d^4x,$$
$$A^a=\sum_f\bar\psi_f\gamma_5\gamma^a\psi_f,\quad T_{abc}=-\frac\kappa2\epsilon_{abcd}A^d,\quad C=T/2,$$
$$S_{eff}=\int e\left[\frac R{2\kappa}+\sum_f\mathcal L_{D,f}^{\circ}-G_A A_aA^a\right]d^4x,\qquad G_A=3\kappa/16.$$

The square includes interspecies cross terms. There is no propagating torsion wave or independently prescribed spin pressure in this minimal theory. Changing the spin state changes the source through the actual fields.

Variation yields

$$i\gamma^\mu D_\mu^{\circ}\psi_f-m_f\psi_f-2G_AA_a\gamma_5\gamma^a\psi_f=0,$$
$$G_{\mu\nu}=\kappa T_{\mu\nu},\qquad T_{\mu\nu}=\sum_f\mathcal K^{(f)}_{\mu\nu}+G_Ag_{\mu\nu}A^2,$$
$$\mathcal K^{(f)}_{\mu\nu}=-\frac i4[\bar\psi_f\gamma_\mu\overleftrightarrow D^{\circ}_\nu\psi_f+\bar\psi_f\gamma_\nu\overleftrightarrow D^{\circ}_\mu\psi_f]\quad\text{(complete on-shell source)}.$$

Independent global phase symmetries give $\nabla_\mu j_f^\mu=0$ in this particular action. Thus the total current is conserved too. Diffeomorphism invariance gives $\nabla_\mu T^{\mu\nu}=0$. These identities do not provide a barotropic EOS, separate isotropic spin transport or a quantum correlation hierarchy.

## General geometry, constraints and closure

The ADM metric has arbitrary lapse, shift and six spatial metric components:

$$ds^2=-N^2dt^2+\gamma_{ij}(dx^i+\beta^idt)(dx^j+\beta^jdt),\qquad K_{ij}=-\frac{(\partial_t-\mathcal L_\beta)\gamma_{ij}}{2N}.$$

For $E=T_{nn}$, $j_i=-T_{in}$ and $S_{ij}=T_{ij}$ with spatial projections,

$$R^{(3)}+K^2-K_{ij}K^{ij}=2\kappa E,\quad D_j(K^j{}_i-\delta^j_iK)=\kappa j_i,$$
$$ (\partial_t-\mathcal L_\beta)K_{ij}=-D_iD_jN+N[R^{(3)}_{ij}+KK_{ij}-2K_{ik}K^k{}_j]-\kappa N[S_{ij}-\gamma_{ij}(S-E)/2].$$

These equations plus metric evolution, all Dirac components and a compatible tetrad/gauge constitute a formally closed classical field theory. Initial geometry/matter profiles must satisfy the four constraints; initial pressure, spin, mass and collapse rate cannot be independently assigned as fluid variables. A complete spatial problem also needs topology, asymptotics or boundary data.

The existing numerical implementation uses harmonic-coordinate reduced Einstein equations, a normal Cholesky tetrad and all metric/spinor components. Its finite-box conformal initial-data family is restricted even though its evolution engine is general. It is tested only in the documented short weak-field regime; formal closure is not global well-posedness, long-time numerical stability or a physical exterior construction.

For the ADM-normal congruence, $H_n=-K/3$ and $K_{ij}=-H_n\gamma_{ij}-\sigma^{(n)}_{ij}$ give

$$6H_n^2=2\kappa E-R^{(3)}+\sigma^{(n)}_{ij}\sigma_{(n)}^{ij}.$$

This is a constraint, not a closed scalar evolution equation for a universal scale factor. Energy flux, anisotropic stress, spinor gradients, slicing and shear still evolve independently.

In a current frame the full stress generally decomposes as $T_{ab}=\epsilon u_a u_b+P h_{ab}+2u_{(a}q_{b)}+\pi_{ab}$, with spatial flux and trace-free anisotropic stress. Energy conservation is

$$\dot\epsilon+(\epsilon+P)\Theta+D_aq^a+2a_aq^a+\sigma_{ab}\pi^{ab}=0,$$

where $D$ is the spatially projected derivative. Thus $\epsilon\propto e^{-3N_u}$ is not a general energy law. Only the declared conserved current density has the simple e-fold relation; flux, anisotropic work and the actual Dirac state remain necessary.

## Exact trace identities, with their species restrictions

On the Dirac equations,

$$T^\mu{}_{\mu}=-\sum_fm_f\bar\psi_f\psi_f+2G_AA^2,\qquad R=\kappa\sum_fm_f\bar\psi_f\psi_f-2\kappa G_AA^2.$$

For a declared timelike total-current frame, let $\mathcal G=h^{\mu\nu}\sum_f\mathcal K^{(f)}_{\mu\nu}$. The complete energy and mean spatial stress satisfy

$$\epsilon=\sum_fm_fS_f+G_AA^2+\mathcal G,\quad P=G_AA^2+\mathcal G/3,\quad\epsilon+3P=\sum_fm_fS_f+4G_AA^2+2\mathcal G.$$

These are identities, not a state closure. The individual scalar bilinears and spatial kinetic trace need not have fixed signs. Multiple axial currents can cancel; with different rest frames their total squared norm need not even be spacelike. Therefore neither universal repulsion nor a universal density threshold follows from this formula.

For **one regular commuting spinor only**, Fierz gives $A^2=n^2=S^2+\Pi^2$, $n=\sqrt{-j^2}>0$. It follows that $|S|\leq n$ and the stronger single-field results in [REGULARITY_AND_BOUNCE.md](REGULARITY_AND_BOUNCE.md) apply.

| Statement | Single regular classical spinor | Multiple fields / quantum matter |
|---|---|---|
| Conserved chosen current | Yes for the specified action | Total current yes for the classical multi-field action; quantum interpretation/state must be specified. |
| $A^2=n^2$ | Exact Fierz identity | Not a total-current identity; quantum composite expectations are a different object. |
| Current e-fold/density relation | Exact where the current is timelike/nonzero | Exact for any timelike conserved total current, but not automatically physical particle-number expansion. |
| Quartic source scales as $e^{-6N_u}$ | Exact along the single-current curve | Requires extra polarization/correlation assumptions; not generally valid. |
| Density-only Ricci blow-up bound | Derived for fixed finite mass | Cannot be inferred by substituting total density. |
| Realistic fermion gas / nuclear EOS | Not supplied by the classical spinor | Requires a state, interactions, renormalization and justified approximations. |

## Physical and global meaning

A classical Dirac current gives a definite mathematical congruence. Identifying it with bulk matter or individual particle paths requires a physical approximation; in quantum theory a charge current is not necessarily a conserved, future-timelike particle-number current in a pair-producing state. An unpolarized quantum state can have $\langle A\rangle=0$ but nonzero $\langle A^2\rangle_{ren}$. Replacing that correlator by a classical mean-current square changes the model.

Positive-frequency restrictions in a dynamic curved spacetime require a declared state/mode construction; they are not a pointwise inequality $\mathcal G\geq0$. The previously constructed local bounce is not thereby a verified realistic state. Strong/EM/weak interactions, degeneracy and dense-matter correlations are not generated merely by naming ECD; see the retained [matter-model review](../ec-matter-models/RECOMMENDATION.md).

A smooth classical source-free collar has zero algebraic torsion and GR vacuum, potentially with gravitational radiation/Weyl curvature. It does not provide a solved global matching or constraint-gluing problem. ADM/Bondi mass needs appropriate asymptotics; a local density integral or spherical Misner–Sharp mass is not generally its substitute. Finite bounded curvature over a short interval is not geodesic completeness, and a local current-volume turn is not reversal inside a trapped black-hole spacetime.

## Verificeret flerfelts-eksempel

[Den eksakte seks-felts løsning](CHIRAL_MULTIFIELD_BENCHMARK.md) viser, at en timelig total aksialstrøm og et torsionsdrevet kosmologisk bounce er mulige i denne action. Den er verificeret ved substitution i alle felt- og stresskomponenter. Den er ikke en løsning for vilkårlige startdata eller en realistisk kvantegas.
