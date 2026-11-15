# Independent first-order variation

Let α=M²/2 and vol=*1. With the conventions fixed above, H vol=−2 eᵃ∧eᵇ∧F_ab. The gravitational four-form is

L_g=(α/2)ε_abcd eᵃ∧eᵇ∧Fᶜᵈ−2f eᵃ∧eᵇ∧F_ab−U vol.

Define matter three-forms operationally by δS_D=∫(δeᵃ∧τ_a+δWᵃᵇ∧s_ab)+fermion variations, with antisymmetric-index summation fixed by that equality. Set P_ab=(α/2)ε_cdab eᶜ∧eᵈ−2f e_a∧e_b. Since δFᵃᵇ=DδWᵃᵇ, integration by parts yields

**Tetrad:** αε_abcd eᵇ∧Fᶜᵈ−4f eᵇ∧F_ab−U*e_a+τ_a=0.

**Connection:** DP_ab+s_ab=0.

**Auxiliary:** f_z H−U_z=2c(H−z)=0.

**Minimal Dirac:** iγ^μD̃_μψ_f−m_fψ_f=0, and its adjoint.

These are variations of the action before substituting any on-shell field or scalar potential. For the declared symmetric Dirac action, at fixed W its coframe derivative has component density

e[e_a^μ L_D−(i/2)ψ̄γ^μ↔D̃_aψ]δeᵃ_μ.

The spin-connection source follows directly from

δL_D=−(i/16)ψ̄{γ^μ,[γ_a,γ_b]}ψ δWᵃᵇ_μ.

The gamma anticommutator selects the totally antisymmetric fermion spin current. This does not mean the gravitational connection solution has only axial torsion: the Holst term mixes axial and trace pieces.

## Independent component checks

`verify_connection.py` builds all 24 metric-compatible C_abc basis directions. It computes R̃ and H by direct affine multiplication/first jets, constructs their Hessian, calculates the linear Dirac source from explicit gamma matrices and solves every connection Euler equation for four real f values and generic gradients/spinors. The Hessian has rank 24 and the solution agrees with the irreducible elimination to roundoff. Thus no tensor torsion was discarded to obtain a favorable scalar sector.

A second check uses the reconstructed homogeneous full curvature along the scalar solution. `closed_turn.py` varies **all 16 coframe components** in the original auxiliary action at fixed coordinate curvature and fixed z; numerical first variations vanish within the recorded temporal/finite-difference uncertainty. It also checks the original tetrad trace αR̃+βH=0 and auxiliary H=z. These checks use the original first-order action rather than only identities of the reduced scalar equations.

The Lorentz bivector operator has a real inverse because *²=−1 and its determinant contains α²+4f²>0. Complex self-dual values are outside this real Lorentzian audit and require a different reality/constraint analysis. Conservation follows from local Lorentz/diffeomorphism identities when all field equations hold; quantum renormalized Ward identities have not been solved.
