# Action, ADM equations and the verified reduction

## Conventions and action

Use exactly [the prior ECD conventions](../ec-matter-models/ECD_DERIVATION.md): $\eta=(-+++)$, $\epsilon_{0123}=1$, derivative index first in the affine connection, $T^\rho{}_{\mu\nu}=2\widetilde\Gamma^\rho{}_{[\mu\nu]}$, $R^\rho{}_{\sigma\mu\nu}=\partial_\mu\Gamma^\rho{}_{\nu\sigma}-\partial_\nu\Gamma^\rho{}_{\mu\sigma}+\Gamma^\rho{}_{\mu\lambda}\Gamma^\lambda{}_{\nu\sigma}-\Gamma^\rho{}_{\nu\lambda}\Gamma^\lambda{}_{\mu\sigma}$. Ricci contracts first/third indices. Contortion $C$, distinct from ADM $K$, is $C_{abc}=(T_{abc}-T_{bca}+T_{cab})/2$.

$\{\gamma^a,\gamma^b\}=-2\eta^{ab}$, $\gamma_5=-i\gamma^0\gamma^1\gamma^2\gamma^3$, $\bar\psi=\psi^\dagger\gamma^0$, $\widetilde D_\mu=\partial_\mu+\widetilde\omega_\mu{}^{ab}[\gamma_a,\gamma_b]/8$. One neutral classical commuting spinor, no gauge or nuclear fields:

$$S=\int e\left[\frac{\widetilde R}{2\kappa}+\frac i2\bar\psi\gamma^\mu\overleftrightarrow{\widetilde D}_\mu\psi-m\bar\psi\psi\right]d^4x.$$

Spin current is defined operationally by $\delta S_m=-\tfrac12\int e s^\lambda{}_{ab}\delta\widetilde\omega_\lambda{}^{ab}$, giving $s^\lambda{}_{ab}=-i\bar\psi\{\gamma^\lambda,[\gamma_a,\gamma_b]\}\psi/8$. It is totally antisymmetric, not the convective Frenkel model. For $J_5^a=\bar\psi\gamma_5\gamma^a\psi$, define axial torsion $q^d=\epsilon^{abcd}T_{abc}$. The auxiliary Lagrangian is $q^2/(48\kappa)+q\cdot J_5/8$; its variation gives $q=-3\kappa J_5$. Thus

$$T_{abc}=\frac\kappa2\epsilon_{abcd}J_5^d,\quad C=T/2,\quad S_{eff}=\int e\left[\frac R{2\kappa}+\mathcal L_D^\circ-G_AJ_5^2\right]d^4x,\quad G_A=3\kappa/16.$$

Substitution includes both curvature and material connection terms. Variation gives

$$i\gamma^\mu D^\circ_\mu\psi-m\psi-2G_AJ_{5\mu}\gamma_5\gamma^\mu\psi=0,$$
$$T_{\mu\nu}=-\frac i4[\bar\psi\gamma_\mu\overleftrightarrow D^\circ_\nu\psi+\bar\psi\gamma_\nu\overleftrightarrow D^\circ_\mu\psi]+G_Ag_{\mu\nu}J_5^2\quad\text{(on shell)}.$$

The source follows tetrad variation, with $\mathcal L_D^\circ=2G_AJ_5^2$ on shell. The metric term by itself is not a pressure equation. The Dirac equation and its adjoint imply $\nabla_\mu j^\mu=0$, $j^\mu=\bar\psi\gamma^\mu\psi$, and the action identities imply $\nabla_\mu T^{\mu\nu}=0$.

## General ADM bookkeeping, not a verified PDE integrator

For $n^\mu=N^{-1}(1,-\beta^i)$ and $K_{ij}=-(\partial_t-\mathcal L_\beta)\gamma_{ij}/(2N)$, set $E=T_{nn}$, $j_i=-T_{in}$ and $S_{ij}=T_{ij}$ by spatial projection. In particular the metric contact contribution is $-G_AJ_5^2$ to $E$, zero to $j_i$, and $G_A\gamma_{ij}J_5^2$ to $S_{ij}$; kinetic terms must still be included. The Gauss scalar projection gives twice $G_{nn}$, Codazzi gives the momentum projection, and spatial Ricci projection gives

