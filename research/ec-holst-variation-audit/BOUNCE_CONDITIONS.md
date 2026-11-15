# Bounce conditions, curvature attribution and constrained checks

## Analytic flat/open obstruction

In the healthy canonical-scalar representation, with the **complete** additional matter energy and pressure,

H²+k/a²=[φ̇²/2+V+ρ_m]/(3M²),
Ḣ=k/a²−[φ̇²+ρ_m+p_m]/(2M²).

Matter includes its contact/derivative terms when present. Assuming its full source satisfies NEC, ρ_m+p_m≥0, a strict H=0,Ḣ>0 turn is impossible for k=0 or −1. This conclusion does not require V≥0; a nonnegative V and nonnegative ρ_m additionally make flat H=0 possible only at vanishing total energy. Positive potential/accelerated expansion is not a bounce argument. Shear further opposes a homogeneous Bianchi-I turn under the same source assumptions.

This is a restricted no-go for a healthy scalar plus the stated matter condition. It is **not** a theorem that arbitrary quantum Dirac sources satisfy NEC, nor a universal EC no-go. If a contact/correlation source violates NEC, its actual state and validity must be derived; the scalar potential does not supply that automatically.

## Closed turns

For k=+1 at H=0,

a_b²=3M²/[φ̇_b²/2+V_b+ρ_m,b],
Ḣ_b=[V_b−φ̇_b²−(ρ_m,b+3p_m,b)/2]/(3M²).

For vacuum matter and φ̇_b=0 at φ_b≠0, V_b>0 ensures a nondegenerate regular turn. A nearby homogeneous open set also turns while the strict inequality holds. This is curvature plus potential dominance, not NEC-violating flat repulsion.

A minimal numerical witness fixes M=1, β=1/4,c=10⁸ (no parameter search); m_φ²=1/24×10⁻⁸≈4.16667e−10. Use τ=m_φt and b=m_φa. Cases (φ/M,φ̇/(m_φM))=(.5,0),(.45,0),(.55,.05) each solve their own Hamiltonian for b at H=0. Independent DOP853 continuation to both sides τ=±.5 has contraction before and expansion after; RK4 32/64/128 per half converges at fourth order. At the reference turn b≈4.17160 and Ḣ/m_φ²≈.0574637. Endpoint state errors reach about 2.23e−12 and Hamiltonian error about 6.36e−14 in m_φ² units. These are finite-interval turns, not geodesic completeness or absence of later recollapse/singularity.

Full torsion is reconstructed from q^μ=24∂^μf/(M²D), t_μ=−Bq_μ. A direct Cartan calculation on the S³ coframe computes the full affine curvature, alongside metric R and Kretschmann. It independently checks H=z and all original tetrad variations. At φ̇_b=0 torsion itself vanishes but its derivatives and Holst curvature need not; a zero torsion square alone would be inadequate. All recorded invariants are finite.

## A genuinely inhomogeneous constrained assessment

For the reference closed turn, use time-symmetric data K_ij=0, scalar normal momentum π=0, and γ_ij=a_b²χ⁴γ_unit S³. Declare φ/M=.5+εQ₂(θ), Q₂=4cos²θ−1, with ε=.001,.002; Q₂ is an l=2 harmonic with ΔQ₂=−8Q₂. Solve the nonlinear Hamiltonian

−8Δχ+6χ=χ|D(φ/M)|²+2b_b²χ⁵W(φ/M),
W=V/(m_φ²M²).

Momentum constraints vanish exactly. The reflection-even BVP has χ′(0)=χ′(π/2)=0 and a positive smooth solution. Independent centered finite differences at 65/129/257 full-sphere points show second-order constraint convergence (reported BVP residual is not used as independent validation). The linear l=2 solution u=χ−1=b_b²W′ εQ₂/[4(8−3)] predicts the observed first-order perturbation; nonlinear correction scales approximately as ε². Raw BVP meshes/χ/χ′ are retained.

On this slice a Gaussian-normal geodesic congruence has Θ=0, shear=0 and Θ̇=V/M²>0 pointwise, since scalar spatial-gradient contributions cancel in ρ+ΣP. The scalar gradient is spacelike on the initial slice, so this is **normal geodesic volume**, not a purported scalar fluid rest frame. Smooth positive constrained data imply regular local Einstein-scalar continuation; no evolved nonlinear inhomogeneous trajectory or long-time stability is claimed.

## Attribution and controls

Torsion-free GR with the same canonical scalar action has exactly the same metric equations, constraints and turns; it is the mathematical field-representation control, not removal of the original action's scalar sector. A scalar-free GR+Λ control with Λ=V_b/M² also has separately constrained closed de Sitter turning data a_b,H=0. It is a distinct matter action, illustrating curvature/potential mechanics, not identical microscopic matter. Pure scalar-free vacuum GR has **no real k=+1 H=0 data** at that radius; keeping the same data after deleting the scalar violates the constraint.

The potential genuinely originates from the nonlinear torsion sector, so it can enable a curvature-assisted cosmology absent in the scalar-free theory. That is different from demonstrating a controlled torsion repulsion that evades the flat scalar NEC obstruction. The closed examples are CONDITIONAL mathematical curvature turns and do not establish the requested Level B torsion-caused mechanism.

For the separate scalar-free control, a(t)=ell cosh(t/ell), H=tanh(t/ell)/ell and Lambda=3/ell² solve the closed GR constraint and evolution exactly. Setting ell²=3M²/V_b matches turning a and H at the reference zero-velocity point; it does not pretend the microscopic matter action is unchanged. Both identities are checked symbolically.
