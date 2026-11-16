# Fixed action and independent variation

Issue #9; 2026-11-16. Signature (-+++), epsilon_0123=+1; {gamma^a,gamma^b}=-2 eta^ab, gamma5=-i gamma0 gamma1 gamma2 gamma3, bar psi=psi†gamma0. All spinor calculations here use commuting classical fields, not a renormalized quantum state.

S = integral sqrt(-g) [M² Rtilde/2 + beta H + c H² + L_D], beta != 0, c>0.

H=epsilon^{abcd} R_abcd uses the full metric-compatible connection. C_{rho mu nu}=-C_{nu mu rho}, with the derivative index in the middle; T^rho_mu_nu=C^rho_mu_nu-C^rho_nu_mu. Extrinsic curvature K is a different object. Introduce z, f=beta+2cz, U=cz². The auxiliary action has fH-U; variation gives H=z. No curvature-squared expansion is used.

With alpha=M²/2 the coframe/connection equations are

    P_ab=(alpha/2) epsilon_cdab e^c wedge e^d - 2f e_a wedge e_b
    D P_ab + s_ab = 0
    alpha epsilon_abcd e^b wedge F^cd -4f e^b wedge F_ab -U *e_a + tau_a=0.

The spin source follows directly from delta L_D=-i/16 bar psi {gamma^mu,[gamma_a,gamma_b]} psi delta W^ab_mu. These equations are checked against PR #8 conventions, rather than importing a differently normalized Holst invariant.

For metric/contortion variables, independent connection coordinates must be compatible LOWERED C_{rho mu nu}. Raising an index changes under metric variation. Let

    Q_R=g^{bd}(C^a_ae C^e_db-C^a_de C^e_ab)
    Q_H=epsilon^{abcd} g_ar(C^r_cl C^l_db-C^r_dl C^l_cb).

After integration by parts the complete algebraic connection contribution is alpha Q_R+f Q_H-df.q-q.A/8. Together with the Levi-Civita Einstein and Dirac actions this is an explicit off-shell functional of all 24 independent C components. It defines the ten metric equations by variation at fixed lowered C and symmetric tetrad lift; it avoids an inconsistent fixed-upper-C metric variation.

Writing W=W_LC(e)+C means fixed-C metric variation differs OFF SHELL from fixed-W coframe variation by connection-Euler terms and their derivatives. On the connection equation the envelope identity gives delta S_eff/dg=delta S_aux/dg|C*, and the metric equation is M² G_mu_nu=T_mu_nu in EFFECTIVE_EQUATIONS.md. Local Lorentz invariance relates the antisymmetric coframe equation to connection and spinor Euler equations; it supplies no additional independent metric equation on shell.

verify_local.py varies the ORIGINAL auxiliary action at fixed compatible lowered C in all ten symmetric metric directions and all 24 connection directions, as well as varying the reduced action. Six arbitrary lapse/shift/off-diagonal metrics are tested. This is a local variation test, not a spacetime existence theorem.

Boundary scope: the divergence terms discarded in eliminating torsion are M² div(t)+div(f q). Their variations must vanish by compact-support variations or appropriate fixed boundary data/counterterms. All tests use local jets or periodic spatial boundaries and fixed time endpoints. A well-posed finite timelike gravitational/spinor boundary variational principle is not supplied here. The canonical map covers all real phi because asinh is global for real f.
