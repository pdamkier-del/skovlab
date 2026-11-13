# Limited minimal Einstein–Cartan–Dirac calculation

## 1. Conventions and action

Set $\hbar=c=1$, $\kappa=8\pi G=\bar M_P^{-2}$, signature $(-+++)$, $\epsilon_{0123}=+1$, hence $\epsilon^{0123}=-1$. The derivative index is first:

$$
\widetilde\nabla_\mu V^\rho=\partial_\mu V^\rho+\widetilde\Gamma^\rho{}_{\mu\nu}V^\nu,\quad
T^\rho{}_{\mu\nu}=2\widetilde\Gamma^\rho{}_{[\mu\nu]},\quad
K_{abc}=\tfrac12(T_{abc}-T_{bca}+T_{cab}).
$$

Use the previous audit's curvature $ \widetilde R^\rho{}_{\sigma\mu\nu}=\partial_\mu\widetilde\Gamma^\rho{}_{\nu\sigma}-\partial_\nu\widetilde\Gamma^\rho{}_{\mu\sigma}+\widetilde\Gamma^\rho{}_{\mu\lambda}\widetilde\Gamma^\lambda{}_{\nu\sigma}-\widetilde\Gamma^\rho{}_{\nu\lambda}\widetilde\Gamma^\lambda{}_{\mu\sigma}$, with Ricci $R_{\sigma\nu}=R^\rho{}_{\sigma\rho\nu}$. Weighted brackets have factor $1/2$.

For spinors choose $\{\gamma^a,\gamma^b\}=-2\eta^{ab}$, $\gamma_5=-i\gamma^0\gamma^1\gamma^2\gamma^3$, $\bar\psi=\psi^\dagger\gamma^0$. This **negative Clifford sign** is intentional with our mostly-plus metric and $i\gamma^\mu D_\mu-m$ convention; do not combine it with a mostly-minus formula without conversion. For vectorlike Dirac species,

$$
S=\int d^4x\,e\left[
\frac{\widetilde R}{2\kappa}
+\sum_f\left\{\frac i2\left(\bar\psi_f\gamma^\mu\widetilde{\mathcal D}_\mu\psi_f
-(\widetilde{\mathcal D}_\mu\bar\psi_f)\gamma^\mu\psi_f\right)-m_f\bar\psi_f\psi_f\right\}
-\frac14 F_{\mu\nu}F^{\mu\nu}\right],
$$
$$
\widetilde{\mathcal D}_\mu\psi_f
=\left(\partial_\mu+\frac18\widetilde\omega_\mu{}^{ab}[\gamma_a,\gamma_b]-ie_f A_\mu\right)\psi_f,\qquad F=dA.
$$

Set charges/Maxwell field to zero for neutral ECD. QCD and the chiral SM replace the relevant matter sector by their established gauge, fermion, Higgs and Yukawa terms. They are not reproduced by declaring neutrons elementary Dirac particles at all densities. No Holst term, free torsion-square coupling, nonminimal fermion term or new particle is assumed.

## 2. Algebraic torsion equation

The connection variation of the symmetric Dirac kinetic term is

$$
\delta\mathcal L_D=\frac{i}{16}\delta\widetilde\omega_\mu{}^{ab}
\sum_f\bar\psi_f\{\gamma^\mu,[\gamma_a,\gamma_b]\}\psi_f.
$$

The gamma anticommutator is totally antisymmetric in the three Lorentz indices. Thus only axial torsion is sourced; the trace and remaining tensor components vanish in the minimal Cartan equation. Define **our** axial torsion by

$$
a^d=\epsilon^{abcd}T_{abc},\qquad
T_{abc}=-\frac16\epsilon_{abcd}a^d,\qquad
J_5^a=\sum_f\bar\psi_f\gamma_5\gamma^a\psi_f.
$$

The epsilon-slot ordering fixes the sign of $a$; other papers can define the opposite axial vector. For total antisymmetric torsion $K_{abc}=T_{abc}/2$. Direct contraction of the curvature and the gamma variation gives, up to the usual bulk total derivative,

$$
\widetilde R=R+\frac1{24}a_\mu a^\mu,\qquad
\mathcal L_D=\mathcal L_D^\circ+\frac18a_\mu J_5^\mu.
$$

Both identities are independently checked with all four axial components and explicit Dirac matrices. The torsion-dependent action is therefore

$$
\mathcal L_a=\frac{a^2}{48\kappa}+\frac18a\cdot J_5,\qquad
\frac{\delta S}{\delta a_\mu}=0
\ \Longrightarrow\ a^\mu=-3\kappa J_5^\mu,
$$
$$
\boxed{T_{abc}=\frac{\kappa}{2}\epsilon_{abcd}J_5^d.}
$$

This is the algebraic torsion–spin equation in the stated conventions. Dirac spin is a totally antisymmetric current, not the earlier convective Frenkel $u^\lambda b_{\mu\nu}$ source. No phenomenological spin transport is added.

## 3. Elimination and field equation

Substitution in the **whole** action, including the material connection term, yields

$$
\frac{9\kappa}{48}J_5^2-\frac{3\kappa}{8}J_5^2
=\boxed{-\frac{3\kappa}{16}J_5^\mu J_{5\mu}}
\equiv -G_AJ_5^2,\qquad G_A=\frac{3}{16\bar M_P^2}.
$$

