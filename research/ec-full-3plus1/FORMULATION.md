# Full local ECD equations and their numerical realization

## 1. One action, no fluid closure

The gravitational curvature and affine derivative conventions are those of the previous audit: signature $(-+++)$, derivative index first, $T^a{}_{bc}=2\widetilde\Gamma^a{}_{[bc]}$, $\epsilon_{0123}=1$, and

$$R^\rho{}_{\sigma\mu\nu}=\partial_\mu\Gamma^\rho{}_{\nu\sigma}-\partial_\nu\Gamma^\rho{}_{\mu\sigma}+\Gamma^\rho{}_{\mu\lambda}\Gamma^\lambda{}_{\nu\sigma}-\Gamma^\rho{}_{\nu\lambda}\Gamma^\lambda{}_{\mu\sigma}.$$

Use $\{\gamma^a,\gamma^b\}=-2\eta^{ab}$, $\gamma_5=-i\gamma^0\gamma^1\gamma^2\gamma^3$ and $\bar\psi=\psi^\dagger\gamma^0$. Define the **geometric** frame connection unambiguously as

$$W_\mu{}^a{}_b=e^a{}_\nu(\partial_\mu e_b{}^\nu+\widetilde\Gamma^\nu{}_{\mu\lambda}e_b{}^\lambda),\qquad \widetilde D_\mu=\partial_\mu-\tfrac18 W_\mu{}^{ab}[\gamma_a,\gamma_b].$$

The minus sign is required by our negative Clifford convention. If writing $D=\partial+\omega[\gamma,\gamma]/8$, then $\omega=-W$, not $W$. This distinction was not specified consistently in the older geometric torsion formula; the independent correction is in [CONVENTION_AUDIT.md](CONVENTION_AUDIT.md).

Start with

$$S=\int e\,d^4x\left[\frac{\widetilde R}{2\kappa}+\frac i2\bar\psi\gamma^\mu\overleftrightarrow{\widetilde D}_\mu\psi-m\bar\psi\psi\right].$$

With $q^d=\epsilon^{abcd}T_{abc}$, direct connection substitution now gives

$$\mathcal L_{aux}=\frac{q^2}{48\kappa}-\frac{q\cdot J_5}{8},\quad J_5^a=\bar\psi\gamma_5\gamma^a\psi,\quad q^a=3\kappa J_5^a,$$
$$T_{abc}=-\frac\kappa2\epsilon_{abcd}J_5^d,\qquad C_{abc}=T_{abc}/2.$$

Eliminating the auxiliary field gives the same established effective action

$$S_{eff}=\int e\,d^4x\left[\frac R{2\kappa}+\mathcal L_D^\circ-G_AJ_5^aJ_{5a}\right],\qquad G_A=3\kappa/16.$$

The spin-connection variation is totally antisymmetric and determined by the Dirac field, not a Frenkel fluid or an independent spin-pressure ansatz. In the geometric $W$ convention, $\delta S_m=-\frac i{16}\int e\bar\psi\{\gamma^\mu,[\gamma_a,\gamma_b]\}\psi\,\delta W_\mu{}^{ab}$. An operational spin current must specify which connection variable it differentiates.

Spinor and tetrad variation give

$$i\gamma^\mu D_\mu^\circ\psi-m\psi-2G_AJ_{5a}\gamma_5\gamma^a\psi=0,$$
$$T_{\mu\nu}=-\frac i4\left[\bar\psi\gamma_\mu\overleftrightarrow D_\nu^\circ\psi+\bar\psi\gamma_\nu\overleftrightarrow D_\mu^\circ\psi\right]+G_Ag_{\mu\nu}J_5^2.$$

The stress formula is on shell. The Dirac equation supplies its time derivatives; the derivative term is not omitted when computing energy, flux or stresses. The adjoint is evaluated with the same connection. In particular the boosted nonlinear plane-wave test independently checks the full stress, not merely its trace or rest limit. Global U(1) and diffeomorphism identities imply $\nabla_\mu j^\mu=0$ and $\nabla_\mu T^{\mu\nu}=0$ in the continuum. Axial current need not be conserved.

## 2. General triad and explicit Dirac time derivative

