# Assessment of bounce and no-bounce results

Baseline: d069bfac8398cc71793c542ad93d650cc511794c. A result is always attached to its action, state, symmetry, initial data and observable.

## What qualifies as a bounce?

For a nonzero timelike chosen current \(j^\mu=nu^\mu\), a strict infinitesimal material-volume minimum needs
\[
\Theta=\nabla_\mu u^\mu=0,\qquad \dot\Theta=u^\mu\nabla_\mu\Theta>0
\]
and a regular solution on both sides. After torsion elimination the metric Raychaudhuri equation is
\[
\dot\Theta=-\Theta^2/3-\sigma_{ab}\sigma^{ab}
+\omega_{ab}\omega^{ab}-\kappa(\epsilon+3P)/2+\nabla_a a^a.
\]
Normal expansion, areal-radius extrema, principal directional turns and material-volume minima are different observables. At current nodes or null current the rest-frame observable fails, which need not indicate curvature blow-up.

A **finite-cloud bounce** additionally needs complete constrained initial data for an isolated distribution, a physical state/regime, consistent exterior or controlled asymptotics, actual regular evolution of a declared finite material domain, and bounds on relevant metric/torsion curvature. A black-hole reversal needs trapping/causal information as well. Failure of a singularity-theorem energy hypothesis supplies no replacement completeness proof.

## Inventory

| Investigation | Configuration and initial data | Turning/no-turn condition | Local/global status and torsion attribution |
|---|---|---|---|
| Averaged FLRW spin fluid | \(p=w\rho,\epsilon=\rho-q,P=w\rho-q\); homogeneous conserved \(\rho\propto a^{-3(1+w)},q\propto a^{-6}\); initial contracting constraint branch, curvature k as specified in each run | \(H=0\), \(\kappa(\rho-q)=3k/a^2\), \(\ddot a/a=-\kappa[(1+3w)\rho-4q]/6>0\) | A legitimate homogeneous reduced-model turn for admissible parameters; flat case q=ρ. Does not establish a causal perturbed finite body |
| Coherent aligned ideal Weyssenhoff metric-only FLRW | Spatially oriented coherent spin, \(\dot b=-3Hb,q=\kappa b^2\); complete source is not isotropic under all rotations | Same scalar source equations in this special branch | Compatibility example, not statistically isotropic microscopic matter or a new isolated collapse |
| General spherical averaged/full ideal radial fluid | Constrained spherical profiles; coherent radial spin must be regular at center; no evolved trajectory | Areal turn \(U=0,D_tU>0\); volume turn \(\Theta=0,D_t\Theta>0\), retaining gradients/shear | Necessary conditions and restricted no-go only; no computed finite-cloud bounce |
| One aligned positive-density ECD LRS field | Homogeneous flat LRS metric; \(n_0,m\ge0\), D₀ chosen and contracting H₀ solved from constraint | \(6H^2=2\kappa(mn+G_An^2)+2D^2/3\) excludes H=0 for nonzero source/shear | Exact no-volume-bounce on this branch. Not general ECD, not finite matter |
| Broader flat homogeneous single-field \(\mathcal G=0\) obstruction | Current-normal homogeneous branch, no spatial kinetic trace; allow either sign of S | At H=0, \(\dot H=-\sigma_{ij}\sigma^{ij}/4-\kappa G_An^2/2\le0\) | Conditional local obstruction; gradients, curvature or tilt fall outside hypotheses |
| Analytic planar single-field construction | Local analytic constrained patch, Kᵢⱼ=0, positive χ; exact spinor profile below | Both initial expansions zero and explicit positive derivatives | Genuine regular local turn with NEC violation; exists also without torsion, which suppresses it |
| Full 3D prototype and passive tracers | Compact triaxial seed on finite cube, discrete constraints; very short weak fields | No validated event detector or finite-domain bounce result | Outputs correctly say “not-assessed”; tiny positive tracer e-folds are not a collapse bounce |
| Six chiral classical fields | Six independent massless species, same chirality, equal opposite axis momenta and populations, flat torus FLRW | Exact a≥a_b>0, H_b=0, \(\dot H_b>0\) | Globally regular classical cosmological bounce; torsion genuinely responsible within matched family; no finite cloud or quantum-state validity |

