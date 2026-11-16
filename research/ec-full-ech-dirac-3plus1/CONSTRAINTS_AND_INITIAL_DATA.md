# New constrained mixed initial data

The general equations are unrestricted. The inexpensive numerical family is explicitly restricted to planar periodic T³, L=8, k=2pi/L. Units M=1; beta=.25, c=10000, m=.1. Both Holst terms remain nonzero.

    n_seed=1e-4(1+.1 cos kz), phi=.2+.01 sin kz, Pi=0
    gamma_ij=chi^4 delta_ij, K_ij=K gamma_ij/3
    psi=chi^-3 sqrt(n_seed/2)(1,0,1,0).

This is a regular classical Weyl-basis spinor, not a quantum many-body prescription. The full matrix source verifies J_i=0 and

    rho=.5 chi^-4 phi'^2+V+m n_seed chi^-6+g n_seed² chi^-12
         +h n_seed phi' chi^-8.

Solve the Hamiltonian boundary value problem

    -8chi''+(2/3)K²chi^5=[chi phi'^2+2Vchi^5+2m n_seed chi^-1
                   +2g n_seed²chi^-7+2h n_seed phi'chi^-3]/M².

Periodic log chi and derivative, with integral log chi=0, determine the unknown positive contraction K. Main K=.008751786441954673. Raw collocation data are retained for reload.

Two counterfactual actions solve their OWN constraints at the same free conformal Dirac charge: scalar_GR sets h=g=0 but retains V and scalar; einstein_dirac removes scalar and torsion interactions. They are controls, not solutions of the full fixed action. Their K values are .008749078816132537 and .005477225519551976 respectively. Changing sources without resolving constraints would be invalid.

These data are not asymptotically flat, do not define ADM mass and have not been time evolved. Current initially aligns with the normal; later material and normal congruences need not coincide.
