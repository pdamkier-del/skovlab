# Exact torsion-driven cosmological bounce: six classical chiral fields

This is an **explicit special benchmark of the finite-field action**, not a replacement for the general 3D solver, an averaged spin fluid, or a bounded black-hole interior. It shows why single-spinor results must not be generalized to all classical ECD matter. All six Dirac equations and the complete summed stress are checked directly with gamma matrices.

## 1. Full fields and symmetry assumptions

Take six independent, neutral, massless classical Dirac fields with the same chirality and the minimal common ECD action. Use a spatially flat FLRW **metric** on a periodic three-torus of coordinate side L, with periodic spin structure:

$$ds^2=-dt^2+a(t)^2d\mathbf x^2=a(\eta)^2(-d\eta^2+d\mathbf x^2).$$

The momenta have equal magnitude $p$ and directions $\mathbf d_f=\pm\mathbf e_x,\pm\mathbf e_y,\pm\mathbf e_z$. Choose normalized constant spinors $u_f$ satisfying

$$u_f^\dagger u_f=1,\quad\gamma_5u_f=u_f,\quad(\gamma^0\gamma^i d_{fi})u_f=u_f.$$

They are positive eigenmodes of the *free* massless kinetic Hamiltonian. Their physical interacting temporal frequency is determined below, not assumed positive at all densities. The actual fields are

$$\psi_f=\sqrt{n_0/6}\,a^{-3/2}u_f\exp[i p\mathbf d_f\cdot\mathbf x-i\vartheta(t)].$$

For fundamental torus modes, $p=2\pi/L$. No interference terms between independent species are added to their kinetic stresses; all action-required cross-species terms in the **total axial current square** are retained. A single spinor formed by superposing these modes would have extra interference and is not this model.

The identities $\sum\mathbf d_f=0$ and $\sum d_{fi}d_{fj}=2\delta_{ij}$ make the total source exactly isotropic. The individual fields are not SO(3)-invariant. This is a consistent metric-only reduction verified by the field equations, not an assumed symmetry of every field or an averaging rule.

## 2. Timelike axial source and exact effective stress

Each chiral current is null, but their sum is timelike:

$$j_{tot}^{\hat a}=(n,0,0,0),\qquad A_{tot}^{\hat a}=(-n,0,0,0),\qquad n=n_0a^{-3},\quad A_{tot}^2=-n^2.$$

This **opposite sign** to the regular single-spinor Fierz relation is permitted for several fields. Vary the action with this total current before substituting the modes. The six nonlinear Dirac equations require a common phase

$$\dot\vartheta=p/a-2G_A n.$$

The complete on-shell summed stress is diagonal and gives

$$\boxed{\epsilon=\rho_r-\rho_s,\qquad P=\rho_r/3-\rho_s,\qquad\rho_r=pn_0a^{-4},\quad\rho_s=G_A n_0^2a^{-6}.}$$

Here $\rho_s$ is merely a positive abbreviation for a **derived negative contribution**, not an independently introduced fluid. The pressures, coefficients, cross terms and phase all follow from the same action. In particular the contact metric term alone is not the whole interaction energy: the kinetic frequency shifts too. The conservation law $\dot\epsilon+3H(\epsilon+P)=0$ follows directly.

## 3. Closed-form spacetime and spinor phase

Let $C_r=pn_0$, $C_s=G_A n_0^2$, $a_b^2=C_s/C_r=G_A n_0/p$ and $q^2=\kappa C_r/3$. The flat Hamiltonian constraint is

$$H^2=\frac\kappa3(C_ra^{-4}-C_sa^{-6}).$$

In conformal time it becomes $a'^2=q^2(1-a_b^2/a^2)$ and integrates exactly to

$$\boxed{a(\eta)=\sqrt{a_b^2+q^2\eta^2},\qquad -\infty<\eta<\infty.}$$

This curve is the result of the action-derived Einstein equations, not an assigned bounce shape. The independent spatial equation $\dot H=-\kappa(\epsilon+P)/2$ is also satisfied. Proper time from the bounce is

