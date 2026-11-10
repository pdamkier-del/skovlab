# Source and convention ledger

Primary material inspected for this audit on 10 November 2026. No full papers are redistributed. Mathematical identities independently derived in the audit are separated from constitutive choices imported from literature.

| Reference | Material checked | Role / limit |
|---|---|---|
| [Trautman, gr-qc/0606062](https://arxiv.org/abs/gr-qc/0606062) | Full accessible PDF, variational EC discussion and spin source definitions | Minimal action and algebraic torsion. Our derivative-index-first connection, full torsion and operational spin variation are explicitly defined; no paper's source normalization is transferred silently. |
| [Bréchet–Hobson–Lasenby, 0706.2367v2](https://arxiv.org/abs/0706.2367v2) | Eqs. 1–5, 19–28, 60–63, Appendix B and associated discussion | Selected full Weyssenhoff field formulation. Original signature +---, derivative index last, half-antisymmetric torsion Q and Γ̃=Γ−K_B. The full linear-spin tensor is translated under their Appendix B rules before use. |
| [Hashemi–Jalalzadeh–Ziaie, 1407.4103v2](https://arxiv.org/html/1407.4103v2) | Action/torsion definitions, Eqs. 2, 5, 8–9, homogeneous conservation/reduction | Existing closure subtracts κS_H²/4. Mean spin zero and nonzero variance are distinct; local inhomogeneous applicability requires extra assumptions. |
| [Obukhov–Korotky (1987)](https://doi.org/10.1088/0264-9381/4/6/021) | Primary bibliographic record and field formulation reproduced by BHL | Identified underlying ideal spin-fluid formulation. Full constrained matter action was not independently reconstructed from the original article. No replacement action is invented. |
| [Brown, gr-qc/9304026](https://arxiv.org/abs/gr-qc/9304026) | Accessible original PDF, conserved-current material action and metric variation | Standard perfect-fluid action used for GR and the explicitly conditional effective EOS. The composition multiplier may be relabelled/integrated by parts; it is not a microscopic spin action. |
| [Böhmer–Bronowski, gr-qc/0601089v2](https://arxiv.org/abs/gr-qc/0601089v2) | Full accessible PDF, symmetry condition on torsion and Frenkel discussion | Strong cosmological symmetry differs from metric-only FLRW. The audit independently checks a weaker aligned-spin flat-FLRW-metric example and does not claim it obeys strong isotropy. |
| [Misner–Sharp (1964)](https://doi.org/10.1103/PhysRev.136.B571) | Primary publication record | Historical spherical-fluid formulation. The mass/flux relations in this audit are independently derived from our metric Einstein tensor. |
| [Luz–Mena–Ziaie, 1811.12292v1](https://arxiv.org/abs/1811.12292v1) | Accessible full PDF, Eqs. 17–24, 31, effective-dust setup and conclusions | p_eff=0 is achieved by ordinary-pressure cancellation; not the same as ordinary p=0 with P=-q. Their assumptions and nonsingularity restrictions are not transferred to our different EOS. |
| [Popławski, 2008.02136v2](https://arxiv.org/html/2008.02136v2) | Accessible revised primary text, 20 March 2026 version | Spherical Tolman geometry, source normalization and synchronous/no-pressure-gradient restriction. Relativistic thermodynamics and particle production require their own laws, which are not imported. |
| [Arkuszewski–Kopczyński–Ponomariev (1975)](https://doi.org/10.1007/BF01629248) | Publisher metadata and abstract; full component junction derivation not reproduced | Identified junction reference; not a claimed validated spinful matching implementation. General surface-layer action and distributional assumptions remain missing. |

## Normalization safeguards

- Audit torsion: `T^ρ_{μν}=2 Γ̃^ρ_[μν]` with derivative index first. BHL's connection has derivative index last: for the same geometric connection, `T_ours=-2Q_B` and `K_ours^ρ_{μν}=-K_B^ρ_{νμ}`.
- Operational audit source is fixed by `δI_m=-½∫δω^{ab}∧τ_ab+...`. For a convective Frenkel source it gives `T=κ u s` in that source variable.
- The scalar correction is aligned as `q=κS_H²/4=κs²/4=κb²`, hence `S_H²=s²=4b²`, only when matching the stated ideal source/coupling. Scalar alignment does not prove microscopic equivalence or fix every linear-spin sign.
- Full linear-spin expressions retain BHL's b variable and are explicitly signature-transformed. No raw Hashemi spin input is inserted into those terms.
- The auxiliary-contortion coefficient check assumes minimal coupling linear in the connection and a convective Frenkel source. More general material terms or nonminimal couplings require a new derivation.
- The local averaged source/action and its characteristic speed are conditional on a stated moment truncation. This is not a universal equation of state of all EC fermionic matter.
