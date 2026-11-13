# Analytical local-volume bounce audit

## 1. Model, conventions and the exact focusing scalar

Use the **corrected** conventions in [the full-field convention audit](../ec-full-3plus1/CONVENTION_AUDIT.md): signature $(-+++)$, derivative index first, $\epsilon_{0123}=1$, $\{\gamma^a,\gamma^b\}=-2\eta^{ab}$, $\gamma_5=-i\gamma^0\gamma^1\gamma^2\gamma^3$, $\bar\psi=\psi^\dagger\gamma^0$. The geometric frame connection is $W_\mu{}^a{}_b=e^a{}_\nu\widetilde\nabla_\mu e_b{}^\nu$, so $D=\partial-W^{ab}[\gamma_a,\gamma_b]/8$. Full torsion is algebraic: $T_{abc}=-\kappa\epsilon_{abcd}J_5^d/2$ with $J_5^a=\bar\psi\gamma_5\gamma^a\psi$.

After eliminating torsion, the common action, Dirac equation and on-shell Hilbert stress are

$$S_{eff}=\int e\left[\frac R{2\kappa}+\frac i2\bar\psi\gamma^\mu\overleftrightarrow D_\mu\psi-m\bar\psi\psi-G_AJ_5^2\right]d^4x,\qquad G_A=3\kappa/16,$$
$$i\gamma^\mu D_\mu\psi-m\psi-2G_AJ_{5a}\gamma_5\gamma^a\psi=0,$$
$$T_{\mu\nu}=\mathcal K_{\mu\nu}+G_Ag_{\mu\nu}J_5^2,\quad \mathcal K_{\mu\nu}=-\frac i4\left[\bar\psi\gamma_\mu\overleftrightarrow D_\nu\psi+\bar\psi\gamma_\nu\overleftrightarrow D_\mu\psi\right].$$

All derivatives here are Levi–Civita after elimination. This is one commuting classical neutral spinor, not a spin average, a quantum gas or a multiple-species mean-current closure.

For a regular timelike vector current, define $n=\sqrt{-j^2}$ and $u=j/n$. The single-spinor Fierz identity is $J_5^2=n^2=S^2+\Pi^2$, where $S=\bar\psi\psi$ and $\Pi=i\bar\psi\gamma_5\psi$. In particular $S$ need not equal $n$ or be positive.

Multiplying Dirac and adjoint equations gives the **on-shell** kinetic-Lagrangian identity $\mathcal L_{kin}=mS+2G_A n^2$. Therefore

$$\mathcal K^\mu{}_{\mu}=-(mS+2G_A n^2),\qquad T^\mu{}_{\mu}=-mS+2G_A n^2.$$

Let $h=g+uu$ and $\mathcal G=h^{\mu\nu}\mathcal K_{\mu\nu}$. In a current-adapted tetrad this is the spatial kinetic trace $-i\bar\psi\gamma^{\hat i}\overleftrightarrow D_{\hat i}\psi/2$, summed over $i$. Since $\mathcal K^\mu{}_{\mu}=-\mathcal K_{uu}+\mathcal G$, the complete energy and mean spatial stress satisfy

$$\boxed{\epsilon=mS+G_A n^2+\mathcal G,\qquad P=G_A n^2+\mathcal G/3,\qquad \epsilon+3P=mS+4G_A n^2+2\mathcal G.}$$

These are source identities, **not an EOS or closure for $\mathcal G$**. The spatial kinetic trace can have either sign and is constrained by actual spinor data. Nonnegative Fourier energy, if a suitable spectral notion exists, is not equivalent to assuming this pointwise trace is nonnegative.

## 2. What a local no-bounce theorem can say

For $\Theta=\nabla_\mu u^\mu$ and proper-time derivative $\dot\Theta=u\cdot\nabla\Theta$, Raychaudhuri at a putative turn reads

$$\left.\dot\Theta\right|_{\Theta=0}=-\sigma_{\mu\nu}\sigma^{\mu\nu}+\omega_{\mu\nu}\omega^{\mu\nu}-\frac\kappa2(mS+4G_A n^2+2\mathcal G)+\nabla_\mu a^\mu.$$

Thus a sufficient local exclusion is $mS+4G_A n^2+2\mathcal G\geq0$ and $\omega_{\mu\nu}\omega^{\mu\nu}+\nabla\cdot a\leq\sigma_{\mu\nu}\sigma^{\mu\nu}$. The geodesic, irrotational case with $S\geq0,\mathcal G\geq0$ is an immediate example. These extra assumptions are **not** universal consequences of classical ECD.

