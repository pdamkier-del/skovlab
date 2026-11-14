# Sources and convention checks

The new identities are derived in the accompanying documents and independently tested. Sources were checked on 13 November 2026; later apparent HTML renderer dates are not treated as paper revision dates.

- Hehl–Datta (1971), [doi:10.1063/1.1665738](https://doi.org/10.1063/1.1665738), and Shaposhnikov et al., [arXiv:2008.11686v2](https://arxiv.org/abs/2008.11686): minimal effective ECD action. The repository's [corrected geometric spin-connection audit](../ec-full-3plus1/CONVENTION_AUDIT.md) fixes all transferred signs.
- Gourgoulhon, [gr-qc/0703035](https://arxiv.org/abs/gr-qc/0703035): ADM normal/constraint conventions. The material-current congruence is kept separate from the normal.
- Langlois–Vernizzi, [astro-ph/0509078v3](https://arxiv.org/html/astro-ph/0509078), Phys. Rev. D 72, 103501 (2005), Eqs. (3)–(6), §6.3: covariant integrated expansion and conserved-number context. We use the geometric definition and derive the current relation directly; their perfect-fluid/adiabatic energy closures are not imported into anisotropic ECD.
- Buchert, [gr-qc/9906015v2](https://arxiv.org/abs/gr-qc/9906015), Gen. Rel. Grav. 32, 105–125 (2000): domain-volume scale-factor context. Its dust evolution is not used as an ECD equation.
- Buchert–Mourier–Roy, [arXiv:1912.04213v2](https://arxiv.org/abs/1912.04213), Gen. Rel. Grav. 52, 27 (2020), [doi:10.1007/s10714-020-02670-6](https://doi.org/10.1007/s10714-020-02670-6): arbitrary foliation, tilt/vorticity and averaging context. The local volume/tilt identities here follow explicitly from current flux and the projected Gram determinant; no averaged closure is borrowed.
- Müller–Nowaczyk, [arXiv:1504.01034v3](https://arxiv.org/abs/1504.01034): torsion-free Cauchy framework. The existing [analytic local ECD continuation argument](../ec-analytical-bounce/EXISTENCE_AND_SCOPE.md) states its separate assumptions and does not claim a new global stability theorem.
- Finster–Hainzl, [arXiv:1101.1872v2](https://arxiv.org/abs/1101.1872), J. Math. Phys. 52, 042501 (2011): special torsion-free cosmological bounce/periodic examples. Their existence does not supply realistic finite-cloud ECD e-folds. No state/metric restriction or coefficient from that model is substituted into this analysis.

The quantum/dense-matter interaction and physical-scale limitations remain documented in [ec-matter-models](../ec-matter-models/) and [ec-two-matter-models](../ec-two-matter-models/). Classical mean-current Fierz identities are never substituted for renormalized quantum composite expectations.

## Nyt analytisk benchmark

Den seks-felts kirale konstruktion i `CHIRAL_MULTIFIELD_BENCHMARK.md` er udledt og kontrolleret her ved direkte substitution i projektets konventioner. Der fremsættes ingen prioriterings- eller nyhedspåstand. Testene kontrollerer spinorer, den fulde stress, feltligninger, Friedmann-løsning og accelererede e-folds; de etablerer ikke kvantestatistisk fysisk gyldighed.
