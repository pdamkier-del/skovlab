# Conditional Pauli bound and validity gate

## Theorem for the stated continuum Gaussian cutoff class

Assume the massless independent isotropic channels of `STATE_AND_RENORMALIZATION.md`, 0≤f_i±≤1, all occupied momenta p≤Λ, positive free energy, and the matched leading contact operator. There are g Weyl channels. Let d_max=Λ³/(6π²).

For each channel |d_i|≤d_max. At fixed |d_i|, the minimum free energy fills only the majority charge's lowest momentum modes; adding particle-antiparticle pairs increases the energy. Thus

ρ0≥(3/4)(6π²)^(1/3) Σ_i |d_i|^(4/3).

Cauchy–Schwarz and the occupation cap give

B=(Σs_i d_i)²+Σd_i²≤(g+1)Σd_i²
≤(g+1)d_max^(2/3)Σ|d_i|^(4/3).

Consequently the sharp bound is

**r≡G_A B/ρ0≤(g+1)κΛ²/(24π²).**

Full zero-temperature aligned seas saturate it. This extends the old equal-sea estimate to arbitrary isotropic nonthermal particle/antiparticle spectra in the declared Gaussian class. An independent exact-shell integration tests 800 random spectra for g=1,2,6,24 and explicitly checks saturation. Thermal quadratures are separately verified against analytical polynomials; infinite thermal tails are not treated as compact support.

For g=6, r≤0.0295520 κΛ²; Λ=0.1M̄P gives r≤0.000295520. To reach formal r=1, Λ≥√[24π²/(g+1)]M̄P=5.81710M̄P. The proof concerns the contact fraction, not an arbitrary hard Planck cutoff.

As a **power-counting diagnostic**, define ε_species=gκΛ²/(16π²). Then r≤(2/3)(1+1/g)ε_species; formal equality requires ε_species≥3g/[2(g+1)]. Increasing species therefore does not produce a parametrically small conventional species-loop expansion in this calculation. The factor 16π² is a conventional loop estimate, not a derived universal gravitational cutoff or a theorem against a separately controlled large-N resummation.

## Restricted no-bounce conclusion

For flat homogeneous semiclassical data with this leading adiabatic source, no independent negative energy or cosmological constant, and quantitatively bounded higher corrections δρ, a bounce needs ρ=0. If

r_bound+|δρ|/ρ0<1,

then ρ≥ρ0(1−r_bound−|δρ|/ρ0)>0, and H²=κρ/3 cannot vanish. This is a conditional energy-positivity/no-turn bound. We have **not** computed an all-orders remainder; in an uncontrolled regime the inequality cannot be asserted. It does not cover general correlated, paired, coherent, anisotropic or vacuum-driven states, spatial curvature mechanisms, modified gravity, or arbitrary inhomogeneous material turns.

## Massive low-momentum class

For unpolarized independent Dirac species, Q_f=−D_f²/2−S_f², |D_f|≤n_f,total and 0≤S_f≤n_f,total. If populated physical p≤P≪m_f and antiparticles are negligible, Pauli gives n_f≤P³/(3π²), ρ0,f≥m_fn_f. Therefore

|Δρ_f|/ρ0,f≤G_A P³/(2π²m_f)
=(G_A m_f²)(P/m_f)³/(2π²).

A many-species sum is bounded by the largest such ratio because the unpolarized interspecies axial Hartree term is zero. This is tiny when G_A m_f² and P/m_f are both small. The contact cannot cancel the rest energy in that controlled weak free-gas regime. It is not a bound for a coherently polarized/correlated 2PI state. The nonrelativistic numerical checks use genuine integrals, not the bound as their implementation.

## Missing control criteria

No specified state here achieves the actual turn while demonstrating small interaction/remainder corrections, curvature operators, omitted gauge forces and spacetime-smeared stress fluctuations. Small H at a flat bounce is insufficient: Ḣ and curvature can be large even when H=0. Curvature counterterms and trace anomaly were not computed; smooth classical geometry cannot suppress them by assertion. No UV completion, many-body resummation or state with sufficiently enhanced connected correlations and controlled noise has been supplied. That is the remaining scientific question.