This agrees with the minimal limit of [Shaposhnikov et al., Eq. (2)](https://arxiv.org/pdf/2008.11686v2), in mostly-plus conventions. Dropping the material term or mixing half/full torsion gives a wrong coefficient. For several species the square is of the **sum** of currents: cross-species interactions remain. For chiral SM fields use their Lorentz spin currents; no right-handed neutrino is silently introduced.

For a Dirac species the resulting Hehl–Datta equation is

$$
i\gamma^\mu\mathcal D_\mu^\circ\psi_f-m_f\psi_f
-2G_AJ_{5\mu}\gamma_5\gamma^\mu\psi_f=0.
$$

The contact term has no field derivatives. The fixed-background principal determinant is $\det(\gamma^\mu\xi_\mu)=(g^{\mu\nu}\xi_\mu\xi_\nu)^2$; it leaves the metric-null front cone unchanged. This does **not** prove positive compressibility, nonlinear stability, a quantum many-body Cauchy theorem or a regular coupled collapse. The classical torsion-free Einstein–Dirac–Maxwell Cauchy framework [Müller–Nowaczyk](https://arxiv.org/pdf/1504.01034v3) is relevant; its theorem is not automatically a theorem for dense quantum EC matter.

Vector charge conservation follows from gauge symmetry. Spin/orbital angular momentum obeys the local Lorentz identity. The axial current is generally not separately conserved: mass terms and quantum anomalies matter. There is no general $q\propto n^2$ transport law implied by this action.

## 4. Energy and pressure require a state

For a quantum theory, eliminate the auxiliary connection at the action level, then define a renormalized composite operator and matter state. Generally

$$
\langle J_5^2\rangle_{\rm ren}\ne
\langle J_5^\mu\rangle\langle J_{5\mu}\rangle.
$$

The mean current can vanish while exchange/connected terms survive. Solving a classical Cartan equation sourced only by a mean current is a different semiclassical truncation. The choice and errors must be explicit; microscopic torsion fluctuations are not fixed by a scalar EOS.

In a local flat equilibrium patch, the interaction Hamiltonian density is $+G_A[J_5^2]_{\rm ren}$. To first order at fixed number densities and temperature,

$$
\Delta f=G_A\langle[J_5^2]_{\rm ren}\rangle_0,\quad
\Delta P=\sum_f n_f\frac{\partial\Delta f}{\partial n_f}-\Delta f,\quad
\Delta\epsilon=\Delta f-T\frac{\partial\Delta f}{\partial T}.
$$

Here $f$ is Helmholtz free-energy density, all composition/polarization constraints in the derivatives are specified, and the subscript denotes the reference interacting or free state. Varying an isolated action term while freezing the state is not a complete thermodynamic pressure calculation. A density-dependent correlator or running/matched coefficient must also be differentiated.

**Explicit limited example.** Take a single, dilute **nonrelativistic normal free Fermi sea**, no antiparticles or ordinary interactions, $p_F\ll m$, and vacuum normal ordering. To leading order $J_5^2$ is the square of the Pauli spin density. Write the one-body spin density matrix $r=\operatorname{diag}(n_\uparrow,n_\downarrow)$. Wick contraction gives

$$
\left\langle:(\chi^\dagger\boldsymbol\sigma\chi)^2:\right\rangle
=\sum_i\left\{[\operatorname{tr}(\sigma_i r)]^2-
\operatorname{tr}(\sigma_i r\,\sigma_i r)\right\}
=-6n_\uparrow n_\downarrow.
$$

The exchange subtraction is essential: the Hartree term alone gives the wrong result. With $n=n_\uparrow+n_\downarrow$, $\zeta=(n_\uparrow-n_\downarrow)/n$, at fixed polarization and zero temperature,

$$
\boxed{\Delta\epsilon=\Delta P
=-\frac32G_A n^2(1-\zeta^2)}
\quad\text{(this reference state and first order only).}
$$

A separate two-mode Fock-space calculation verifies the factor and sign. This normal-state perturbative calculation is not a claim about the exact interacting ground state, pairing stability, neutron matter or a relativistic plasma. Full polarization makes this identical-species local contact expectation vanish through Pauli exclusion. Other species, correlations and relativistic components change the answer. This example illustrates why “torsion is repulsive” is not a universal EOS statement. It also shows that a negative $n^2$ correction can reappear in a particular microscopic approximation; ECD does not automatically cure collective instabilities.

The contact operator, gamma identities and state-dependent pressure derivative are mathematical checks, not a demonstrated bounce. Numerical scales and the failure of a nonrelativistic high-density extrapolation are in [PHYSICAL_SCALES.md](PHYSICAL_SCALES.md).

## Reproduce the checks

With Python 3.12, Node and the existing pinned SymPy requirement:

~~~sh
python -m pip install -r research/ec-spherical/requirements.txt
python research/ec-matter-models/validation/run_checks.py
~~~

The runner records the new checks, previous mathematical regressions, existing application tests, actual tool versions and unchanged-file evidence in [validation-results.json](validation-results.json). The preservation comparison is this task's snapshot against commit e5e8aa6, not a permanent ban on future intentional research updates. CI runs standalone checks without imposing that snapshot on later work. Passing algebra does not validate the microscopic matter approximations.