$$ {}^{(3)}R+K^2-K_{ij}K^{ij}=2\kappa E,\qquad D_j(K^j{}_i-\delta^j_iK)=\kappa j_i,$$
$$ (\partial_t-\mathcal L_\beta)\gamma_{ij}=-2NK_{ij},$$
$$ (\partial_t-\mathcal L_\beta)K_{ij}=-D_iD_jN+N[{}^{(3)}R_{ij}+KK_{ij}-2K_{ik}K^k{}_j]-\kappa N[S_{ij}-\gamma_{ij}(S-E)/2].$$

For $Q_{ab}=\bar\psi\gamma_a\overleftrightarrow D^\circ_b\psi$ with projected indices, the actual source projections are

$$E=-\frac i2 Q_{nn}-G_AJ_5^2,\quad j_i=\frac i4(Q_{in}+Q_{ni}),\quad S_{ij}=-\frac i4(Q_{ij}+Q_{ji})+G_A\gamma_{ij}J_5^2.$$

These give six metric and six extrinsic-curvature evolution equations. With $\Omega_\mu=\omega_\mu{}^{ab}[\gamma_a,\gamma_b]/8$ and $B=m+2G_AJ_{5\mu}\gamma_5\gamma^\mu$, the Dirac time equation is explicitly

$$\partial_t\psi=-\Omega_t\psi-(\gamma^t)^{-1}\gamma^i(\partial_i+\Omega_i)\psi-i(\gamma^t)^{-1}B\psi,$$

where $(\gamma^t)^{-1}=N^2\gamma^t$. A normal-adapted tetrad still needs a spatial triad and rotation gauge; its connection must be computed from that same metric/tetrad. The contracted Bianchi identity and conserved full stress imply homogeneous constraint propagation. A discretization need not inherit it. General synchronous ADM is not asserted to be a stable hyperbolic PDE algorithm here; a verified generalized-harmonic or suitable BSSN/Z4 plus Dirac/tetrad formulation remains required.

Write $K_{ij}=-H\gamma_{ij}-\sigma_{ij}$ for the normal congruence, with trace-free $\sigma$. Then $K^2=9H^2$ and $K_{ij}K^{ij}=3H^2+\sigma_{ij}\sigma^{ij}$. Substitution proves

$$\boxed{6H_{ADM}^2=2\kappa E-{}^{(3)}R+\sigma_{ij}\sigma^{ij}}.$$

The geometrical derivative of a scalar is $\partial_n=N^{-1}(\partial_t-\beta^i\partial_i)$. Raychaudhuri gives

$$\partial_nH=-H^2-\sigma_{ij}\sigma^{ij}/3-\kappa(E+S)/6+\frac{D_iD^iN}{3N}.$$

At $H=0$, positivity of the right side and regular continuation are needed for a local normal-volume bounce. Normals need not follow matter; this is not generally a material-volume theorem. Directional rates can turn separately. For a followed matter domain in a declared time slicing, $H_V=\dot V/(3V)$; it is not automatically equal to this local $H$.

## A consistent anisotropic classical-field branch

Take $ds^2=-d\tau^2+a^2(dx^2+dy^2)+b^2dz^2$, $N=1$, $\beta=0$, and the nonrotating diagonal coframe $(d\tau,a\,dx,a\,dy,b\,dz)$. Let $A=\dot a/a$, $B=\dot b/b$, $H=(2A+B)/3$, $D=B-A$, $v=a^2b$, with $a_0=b_0=1$. The orthonormal spin connection is $\Omega_{\hat0}=0$, $\Omega_{\hat i}=H_i\gamma^0\gamma^i/2$, hence $\gamma^aD_a=\gamma^0(\partial_\tau+3H/2)$ for homogeneous spinors.

In the explicit gamma representation used by the tests, take

$$\psi=\sqrt{n_0/v}\,e^{-i\theta}(0,0,1,0)^T,\quad \dot\theta=m+2G_A n,\quad n=n_0/v.$$

