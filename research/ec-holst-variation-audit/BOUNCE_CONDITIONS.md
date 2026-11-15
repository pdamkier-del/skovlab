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

## Attribution and controls

Torsion-free GR with the same canonical scalar action has exactly the same metric equations, constraints and turns; it is the mathematical field-representation control, not removal of the original action's scalar sector. A scalar-free GR+Λ control with Λ=V_b/M² also has separately constrained closed de Sitter turning data a_b,H=0. It is a distinct matter action, illustrating curvature/potential mechanics, not identical microscopic matter. Pure scalar-free vacuum GR has **no real k=+1 H=0 data** at that radius; keeping the same data after deleting the scalar violates the constraint.

The potential genuinely originates from the nonlinear torsion sector, so it can enable a curvature-assisted cosmology absent in the scalar-free theory. That is different from demonstrating a controlled torsion repulsion that evades the flat scalar NEC obstruction. The closed examples are CONDITIONAL mathematical curvature turns and do not establish the requested Level B torsion-caused mechanism.

For the separate scalar-free control, a(t)=ell cosh(t/ell), H=tanh(t/ell)/ell and Lambda=3/ell² solve the closed GR constraint and evolution exactly. Setting ell²=3M²/V_b matches turning a and H at the reference zero-velocity point; it does not pretend the microscopic matter action is unchanged. Both identities are checked symbolically.
