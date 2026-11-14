# E-folds without homogeneity, isotropy or a universal scale factor

## 1. Local material-current volume

Declare a timelike nonzero current $j^\mu=n u^\mu$, $u^2=-1$, and reference events on each flow line. In the classical model $\nabla_\mu j^\mu=0$. Then

$$\dot n+n\Theta_u=0,\quad\Theta_u=\nabla_\mu u^\mu,\quad\dot{}=u\cdot\nabla.$$

A followed infinitesimal rest volume $v_u$ obeys $\dot v_u/v_u=\Theta_u$. Thus

$$\boxed{N_u(\tau;\tau_0)=\frac13\ln(v_u/v_{u0})=\frac13\int_{\tau_0}^{\tau}\Theta_u\,d\tau'=-\frac13\ln(n/n_0).}$$

This is an exact covariant identity, not an FLRW approximation. It remains true with arbitrary shear, vorticity, acceleration and spatial gradients. The congruence and endpoints are essential: changing the reference surfaces changes what is being measured. Nodes/null current invalidate this current-rest frame; they do not by themselves prove spacetime singularity.

Expansion gives positive $N_u$ and contraction negative. One e-fold multiplies local linear volume scale by $e$, volume by $e^3$ and conserved-current density by $e^{-3}$. A cycle with the same initial/final density has zero **net** e-folds even if both large contraction and expansion occurred. Report separately

$$N_+=\int\max(\Theta_u/3,0)d\tau,\quad N_-=-\int\min(\Theta_u/3,0)d\tau,\quad N_{net}=N_+-N_-.$$

If a physical approximation has a justified current source $\nabla_\mu j^\mu=\mathcal S$, the density relation instead includes $\frac13\int\mathcal S/n\,d\tau$. No particle-production source is invented here. The same term is used as a **measured numerical continuity defect**, not silently forced to zero.

## 2. Proper clocks and tilted slicing

For ADM normal $n_A$ write $u=W(n_A+v_E)$, $W=-u\cdot n_A=N u^0$. A material worldline has coordinate speed

$$\frac{dx^i}{dt}=\frac{j^i}{j^0}=Nv_E^i-\beta^i,\qquad\frac{d\tau}{dt}=\frac N W=\frac1{u^0}.$$

Consequently $dN_u/dt=N\Theta_u/(3W)$, not $N\Theta_u/3$ for a tilted current, and not $H_n=-K/3$.

Let $J=\partial x(t,X)/\partial X$ be the spatial flow Jacobian for the same material labels on successive ADM slices. A local slice-volume element is $v_\Sigma=\sqrt\gamma\det J\,d^3X$. The conserved flux through it is $dQ=nWv_\Sigma$. The infinitesimal rest volume is $v_u=Wv_\Sigma$, giving

$$\boxed{N_\Sigma=N_u-\frac13\ln(W/W_0).}$$

This local relation is geometric even for nonconserved currents if $N_u$ is computed from true expansion/volume rather than incorrectly from density alone. The physical conserved-current assumption only enters the density version.

For normal flow itself, $dx^i/dt=-\beta^i$, $d\tau_n=Ndt$ and $\Theta_n=-K$:

$$N_n=-\frac13\int NK\,dt.$$

The normal-flow Jacobian must be included if reconstructing this from coordinate metric volumes. At fixed coordinates, $\partial_t\ln\sqrt\gamma=-NK+D_i\beta^i$. Thus a fixed-point determinant ratio is not generally a normal-worldline e-fold count. Normal geometry remains defined in vacuum even when the material frame is undefined.

## 3. Directional stretch, shear and rotation

A transported material rest direction has stretching rate $H_e=\Theta_u/3+\sigma_{ab}e^ae^b$. Directions rotate and the deformation matrices at different times need not commute. Integrating instantaneous strain eigenvalues as if the axes remained material is generally wrong.

The numerical audit evolves the exact geometric separation equation

$$\frac{dJ^i{}_A}{dt}=\partial_j\!\left(\frac{j^i}{j^0}\right)J^j{}_A.$$

This is passive congruence kinematics, not a new matter/spin transport law. A same-time connector has rest-projected spatial Gram matrix $H^u_{ij}=\gamma_{ij}+u_i u_j$. Its determinant obeys $\det H^u=W^2\det\gamma$. If $C_0$ orthonormalizes the initial rest metric, the relative deformation tensor is

$$C=C_0^T J^T H^u(t)J C_0.$$

For its positive eigenvalues $\lambda_i$, define principal stretch e-folds $N_i=\frac12\ln\lambda_i$. Then $\sum_iN_i=3N_u$. The principal axes need not keep their labels over time; these are net principal stretches, not three invariant preassigned coordinate axes. Positive mean expansion can coexist with contraction in one direction.

## 4. A finite domain is a separate observable

For a material-followed domain $D(t)$ on a chosen slicing,

$$V_\Sigma(t)=\int_{D(t)}\sqrt\gamma\,d^3x,\quad N_{D,\Sigma}=\frac13\ln[V_\Sigma(t)/V_\Sigma(t_0)].$$

Reynolds transport yields

$$\frac{dV_\Sigma}{dt}=\int_D\sqrt\gamma[-NK+D_i(\beta^i+v^i)]d^3x,\quad v^i=j^i/j^0.$$

This is not the unweighted average of local logarithmic e-folds. It also uses coordinate time/slicing, not a universal proper clock shared by the cloud. Summing local rest-volume elements gives $V_{rest,sum}=\int_D W\sqrt\gamma\,d^3x=\int dQ/n$; it samples different worldline events on the selected slices. With vorticity, Frobenius forbids a global hypersurface orthogonal to $u$ in general. Such a sum must not be called an observer-independent global rest volume.

The audit currently tracks infinitesimal elements at three selected trajectories. It does **not** construct a converged whole-cloud domain integral, match an exterior or compute a cosmological background scale factor. Buchert-type averaging provides relevant domain definitions, but dust/perfect-fluid averaged evolution cannot be transferred to ECD without its full flux and anisotropic stress.

## 5. Bounce e-folds and inflation are different questions

A regular local bounce requires $\Theta_u=0$ and $\dot\Theta_u>0$. Expanding accelerated local volume additionally requires $H_u>0$ and $\dot H_u+H_u^2>0$. Positive $N_u$ alone proves neither acceleration, inflationary horizon behavior, isotropy nor a global expanding universe. The usual $-\dot H/H^2$ is undefined at a bounce where $H=0$.

For the previous analytical witness, $\dot\Theta_u(0)=287m^2/96$ implies only

$$N_u(\tau;0)=\frac{287}{576}m^2\tau^2+O(\tau^3).$$

Normal e-folds have a different leading coefficient $m^2\tau_n^2/144$. The local Taylor expansion gives no controlled lifetime and cannot be extrapolated to $N=1$, $60$ or any long post-bounce era. Rescaling $m$ rescales the physical time; it does not generate arbitrary dimensionless e-folds in the same dimensionless solution. A requested total requires a fully controlled solution and a declared end condition.

For one classical regular spinor, along its own current,

$$A^2/A_0^2=(n/n_0)^2=e^{-6N_u}.$$

This is a scaling of the axial invariant/contact operator, not permission to introduce a separately conserved spin fluid with an assumed EOS. Scalar mass energy also contains $S/n$, which can vary. The multi-field/quantum generalizations need not obey this scaling.

## 6. What the new numerical measurements establish

The passive tracker uses exactly the existing field RK4 stages and initial constraint solver. A test verifies that adding tracers does not change the evolved field step. It integrates material and normal paths/clocks, $N_u$, phase-resolved $N_\pm$, the spatial separation matrix and a measured continuity-defect integral.

A near-null current is rejected when its rest-density squared is not resolved relative to the squared normal-frame current density (default ratio 1e-12); this is a numerical conditioning guard, not a physical matter threshold. Primitive metric/spinor values are reconstructed trilinearly; their piecewise derivatives are taken from the same interpolant. Time derivatives use the interpolated actual discrete RHS. Therefore geometric volume/tilt identities can be checked independently while the reconstructed current need not be exactly conserved. In particular

$$N_{integral}-N_{density}=\int\frac{\nabla\cdot j}{3nu^0}dt.$$

The stored values include all three quantities; the defect is never hidden by replacing measured volume expansion with a density formula. Very small geometric consistency error does not bound discretization or interpolation errors.

Numerical times are in reduced Planck model units $c=\hbar=\kappa=1$, not seconds; all e-folds are dimensionless. In the fixed weak-field data family, at $t=0.02$ the measured net $N_u$ values at the three markers are:

| Grid | Marker 1 | Marker 2 | Marker 3 |
|---|---:|---:|---:|
| $9^3$ | 0.0001816 | 0.0001598 | 0.0002022 |
| $13^3$ | 0.0001622 | 0.0001499 | 0.0002084 |
| $17^3$ | 0.0001398 | 0.0001303 | 0.0001883 |

The density/integral discrepancies at $17^3$ still reach about $1.5\times10^{-5}$, and grid differences remain visible. There is no clean asserted asymptotic convergence order for these pointwise tracer observables. Normal e-folds are negative, approximately $10^{-5}$ in magnitude. Some principal directions contract even while the material mean grows. No local turning event is promoted to a validated bounce, and these data give no estimate of a long post-collapse expansion.

## Eksakt eksempel med fuld tidsudvikling

[Den seks-felts kirale løsning](CHIRAL_MULTIFIELD_BENCHMARK.md) giver et torsionsdrevet kosmologisk bounce og præcist `N_acc = ln(2)/2 ≈ 0.346574` accelererede e-folds. Den samlede fremtidige ekspansion er ubegrænset, men den sene fase er decelereret. Det er en særlig klassisk FLRW-metrik, ikke et generelt resultat for afgrænset kollaps.
