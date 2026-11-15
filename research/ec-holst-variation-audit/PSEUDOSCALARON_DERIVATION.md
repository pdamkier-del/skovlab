# Nonlinear Holst pseudoscalaron: independent derivation

For general Δ(H), introduce z and replace Δ(H) by Δ(z)+Δ′(z)(H−z). Its equation is Δ″(z)(H−z)=0; equivalence requires a nondegenerate Legendre branch. With f=β+Δ′(z), U=zΔ′−Δ and B=f/M², the independently eliminated vacuum connection produces

S_eff=∫e[M²R/2−K_z(z)(∂z)²/2−U(z)],
K_z=24 f_z²/[M²(1+16f²/M⁴)]
=24M² B_z²/(1+16B²).

This reproduces Pradisi–Salvio Eq. (4.19) after orientation/parameter conversion. The kinetic coefficient is positive for M²>0, real f and Δ″≠0. The scalar is a genuine propagating combination of the original distortion; auxiliary connection elimination does not remove its kinetic term.

For Δ=cH², c>0,

K_z=96c²/[M²(1+16(β+2cz)²/M⁴)],  U=cz².

Integrating the kinetic norm with the vacuum at φ=0 gives

φ=√(3/2)M[asinh(4(β+2cz)/M²)−asinh(4β/M²)],
X=√(2/3)φ/M+asinh(4β/M²),
z(φ)=[M²sinh X/4−β]/(2c),
V(φ)=[M²sinh X/4−β]²/(4c).

The field map is smooth, invertible and canonical over the real branch. These forms are independently obtained from the connection functional, rather than importing an inflationary potential. The identities atanh[y/√(1+y²)]=asinh(y) and tanh X/√(1−tanh²X)=sinh X map them to Eqs. (4.28)–(4.31).

At the Lorentz-invariant zero-energy vacuum z=φ=0,

m_φ²=M²(1+16β²/M⁴)/(48c)>0.

For general nondegenerate Δ with Δ(0)=0 and its linear term absorbed into β, m²=M²(1+16B₀²)/(24Δ″(0)); Δ″(0)>0 is the no-tachyon condition. These match Eqs. (4.25)–(4.27). Kinetic positivity is not identical to potential stability: c<0 still has positive kinetic norm but a tachyonic/unbounded potential and is excluded here. c=0 has no Legendre scalar; the heavy-mode limit cannot be mistaken for a new linear-Holst degree of freedom.

Dimensions: [β]=[z]=M², [c]=1, [B]=1, [K_z]=M⁻² and [φ]=M. `scalar_identities.py` obtains K_z by differentiating the eliminated auxiliary functional and checks canonical normalization, inverse/potential and vacuum mass symbolically. The independent 24-component connection calculation supplies the kinetic coefficient's geometric normalization.

The scalar field representation uses the original metric (α is constant), so a turning point is not produced by a singular conformal-frame transformation. Positive V can support inflation **on an expanding solution**; it does not establish a prior contraction-to-expansion transition. Observational inflation/reheating predictions are not reproduced here.