The evolved variables at each point are ten $g_{\mu\nu}$, ten $p_{\mu\nu}=\partial_tg_{\mu\nu}$ and four complex $\psi_A$: 28 real functions. Derivatives are recomputed rather than independently evolved, so there are no independent first-order reduction fields. A positive-definite spatial metric and $g^{00}<0$ are required:

$$N=(-g^{00})^{-1/2},\quad\beta^i=N^2g^{0i},\quad\gamma_{ij}=g_{ij},\quad n^\mu=N^{-1}(1,-\beta^i).$$

For $\gamma=LL^T$ with lower Cholesky $L$, choose $e_0{}^\mu=n^\mu$, $e_a{}^0=0$, $e_a{}^i=(L^{-T})^i{}_a$. This fixes the local tetrad gauge algebraically, including the spatial rotations. Compute $\partial_\mu L$ by setting $Q=L^{-1}(\partial_\mu\gamma)L^{-T}$, taking its lower triangle with half the diagonal, $X$, and using $\partial_\mu L=LX$. Thus no numerical difference of matrix square roots is used.

The coframe is the inverse frame. The connection formula above supplies $\Omega_\mu=-W_\mu{}^{ab}[\gamma_a,\gamma_b]/8$ and curved matrices $\gamma^\mu=e_a{}^\mu\gamma^a$. Their independently tested identity is

$$\partial_\mu\gamma^\nu+\Gamma^\nu{}_{\mu\lambda}\gamma^\lambda+[\Omega_\mu,\gamma^\nu]=0.$$

Let $B=mI+2G_AJ_{5a}\gamma_5\gamma^a$. Since $(\gamma^t)^{-1}=N^2\gamma^t$, the complete time equation used in code is

$$\partial_t\psi=-\Omega_t\psi-(\gamma^t)^{-1}\left[\gamma^i(\partial_i+\Omega_i)\psi+iB\psi\right].$$

Every field component, spatial derivative, metric velocity and nonlinear current is recomputed at every integration stage. There is no prescribed spin alignment during evolution.

## 3. Harmonic gravitational evolution

Choose harmonic coordinates, $\mathcal C^\mu=g^{\alpha\beta}\Gamma^\mu{}_{\alpha\beta}=0$. Define

$$\mathcal R_{\mu\nu}=R_{\mu\nu}-\nabla_{(\mu}\mathcal C_{\nu)}.$$

Direct Christoffel differentiation cancels the mixed gauge principal part, leaving

$$\mathcal R_{\mu\nu}=-\tfrac12g^{\alpha\beta}\partial_\alpha\partial_\beta g_{\mu\nu}+Q_{\mu\nu}(g,\partial g).$$

No hand-transferred expanded quadratic source is used: the code evaluates Ricci and the covariant derivative of the contracted connection from the same metric jets. Let $\mathcal R^{(0)}$ be this expression with $\partial_t^2g=0$, retaining spatial and mixed derivatives. Then all ten metric accelerations are

$$\boxed{\partial_t p_{\mu\nu}=\frac2{g^{00}}\left[\mathcal R^{(0)}_{\mu\nu}-\kappa\left(T_{\mu\nu}-\tfrac12g_{\mu\nu}T\right)\right],\qquad \partial_tg=p.}$$

The coefficient $-g^{00}/2$ is checked by arbitrary metric-jet perturbations, independently of analytic solutions. There is no added bounce or matter term, no imposed constraint projection and no undocumented damping. For conserved stress the continuum reduced Einstein equations imply the usual homogeneous wave equation for $\mathcal C_\mu$ (Ricci-coupled). Initial $\mathcal C=0$ and its normal derivative, equivalently the gravitational constraints together with gauge initialization, recover Einstein solutions locally where the Cauchy problem is regular.

The gravitational wave principal part and Dirac characteristic cone are metric-null. This does **not** by itself prove a well-posed discretization of the full mixed-order coupled system: the stress contains spinor derivatives. No new general nonlinear stability theorem is claimed. Analytic, time/spatial convergence and noise tests are limited numerical evidence, not a substitute for such an analysis.

## 4. Independent ADM audit and expansion