$$t(\eta)=\frac12\left[\eta\sqrt{a_b^2+q^2\eta^2}+\frac{a_b^2}{q}\operatorname{arsinh}(q\eta/a_b)\right].$$

With the fixed minimal coefficient $G_A=3\kappa/16$, $q/a_b=4p/3$ and

$$\vartheta(\eta)=p\eta-\frac32\arctan(4p\eta/3).$$

These expressions specify all six fields and the metric at all finite times. The frequency changes sign near the bounce; this interacting classical solution is not a proof of a positive-energy quantum quasiparticle state through the turn.

At the bounce $H=0$, $\epsilon=0$ and $P=-2\rho_b/3$, where $\rho_b=C_r/a_b^4$. Thus $\dot H_b=\kappa\rho_b/3>0$. Every finite-time field/curvature component remains bounded because $a\geq a_b>0$. Null affine length is proportional to $\int a^2d\eta$, which diverges at both ends. Timelike geodesics have $d\tau/dt=(1+\mathbf P^2/a^2)^{-1/2}$ bounded below by a positive constant for fixed conserved momentum. Since $t\to\pm\infty$, causal geodesics extend indefinitely both ways. This is a globally regular, causally geodesically complete **classical cosmological benchmark**. No stability under arbitrary perturbations is proved.

## 4. E-folds: accelerated growth is limited

The total current is aligned with the metric normal, so all three directional and material/normal scale e-folds agree. For $\eta>0$,

$$\boxed{N_{post}=\ln(a/a_b)=\frac12\ln[1+(q\eta/a_b)^2].}$$

Total future expansion is unbounded as $\eta\to\infty$, but most is decelerated radiation-like expansion. From the exact source,

$$\ddot a/a=\frac\kappa3(2C_sa^{-6}-C_ra^{-4})>0\quad\Longleftrightarrow\quad a^2<2a_b^2.$$

The post-bounce accelerating phase therefore contains exactly

$$\boxed{N_{acc}=\ln\sqrt2=\frac12\ln2\simeq0.346574.}$$

This is not 50–60 accelerating inflationary e-folds. Formally reaching a large total $N$ later does not turn the radiation tail into inflation. The NEC is violated closer to the bounce ($a^2<3a_b^2/2$), with $N_{NEC}=\frac12\ln(3/2)$; its breakdown is part of the mechanism, not hidden by $\epsilon\geq0$.

## 5. Torsion-free comparison and physical limits

Remove the contact in the **separate Einstein–Dirac action**, keep the same comoving modes/charges and an initial scale factor above $a_b$, and solve its constraints anew. Its contraction obeys $\dot a=-q/a$ and reaches $a=0$ in finite proper time. Radiation has $R=0$ there, but Kretschmann diverges. It has no regular continuation through the zero scale factor. Thus torsion genuinely removes the classical radiation crunch **in this matched six-field cosmological family**, unlike the previous one-field planar example where torsion suppressed a gradient-driven turn.

Physical realism is unresolved. Classical mode amplitudes are arbitrary; a large commuting amplitude is not automatically a permissible fermion occupation. For illustration only, normalize to one particle per independent fundamental torus mode: $n_0=6/L^3$ and $p=2\pi/L$. Substitution into the classical benchmark gives

$$\rho_b=\frac{p^3}{G_A^2n_0}=\frac{1024\pi^3}{27\kappa^2}\simeq1176\,\bar M_P^4.$$

The corresponding metric Ricci scalar is $R_b=2\kappa\rho_b$, far above reduced-Planck curvature. This is outside controlled classical spacetime/EFT expectations, not a reliable quantum prediction. It is not a derivation of the renormalized quantum stress: exchange, correlations, species content and state validity must be calculated separately. Lowering classical curvature by arbitrarily increasing a mode amplitude does not establish a Pauli-compatible physical state.

The background also requires exact chirality, equal momentum magnitudes and balanced directions. Full-field perturbative/nonlinear stability, realistic interactions and robustness are unestablished. This benchmark has no vacuum exterior, ADM mass of an isolated body, matched black-hole interior or baby-universe construction. It establishes a precise mathematical possibility and e-fold count in one declared action/data family, not a general prediction for gravitational collapse.
