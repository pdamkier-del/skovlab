# GSM + averaged versus GSM + full Weyssenhoff

Both models use \(A=e^\Phi,\ B=e^\Lambda,\ D_t=A^{-1}\partial_t,\ D_r=B^{-1}\partial_r\), \(U=D_tR,\ \Gamma=D_rR\), \(H_r=D_t\Lambda,\ H_\perp=U/R\), \(\Theta=H_r+2H_\perp\). None of these functions is assumed homogeneous or geodesic. The PDF derives all four mixed Einstein components explicitly.

| Term or equation | Model A — local averaged | Model B — selected full ideal coherent |
|---|---|---|
| Spin current | Microscopic convective \(u^\lambda s_{\mu\nu}\), zero mean under stated common-velocity averaging; nonzero variance. | BHL current \(u^\lambda b_{\mu\nu}\); operational audit source is \(-2u^\lambda b_{\mu\nu}\). |
| Frenkel | Holds microscopically before averaging. | \(b_{\mu\nu}u^\nu=0\), preserved by full transport. |
| Cartan / contortion | Microscopic \(\mathcal T^\rho{}_{\mu\nu}=\kappa u^\rho s_{\mu\nu}\), \(K_{abc}=\kappa(u_as_{bc}-u_bs_{ca}+u_cs_{ab})/2\). Mean zero does not remove quadratic averages. | Same operational formula with \(s=-2b\). |
| Quadratic source | \(q_A=\kappa\langle s^2\rangle/4=\kappa S_H^2/4\). | \(q_B=\kappa b^2\). |
| Full derivative stress | Mean linear term set to zero only under explicit derivative/averaging and neglected-correlation assumptions. | \(-2(g^{\alpha\beta}-u^\alpha u^\beta)\nabla_\alpha[u_{(\mu}b_{\nu)\beta}]\), retained before symmetry. |
| Exact spherical reduction | Statistical source remains isotropic only under the selected local moment truncation. | Proper rotations and Frenkel leave \(b_{\theta\phi}=R^2\sin\theta\,b(t,r)\). Divergence, spin–acceleration and spin–shear terms cancel separately. |
| Effective source | \(\epsilon=\rho-q,\ P=w\rho-q,\ Q=0,\ P_r=P_\perp\). | Same scalar form **after** demonstrated exact radial reduction. |
| Spin transport | \(D_tq=-2q\Theta\), with advected \(\chi=q/n^2\). | \(D_tb=-b\Theta\), with advected signed \(\beta=b/n\). |
| Matter energy | \(D_t\rho=-(1+w)\rho\Theta\). | Same for this reduced ideal branch. |
| Momentum | \(D_rP+h\,D_r\Phi=0\), \(h=(1+w)\rho-2q\). | Same; not geodesic unless the pressure-gradient equation permits it. |
| Independent matter data | \((\rho,q)\), or \((n,\chi)\) for fixed isentropic \(C\). | \((\rho,b)\), or \((n,\beta)\); \(q=\kappa b^2\) is derived. |
| Regular center | Even variance can remain nonzero. | Signed coherent \(b=O(r)\), so \(q=O(r^2)\). |
| Full microscopic curvature | Not fixed by a variance scalar; unresolved derivative/geometry statistics matter. | Computable from metric, spin and derivatives within the selected coherent formulation. |

For both selected reduced sources the common gravitational constraints and evolution identities are

\[
M=\frac{R}{2}(1+U^2-\Gamma^2),\quad
D_rM=\frac{\kappa}{2}\epsilon R^2\Gamma,\quad
D_tM=-\frac{\kappa}{2}PR^2U,
\]
\[
D_rU=\Gamma H_r,\quad D_t\Gamma=U a_r,\quad
D_tU=\Gamma a_r-\frac{M}{R^2}-\frac{\kappa}{2}PR,\quad a_r=D_r\Phi.
\]

On a monotone, nondegenerate patch, \(B=R'/\Gamma\) and \(\Phi'=-P'/h\). A constrained continuum choice evolves \(R,U,\rho,q\) for A or \(R,U,\rho,b\) for B; integrate \(M'\) with \(M(0)=0\), derive \(\Gamma,B\), and integrate the lapse gradient with one time normalization. The unused mass-time, angular Einstein and ADM equations are residuals. This is a theoretical equation split, not an implemented method. The \(h=0\) and \(\Gamma=0\) divided forms must not be used.

The two independent radial pencils are

\[
A_A^0=\operatorname{diag}(1,1,h),\quad
A_A^1=\begin{pmatrix}0&0&(1+w)\rho\\0&0&2q\\w&-1&0\end{pmatrix}
\quad \text{in }(\rho,q,v),
\]
\[
A_B^0=\operatorname{diag}(1,1,h),\quad
A_B^1=\begin{pmatrix}0&0&(1+w)\rho\\0&0&b\\w&-2\kappa b&0\end{pmatrix}
\quad \text{in }(\rho,b,v).
\]

They have the same acoustic polynomial with \(q=\kappa b^2\) for B, but different spin interpretation and zero-background perturbations. The map \(b\mapsto q\) is not invertible at \(b=0\); an independent variance perturbation is not the square of a linear perturbation of a vanishing coherent mean.

General spin correlations could yield nonzero radial \(Q\) or anisotropic pressure. The general spherical metric/conservation identities are in the PDF and Stage 1; constitutive evolution for those sources is missing. Their absence in the selected reductions is not an assumption that every full spin theory is a perfect fluid.
