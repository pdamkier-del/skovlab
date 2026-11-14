# General regularity statements and what bounce does not follow from them

## 1. Exact single-spinor compression obstruction

Assume the specified minimally coupled classical action, one finite constant mass, $\kappa>0$, $G_A=3\kappa/16>0$, a regular timelike nonzero current, and the field equations. No homogeneity, spatial symmetry, isotropy, EOS or absence of shear/vorticity is assumed.

The **Levi–Civita metric** trace equation is

$$R=\kappa mS-2\kappa G_A n^2,\quad S=\bar\psi\psi,\quad |S|\leq n.$$

The scalar $S$ may vary and change sign, but its magnitude is only linear in $n$. Hence

$$\lim_{n\to\infty}\frac R{n^2}=-2\kappa G_A<0.$$

The geometric full torsion contraction independently satisfies

$$\mathcal T_2=T_{abc}T^{abc}=-\frac32\kappa^2 A^2=-\frac32\kappa^2n^2.$$

Because conservation gives $n=n_0e^{-3N_u}$, both invariants diverge if a followed element undergoes unlimited compression $N_u\to-\infty$. No negative spatial kinetic trace or anisotropic stress can cancel the leading term in this *scalar trace* for a single field; those terms already canceled on shell.

This is conditional: it does not prove that any chosen initial cloud reaches unlimited compression. A regular bounce or some other evolution could prevent it. If the divergence occurs at finite material proper time, it is an invariant obstruction to a regular metric/connection extension there. If it occurs only asymptotically at infinite proper time, curvature unboundedness alone is not a proof of finite-time geodesic incompleteness. Classical validity may fail before either limit.

One must also not monitor only the full-connection scalar. Purely axial algebraic torsion gives

$$\widetilde R=R+q^2/24=R+3\kappa^2 n^2/8=\kappa mS.$$

Thus $\widetilde R$ can vanish in a massless example while the metric Ricci scalar and torsion invariant diverge. A cancellation in one scalar is not full regularity.

## 2. A necessary density/e-fold bound if metric scalar curvature is bounded

If $|R|\leq R_*$ throughout a region, the preceding trace and $S\leq n$ require

$$2G_A n^2-mn-R_*/\kappa\leq0,$$
$$\boxed{n\leq n_{max}(R_*)=\frac{m+\sqrt{m^2+8G_A R_*/\kappa}}{4G_A}.}$$

Along a declared current curve this implies

$$N_u\geq-\frac13\ln[n_{max}(R_*)/n_0].$$

This is a **necessary regularity bound**, not a predicted bounce density, time or universal number of contraction e-folds. $R_*$ must be specified; an arbitrary numerical cutoff is not a physically established transition. Bounded scalar $R$ is not sufficient for bounded Weyl, other Ricci components, torsion derivatives, a regular current frame or a complete spacetime. A model can cease to be physically/numerically valid before reaching this bound.

For several species, $R=\kappa\sum m_fS_f-2\kappa G_AA_{tot}^2$. The total axial invariant is not $n_{tot}^2$ and can cancel. The single-field density bound cannot be reused with a total fermion density. Quantum renormalized composite/trace-anomaly terms require a different derivation.

## 3. Conditional bounds on expansion in a positive-Ricci phase

For one field, completing the trace square gives a pointwise upper bound

$$R\leq\kappa mn-2\kappa G_A n^2\leq\frac{\kappa m^2}{8G_A}=\frac23m^2.$$

If a phase satisfies a **uniform positive lower floor** $R\geq R_{min}>0$ along the current, it necessarily has

$$n_-\leq n\leq n_+,\qquad n_\pm=\frac{m\pm\sqrt{m^2-8G_A R_{min}/\kappa}}{4G_A}.$$

It can therefore accumulate at most the following **net** current-volume expansion:

$$N_u\leq\frac13\ln(n_+/n_-).$$

These are necessary trace/current conditions, not existence of such a phase. No bound on accumulated positive expansion over arbitrary repeated contraction/expansion cycles follows from the net endpoint relation. For an exact de Sitter curvature $R=12H_{dS}^2$ during the phase, the single-field bound implies

$$H_{dS}/m\leq\frac1{\sqrt{18}}\operatorname{sech}(3N_u/2).$$

This is **not a general inflation bound**: local acceleration in an arbitrary inhomogeneous geometry need not imply a positive scalar-Ricci floor. It does show why a short positive local bounce acceleration alone cannot establish a long positive-curvature expanding era in this minimal one-field model. For $m=0$ its trace forbids $R>0$ entirely; the multi-field example below has different algebra and does not obey that single-field conclusion.

