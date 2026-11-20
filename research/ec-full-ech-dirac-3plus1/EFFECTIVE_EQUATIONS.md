# Coupled effective equations

All derivatives here are Levi-Civita. Define S_b=bar psi psi, P=i bar psi gamma5 psi and A as in TORSION_ELIMINATION.md. Parentheses have weight one half.

    M² G_mu_nu = T_mu_nu
    i gamma^mu D_mu psi-m psi-[h partial_mu phi+2g A_mu]gamma5 gamma^mu psi=0
    Box phi-V'+h div A-g' A²=0.

The adjoint equation follows by conjugation in the fixed Clifford convention. Classical Ward identities are div j=0 and div A=-2mP. Thus the scalar equation is Box phi-V'-2hmP-g'A²=0. On all coupled Euler equations div T=0.

    KD_mu_nu=-i/4 [bar psi gamma_mu ↔D_nu psi+bar psi gamma_nu ↔D_mu psi]
    T_mu_nu=partial_mu phi partial_nu phi
       -g_mu_nu[(partial phi)²/2+V]+KD_mu_nu
       +h A_(mu partial_nu)phi+g g_mu_nu A².

KD time derivatives MUST use the interacting Dirac equation. Omitting the explicit h term fails our conservation falsification test. The metric trace is M²R=(partial phi)²+4V+mS_b-2gA²; the original connection trace is M² Rtilde+2beta H=mS_b. Both belong to the SAME action.

A useful independent transformation is psi=exp(i theta gamma5)chi with

    theta=3/4[atan(sinh X)-atan(4beta/M²)], theta'=h.

The kinetic transformation cancels the derivative coupling, leaving mass -m[cos(2theta)S_chi+sin(2theta)P_chi]; A and j are invariant. This establishes classical principal-part equivalence, not a quantum statement: the anomalous Jacobian has not been computed.
