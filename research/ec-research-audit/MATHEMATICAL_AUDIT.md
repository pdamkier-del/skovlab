# Mathematical audit

Baseline and review limits: [SCIENTIFIC_AUDIT.md](SCIENTIFIC_AUDIT.md). Use \(c=\hbar=1\), signature \((-+++)\), \(\kappa>0\), full torsion \(T^\rho{}_{\mu\nu}=2\widetilde\Gamma^\rho{}_{[\mu\nu]}\), derivative index first and \(\epsilon_{0123}=+1\). Contortion is denoted \(C\), avoiding confusion with ADM \(K_{ij}\).

## 1. Action, connection and elimination

The corrected geometric frame connection is
\[
W_\mu{}^a{}_b=e^a{}_\nu(\partial_\mu e_b{}^\nu+
 \widetilde\Gamma^\nu{}_{\mu\lambda}e_b{}^\lambda),\qquad
\Omega_\mu=-\tfrac18W_\mu{}^{ab}[\gamma_a,\gamma_b].
\]
The negative sign matches \(\{\gamma^a,\gamma^b\}=-2\eta^{ab}\).
The chosen \(\gamma_5=-i\gamma^0\gamma^1\gamma^2\gamma^3\) and
\(\bar\psi=\psi^\dagger\gamma^0\) are internally consistent.

For the original Einstein–Hilbert plus symmetrized Dirac action, the axial auxiliary terms are
\[
\mathcal L_q=\frac{q^2}{48\kappa}-\frac{q_aA^a}{8},\quad
q^a=\epsilon^{bcda}T_{bcd},\quad q^a=3\kappa A^a.
\]
Thus \(T_{abc}=-\kappa\epsilon_{abcd}A^d/2\), \(C=T/2\), and substitution into the *whole* action gives
\[
S_{\rm eff}=\int e\left[\frac R{2\kappa}+
\sum_f\mathcal L_{D,f}^{\circ}-G_A A^2\right]d^4x,\qquad G_A=3\kappa/16.
\]
For multiple species \(A\) is the sum before squaring.

**Confirmed historical error:** the literal geometric torsion orientation in older ECD reports has the opposite sign. The full-field convention correction resolves it; this is not a newly discovered fault in current ecd.py. Squaring the eliminated auxiliary source leaves the effective quartic interaction unchanged. The old LRS result is therefore not overturned. The rerun explicit affine/gamma test supports this correction.

