# From constrained data to a regular local turn

## A. What still needs proving after Raychaudhuri

A positive right-hand side at an arbitrarily assigned point is not an existence proof. The construction in [DERIVATION.md](DERIVATION.md) instead supplies actual analytic spinor/metric data on an open initial patch. Its full matter momentum vanishes; $K_{ij}=0$ solves all momentum constraints; the analytic positive solution of the displayed $\chi$-ODE solves the Hamiltonian constraint **throughout** that patch. The current is timelike and nonzero there.

The following local analytic Cauchy argument explains why these data have a genuine short two-sided spacetime continuation. It is not a theorem of global smooth stability, a bound on the lifetime or a justification of the existing numerical scheme.

## B. Analytic local continuation of the action-defined ECD system

In harmonic coordinates and a locally analytic algebraic tetrad gauge, eliminate torsion and use Dirac to remove spinor time derivatives from the Hilbert source. Schematically the exact equations have the form

$$g_{tt}=F(g,g_t,\partial_i g,\partial_i g_t,\partial_i\partial_jg,\Psi,\partial_i\Psi),\qquad\Psi_t=D(g,g_t,\partial_i g,\Psi,\partial_i\Psi),$$

where $\Psi$ lists the eight real spinor components. The maps are real analytic for positive spatial metric and spacelike slices; inverse $g^{00}$ and $\gamma^t$ exist. The ECD contact term is polynomial in the real spinor components. Complex conjugation therefore causes no analytic regularity problem.

One must not apply the simplest first-order-in-time Cauchy–Kowalevski theorem directly to a metric equation containing second spatial derivatives. Instead prolong Dirac to the same second order. Write $p=g_t$, $q_i=\partial_i g$ and $r_i=\partial_i\Psi$. Differentiating its RHS and substituting the two original time equations gives the explicit normal form

$$\Psi_{tt}=D_g p+D_pF+\sum_iD_{q_i}\partial_i p+D_\Psi D+\sum_iD_{r_i}\partial_iD.$$

Together with $g_{tt}=F$, this is a common second-order analytic system, solved for all pure second time derivatives. Every RHS derivative has total order at most two and fewer than two time derivatives. Analytic data $(g,g_t,\Psi,\Psi_t=D)$ therefore have a unique analytic local solution by the ordinary noncharacteristic Cauchy–Kowalevski theorem, applied to the real field components.

The prolongation must also preserve the original first-order Dirac equation. For the defect $Z=\Psi_t-D$, subtraction of the actual time chain rule gives

$$Z_t=-D_\Psi Z-\sum_iD_{r_i}\partial_i Z.$$

This is homogeneous with analytic coefficients and zero initial data, so uniqueness gives $Z=0$. Thus the prolonged solution solves Dirac itself, not just a second-order equation with extra spinor solutions.

For the constructed conformal data a fully explicit harmonic initial choice is $N=1,\beta=0$, $\partial_tg_{ij}=0$, $\partial_tg_{00}=0$, $\partial_tg_{0x}=\partial_tg_{0y}=0$, and $\partial_tg_{0z}=-2\chi'/\chi$. These set the contracted connection constraint $\mathcal C^\mu=0$; the Hamiltonian/momentum constraints then give its zero initial normal derivative. On the Dirac equations the full action stress is conserved. Bianchi applied to reduced Einstein gives the homogeneous constraint-wave system; zero gauge data propagate. The resulting local analytic solution consequently solves the full Einstein equations with the action-defined ECD source.

This local analytic argument does not assume a smooth global Cauchy development on a complete asymptotically flat slice. It is consistent with the local Einstein–Dirac Cauchy framework of Müller–Nowaczyk, Lemma 3.20, but their global/maximal-extension conclusions for the linear torsion-free matter equation are **not** imported into nonlinear ECD.

## C. Relating the existence gauge to the calculated expansion

The initial-data calculations used Gaussian normal coordinates. The existence argument may choose harmonic initial lapse/shift velocities; that changes coordinates, not the intrinsic initial geometry or spinor data. A regular analytic spacetime admits a sufficiently small Gaussian neighborhood of the same initial slice, obtained by its normal geodesics. No arbitrary lapse acceleration is used to make the turn positive.

The actual material frame is always $u=j/n$. At the slice it equals the slice normal, and has zero expansion/shear/vorticity because $u^i=0$ identically on the slice and $K_{ij}=0$. Its acceleration is fixed by Dirac. At the central point this acceleration vanishes but its divergence is nonzero, which is why equality of the two initial velocities does not imply equality of the two expansion derivatives.

For the explicit witness, $\dot\Theta_u(0)>0$ and $\Theta_u(0)=0$. Along the central current curve with proper time $\tau=0$ at the slice,

$$\Theta_u(\tau)=\dot\Theta_u(0)\tau+O(\tau^2),\qquad v_u(\tau)=v_u(0)[1+\tfrac12\dot\Theta_u(0)\tau^2+O(\tau^3)].$$

Thus a followed infinitesimal rest volume contracts just before and expands just after a regular local minimum. Strict inequalities persist on a smaller open initial patch by continuity. Analytic metric/spinor fields, $\chi>0$ and $n>0$ make both Levi–Civita and full algebraic-torsion curvature finite on compact sub-neighborhoods. This is a **local** continuation and regularity statement, not geodesic completeness or an exact closed-form spacetime for all times.

## D. Physical and global limits of the result

1. **A local turn is not an isolated cloud collapse.** The data are planar on an open patch. No compact support, complete spatial slice, ADM mass, vacuum junction, trapped surface or earlier large-scale collapse is supplied. Cutting off the spinor would change the constraints and is not a gluing proof. In addition, $K_{ij}=0$ makes the two future null expansions of any two-surface on this slice opposite, $\theta_\pm=\pm k_s$; this initial slice contains no strictly future-trapped surface lying wholly in the patch. It is not a constructed trapped-black-hole reversal.
2. **The effect is not caused by torsion.** Removing the contact from the action, retaining gravity and resolving the constraint ODE gives a turning member of the same free-data family. The exact central contact changes reduce both computed expansion derivatives. This is not a universal no-torsion-bounce theorem for other states.
3. **Energy admissibility matters.** The witness has $E_0>0$ but $E_0+P_{z,0}<0$, violating NEC and hence DEC in that direction. It cannot be described as ordinary positive-pressure matter. Its flat periodic reference also has substantial negative-frequency content. No positive-frequency projection or quantum many-fermion realization is established on the actual local geometry.
4. **Classical and quantum questions differ.** A commuting spinor is the specified classical model, not automatically an admissible occupied fermion mode or a dense Fermi state. The formal witness can be scaled to small curvature with small $m$, but that does not prove its many-body physical validity, Pauli/statistical admissibility or small quantum corrections.
5. **The conditional no-go has conditions.** It excludes turns only where its source and kinematic sign bounds hold. We have not proved these signs for every physically relevant class of fermionic matter.

The defensible conclusion is therefore: **local regular volume bounces are not universally forbidden by the unrestricted classical-spinor state space of ECD; realistic torsion-induced reversal of a bounded gravitational collapse remains unestablished.** The appropriate next analytical question is which physically justified restrictions on the fermion state preserve or forbid the required source/acceleration terms, rather than searching parameters until a turn appears.