A weaker but broader statement holds for any finite set of the classical fields. In the total-current rest frame, the bilinear bounds give $|A_{tot}^2|\leq n_{tot}^2$ and $|\sum m_fS_f|\leq m_{max}n_{tot}$. One proof writes total chiral currents $J_L,J_R$ as future causal vectors: $j=J_L+J_R$, $A=J_L-J_R$. Their norms and mutual inner products imply $-n_{tot}^2\leq A^2\leq n_{tot}^2$. The scalar bound also follows from $|S_f|\leq\sqrt{-j_f^2}$ and the reverse Lorentzian triangle inequality. Thus

$$|R|\leq\kappa m_{max}n_{tot}+2\kappa G_A n_{tot}^2.$$

Unbounded expansion of that conserved timelike total-current volume sends $n_{tot}\to0$ and consequently $R\to0$. A uniformly positive Ricci floor cannot persist through arbitrarily many such e-folds from a finite initial density. For a declared initial $n_0$, a necessary multi-field bound is

$$n_{tot}\geq\frac{-m_{max}+\sqrt{m_{max}^2+8G_A R_{min}/\kappa}}{4G_A},\qquad N_u\leq\tfrac13\ln(n_0/n_{min}).$$

There is no trace-only universal upper initial density in the multi-field case. These arguments do not apply directly to renormalized quantum charge/composite expectations.

## 4. General local bounce/acceleration condition

For any declared regular timelike matter congruence, the metric Einstein equations give

$$\dot\Theta=-\Theta^2/3-\sigma_{ab}\sigma^{ab}+\omega_{ab}\omega^{ab}-\frac\kappa2(\epsilon+3P)+\nabla_a a^a.$$

A strict local material volume turn requires $\Theta=0$, $\dot\Theta>0$ and regular continuation. The full ECD source identities in [GENERAL_ECD.md](GENERAL_ECD.md) identify its matter terms without choosing them independently. A no-bounce theorem follows only after justified sign bounds on the complete source and the shear/rotation/acceleration terms. Those bounds are not universal properties of arbitrary classical Dirac data.

Writing $a_u\propto v_u^{1/3}$ gives the exact local acceleration relation

$$\ddot a_u/a_u=\dot H_u+H_u^2=\frac13[-\sigma_{ab}\sigma^{ab}+\omega_{ab}\omega^{ab}-\tfrac\kappa2(\epsilon+3P)+\nabla_a a^a].$$

This is not a closed ODE for $a_u$; the other quantities require the full field solution. Local acceleration plus positive e-folds is also insufficient to establish an inflationary cosmology or an observational horizon history.

The [analytical local family](../ec-analytical-bounce/DERIVATION.md) shows a strict local turn with all constraints satisfied on an open patch and analytic local continuation. It violates a null energy condition and has no demonstrated physical positive-frequency fermion realization. The matching torsion-free Einstein–Dirac family also turns; its contact correction suppresses the turn. Its local Taylor coefficient determines an infinitesimal expansion, not a controlled long expansion or total e-fold count. Its time-symmetric initial geometry contains no strictly future-trapped surface lying wholly in the patch.

## 5. What is required for a whole cloud or black-hole conclusion

A finite collapse problem needs a complete constrained data family, specified matter state, asymptotic mass/charges, consistent exterior/boundaries, convergent evolution, regularity/validity control and declared material domains. Null expansions must be computed on actual two-surfaces. In general there is no spherical Misner–Sharp mass or single shell radius. Event horizons require global causal information, not one local expansion rate.

Raychaudhuri and singularity theorems have hypotheses, including energy/global conditions. Failure of an energy condition removes a theorem's guarantee; it does not itself prove a nonsingular complete spacetime. Conversely, a local turn or a finite numerical interval does not establish escape from a black hole or absence of later singularities.

A density tending to zero or a current becoming null can also make the chosen current-rest e-fold observable unusable without a curvature singularity. Very large rest-frame e-folds may partly reflect an unbounded tilt factor relative to a slice rather than a uniformly expanding universe. Monitor current conditioning, $W$, geometry and matter state together.

## 6. Useful research outcomes, without selecting for a desired bounce

A controlled experiment can conclude: a validated local turn; no turn within the computed interval; a restricted-class no-go; or an unresolved stop due to curvature, matter validity, boundary contamination, conditioning or numerical error. It cannot conclude universal bounce/non-bounce from a parameter scan. A true torsion attribution compares two action-consistent problems, with constraints resolved and the same declared physical free-data family, not by deleting a term while retaining invalid initial geometry.

The [six-chiral-field benchmark](CHIRAL_MULTIFIELD_BENCHMARK.md) additionally supplies an exact regular torsion-driven cosmological bounce and a finite accelerating e-fold count. It is not a bounded black-hole collapse or a controlled quantum-matter prediction. The general evidence otherwise supports exact identities and short weak-field diagnostics. It does not supply a universal count of post-collapse e-folds, an established realistic torsion-driven bounce or a general theorem covering every initial state of ECD.
