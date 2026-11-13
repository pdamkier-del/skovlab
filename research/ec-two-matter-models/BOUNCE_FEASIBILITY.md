# What would count as reversal of collapse?

## Physical interpretation

A volume can stop contracting while one direction is still shrinking. A wave-packet width can turn without the whole cloud bouncing. Positive local acceleration therefore does not establish a regular spacetime continuation.

For A, a material velocity may be defined from a timelike conserved Dirac current. For B, choose a timelike particle-current or Landau frame and keep that choice throughout. At vacuum points or where this frame degenerates, a fluid-element volume diagnostic has no definition; that alone is not a spacetime singularity.

## Common mathematical conditions

For the selected timelike $u^\mu$ define $\Theta=\nabla_\mu u^\mu$ and $\dot\Theta=u^\mu\nabla_\mu\Theta$. With no assumption of zero shear, acceleration or vorticity,

$$
\dot\Theta=-\frac{\Theta^2}{3}-2\sigma^2+2\omega^2
-\frac\kappa2(\epsilon+3P)+\nabla_\mu a^\mu,
$$

where $\epsilon=T^{\rm eff}_{\mu\nu}u^\mu u^\nu$, $P=h^{\mu\nu}T^{\rm eff}_{\mu\nu}/3$, $\sigma^2=\sigma_{\mu\nu}\sigma^{\mu\nu}/2$, $\omega^2=\omega_{\mu\nu}\omega^{\mu\nu}/2$. These are complete effective-source quantities, not the earlier Weyssenhoff ordinary density/pressure.

At a candidate local volume minimum, $\Theta=0$, one needs

$$
\boxed{\kappa(\epsilon+3P)
<4(\omega^2-\sigma^2)+2\nabla_\mu a^\mu.}
$$

This follows from the metric Einstein equation and the kinematic Ricci identity. Trace-free anisotropic stress and rest-frame energy flux do not appear explicitly in $\epsilon+3P$, but they affect momentum balance, acceleration, shear and the chosen material frame. Spatial curvature constrains the allowed initial geometry through ADM; it is not an independent repulsive term.

Let $\xi^\mu$ join neighboring fluid elements and let $\ell$ be its projected proper separation. For the corresponding unit material direction $e^\mu$, the instantaneous stretching rate is

$$
\dot\ell/\ell=H_e=e^\mu e^\nu
\left(\frac{\Theta}{3}h_{\mu\nu}+\sigma_{\mu\nu}\right).
$$

A directional turn requires $H_e=0$ and a positive derivative along the **transported material direction**. Following an arbitrary coordinate axis or changing strain eigenvectors is not equivalent. Different directional rates can sum to zero without all of them reversing.

## What compression actually establishes

For a conserved particle current $nu^\mu$, $\dot n=-n\Theta$ establishes density growth under contraction. It does not alone establish alignment or the sign of a quantum spin correlation energy. A single classical regular Dirac field has the additional Fierz relation $J_5^2=n^2$; an unpolarized many-body state does not obey that relation for its mean axial current.

A's torsion and spin dynamics follow from the nonlinear Dirac action. B must derive its interaction-corrected stress and correlators before evaluating the boxed inequality. In neither case may one replace the unknown source by $P=p-q$ or choose a spin relaxation law to force defocusing.

A useful local classical check is a homogeneous, single coherent rest spinor with number density $n$ and frequency $E=m+2G_A n$. Its matter equation and full field stress give $\epsilon=mn+G_A n^2$, $P=G_A n^2$, hence $\epsilon+3P=mn+4G_A n^2>0$. This is a fixed-background matter identity, not an Einstein collapse solution or gas EOS. It illustrates that growing axial density need not cause defocusing. The quantum free-sea exchange example in the previous audit is a different state/quantization and can have the opposite contact-energy sign.

The prior microscopic audit independently found a state-dependent attractive free-sea correction; minimal ECD is not uniformly repulsive. Its [scale comparison](../ec-matter-models/PHYSICAL_SCALES.md) also found that generic minimal torsion dominance in relativistic matter is Planckian without a controlled enhancement. Strong curvature or microscopic gradients can invalidate classical geometry and the kinetic expansion. These limits are unchanged by using ADM coordinates.

## Additional work before claiming a regular bounce

For A: specify admissible constrained field data, derive the complete source/gauge Cauchy formulation, check the chosen current frame and follow the actual solution through a turn while bounding metric and torsionful curvature. A null principal cone is not a nonlinear stability or completeness theorem.

For B: first complete action-consistent EC kinetic/self-energy and collision closure, demonstrate conservation and causal/stable evolution in the intended density/gradient regime, and analyze the edge. The distribution must remain physically admissible and its moments finite.

For both: exclude material/coordinate caustic misclassification, establish regular continuation and a consistent vacuum transition, and compare every approximation with its validity scale. A global cloud bounce needs these properties across the distribution, not at one point. No local turning condition proves a global nonsingular bounce, an event horizon or a baby universe.

## References

The general focusing equation follows the Levi–Civita Ricci identity after torsion elimination; the [spherical audit](../ec-spherical/full-weyssenhoff/BOUNCE_ANALYSIS.md) is its regression limit. Action/state inputs are from [DIRAC_MODEL.md](DIRAC_MODEL.md) and [KINETIC_MODEL.md](KINETIC_MODEL.md), including their primary references. No numerical evolution is performed.