The minimal effective coefficient is independently consistent with [Shaposhnikov et al., Eq. (2)](https://arxiv.org/html/2008.11686v2). Matching an effective coefficient alone would not settle geometric spin-connection orientation.

## 2. Field equations and full stress

Variation of the effective action gives
\[
i\gamma^\mu D^\circ_\mu\psi_f-m_f\psi_f-
2G_A A_a\gamma_5\gamma^a\psi_f=0,
\]
\[
T_{\mu\nu}=-\frac i4\sum_f
[\bar\psi_f\gamma_\mu\overleftrightarrow D^\circ_\nu\psi_f+
 \bar\psi_f\gamma_\nu\overleftrightarrow D^\circ_\mu\psi_f]
+G_Ag_{\mu\nu}A^2.
\]
The stress shown is **on shell**. The derivative term changes when the interaction changes the Dirac temporal frequency; reading energy or pressure off the final metric term alone is wrong.

The implementation uses the Dirac equation to supply temporal derivatives in this stress. Direct rest-state lapse/scale variation of the constant-tetrad action was independently checked in this audit: for \(m=.17,n=.013,\kappa=.7\),
\(E=.00223218125\) and \(P=.00002218125\), agreeing with the source to \(1.3\times10^{-14}\) in energy. Boosted and generic-jet tests supply further restricted checks, rather than a complete independent symbolic metric variation.

No actual error was found in the present action/source pair in the checked cases. This conclusion does not certify every nonlinear tensor operation for arbitrary input.

## 3. Tetrad and spinor evolution

The Cholesky choice \(\gamma_{ij}=LL^T\), \(e_0=n_{\rm ADM}\), \(e_a{}^i=(L^{-T})^i{}_a\) fixes the spatial rotation gauge. It requires positive spatial metric and spacelike slices. Analytic differentiation of the Cholesky factor is used, not spatial differencing of a tetrad built independently at each derivative evaluation.

The identity
\[
\partial_\mu\gamma^\nu+\Gamma^\nu{}_{\mu\lambda}\gamma^\lambda+
[\Omega_\mu,\gamma^\nu]=0
\]
is checked for off-diagonal geometry, shift and arbitrary first metric jets. A fresh finite-difference check of the frame map itself gave maximum derivative discrepancy \(8.7\times10^{-12}\), supporting the implemented analytic tetrad derivative.

With \(B=mI+2G_AA_a\gamma_5\gamma^a\),
\[
\partial_t\psi=-\Omega_t\psi-
(\gamma^t)^{-1}[\gamma^i(\partial_i+\Omega_i)\psi+iB\psi],
\quad(\gamma^t)^{-1}=N^2\gamma^t.
\]
This agrees with matter() in the reviewed engine. There is no independently imposed spin alignment in its evolution.

## 4. Einstein reduction, ADM constraints and gauge

The code evolves ten symmetric metric components and their ten time derivatives, plus four complex spinor components. It is a second-order spatial harmonic reduction, not a full implementation of a published first-order damped GH algorithm:
\[
\mathcal C^\mu=g^{\alpha\beta}\Gamma^\mu{}_{\alpha\beta},\quad
\mathcal R_{\mu\nu}=R_{\mu\nu}-\nabla_{(\mu}\mathcal C_{\nu)},\quad
\mathcal R_{\mu\nu}=-\tfrac12g^{\alpha\beta}\partial_{\alpha\beta}g_{\mu\nu}+Q_{\mu\nu}.
\]
Setting \(g_{tt}=0\) while evaluating \(\mathcal R^{(0)}\) gives
\[
g_{\mu\nu,tt}=\frac2{g^{00}}
[\mathcal R_{\mu\nu}^{(0)}-\kappa(T_{\mu\nu}-g_{\mu\nu}T/2)].
\]
The sign and principal temporal coefficient pass the metric-jet and flat gauge-wave checks.

ADM quantities are extracted using
\[
K_{ij}=-(\partial_t\gamma_{ij}-\mathcal L_\beta\gamma_{ij})/(2N),\quad
E=T_{nn},\quad j_i=-T_{in},
\]
\[
\mathcal H=R^{(3)}+K^2-K_{ij}K^{ij}-2\kappa E,\quad
\mathcal M_i=D_j(K^j{}_i-\delta^j_iK)-\kappa j_i.
\]
The displayed contractions in diagnostics() agree with these conventions. In particular,
\[
6H_n^2-2\kappa E+R^{(3)}-\sigma_{ij}\sigma^{ij}=\mathcal H.
\]
Its machine-precision agreement is an algebraic identity using the same variables, **not** an independent gravitational validation.

Initial harmonic velocities are solved algebraically for \(p_{0\mu}\); setting them all to zero would generally be incorrect. In the continuum, conserved full stress plus Bianchi gives homogeneous gauge-constraint propagation. Both initial Einstein constraints and the harmonic data are needed. A small discrete residual does not establish exact continuum constraint satisfaction.

**Missing evidence:** a complete reduction/energy estimate for the implemented mixed-order coupled variables and their boundary problem. The contact is algebraic and does not change the fixed-background Dirac light cone. Stress contains spinor derivatives, so juxtaposing the metric and Dirac cones does not prove coupled discrete stability. [Müller–Nowaczyk, Lemma 3.20](https://arxiv.org/html/1504.01034v3) is relevant continuum guidance; [Lindblom et al.](https://arxiv.org/html/gr-qc/0512093v3) supplies a different GH system whose boundary and damping results cannot be inherited.

## 5. Initial data and exterior

The finite-box ansatz
\[
\gamma_{ij}=\chi^4\delta_{ij},\quad
K_{ij}=\chi^{-2}(LW)_{ij}+\gamma_{ij}K_*/3,\quad
\psi=\chi^{-3}\Psi
\]
is a restricted family, not an assumption of conformal flatness throughout evolution. Solving four full-source discrete constraints for \(\log\chi,W^i\) is a meaningful improvement over prescribing inconsistent mass/radius/speed parameters. Rejecting nonconvergence is appropriate.

However, \(\chi=1,W=0\) on a finite cube is neither asymptotic-flat constraint gluing nor an ADM-mass calculation. Existence, uniqueness and conditioning across the intended collapse-data family remain unproved. A solver return flag establishes none of these.

Smooth vanishing spinors in an open collar imply zero local classical stress and algebraic torsion there. The remaining field equation is vacuum GR, which can still contain Weyl curvature and radiation. Fixed metric boundary values do not construct this exterior. At a layer-free non-null interface, induced metric and Levi–Civita extrinsic curvature must match and normal traction must vanish against vacuum. Requiring regular full curvature additionally constrains contortion jumps. A null support front needs null junction treatment. The earlier reports correctly distinguish these requirements.

## 6. Exact identities with restricted implications

For one regular commuting spinor,
\[
A^2=n^2=S^2+\Pi^2,\qquad n=\sqrt{-j^2}>0,\quad |S|\le n.
\]
On shell,
\[
T^\mu{}_\mu=-mS+2G_A n^2,\qquad
R=\kappa mS-2\kappa G_A n^2.
\]
Consequently \(n\to\infty\) entails \(R/n^2\to-2\kappa G_A\). Also
\(T_{abc}T^{abc}=-3\kappa^2n^2/2\). This is a conditional blow-up obstruction if compression actually reaches that limit, not a proof that a given cloud does so. Finite versus infinite proper time must be distinguished.

The full-connection scalar \(\widetilde R=\kappa mS\) can mask divergences in other invariants. Bounded scalar curvature alone cannot certify regularity.

For the current flow, \(N_u=\frac13\int\Theta\,d\tau=-\frac13\ln(n/n_0)\). This is a net local identity where the frame exists. It is not a global cloud scale factor or an inflation prediction. With tilt \(W\), slice and rest volumes differ by \(N_\Sigma=N_u-\ln(W/W_0)/3\).

For several species the total axial square can be timelike, spacelike or zero. Substituting total density into the single-spinor identity would be an actual mathematical error. The repository's six-field benchmark correctly avoids it.

## 7. Analytical local existence

The planar construction solves its constraints on an open patch through an analytic positive-\(\chi\) ODE. Its proposed Cauchy–Kowalevski argument is appropriate **locally in the analytic category**: prolong Dirac so both fields obey common second-order normal-form equations; use the homogeneous first-order Dirac-defect equation to recover the original Dirac system; propagate harmonic constraints using the on-shell identity.

The RHS contains at most second derivatives and is analytic while the metric/tetrad remain regular. Initial spinor time derivatives are fixed by Dirac. No obvious order-counting inconsistency was found in this argument. It is a mathematical continuation argument deserving expert review, not a consequence of unit tests, a general smooth-data stability theorem, or global completeness.

## 8. Earlier spin-fluid obstruction

For the specified conserved-spin closure,
\[
\epsilon=\rho-q,\quad P=w\rho-q,\quad
c_{\rm eff}^2=\frac{w(1+w)\rho-2q}{(1+w)\rho-2q}.
\]
Independent differentiation at fixed entropy/spin composition reproduces this result. For ordinary dust, \(0<q/\rho<1/2\) has negative acoustic speed squared; at \(q/\rho=(1+w)/2\) enthalpy vanishes. For \(w<1\) the larger-spin branch is superluminal. The stiff case \(w=1\) is a documented exception to the latter claim but still has a degenerate crossing.

A homogeneous ODE bypasses the spatial acoustic question. Its regular bounce does not validate an inhomogeneous causal fluid evolution. This is a defect of that closure's proposed use, not a general failure of EC gravity or Dirac matter. The full coherent radial ideal-spin reduction retains the same acoustic pair. The selected source/transport assumptions can be compared to [Bréchet et al.](https://arxiv.org/html/0706.2367v2).

## Classification

- **Actual documented historical error:** geometric torsion/connection orientation, corrected in the current engine.
- **Actual current diagnostic error:** periodic number quadrature; see [NUMERICAL_AUDIT.md](NUMERICAL_AUDIT.md).
- **Demonstrated restricted model obstruction:** acoustic failure of the selected spin-fluid continuation.
- **Missing evidence:** realistic state, complete exterior, strong-field convergence and coupled scheme stability.
- **No confirmed current equation error in the cases checked:** effective action, on-shell source, tetrad, harmonic acceleration and ADM projections.

These categories must remain separate.
