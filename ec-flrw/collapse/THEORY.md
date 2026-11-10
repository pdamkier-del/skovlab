# EC Collapse Laboratory: theory, conventions and validation

This document describes the new homogeneous-collapse laboratory at `ec-flrw/`. The retained `geometry-lab.html` is a separate reduced-geometry explorer documented in `../MODEL.md`. Its density/spin inputs use older absorbed coefficients and must not be transferred numerically into this laboratory.

## Scope and status

The first deliverable implements FLRW ordinary GR and a specified minimal-EC averaged spin-fluid closure, Hamiltonian-constrained initial data, a diagnostic comoving spherical boundary, geometric Misner–Sharp mass, future-directed radial null expansions and local trapping events. The field-equation reductions and numerical method have automated benchmark tests. An individual parameter choice still requires its displayed constraint and convergence checks.

The parameter screen is an exploratory finite-interval calculation. The retained KS module is a reduced anisotropic model with its own equation tests, not a demonstrated matched black-hole interior. Radial inhomogeneity, anisotropic thermodynamic pressure, junction matching, particle production, thermodynamics and entropy evolution are **not implemented**. Neither a bounce nor an interior trapped surface establishes a black-hole event horizon or baby universe.

## 1. Action, signature and spin convention

Use signature (−+++), c=1 and κ=8πG, no cosmological constant, Holst term or higher-curvature action. With a metric-compatible connection, the minimal actions are

    I_GR = (1/2κ) ∫ d⁴x √−g R[g] + I_m[g,ψ]
    I_EC = (1/2κ) ∫ d⁴x √−g R̃[g,Γ̃] + I_m[g,Γ̃,ψ].

