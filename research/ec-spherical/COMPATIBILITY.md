# Six geometry–matter combinations

The two geometries are homogeneous FLRW and general spherical collapse. “Exact” symmetry here applies to spin/torsion fields too; “effective” symmetry can apply only after explicitly assumed averaging. See `derivation.pdf`, Sections 1–4, for equations and source normalization.

| Geometry | Matter description | Consistency and closure | Decision |
|---|---|---|---|
| FLRW | 1. Spinless p=wρ | Exact perfect-fluid system. Constraint plus regular a,ȧ evolution and ordinary conservation. | Supported; preserve current module. |
| FLRW | 2. Unpolarized averaged Weyssenhoff | Statistically isotropic effective metric under fixed-spin/no-production closure; vanishing mean spin does not remove spin variance. | Supported as the documented Hashemi homogeneous approximation; radial stability and matching do not follow. |
| FLRW | 3. Full/coherent Weyssenhoff | Nonzero convective Frenkel spin cannot obey strong full-field FLRW symmetry. A verified flat metric-only aligned-spin branch exists with non-isotropic spin/torsion; its homogeneous equations use q=κβ² and β̇=−3Hβ. A full statistical model requires a moment closure. | Restricted cases depend on the declared symmetry; a generic full-spin FLRW mode is not justified. |
| Spherical | 1. Spinless p=wρ | GR Einstein–Euler, with physical w/gauge/smoothness/boundary restrictions. Dust needs a pre-caustic Lagrangian treatment. | Candidate first spherical implementation after a selected boundary problem; only specified here. |
| Spherical | 2. Unpolarized averaged Weyssenhoff | Conditional local action and conservation close the algebraic system, but c_eff² can be negative; h can vanish. Ordinary dust with low nonzero spin is not a well-posed generic acoustic Euler model. | No generic dust/bounce PDE authorized. A positive-pressure low-spin subdomain needs an explicit hyperbolicity/gauge analysis. |
| Spherical | 3. Full Weyssenhoff | For the selected BHL ideal formulation, coherent SO(3) spin is radial; parity and center regularity restrict it. Retained linear-spin stress cancels in that branch. Broader spin/velocity/metric correlation models require additional transport and constitutive data. | Formal restricted branch only, with the same effective-fluid acoustic issue. Generic correlation-retaining system not closed. |

No new matter action, spin-relaxation law, anisotropic pressure or bounce term is introduced. The full Weyssenhoff formulation is identified by BHL Eqs. (19)–(27), with its spin units retained for linear terms. It is not identified with the Hashemi input merely because both variables are named spin.

## Independent variables and constraints

| Supported/conditional system | Independent profiles after R_i=r gauge | Derived initial constraints/gauge | Evolution target |
|---|---|---|---|
| GR perfect fluid | U_i(r), ρ_i(r), parameter w; domain/boundary model | M_i'=κρ_i R_i²R_i'/2, M_i(0)=0; Γ_i²=1+U_i²−2M_i/R_i; B_i=R_i'/Γ_i; H_ri=U_i'/R_i'; Φ_i'=-p_i'/(ρ_i+p_i) plus one lapse normalization | R,U,ρ; pressureless dust separately |
| Averaged EC perfect effective source | U_i,ρ_i,q_i, w, with q=κ S_H²/4 | Same geometry with ε=ρ−q, P=wρ−q; lapse gradient −P'/h and principal-symbol domain | R,U,ρ,q; algebraically closed only under stated averaging/transport, not automatically well posed |
| Coherent radial BHL branch | U_i,ρ_i,signed b_i, w, with b_i=O(r) and a parity decision | q=κb_i², so q_i is not extra independent input; same no-flux constraints | Above plus ∂t(BR²b)=0, not an invented relaxation law |
| General retained-correlation proposal | Not yet determined | Full source Q,P_r,P_perp and moment constraints must be derived first | No closed evolution target available |

The homogeneous system instead has a_i, one independent member of (H_i,ρ_i), initial spin variance if applicable, k,w and the boundary/exterior choices. Its normalized simulator spin input remains κ²L*²S_H,i², with one-quarter subtraction in normalized density.