A stronger necessary obstruction applies to an admissible homogeneous, spatially flat, current-normal branch with $\mathcal G=0$. At $H=0$, the Hamiltonian constraint gives $E=-\sigma_{ij}\sigma^{ij}/(2\kappa)$, while spatial Einstein evolution gives $\dot H=\kappa(E-P)/2=\kappa mS/2$. Hence

$$\dot H=-\frac14\sigma_{ij}\sigma^{ij}-\frac\kappa2G_A n^2\leq0.$$

This extends the previous flat homogeneous obstruction without assuming $S=n$. It does not apply to inhomogeneous gradient stresses, curved slices, tilted matter or arbitrary acceleration/vorticity.

## 3. Exact local constrained data with a turn

A concrete admissible example is sufficient to disprove a universal local no-bounce claim. Work on an open spatial patch, with coordinates $x,y,z$, and take

$$\gamma_{ij}=\chi(z)^4\delta_{ij},\qquad K_{ij}=0,\qquad\chi(0)=1,\quad\chi'(0)=0,$$
$$\psi(z)=\sqrt{n_*}\,\chi(z)^{-3}\begin{pmatrix}i\sin(cz)\\0\\\cos(cz)\\0\end{pmatrix},\qquad m,n_*,c>0.$$

Use the diagonal tetrad on the initial slice and Gaussian time ($N=1,\beta=0$). The time derivative of the field is fixed by the Dirac equation; it is not independently chosen. These data are planar, inhomogeneous and local, not FLRW or a bounded cloud. The symbol $n_*$ is a fixed seed coefficient; the physical current density is $n(z)=n_*\chi^{-6}$.

The current and axial bilinears are

$$j^{\hat a}=(n,0,0,0),\qquad J_5^{\hat a}=(0,0,0,n),\qquad S=n\cos(2cz).$$

For the conformal spatial tetrad, the nonzero initial spin-connection matrices are

$$\Omega_x=-\frac{\chi'}\chi\gamma^1\gamma^3,\qquad\Omega_y=-\frac{\chi'}\chi\gamma^2\gamma^3,\qquad\Omega_z=\Omega_t=0.$$