Extract $K_{ij}=-(\partial_t\gamma_{ij}-\mathcal L_\beta\gamma_{ij})/(2N)$ and $E=T_{nn}$, $j_i=-T_{in}$, $S_{ij}=T_{ij}$. Independently recompute spatial Christoffel/Ricci, then

$$\mathcal H={}^{(3)}R+K^2-K_{ij}K^{ij}-2\kappa E,\qquad \mathcal M_i=D_j(K^j{}_i-\delta^j_iK)-\kappa j_i.$$

These are diagnostics, not replaced by reduced Einstein equations. Set $H=-K/3$ and $\sigma_{ij}=-K_{ij}-H\gamma_{ij}$. Algebra gives

$$6H^2=2\kappa E-{}^{(3)}R+\sigma_{ij}\sigma^{ij}+\mathcal H.$$

Thus the Friedmann residual equals $\mathcal H$ off constraint; it is not an additional independent gravitational test. The shear norm, local normal expansion and its distinction from matter flow remain as in the previous ADM audit. A local normal-volume turn needs $H=0$ and $\partial_nH>0$ along with regularity, but says nothing alone about a global cloud bounce. The current frame can be undefined at nodes/null current. The prototype does not construct a followed material volume or identify a bounce.

## 5. Constrained, inhomogeneous initial data

On a finite cube choose compact smooth complex seed $\Psi(x)$, a free mean-curvature profile $K_*(x)$, and conformal variables

$$\gamma_{ij}=\chi^4\delta_{ij},\quad K_{ij}=\chi^{-2}(LW)_{ij}+\gamma_{ij}K_*/3,\quad\psi=\chi^{-3}\Psi,$$
$$ (LW)_{ij}=\partial_iW_j+\partial_jW_i-\tfrac23\delta_{ij}\partial_kW^k.$$

Solve four discrete nonlinear equations $\mathcal H=0$, $\mathcal M_i=0$ for $\log\chi,W^i$ at all interior nodes. The **full ECD stress** is recomputed for every trial. This is not a dust conformal-source substitution. The finite-cube boundary is $\chi=1,W=0$. Nonconvergence or an excessive final residual rejects the data; existence/uniqueness for arbitrary seeds is not assumed.

Initially set $N=1,\beta=0$, $p_{ij}=-2K_{ij}$. The four unknown $p_{0\mu}$ are solved algebraically from $\mathcal C^\mu=0$, rather than assuming lapse/shift time derivatives vanish. The test seed is a triaxial $C^\infty$ bump times a spatially complex four-component vector, an optional phase and a spatial SU(2) spin rotation. These are actual spinor initial data, not a spin transport prescription. The scalar/vector conformal ansatz restricts this initial-data family but does not restrict the evolved metric thereafter.

An ADM mass requires an asymptotically flat constraint solution and an asymptotic surface integral; this finite-cube solve supplies neither. Seed amplitude, coordinate support radius and prescribed mean-curvature profile are therefore exposed as field-data controls, not presented as independent physical mass/radius/collapse-speed controls. In the continuum a smooth source-free collar has algebraic torsion zero and vacuum GR if constraints/gauge remain satisfied. Fixed numerical boundary values do not construct that exterior or its junction conditions.

## References and scope

- Hehl & Datta (1971), [doi:10.1063/1.1665738](https://doi.org/10.1063/1.1665738): nonlinear Dirac theory.
- Shaposhnikov et al., [arXiv:2008.11686](https://arxiv.org/abs/2008.11686): effective minimal quartic interaction; retain the present explicit geometric connection convention.
- Gourgoulhon, [gr-qc/0703035](https://arxiv.org/abs/gr-qc/0703035): ADM projections and conformal initial data.
- Lindblom et al., [gr-qc/0512093](https://arxiv.org/abs/gr-qc/0512093): generalized harmonic evolution and constraints. We use the second-order zero-gauge-source reduction, not their entire first-order/damped boundary algorithm.
- Müller & Nowaczyk, [arXiv:1504.01034](https://arxiv.org/abs/1504.01034): torsion-free Einstein–Dirac Cauchy analysis. Not a proof of our finite-difference scheme.

The implemented engine is general local classical ECD. Its validation is presently limited to short weak fields and documented benchmarks. It is not a quantum gas, EC–Standard-Model simulation, established complete black-hole spacetime or a bounce demonstration.
