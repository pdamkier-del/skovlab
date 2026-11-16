# General inhomogeneous ADM system

No symmetry is assumed in this derivation. ds²=-N²dt²+gamma_ij(dx^i+beta^i dt)(dx^j+beta^j dt), N>0, n=(1,-beta)/N, K_ij=-L_n gamma_ij/2. Let Pi=n.phi, Q_i=D_i phi, a=-n.A and A_sp=A-a n. Define rho=T_nn, J_i=-T_ni, S_ij=T_ij, S=gamma^ij S_ij. Distinguish S from the bilinear S_b.

    rho=Pi²/2+Q²/2+V+KD_nn-h a Pi-g A²
    J_i=-Pi Q_i-KD_ni-h(A_sp_i Pi-a Q_i)/2
    S_ij=Q_i Q_j+gamma_ij(Pi²/2-Q²/2-V)
         +KD_ij+h A_sp_(i Q_j)+g gamma_ij A².

After using the full Dirac equation, the equivalent constraint energy is rho=Pi²/2+Q²/2+V+mS_b+gamma^ij KD_ij+h A_sp.Q+gA². These expressions include all interaction terms.

    R3+K²-K_ij K^ij=2rho/M²
    D_j(K^j_i-delta^j_i K)=J_i/M²
    (partial_t-L_beta)gamma_ij=-2N K_ij
    (partial_t-L_beta)K_ij=-D_iD_jN
       +N[R3_ij+K K_ij-2K_ik K^k_j-(S_ij-gamma_ij(S-rho)/2)/M²]
    (partial_t-beta.grad)phi=N Pi
    (partial_t-beta.grad)Pi=N[D_iQ^i+K Pi-V'-2hmP-g'A²]+D_iN Q^i.

If Q is evolved separately, partial_t Q_i=partial_i(N Pi+beta^j Q_j); Q_i-partial_i phi is an additional constraint.

Choose a normal-adapted orthonormal frame and Omega_mu=-W_mu^ab[gamma_a,gamma_b]/8. The coordinate Dirac equation, including arbitrary shift in gamma^i, is

    partial_t psi=-Omega_t psi-N² gamma^t[gamma^i(partial_i+Omega_i)psi
                     +i(m I+b_a gamma5 gamma^a)psi]
    b_a=h e_a^mu partial_mu phi+2g eta_ab A^b.

Do not add the shift advection twice. The frame and its spatial rotation gauge must be evolved consistently with the metric.

The scalar canonical momentum is p_phi=sqrt(gamma)(Pi-h a), not sqrt(gamma)Pi. Its equation is

    partial_t p_phi-partial_i(beta^i p_phi)
      =partial_i[N sqrt(gamma)(Q^i+h A_sp^i)]
       -N sqrt(gamma)[V'+g'A²+h'(a Pi+A_sp.Q)].

verify_canonical.py checks its equivalence to the normal equation using the Ward identity. Normal-frame Dirac primary momenta are i sqrt(gamma)psi†/2 and -i sqrt(gamma)psi/2; they are second-class constraints. A complete reduced Dirac-bracket/triad Gauss analysis is not claimed.

For r=-n.j, partial_t(sqrt(gamma)r)+partial_i[sqrt(gamma)(N j_sp^i-beta^i r)]=0. Coupled matter conservation and the Bianchi identity yield homogeneous continuum propagation of Einstein constraints. verify_adm.py independently checks Gauss, Codazzi and ADM evolution against arbitrary four-metric jets, with geometric Einstein tensor as a kinematic source; this is not a matter solution.

These are exact ADM equations, not an implemented strongly hyperbolic evolution formulation. Standard ADM with arbitrary prescribed gauge is not automatically strongly hyperbolic. A GH/BSSN/Z4 reduction, gauge/frame evolution and boundary analysis remain necessary. Chiral diagonalization gives classical scalar/Dirac principal parts; no torsion-free global existence theorem has been imported for this nonlinear system. Our numerical boundaries are periodic T³; no physical cloud exterior or constraint-preserving timelike boundary has been constructed.
