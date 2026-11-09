# Equation audit and numerical methods

The redesign preserves the equations in the original `ec-flrw/index.html` (repository baseline 2026-11-09). The previous page had no separate automated tests; its analytic dust solution and accelerated e-fold benchmark are now executable regression tests. No Holst term, particle creation, cosmological constant or anisotropic spin stress was added.

## Adopted closure

Einstein–Cartan theory algebraically relates torsion to spin. The equations here **assume** an isotropically averaged, unpolarized Weyssenhoff fluid, a barotropic ordinary fluid p=wρ with constant 0≤w<1, separate ordinary-fluid conservation, conserved particle number and no anisotropic effective stresses. Spin density squared then scales as inverse volume squared. This is a reduced effective model, not a general solution for a spin-polarized medium, inhomogeneous collapse or rotating black hole.

For a selected reference time t*, use τ=t/t*, c=1, L*=t*. All derivatives in the implementation are with respect to τ. The numerical KS X and Y are lengths divided by L*; its volume scale is (XY²)^(1/3). FLRW a is dimensionless. Physical rates and curvature are obtained by multiplying the displayed numerical values by t*⁻¹, t*⁻² or t*⁻⁴ as labelled. No physical seconds can be assigned without a density normalization.

## Spatially flat FLRW

Define ρbar=(8πG/3)ρ t\*² and the spin contribution B a⁻⁶ in the same convention:

- H² = A a⁻³⁽¹⁺ʷ⁾ − B a⁻⁶.
- ä/a = −(1+3w) A a⁻³⁽¹⁺ʷ⁾ / 2 + 2B a⁻⁶.
- Ḣ = ä/a − H².

Differentiating the constraint and using the scaling laws gives this acceleration equation; integrating (a,ȧ) avoids dividing by H at a bounce. A contracting or expanding initial state fixes A=1 and computes the signed H from the constraint. Impossible H²<0 is rejected.

The retained benchmark fixes H(0)=0, a(0)=a₀, B>0 and A=B a₀⁻³⁽¹⁻ʷ⁾. It integrates both forward and backward from τ=0. This **imposes** a regular candidate bounce for w<1, rather than predicting one from independent collapsing initial data. The original A=B=a₀=1 benchmark is unchanged.

For dust, a³=1+9τ²/4, H=(3τ/2)/(1+9τ²/4). The expanding accelerated e-fold benchmark is ln(4)/3; for general w with the original normalization it is ln[4/(1+3w)]/[3(1−w)]. Negative-time samples are genuine integration in negative proper time; every plotted quantity is evaluated on the same state. No individual curve is reversed independently.

## Kantowski–Sachs

For ds²=−dt²+X²dr²+Y²dΩ², define Hᵣ=Ẋ/X and HΩ=Ẏ/Y. In this convention ρ and S include 8πG t\*²:

- Constraint: HΩ²+1/Y²+2HᵣHΩ=ρ−S.
- Angular equation: 2Ÿ/Y+HΩ²+1/Y²=−(wρ−S).
- Mixed equation: Ẍ/X+Ÿ/Y+HᵣHΩ=−(wρ−S).

These are the Einstein equations for the stated **isotropic effective** energy density ρ−S and pressure wρ−S. With V=XY², ρ=ρ₀V⁻⁽¹⁺ʷ⁾ and S=S_coeff V⁻², their combined conservation equation holds: d(ρ−S)/dt+(Hᵣ+2HΩ)[(1+w)ρ−2S]=0. Consequently the constraint propagates in the continuum equations. Initial ρ is solved from the constraint; a nonpositive ordinary-fluid density is rejected. The spin control is S(0), with S_coeff=S(0)V(0)².

Set Hᵥ=(Hᵣ+2HΩ)/3, σ²=(Hᵣ−HΩ)²/3, Ḣᵥ=[Ẍ/X−Hᵣ²+2(Ÿ/Y−HΩ²)]/3. Then äᵥ/aᵥ=Ḣᵥ+Hᵥ² follows kinematically. No FLRW acceleration equation is applied to KS. Radial, angular and volume reversals are separate events. A volume minimum need not reverse both directions or avoid future curvature growth.