Then $j^{\hat a}=(n,0,0,0)$ and $J_5^{\hat a}=(0,0,0,n)$; the lower fourth component instead reverses spin. Direct substitution verifies the Dirac equation and full stress. Importantly, before imposing $H_x=H_y$, $T_{\hat x\hat y}=n(H_y-H_x)/4$. Thus arbitrary triaxial expansion with this spinor is inconsistent. LRS removes this term; the other mixed components vanish. We get

$$E=mn+G_A n^2,\quad j_i=0,\quad S_{ij}=P\gamma_{ij},\quad P=G_A n^2.$$

No FLRW spin average or fluid closure was used. The metric can be isotropic while the torsion/spin remains oriented: this is metric symmetry, not an isotropic complete matter configuration.

Independent coordinate Christoffel/Ricci calculation gives

$$G_{00}=A^2+2AB,\quad G_{xx}/a^2=-(\dot A+\dot B+A^2+B^2+AB),\quad G_{zz}/b^2=-(2\dot A+3A^2).$$

All off-diagonal metric Einstein components vanish. Subtracting spatial equations gives $\dot D=-3HD$. Their trace and the Hamiltonian constraint give the evolution and diagnostic equations below. No momentum constraint is left unsolved: homogeneity, diagonal $K$ and $j_i=0$ make all three identically zero.

## Actual ODE algorithm and analytical benchmark

The six evolved real variables are $(\log v,H,D,\log a,\log b,\theta)$:

$$\partial_\tau(\log v,H,D,\log a,\log b,\theta)=\left(3H,-3H^2+\frac\kappa2(E-P),-3HD,H-D/3,H+2D/3,m+2G_A n\right).$$

The second entry is the spatial ADM evolution **without projecting the constraint back to zero**. For $C=6H^2-2\kappa E-2D^2/3$, direct differentiation gives $\dot C=-6HC$. Thus errors can grow during contraction; they are measured, not reset. On $C=0$, $\dot H=-\kappa(E+P)/2-D^2/3$. Also $\dot E+3H(E+P)=0$, $nv=n_0$, $Dv=D_0$ and $\log v=2\log a+\log b$.

For $m,n\geq0$ there is no local volume bounce on this branch. With nonzero source/shear the flat-slice Hamiltonian constraint also excludes $H=0$. Some directional scale factors may behave differently; the three displayed graphs are volume diagnostics, not individual-axis bounce detection.

An independent exact benchmark follows because $\ddot v=3\kappa mn_0/2$:

$$v(\tau)=1+3H_0\tau+\frac34\kappa mn_0\tau^2,\qquad H=\frac{3H_0+(3/2)\kappa mn_0\tau}{3v}.$$

The production RK4 integrator does not use this formula. The formal contracting solution approaches zero volume, with growing density and curvature; the browser stops at its operational cutoff and never follows a claimed physical singularity. In vacuum $v$ is linear (Kasner), with zero Ricci but potentially nonzero Weyl curvature; zero shear gives Minkowski. $m=0$ is massless ECD, **not** a spinless limit. For a single regular coherent spinor $J_5^2=n^2$, so removing spin at fixed nonzero density is not a consistent independent option.

## Sources

- [Hehl–Datta, J. Math. Phys. 12 (1971), 1334, doi:10.1063/1.1665738](https://doi.org/10.1063/1.1665738), nonlinear Dirac theory.
- [Shaposhnikov et al., arXiv:2008.11686v2](https://arxiv.org/abs/2008.11686), minimal effective contact coefficient after convention translation.
- [Gourgoulhon, arXiv:gr-qc/0703035](https://arxiv.org/abs/gr-qc/0703035), Gauss–Codazzi and ADM.
- [Müller–Nowaczyk, arXiv:1504.01034](https://arxiv.org/abs/1504.01034), torsion-free Einstein–Dirac Cauchy framework; not a ready numerical ECD solver.
- The [prior source audit](../ec-two-matter-models/COMPARISON.md) and [spherical derivation](../ec-spherical/derivation.pdf) retain the broader literature comparison. The particular LRS branch above is directly substituted and independently checked here rather than transferred with unverified literature signs.