Define ∇̃*μ V^ρ = ∂*μV^ρ + Γ̃^ρ*{μν} V^ν, torsion T^ρ*{μν}=2Γ̃^ρ*[μν], and contortion K^ρ*{μν}=Γ̃^ρ*{μν}−{^ρ*{μν}}. Curvature convention is R^ρ*{σμν}=∂*μΓ^ρ*{νσ}−∂*νΓ^ρ*{μσ}+Γ^ρ*{μλ}Γ^λ*{νσ}−Γ^ρ*{νλ}Γ^λ*{μσ}, with R*{σν}=R^ρ\_{σρν}. Connection variation algebraically relates torsion to intrinsic spin; there is no independently propagating torsion wave in this minimal model. [Trautman, gr-qc/0606062](https://arxiv.org/abs/gr-qc/0606062) gives the theoretical background; numerical coefficients depend on definitions of spin current and torsion.

The implemented matter convention is specifically [Hashemi, Jalalzadeh and Ziaie, arXiv:1407.4103v2](https://arxiv.org/html/1407.4103v2), Eq. (9), translated to our signature:

    S² = ½〈S_{μν} S^{μν}〉,
    ρ_s = κ S²/4,
    ρ_eff = ρ − ρ_s,       p_eff = p − ρ_s,
    T_eff,μν = (ρ_eff+p_eff) u_μu_ν + p_eff g_μν,  u·u=−1.

This closure assumes an unpolarized homogeneous ensemble, 〈S*{μν}〉=0 but S²≠0, the Frenkel rest-frame spin condition S*{μν}u^ν=0, no resolved spin gradients, vorticity, mean polarization or anisotropic effective stress. It is not the universal stress tensor of every Weyssenhoff medium. In particular, [Bréchet, Hobson and Lasenby, arXiv:0706.2367](https://arxiv.org/abs/0706.2367) Eq. (25) writes a κS² correction in its own convention and contains additional spin-divergence and spin/kinematics terms in the full stress tensor. We do not mix their raw spin input with Hashemi's quarter-coefficient.

Ordinary matter obeys p=wρ, constant 0≤w<1. The selected homogeneous conservation equations are

    ρ̇ = −3H(ρ+p),       (S²)̇ = −6H S²,
    ρ = ρ_i (a_i/a)^[3(1+w)],    S² = S_i² (a_i/a)^6.

They imply effective energy conservation as well. Conserved particle number and fixed spin statistics underlie the spin scaling. Varying S_i² independently of ρ_i explores different microscopic normalization constants within this closure; it does not calibrate a particular stellar fermion gas. No temperature, baryonic mass, entropy or particle-production law is inferred.

## 2. Units and geometry

Choose a reference length L*, with reference time L* because c=1. All calculations use

    τ=t/L*,   ā=a_phys/L*,   R̄=R_phys/L*,
    ρ̄=κL*²ρ_phys,   p̄=κL*²p_phys,
    S̄²=κ²L*²S_phys²,   μ=Gm_MS/L*.

The bars are usually omitted in the source. The spin correction in normalized density units is S̄²/4. H is in L*⁻¹, Ḣ in L*⁻² and metric Kretschmann curvature in L*⁻⁴. The spin-squared plot's numeric value multiplies 1/(κ²L*²); it is not the same variable as the spin density correction.

The metric is

    ds² = −dt² + a²[dr²/(1−kr²)+r²dΩ²],   k∈{−1,0,+1}.

r is dimensionless; k is the normalized curvature sign. In the closed chart we require 0<r_b<1. We do not extrapolate the formulas across the chart equator. R_b=a r_b is an **areal radius**, not radial proper distance. Its rate is Ṙ_b=r_b ȧ, distinct from ȧ.

Optional L*/km only converts results: t_seconds=τ L*\_km/299792.458; R_km=R̄ L*\_km; m_MS/M_sun≈μ L*\_km/1.47662504. This does not supply an exterior solution or realistic stellar microphysics. With no scale entered, all outputs remain explicitly normalized.

## 3. Evolution and constrained initial conditions

In the normalized units above:

    H²+k/a² = (ρ−S²/4)/3,
    ä/a = −[ρ+3p−S²]/6,
    Ḣ = ä/a−H².

We evolve the regular system ȧ=v, v̇=−a[ρ+3p−S²]/6. The Friedmann equation is an initial constraint and an independent residual, not a square-root evolution equation. H=0 causes no solver division by zero. GR sets S²=0 throughout.

The user chooses either ordinary initial density and a branch (derive signed H_i) or signed H_i (derive ρ_i). Inadmissible H_i²<0, negative ordinary density, spin without ordinary matter, nonpositive scale or a boundary outside the regular chart are rejected. Initial R_i and r_b are linked through a_i: specifying one derives the other. A user-selected H_i=0 can impose a bounce or recollapse; the event is explicitly labelled as an initial turning point.

For this closure, a finite positive-scale bounce requires H=0 and Ḣ>0. At the event we display the constraint relation ρ−S²/4=3k/a² and margin S²−(ρ+3p)>0, equivalent to 4ρ_s>ρ+3p. These are local conditions within the chosen closure, not proof of a global regular spacetime.

Comparisons have a common proper-time origin τ=0 and declared L\*. Matching density, geometry, equation of state and boundary means GR and EC generally have **different initial H**. Matching H and geometry instead requires **different ordinary densities**. The interface states which comparison is being made. If the companion initial constraint fails, the primary run remains usable and a comparison error is shown.

## 4. Geometric mass, expansion and trapping

For R=ar and future null vectors l*±=∂_t±√(1−kr²)/a ∂_r, l*+·l_−=−2. Define

    θ_± = (2/R)[HR ± √(1−kr²)].

The geometric definition 1−2Gm*MS/R=g^{μν}(∂*μR)(∂_νR) gives

    C = 2Gm_MS/R = (ȧ²+k) r²,
    μ = R C/2 = R³ρ_eff/6,
    θ_+θ_- = 4(C−1)/R².

The mass plot independently compares geometric and effective-source expressions. μ is effective gravitational mass, not baryonic rest mass. It obeys the pressure-work identity μ̇=−p_eff R²Ṙ/2 and need not remain constant with spin or pressure. These formulas use the metric effective Einstein equations, not an independently integrated exterior torsion field.

Classification uses both expansions:

- θ*+>0, θ*-<0: untrapped.
- Both negative: future trapped.
- θ*+=0, θ*-<0: marginally outer trapped.
- Both positive: anti-trapped.
- θ*-=0, θ*+>0: marginally inner trapped.

C>1 alone cannot distinguish future trapping from anti-trapping. The radial map classifies shells inside the finite matter region, excluding r=0 where the expansion formula divides by zero. The marginal sphere has r_AH=1/√(ȧ²+k) when the denominator is positive. Only its part inside the plotted region is shown. In this homogeneous interior the trapped region can extend outward from that sphere; no exterior outermost horizon or event horizon is inferred.

A finite homogeneous region with effective pressure generally needs a consistent exterior/junction treatment; drawing its boundary does not solve that problem. No Schwarzschild or Vaidya exterior is attached by this version.

## 5. Solver, events and failure semantics

`solver.mjs` implements the seven-stage Dormand–Prince embedded 5(4) coefficients, using max_j |error_j|/[tol(1+max(|q_old,j|,|q_new,j|))]. The fifth-order state is accepted when this norm≤1; rejected steps shrink, and growth is limited to ×2. Reference: [Dormand and Prince (1980), J. Comput. Appl. Math. 6, 19–26](<https://doi.org/10.1016/0771-050X(80)90013-3>).

Output uses 640 common regular time samples, plus refined event states and the last accepted state. Internal steps are capped at T/640. Event functions are ȧ and HR_b±√(1−kr_b²); sign changes are refined by 38 bisections with reintegration inside the accepted step. Initial zero expansions are classified directly; initial zero H with nonzero acceleration is recorded as an imposed turning point. Several roots can occur in one accepted step; an even number of crossings of the same event within a single step can be missed, so convergence and short-episode resolution remain important.

Integration stops at a/a_i<10⁻⁵, |H|>10⁷, |Ḣ|>10¹⁴ or K>10³². These are display-independent **stopping thresholds**, not computed singular endpoints. Minimum step 10⁻¹³, nonfinite diagnostics or 100,000 attempts report numerical failure/work limit. Metric curvature is K=12[(ä/a)²+(H²+k/a²)²], R=6[ä/a+H²+k/a²]. A large rate or curvature produces a candidate-growth warning, not a proof of a singularity. In the empty open Milne limit, a→0 is a coordinate boundary with K=0; a small scale alone is especially insufficient.

The relative Friedmann residual divides |H²+k/a²−ρ_eff/3| by H²+|k/a²|+(ρ+ρ_s)/3, with floor 10⁻³⁰. Values above 10⁻⁶ warn of inadequate accuracy. Ordinary/spin invariant drifts monitor evaluation of the prescribed scalings; because conservation is imposed algebraically here, tiny drift alone does not independently validate the evolution.

The validation control repeats with tol/16 and max step T/1280. It compares a,H,K,θ_± at identical regular output times and turning-event times. PASS requires the same endpoint, scaled differences below 10⁻⁵, event-time differences below 10⁻⁵ and both relative constraints below 10⁻⁶. A numerical stopping endpoint generally fails this check even when its regular earlier history is accurate. No tail extrapolation is drawn after either run stops.

## 6. Benchmarks and literature reproduction

Automated tests include:

- Generic solver exponential and harmonic-oscillator solutions, root refinement and explicit failures.
- Flat GR dust: a=a_i[1+(3/2)H_iτ]^(2/3); geometric mass constant.
- Flat EC dust: let A=ρ_i a_i³/3 and D=S_i²a_i⁶/12. Then a³=D/A+(9A/4)(τ−τ_B)² and a_B=(D/A)^(1/3). This checks the exact flat equation corresponding to the small-curvature relation in Hashemi Eq. (31–33), without applying the small-curvature approximation to a finite-k trajectory.
- Closed GR dust cycloid and empty open Milne limit.
- Geometric/source mass equality, null product, Ricci trace, ordinary/spin invariants and pressure-work relation.
- Future trapping versus anti-trapping with the same compactness; marginal boundary roots and their ordering relative to a bounce.
- Actual half-step and tighter-tolerance convergence through a bounce.

**Published-parameter preset:** Hashemi Fig. 1 gives C=1.11, D=0.08, a_i=1 and ȧ_i=0 in H²=2Ca⁻³−Da⁻⁶−k/a². The constraint implies k_old=2.14. To use our discrete k=+1 chart, set a_new=a_old/√2.14 and r_new=√2.14 r_old, without rescaling time. Thus a_i,new=1/√2.14, ρ̄_i=6.66, S̄_i²=0.96, H_i=0. This normalized preset is tested against an independent quadrature of the full first integral between its two positive roots, with endpoint square-root behaviour removed by a sine-squared substitution. It reproduces the specified EC equation/parameter case, not a digitized figure fit or the paper's exterior matching. Its GR overlay follows our stated matching rule; it need not equal the paper's separate rest-start GR curve. Positive-curvature, conserved-dust solutions can recollapse at later times; unlimited dispersal is not imposed.

The original analytic dust and KS tests remain available for the retained geometry module. No new anisotropic finding is claimed from those tests.

## 7. Research screen and later stages

The Web Worker screen samples initial spin² versus comoving radius with fixed ordinary density, a_i, k, w and T; each H_i is derived. Colors distinguish a detected bounce with/without future trapping, other turning behaviour, no bounce during the interval, inadmissible data and unresolved stopping/numerical outcomes. The exported record includes all base parameters, every actual run parameter set, residual, endpoint, trapping flag and status. A screen cell is not convergence-certified; selecting it loads the run so that the user can perform the half-step check. Lack of detected trapping only means none found within the computed interval.

For KS, the retained isotropic effective-stress reduction is described separately and does not include an exterior star, microscopic spin alignment or a shear parameter guessed into FLRW. Anisotropic pressure and radial profiles remain disabled. Their prerequisites include a stress/spin closure, radial constraints, matter evolution, a suitable PDE solver, boundary data and a consistent EC junction formalism. A possible future reference is [Arkuszewski, Kopczyński and Ponomariev (1975), Matching conditions in the Einstein–Cartan theory of gravitation](https://doi.org/10.1007/BF01629248); it is not an implemented matching algorithm here.

Background on torsion and collapse also includes [Popławski, arXiv:2007.11556](https://arxiv.org/abs/2007.11556). This is context, not justification for adding particle production or claiming a baby universe. Matter entropy, gravitational entropy and horizon entropy are separate questions; none is inferred from compression, shear or a drawn sphere.

## 8. Reproducible development

No server, paid service or CDN is required in production. The versioned Plotly bundle and license are local. GitHub Pages continues to serve `ec-flrw/`.

    npm ci
    npm test
    npm run serve
    # In another terminal, with Chromium available:
    npm run test:browser

Set CHROMIUM_PATH if the executable is not `/usr/bin/chromium`; or install the Playwright Chromium build and point the variable at it. `npm test` covers the new collapse equations and solver, research screen, and retained geometry tests. Browser regression covers both interfaces, controls, trapping maps, shared time, comparisons, exports, sweeps and responsive layouts.

The Run JSON export records parameters, units, assumptions, events, all samples, diagnostics, comparison data and stopping status. CSV has the same primary-run metadata in a leading comment. Preserve this record when interpreting or sharing a result.