Consequently the spatial Dirac operator contracts to $\chi^{-2}\gamma^3(\partial_z+2\chi'/\chi)$. Acting on $\chi^{-3}\psi_{seed}$ retains a $-\chi'/\chi$ term. Omitting this term would give a wrong matter acceleration.

Substitution in the **full field stress**, including the Dirac time derivative, gives zero $T_{0i}$ and no off-diagonal stress. Its orthonormal components are

$$\epsilon=m n_*\chi^{-6}\cos(2cz)+G_A n_*^2\chi^{-12}-c n_*\chi^{-8},$$
$$P_x=P_y=G_A n_*^2\chi^{-12},\qquad P_z=G_A n_*^2\chi^{-12}-c n_*\chi^{-8}.$$

In particular $\mathcal G=-c n_*\chi^{-8}$ is a derived negative gradient stress. It was not added as a phenomenological force. The three momentum constraints hold everywhere on the patch because $K_{ij}=0$ and the actual matter momentum is zero.

An independent spatial Ricci calculation gives $R^{(3)}=-8\chi^{-5}\chi''$. The remaining Hamiltonian constraint $R^{(3)}=2\kappa\epsilon$ is therefore exactly the initial-value ODE

$$\boxed{\chi''=-\frac\kappa4\left[m n_*\chi^{-1}\cos(2cz)+G_A n_*^2\chi^{-7}-c n_*\chi^{-3}\right],\qquad\chi(0)=1,\quad\chi'(0)=0.}$$

Its right side is analytic near $\chi=1$. The ordinary analytic initial-value theorem supplies a unique positive analytic $\chi$ on some interval around zero. This is an exact local definition of the constrained data, not a discretized residual or an approximate choice of curvature. No global solution of this ODE or exterior gluing is assumed.

## 4. Normal expansion versus actual current expansion

Initially $u=n_{ADM}$ on the whole patch, $K=0$, and both congruences have $\Theta=0$, zero shear and zero vorticity. The normal congruence is geodesic in Gaussian time. Define central source values

$$E_0=mn_*+G_A n_*^2-cn_*,\qquad F_0=mn_*+4G_A n_*^2-2cn_*.$$

Einstein–Raychaudhuri then gives

$$\partial_n\Theta_n(0)=-\frac\kappa2F_0.$$

The field current is not geodesic. Differentiating its bilinear with the Dirac time equation, rather than assigning an acceleration, yields the initial coordinate acceleration

$$a^z=2\chi^{-5}\chi'+2m\chi^{-2}\sin(2cz),\qquad a^x=a^y=0.$$

At the center $a^\mu=0$, but **its divergence is not zero**:

$$\nabla_\mu a^\mu(0)=2\chi''(0)+4mc=-\frac\kappa2E_0+4mc.$$

At the central point $\partial_t a^0=a_i a^i=0$ by normalization, so this divergence is precisely the spatial derivative shown. Substitution gives the actual material expansion derivative

$$\boxed{\dot\Theta_u(0)=4mc-\kappa mn_*+\frac32\kappa cn_*-\frac52\kappa G_A n_*^2.}$$

The tests independently recover this expression from the **twice differentiated Dirac density equation**, not only from Raychaudhuri. At the center $\dot j^{\hat i}=0$, so $\dot\Theta_u=-\ddot n/n$. Keeping the time derivative of the normal-frame volume term in Dirac is essential; simply freezing the metric at second order gives the wrong result.

There is an **open parameter region**, not just an isolated tuned witness. Write $b=G_A n_*$ and choose

$$0<b<m/2,\qquad m/2+2b<c<m+b.$$

The upper bound makes $E_0>0$ and the lower makes the normal turn positive. With $d=c-m/2-2b>0$ and $b+d<m/2$, the fixed ECD relation $G_A=3\kappa/16$ gives

$$\partial_n\Theta_n=\kappa n_*d>0,$$
$$\dot\Theta_u=2m^2+\frac{20}{3}mb+\frac83b^2+(4m+8b)d>0.$$

The entire band violates the longitudinal NEC: $E_0+P_{z,0}=-2n_*(b+d)<0$. Thus positivity and local-turn existence are established for an open classical-data family, but not for NEC-obeying or positive-frequency fermion matter. For this particular family the exact material-turn threshold outside the band is also explicit:

$$c>\frac{\kappa n_*\left(m+\tfrac52G_A n_*\right)}{4m+\tfrac32\kappa n_*}.$$

It is a criterion for this constructed family's central current volume, not a universal ECD density threshold.

For an explicit rational witness, choose

$$c=3m/4,\qquad n_*=m/(3\kappa),\qquad G_A=3\kappa/16.$$

Then

$$E_0=\frac{5m^2}{48\kappa}>0,\quad F_0=-\frac{m^2}{12\kappa},\quad\chi''(0)=-\frac{5m^2}{192},$$
$$\boxed{\partial_n\Theta_n(0)=\frac{m^2}{24}>0,\qquad\dot\Theta_u(0)=\frac{287m^2}{96}>0.}$$

A regular local Cauchy continuation is justified in [EXISTENCE_AND_SCOPE.md](EXISTENCE_AND_SCOPE.md). Smoothness and the strict positive derivative imply $\Theta_u(\tau)=\dot\Theta_u(0)\tau+O(\tau^2)$ along the central current curve. Thus a followed infinitesimal rest volume has a strict local minimum: contraction immediately before, expansion immediately after. The normal volume also turns, with a different acceleration. All fields and metric/torsion curvature remain finite on a sufficiently small regular neighborhood.

## 5. What drives this example?

Compare with **torsion-free Einstein–Dirac**, a separate action with the contact term absent but the same $\kappa,m,n_*,c$ and the constraints solved anew. At the center,

$$\Delta(\partial_n\Theta_n)=-2\kappa G_A n_*^2,\qquad\Delta(\dot\Theta_u)=-\frac52\kappa G_A n_*^2.$$

Both are negative. The corresponding torsion-free data also bounce locally. This is an inhomogeneous coherent-field/gradient construction, not a demonstration that repulsive torsion reverses collapse. In general solutions, changing the action changes the entire field state and geometry; these differences are a statement about this matched free-data family, not a monotonicity theorem for all ECD.

The witness also violates the longitudinal null energy condition:

$$E_0+P_{z,0}=-\frac{m^2}{8\kappa}<0.$$

Positive energy at a point therefore does not make it ordinary realistic fermion matter. For the flat, periodic reference profile with the conformal factor removed, the *free* Dirac Hamiltonian has average energy $-cn_*$. At $c=3m/4$, its negative-energy spectral sector carries 4/5 of the norm. This is a diagnostic of that reference profile, not a spectral decomposition on the actual local curved patch. It shows why no positive-frequency physical-cloud interpretation may be silently attached to these classical data.

The result resolves a mathematical possibility question for local classical ECD. It leaves realistic torsion-caused reversal of a bounded gravitational collapse unanswered.
