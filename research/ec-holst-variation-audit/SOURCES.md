# Primary-source ledger and convention checks

All three specified original articles were inspected through authoritative arXiv HTML. Full texts were not archived in the repository. Exact versions and the full issue specification are retained in `results/provenance.json`.

| Source | Inspected / checked | Independent conclusion |
|---|---|---|
| [Pradisi–Salvio, 2206.15041v3](https://arxiv.org/html/2206.15041v3), Sec. 2 and 4.2.1 | Curvature slots and upper epsilon symbol; Eqs. 4.17–4.22, 4.25–4.31 | Metric-compatible derivation reproduces the canonical quadratic branch. K_z, inverse potential and vacuum mass are derived, not adopted as an ansatz. Its full metric-affine theory is broader than our selected EC sector. |
| [Inagaki–Yoshioka, 2406.14982v2](https://arxiv.org/html/2406.14982v2), Sec. II–III | Action/auxiliary and canonical scalar Eqs. 9–14, torsion-current and effective-coupling formulas 27–37 | Scalar/kinetic normalization agrees after orientation and dimension conversion. Effective nonminimal derivative/contact algebra matches under the stated map; exact microscopic trace-source sign conversion is left explicit and unresolved rather than guessed. |
| [Di Benedetto et al., 2605.09571v2](https://arxiv.org/html/2605.09571v2), Sec. II and III.1 | Mostly-minus action, canonical map, fermion normalization and Eqs. 38–42 | Same healthy scalar structure; local printed normalization/sign flags below. No reheating/leptogenesis prediction or observed-parameter fit is reproduced. |

## Parameter ledger

Our M is the reduced Planck mass. α=M²/2; β has dimension two, c is dimensionless, z has dimension two. Our R′ uses the raised Levi-Civita tensor with negative 0123. The 2022 upper-positive-symbol invariant has opposite sign, so (β,z,φ) can all reverse under comparison without changing K or physical mass.

The 2024 gravity notation S~M²R/2+M²H_p(R′_p)/4 with H_p=b_pR′_p+c_pR′_p² is matched by R′_p=−R′, b_p=−4β/M², c_p=4c/M², χ_p=−z and φ_p=−φ. Thus its c_p has inverse-mass-squared dimension and must not be equated numerically with our c. Its nonminimal beta_N is also distinct from gravitational β. `source_crosschecks.py` records the effective-current matching map; this is not a complete certification of its microscopic torsion-source signs.

The 2026 paper switches to mostly-minus metric and negative EH coefficient. Its K multiplying (∂B)² is K_B, whereas the 2022 K_z includes B_z². A signature/axial convention change must be applied to the entire action, not selected signs.

## Literal 2026v2 equation flags

- Eqs. 14–18: Eq. 15 defines K_B. Integrating over z as printed in Eq. 17 requires the B_z chain-rule factor to agree with the universal map in Eq. 18.
- Eqs. 38–39: C_phi/M_P requires dimensionless C_phi, while the printed dB/dphi in Eq. 39 has inverse-mass dimension for a dimension-one canonical field. An M_P normalization or an explicitly dimensionless field is needed.
- Eqs. 40 and 42: inserting real B(0)=1/(4gamma) into the positive Eq. 40 cannot give the negative Eq. 42. This is an internal printed-sign discrepancy, not a signature conversion between papers.

These local flags do not establish that the physical model, or all reported phenomenology, is invalid. The independently varied action fixes this audit's coefficients. No favorable sign is chosen from an inconsistent pair.

Prior repository evidence: main's ECD convention audit; actual PR #5 status/registry/criteria/continuation at bc0252ab6190728c975cb559dc9786628d8443f4, with older PR #2/#3 limitations preserved. Those branches are consulted read-only; the Model 4 findings live only in this new independent directory until reviewed.

Action-level follow-up: result07 directly checks the nonminimal Eq.27 source under explicit gamma/adjoint transformation in all 24 directions. It confirms the own-action parameter map used in effective matching; the intermediate Eq.29 trace-label dictionary is not silently assumed.
