# Radial stability and characteristic analysis

See the derivation PDF's radial characteristic section and the separate averaged-model section for the documented calculation. This is a frozen-coefficient radial material principal-symbol test; it is not a proof of the coupled gauge/boundary problem or stability against nonspherical perturbations.

For \(W=(n,\beta,v)\), \(\beta=b/n\), \(\rho=Cn^{1+w}\), \(q=\kappa\beta^2n^2\), let \(h=(1+w)\rho-2q\). The principal matrices are

\[
A^0=\operatorname{diag}(1,1,h),\qquad
A^1=\begin{pmatrix}0&0&n\\0&0&0\\P_n&P_\beta&0\end{pmatrix},
\quad P_n=\frac{w(1+w)\rho-2q}{n},\quad P_\beta=-2\kappa\beta n^2.
\]

The characteristic equation is

\[
\det(kA^1-\omega A^0)=-\omega(h\omega^2-nP_nk^2)=0.
\]

There is one contact/polarization mode and an acoustic pair. For \(h\ne0,\ c^2=nP_n/h>0\), eigenvectors can be chosen as \((n,0,\pm c)\) and \((-P_\beta,P_n,0)\). Acoustic modes conserve spin per particle. Holding spin density fixed while compressing would violate the chosen transport.

For \(0\le w<1\), \(z=q/\rho\), define \(z_s=w(1+w)/2\) and \(z_h=(1+w)/2\):

| Domain | Result |
|---|---|
| \(0\le z<z_s,\ w>0\) | Positive enthalpy and causal real nondegenerate radial acoustic pair. Candidate local smooth patch only. |
| \(z=z_s\) | Coincident zero characteristic roots. Primitive matrix is nilpotent and defective; real eigenvalues alone do not establish strong hyperbolicity. |
| \(z_s<z<z_h\) | Negative sound speed squared. Growth rate \(|k|\sqrt{-c^2}\) prevents a wavelength-independent Sobolev estimate for the continuum Cauchy problem. |
| \(z=z_h\) | Time matrix singular. Undivided Euler requires \(D_rP=0\) and does not determine acceleration. No generic continuation is established. |
| \(z>z_h\) | Real but superluminal acoustic pair. This is a causal-fluid failure, not a universal EC ghost theorem. |

For ordinary dust, every \(0<q/\rho<1/2\) lies in the nonreal domain. The spinless dust endpoint also has a defective primitive acoustic matrix, but permits the familiar separate pre-caustic Lagrangian dust treatment.

At \(P_n=0,P_\beta\ne0\), the matrix has rank two, nonzero square and zero cube. The three zero roots have only one eigenvector. For coherent spinless dust, rank is one and the square vanishes. For the averaged model with independent variance composition \(\chi=q/n^2\), \(P_\chi=-n^2\) remains nonzero at \(\chi=0\): its formal three-variable pencil retains rank two, with a one-sided physical variance domain. Exactly restricting to GR removes that independent variance mode. Neither defective endpoint can be included in a uniformly diagonalizable acoustic solver simply by setting the sound speed to zero.

For **stiff matter \(w=1\)**, \(c^2=1\) wherever \(h\ne0\). The original time matrix remains singular at \(q=\rho\). Both \(q\) and \(\rho\) scale as cell volume to power \(-2\), so their ratio is advected: compression does not take initially positive enthalpy into spin dominance. Special initial negative-effective-energy branches are a different physical/boundary problem, not ruled out by the \(w<1\) argument.

For a general spin-independent ordinary EOS, fixed entropy and fixed \(\beta\) give

\[
c_{\rm eff}^2=\frac{c_0^2(\rho+p)-2q}{\rho+p-2q},
\quad c_0^2=\frac{n\,p_n}{\rho+p}.
\]

A subluminal ordinary EOS retains the negative-enthalpy superluminality; positive-enthalpy acoustic reality requires \(2q<c_0^2(\rho+p)\). Spin-dependent internal energy would require specified susceptibilities and a different material derivation. No EOS is chosen to stabilize the result.

Additional ideal second moments on a common congruence add contact modes. They do not change this acoustic pair. General correlations could change the equations, but the missing moment closure prevents calculation of their characteristic structure.

For the constant-\(w\) model, a geodesic volume minimum requires \(q>(1+3w)\rho/4+\sigma^2/\kappa\), above the causal low-spin bound by at least \((1-w)(1+2w)\rho/4\). This conditional result does **not** forbid pressure-driven spherical turning points: acceleration divergence matters, and volume minima differ from areal extrema.

The existing homogeneous FLRW ODE has no acoustic spatial derivatives and remains unchanged. Its flat bounce \(q=\rho\) cannot be interpreted as proof of a viable radial continuation through these material domains.
