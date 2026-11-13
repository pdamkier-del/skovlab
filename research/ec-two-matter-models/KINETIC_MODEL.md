# B. Quantum kinetic fermion matter with spin

## Physical meaning and the selected literature

A distribution records **where particles are, how they move, and how their spins are populated**. Different momenta at one position naturally describe a tidally stretched or multistream cloud. A single density and scalar pressure cannot retain that information.

The primary baseline is **Liu–Mameda–Huang (LMH)**, *Covariant Spin Kinetic Theory I: Collisionless Limit*, [2002.03753v4](https://arxiv.org/pdf/2002.03753v4), Chin. Phys. C 44, 094101, with [erratum, doi:10.1088/1674-1137/ac009b](https://doi.org/10.1088/1674-1137/ac009b). The arXiv metadata explicitly identifies v4 as the erratum-applied version. It derives massive-fermion spin transport through order $\hbar$ in a prescribed **torsion-free curved metric**, with optional external electromagnetism. Its four transport equations are Eqs. (55–56); we refer to that corrected system rather than replacing its curvature/spin terms by an invented scalar Vlasov law. A new term-by-term RC/collision generalization has not been derived here.

For collisions compare **Weickgenannt et al.**, [2103.04896v2](https://arxiv.org/pdf/2103.04896v2), Phys. Rev. D 104, 016022. It derives a **flat-spacetime, low-density, quasiparticle** spin Boltzmann equation with local and nonlocal collisions. In particular its collision approximation omits Pauli-blocking factors (discussion after Eq. (68)). It must not be advertised as a ready dense degenerate-fermion collision model.

These are complementary results, not one already established closed curved-EC collision theory.

## Variables and calculable matter quantities

The underlying covariant Wigner matrix is the Fourier transform of a two-point function, with spin/gauge parallel transport to a common point. Choose the normalization

$$
\int_p\operatorname{tr}(\Gamma W(x,p))
=\langle\bar\psi(x)\Gamma\psi(x)\rangle_{\rm ren},
\qquad \int_p=\int\frac{d^4p}{(2\pi)^4}.
$$

A Wigner function is not generally a positive classical probability. In the massive on-shell quasiparticle limit, a $2\times2$ Hermitian spin occupation matrix $F(x,p)$ has four real components per particle sector. It can be expressed by two spin populations $f_\pm$ and two angles specifying a unit spin direction $\theta^\mu$ with $p\cdot\theta=0$, $\theta^2=1$ in our signature. Antiparticles require their corresponding sector. This is not an arbitrary six-component spin tensor at every momentum.

With $p^2=-m^2$ and $dP=d^3p/[(2\pi)^3p^0]$ in a local orthonormal frame, the leading spin-summed moments are

$$
N^\mu=\int dP\,p^\mu\operatorname{tr}F,\qquad
T_{\rm kin}^{\mu\nu}=\int dP\,p^\mu p^\nu\operatorname{tr}F.
$$

The selected quantum theory also has derivative/magnetization/spin corrections to its currents. The two displayed integrals alone are **not** its complete order-$\hbar$ gravitational source. Energy flux and unequal directional pressures are permitted. A two-beam distribution already gives $P_z>0$, $P_x=P_y=0$, even before spin corrections.

The axial moment is

$$
\langle J_5^\mu\rangle=\int_p\operatorname{tr}(\gamma_5\gamma^\mu W).
$$

It determines the mean minimal Dirac spin source in an action-consistent mean-field treatment. It does not determine $\langle J_5^\mu J_{5\mu}\rangle_{\rm ren}$, which contains exchange and connected two-particle information. One-particle spin polarization is not a complete pair-spin correlation function.

## Tidal forces, streaming and collisions

At zero spin order, the neutral streaming operator is

$$
\mathcal L_0 f=
p^\mu\partial_{x^\mu}f-
\Gamma^i{}_{\alpha\beta}p^\alpha p^\beta\partial_{p^i}f.
$$

It transports the distribution along geodesic characteristics. Neighboring trajectories feel curvature through geodesic deviation; the momentum distribution can become anisotropic. LMH adds spin–curvature transport and spin precession at its stated semiclassical order. Their derivatives are Levi–Civita derivatives; they cannot simply be relabelled as torsionful ones.

The collisional comparison has a scalar distribution on extended spin phase space and $p\cdot\partial f=C[f]$. Its nonlocal collision terms contain displaced arguments $x+\Delta$ at order $\hbar$, describing spin/orbital exchange. Scattering amplitudes and the approximation order define the kernel. Strong, electromagnetic, weak and torsion contact scattering cannot all be represented by an unspecified relaxation time. Finite-density blocking, self-energies and medium correlations require further work.

## Does a consistent EC coupling already exist?

**Related kinetic EC models do exist.** Calogero, *Kinetic dynamics of neutral spin particles in a spacetime with torsion*, [2410.20988v2](https://arxiv.org/pdf/2410.20988v2), constructs collisionless classical spin-particle transport consistent with EC/Bianchi balance. It is neither the above quantum Wigner collision theory nor a derived degenerate Dirac gas. Its phenomenological kinetic source/force construction must not be substituted for minimal Dirac action matching.

For the **selected quantum** model we have not established the combined self-consistent, collisional, dense EC formulation. In particular:

1. Derive the Wigner/self-energy equations from the same ECD effective action, including the axial contact interaction.
2. Match the kinetic spin current and stress to that action's connection/tetrad variations. A flat-space pseudo-gauge change between canonical and other spin currents is not automatically an equivalent torsion coupling.
3. Close the two-/four-point correlations or a controlled self-energy approximation; check its spin and energy Ward identities.
4. Derive the curved collision kernel at the retained order, with medium statistics and relevant interactions. Check characteristics, boundary behavior and the validity hierarchy.

The obstruction is explicit. For $S^<_{\alpha\beta}(x,y)=\langle\bar\psi_\beta(y)\psi_\alpha(x)\rangle$, the ECD operator equation gives

$$
(i\gamma^\mu D^\circ_\mu-m)_xS^<(x,y)
=2G_A\gamma_5\gamma^\mu
\langle\bar\psi(y)J_{5\mu}(x)\psi(x)\rangle,
$$

with spinor indices understood. The right side is a **four-field** correlator. Its value is not fixed by $S^<$ without an additional, justified correlation/self-energy closure. This equation identifies missing information; it is not a proposed collision law.

Known equilibrium linear causality/stability results for [Weickgenannt's 2307.13561v2](https://arxiv.org/html/2307.13561v2) apply to a particular kinetic-derived hydrodynamic closure and coefficient conditions. They are not a theorem of nonlinear dense EC evolution. When wavelengths, collision shifts or curvature radii approach microscopic scales, the semiclassical/gradient expansion may fail before torsion can dominate.

For orientation, sufficient scale separations to investigate include $1/(p_{\rm char}L)\ll1$, $|R_{\hat a\hat b\hat c\hat d}|/p_{\rm char}^2\ll1$ in a regular local frame, $|\Delta|/L\ll1$ and quasiparticle width $\Gamma_{\rm width}/E\ll1$, in units $\hbar=c=1$. These are validity estimates, not a proved sufficiency theorem. A perturbative axial-contact kinetic expansion also needs a controlled interaction/correlation hierarchy; extrapolating it into strong torsion is not justified by formal covariance.