The homogeneous fluid result follows the type of source used by [Hashemi et al.](https://arxiv.org/html/1407.4103v2). Their matching discussion uses generalized Vaidya; it cannot be cited as a constructed source-free exterior for this project's arbitrary ECD data.

## Fluid bounces: mathematically useful but a failed generic collapse closure

For ordinary dust with q>0 the homogeneous turn can have finite \(a,\rho,q\) and finite effective-metric curvature. That is a useful ODE benchmark. It is not enough to bound microscopic torsionful curvature in an averaged state: a variance alone does not specify the underlying connection and its derivative correlations.

In the selected conserved-spin fluid, radial characteristics fail before a low-spin \(w<1\) contracting branch reaches the flat turn: \(c_{\rm eff}^2<0\), then h=0, then superluminal roots. For dust the entire \(0<q/\rho<1/2\) interval is nonreal. The geodesic spherical volume-turn threshold lies above the causal low-spin bound. Pressure gradients/acceleration can change local turns, so this is not a blanket exclusion of spherical bounces.

No smooth vacuum boundary was supplied. A comoving layer-free perfect-source surface against vacuum requires P=0. Homogeneous dust with P=-q violates it whenever boundary spin is nonzero. A different exterior or a surface layer must be physically specified. The coherent ideal radial source does not remove the acoustic issue.

## LRS Dirac no-bounce: strong result, narrow state class

For
\[
\psi=\sqrt{n_0/v}e^{-i\theta}(0,0,1,0)^T,\quad
\dot\theta=m+2G_An,\quad n=n_0/v,
\]
the full source is \(E=mn+G_An^2,P=G_An^2\).
Arbitrary triaxial rates would produce off-diagonal stress; LRS is required for this specified polarization. With D=B-A,
\[
Dv=D_0,\quad v(0)=1,\quad
v(\tau)=1+3H_0\tau+\tfrac34\kappa mn_0\tau^2.
\]
The negative constraint root fixes H₀. For nonzero n₀ or shear the contracting physical branch reaches its first zero of v without an allowed positive-volume turn. A later root or a vertex in the formal polynomial beyond the first zero is not a regular extension of the solution.

The numerical code stops earlier at an operational limit. It has not numerically evolved a physical singularity. In the mathematical limit n diverges and the trace/torsion invariants diverge for nonzero n₀. Pure vacuum needs a separate Kasner/Minkowski classification; zero Ricci alone is insufficient.

## Planar local bounce: keep the result, correct its interpretation

The exact initial patch is
\[
\gamma_{ij}=\chi(z)^4\delta_{ij},\quad K_{ij}=0,\quad
\psi=\sqrt{n_*}\chi^{-3}(i\sin cz,0,\cos cz,0)^T,
\]
with \(\chi(0)=1,\chi'(0)=0\) and the Hamiltonian ODE
\[
\chi''=-\frac\kappa4[mn_*\chi^{-1}\cos(2cz)+G_An_*^2\chi^{-7}-cn_*\chi^{-3}].
\]
All momentum constraints vanish. Analytic ODE existence gives a positive χ near the center; the analytic Cauchy continuation argument supplies a regular short spacetime patch.

For \(c=3m/4,n_*=m/(3\kappa)\),
\[
E_0=5m^2/(48\kappa),\quad
\partial_n\Theta_n=m^2/24,\quad
\dot\Theta_u=287m^2/96.
\]
Both have a strict minimum, but their rates differ because current acceleration divergence does not vanish even though acceleration itself vanishes at the center. The full stress contains a negative longitudinal gradient term.

The witness violates \(E_0+P_{z,0}=-m^2/(8\kappa)<0\). The flat reference profile's negative-energy sector carries 4/5 of its norm; this is a diagnostic of the reference, not an invariant spectral analysis of the actual curved patch.

Removing the contact while retaining the same free spinor seed and resolving the constraints gives another local turn. Contact corrections to the normal and current expansion derivatives are respectively \(-2\kappa G_An_*^2\) and \(-5\kappa G_An_*^2/2\). This example disproves a universal local classical no-turn claim but does **not** exhibit torsion-induced reversal. Small m can make classical curvature small without establishing a permissible fermionic state. Regularity is local, not geodesic completeness. Time-symmetric initial geometry has no strictly future-trapped surface wholly on that slice within the patch.

## Six-field bounce: the strongest exact positive result

Six independent species, rather than a superposition of one species, occupy directions \(\pm e_x,\pm e_y,\pm e_z\) with equal magnitude p on a torus. Each is massless and of the same chirality. The prescribed kinetic eigenspinors and phases solve every nonlinear Dirac equation:
\[
\psi_f=\sqrt{n_0/6}\,a^{-3/2}u_f
e^{ipd_f\cdot x-i\vartheta},\quad
\dot\vartheta=p/a-2G_An,\quad n=n_0a^{-3}.
\]
Each axial/vector current is null; their total has \(A^2=-n^2\), unlike a regular single field. Full summed stress gives
\[
\epsilon=C_ra^{-4}-C_sa^{-6},\quad
P=C_ra^{-4}/3-C_sa^{-6},\quad
C_r=pn_0,\ C_s=G_An_0^2.
\]
Define \(a_b^2=C_s/C_r,q^2=\kappa C_r/3\). Any contracting member with aᵢ>a_b uses the negative Friedmann root, rather than independently chosen aᵢ and Hᵢ. In conformal time,
\[
a(\eta)=\sqrt{a_b^2+q^2\eta^2},\qquad
\vartheta=p\eta-\tfrac32\arctan(4p\eta/3).
\]
At the turn \(\epsilon_b=0,P_b=-2\rho_b/3\), \(\dot H_b=\kappa\rho_b/3>0\). Both Einstein equations independently vanish under substitution.

Metric curvature is finite: \(R_b=2\kappa\rho_b\),
\(K_b=12q^4/a_b^8\). Torsion and its derivatives are smooth and bounded because n and a and their derivatives are regular, with a bounded away from zero. Proper time and null affine time extend to both infinities; this exact background is causally geodesically complete. No perturbative stability conclusion follows.

The torsion-free problem, with the same free comoving modes/charges and its constraints solved anew, has a radiation crunch. This is valid torsion attribution **within this special cosmological classical family**. At the same aᵢ the two constrained Hᵢ differ; retaining both unchanged would make the comparison inconsistent.

Post-bounce acceleration lasts only to \(a=\sqrt2a_b\), hence
\(N_{\rm acc}=\ln2/2=.34657359\). Infinite later radiation-like expansion is not infinite inflation.

For one occupation per independent fundamental mode, \(n_0=6/L^3,p=2\pi/L\):
\[
\rho_b=\frac{1024\pi^3}{27\kappa^2}
\simeq1175.94\,\bar M_P^4.
\]
Physical momentum at that bounce is \(p/a_b=8\pi^{3/2}\bar M_P/3\), also super-Planckian. Enlarging L does not lower these normalized bounce scales. Arbitrarily raising a commuting mode amplitude can lower the formal classical curvature while violating the intended occupation interpretation.

This normalization is an illustration, not a computed renormalized quantum state or a theorem excluding every possible many-fermion state. The interacting temporal frequency becomes negative near the turn; its sign is not by itself a quantum instability proof. Exchange, state fluctuations and higher-order effects need analysis. The exact solution has no vacuum exterior, isolated ADM mass, finite cloud or black-hole interior interpretation.

## Can these benchmarks validate the general solver?

Yes, within their species count, gauge and topology:

- Minkowski, gauge waves and the one-field LRS solution test the present one-field engine. Homogeneous proper-time data need harmonic-coordinate conversion or invariant comparison; a synchronous a(t) cannot simply be imposed as harmonic time.
- The planar data test pointwise stress, constraints and initial expansion derivatives on a patch. A Taylor coefficient does not supply exact boundary data for a long finite-box evolution.
- The six-field solution is an excellent future multi-species action/stress/evolution benchmark. The current one-field engine cannot represent it. Replacing six fields by one summed spinor or by a fitted fluid changes the equations. Total-current cross terms must remain.
- Perturbed-background tests would answer a new question. An exact-background regression test cannot establish stability.

**Answer to the finite-collapse question:** no current result establishes a regular bounce of a finite collapsing matter distribution with a controlled physical fermion interpretation and a consistent exterior. The exact cosmological result should nevertheless be preserved as a useful mathematical achievement.