KS begins at τ=0 and runs forward, unlike the explicitly bounce-centred FLRW benchmark. Comparison overlays use each geometry's saved initial data and the same _declared_ reference t\*. FLRW absorbs a factor of 1/3 in its density coefficient; KS does not. These overlays are not matched-density or matched-initial-geometry physical comparisons. Their labelled times and units are directly comparable only after the user supplies a common physical normalization.

## Curvature and constraint diagnostics

These are Levi-Civita metric curvature scalars, not full torsionful connection invariants. For FLRW:

- R=6(Ḣ+2H²), K=12[(ä/a)²+H⁴].

For KS, write Aᵣ=Ẍ/X, AΩ=Ÿ/Y:

- R=2[Aᵣ+2AΩ+2HᵣHΩ+HΩ²+1/Y²].
- K=4[Aᵣ²+2AΩ²+2(HᵣHΩ)²+(HΩ²+1/Y²)²].

The orthonormal Riemann components give these expressions. An independent trace check is R=ρ−3p+2S in KS units (three times this in FLRW density units). Finite sampled curvature is not a proof of geodesic completeness.

The signed constraint C is exported. The visible residual is |C| divided by the sum of absolute magnitudes of its terms, with floor 10⁻³⁰. It is therefore a dimensionless relative diagnostic even near cancellation, not an absolute error with hidden units. A maximum above 10⁻⁵ triggers a possible numerical-divergence warning.

## Integration and events

`model.mjs` has no DOM dependencies. Adaptive classical RK4 compares one full step with two half steps, using the /15 error estimate and tol·(1+max|state|) per component. It accepts the two-half-step solution, limits step growth to ×2, and emits 800 regularly spaced samples per time direction, plus refined event states and the last accepted state if integration stops early. The same samples back all plots and playback. Events are detected on accepted internal steps, then refined with 35 bisections and reintegration inside that step; direction is classified from the relevant derivative at the root. Refined event states are inserted into the shared time series so the plotted minimum and event cursor are resolved even between regular output times.

A minimum step of 10⁻¹² or work cap of 200,000 attempts is an **integrator breakdown / work limit**, not a physical singularity. A scale below 10⁻⁵, |H| above 10⁶ or |Ḣ| above 10¹² triggers an **integration stopping threshold**. Diagnostics separately flag |H|>100, |Ḣ|>10⁴, a<0.01, individual KS scales<0.01 or σ²>10⁴ as candidate singular behaviour / rapid growth. These dimensionless heuristic thresholds are not physical criteria; tighten tolerances and inspect curvature and constraints before interpretation.

E-folds N=ln[a/a(first sample)]. Nacc integrates H only during expanding, positively accelerating samples with an endpoint-gated trapezoidal rule. Its output-grid quadrature is approximate, especially for an unresolved short accelerated episode. It is not automatically inflation. The root events, constraint, and local curvature do not depend on this e-fold quadrature.

The validation control repeats integration with tol/16 and an explicit maximum step of T/1600, half the original T/800 bound. This forces a smaller step even when output spacing rather than tolerance limits the original run. It reports the maximum |coarse−fine|/(1+|fine|) over a, H, Ḣ and K at identical regular output times (refined events are excluded from this comparison). Different stopping endpoints explicitly fail to establish convergence. Strong-collapse cases can lose accuracy even if a trajectory looks smooth: warnings and failed endpoint comparisons must be retained.

## Verification

Run `node --test ec-flrw/model.test.mjs`. Tests check the analytic dust trajectory and Nacc benchmark, FLRW spin and energy scaling, constraint-satisfying alternate initial data, KS curvature and trace identities, finite-difference derivatives, regular-regime tolerance stability, invalid states and stopping semantics.

For browser regression, serve the repository (`python -m http.server 8000`) and run `node ec-flrw/browser.test.cjs` with Playwright and Chromium installed. Plotly 3.3.0 is vendored with its MIT license header; the application needs no CDN, build service or paid hosting. The route remains `ec-flrw/` for GitHub Pages.

Background references retained from the prior implementation: [Bréchet et al.](https://arxiv.org/abs/0706.2367), [Hashemi et al.](https://arxiv.org/abs/1407.4103), [Popławski](https://arxiv.org/abs/2007.11556). These motivate the approximation; they do not establish every possible physical interpretation of a computed solution.
