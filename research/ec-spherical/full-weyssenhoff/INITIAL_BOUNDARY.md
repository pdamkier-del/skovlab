# Initial and boundary data

The derivation PDF's initial/boundary section provides the equations and assumptions for both models, including an analytical constraint-satisfying patch. No astrophysical spin preparation or artificial taper is selected here.

After \(R_i=r\), the independent isentropic constant-\(w\) profiles are \(U_i,\rho_i,b_i\). The signed coherent spin fixes \(q_i=\kappa b_i^2\). Equivalently specify \(n_i,\beta_i=b_i/n_i\) with fixed \(\rho=Cn^{1+w}\). Additional entropy requires a specified EOS and an advected entropy profile.

Solve, rather than independently prescribe:

\[
M_i'=\frac{\kappa}{2}(\rho_i-\kappa b_i^2)r^2,\quad M_i(0)=0,\quad
\Gamma_i^2=1+U_i^2-\frac{2M_i}{r},\quad B_i=\Gamma_i^{-1}.
\]

Initial expansion rates are \(H_{r,i}=U_i'\), \(H_{\perp,i}=U_i/r\); the lapse satisfies \(\Phi_i'=-P_i'/h_i\), with one time normalization. Require real geometry, a declared characteristic domain, center parity and the chosen boundary/exterior. Finite microscopic spin per particle would bound \(|b|/n\), but its value is material input.

At a regular center, \(R=\ell r+O(r^3)\), \(B=\ell+O(r^2)\), \(U=O(r)\), smooth density/lapse are even, and coherent radial spin is \(b=b_1r+O(r^3)\). Thus \(q=O(r^2)\), \(M=O(r^3)\), \(\Gamma=1+O(r^2)\), and shear vanishes at the center. Ensemble variance need not vanish there.

The lack of coherent spin exactly at the center does not prove absence of a central volume reversal: acceleration divergence depends on gradients. Neighboring dust shells with nonzero coherent spin still fail the material acoustic test.

## Analytical constrained interior family

For a mathematical initial-data check, take \(R_i=r,\ U_i=-H_0r,\ \rho_i=\rho_0,\ q_i=q_0+q_2r^2\) on a sufficiently small patch. Model A allows nonnegative \(q_0,q_2\); Model B requires \(q_0=0,\ q_2=\kappa b_1^2\) with signed \(b_i=b_1r\). These are not proposed astrophysical profiles.

\[
M_i=\kappa\left[\frac{(\rho_0-q_0)r^3}{6}-\frac{q_2r^5}{10}\right],\quad
\Gamma_i^2=1+\left[H_0^2-\frac{\kappa(\rho_0-q_0)}3\right]r^2+\frac{\kappa q_2r^4}5.
\]

Let \(h_c=(1+w)\rho_0-2q_0\), \(h_i=h_c-2q_2r^2>0\). Then \(B_i=1/\Gamma_i\), \(H_{r,i}=H_{\perp,i}=-H_0\), and the central-normalized lapse is \(\Phi_i=-\frac12\ln(h_i/h_c)\). Direct tests verify mass, Hamiltonian, momentum and lapse constraints. An initial zero shear in this family is not imposed on the general calculation. For \(0<w<1\), a small enough radius and spin variance can keep \(\Gamma_i^2>0\) and \(q_i<w(1+w)\rho_0/2\). No evolution or vacuum matching is inferred.

For **either** model, \(P_\Sigma=0,\ \rho_\Sigma>0\) gives \(q_\Sigma=w\rho_\Sigma\) and \(c_{\rm eff,\Sigma}^2=-w\) for \(0<w<1\). Thus such a pressure-free positive-density boundary lies outside the causal low-spin domain. At \(w=1\) it instead gives \(h=0\); at \(w=0\) it requires \(q=0\).

## Three distinct exterior questions

| Question | Condition or limitation |
|---|---|
| Metric matching to vacuum, comoving no-flux boundary, no metric thin shell | Continuous induced metric and Levi–Civita extrinsic curvature; necessary \(P_\Sigma=0\), \(M_\Sigma=M_{\rm ext}\), \(D_tM_\Sigma=0\). |
| Stronger regularity: no delta in the **full torsionful Riemann tensor**, with Darmois metric matching, bounded piecewise smooth contortion and no spin sheet | Radial coherent spin must satisfy \(b_\Sigma=0\) against a torsion-free exterior. Bounded one-sided derivatives and compatible metric evolution still needed. |
| General spinful layer, possible distributional cancellations or radiation | Requires its own surface action, source/transport and junction formalism. Not derived or implemented here. |

For the second row, directly differentiating the connection jump gives

\[
(\widetilde R^\rho{}_{\sigma\mu\nu})_{\rm sing}
=\left(N_\mu[K^\rho{}_{\nu\sigma}]-N_\nu[K^\rho{}_{\mu\sigma}]\right)\delta(\ell).
\]

In a boundary orthonormal frame with radial \(N=e_1\), \(b_{23}=b_\Sigma\) and the audit's source normalization, \(K^0{}_{23}=-\kappa b_\Sigma\). A torsion-free exterior produces \((\widetilde R^0{}_{3 1 2})_{\rm sing}=\kappa b_\Sigma\delta(\ell)\). Its **Ricci contraction vanishes** even though this Riemann coefficient does not. This explains why the metric effective equations alone can miss a full-curvature singularity.

This is an independently derived restricted interface check, consistent with Luz–Carloni 1907.11489, Section V. It is not a universal condition for every distributional EC interface or a replacement for the full AKP surface-layer formalism. Continuous spin vanishing at the surface can remove the contortion-jump delta; a whole spin-free collar is sufficient but not necessary for that particular check. Vanishing spin must be transported consistently, not enforced through an external window.

For ordinary dust, \(P=-\kappa b^2\), so metric vacuum pressure matching already demands \(b_\Sigma=0\). For positive \(w\), zero effective pressure can occur with nonzero spin and density, but then fails the stronger full-curvature condition. Requiring both spin zero and pressure zero gives \(\rho_\Sigma=0\).

A compact zero-density surface remains problematic for the constant-\(w>0\) EOS in a finite-lapse comoving chart: in a spin-free collar, \(\Phi=-w\ln\rho/(1+w)+f(t)\). With bounded spin per particle and \(0<w<1\), spin becomes subleading as \(n\to0\), so ordinary regular edge asymptotics retain this obstruction. No complete regular finite star is constructed. A physically derived surface EOS, exterior medium or specified interface would require further analysis.

For Model A, zero mean spin at the edge is insufficient: variance and microscopic derivative/correlation layers may remain. A microscopic spin-free material collar can consistently remain spin-free under the ideal advection law, but its pressure, metric and surface statistics must still be solved. The coherent jump formula cannot be transferred by substituting a square root of variance.

Vacuum minimal EC is torsion-free GR and locally Schwarzschild under spherical symmetry. Vaidya has radiation and cannot be assigned to these \(Q=0\), comoving, shell-free interiors merely by varying a mass parameter. Full exterior construction and global causal classification remain open.
