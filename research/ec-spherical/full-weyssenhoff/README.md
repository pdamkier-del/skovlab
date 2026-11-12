# Stage 2 — Two Weyssenhoff fluids in general spherical EC collapse

This stage continues [audit commit 3efc961](https://github.com/pdamkier-del/skovlab/tree/3efc96159537e834313ded3ba359624abaa8b26f/research/ec-spherical) and incorporates the 12 November task comparing **GSM + averaged Weyssenhoff (A)** with **GSM + full Weyssenhoff (B)**. Model A's local inhomogeneous use is conditional on stated averaging assumptions; Model B selects the ideal Obukhov–Korotky/BHL fluid with spherical metric and spin fields. The folder retains its initial full-Weyssenhoff research name. Existing FLRW runtime, exports, tests and hosting files are unchanged.

**Decision:** a formal inhomogeneous coherent radial-spin system can be written, and positive-pressure low-spin patches can pass a local material characteristic test. A physically justified, causal finite-collapse problem continuing into the proposed torsion-bounce regime has **not** been established. The six implementation prerequisites are not all satisfied, so no spherical EC prototype is implemented.

## Deliverables

- [Full derivation PDF](derivation.pdf), [LaTeX source](derivation.tex) and [sections](sections/): action/conventions, complete selected stress and spin transport, spherical reduction, mixed Einstein components, constraints, characteristic pencils, center/boundary analysis and research decision.
- [Physical consistency report](PHYSICAL_CONSISTENCY.md): coherent polarization, spin variance, correlations and admissible symmetry.
- [Stability analysis](STABILITY.md): characteristic modes, causal domain, zero-speed Jordan defect, enthalpy degeneracy, stiff exception and conditional bounce bound.
- [Initial/boundary analysis](INITIAL_BOUNDARY.md): independent data and a new full-connection distributional-curvature check.
- [Implementation readiness](IMPLEMENTATION_READINESS.md): explicit status of all six gates and the justified next research direction.
- [Open problems](OPEN_PROBLEMS.md) and [source ledger](SOURCE_LEDGER.md): missing physics, precise scope of primary sources, and distinctions between literature results and audit deductions.
- [Side-by-side equations](EQUATION_COMPARISON.md), [model viability](MATHEMATICAL_VIABILITY.md), and [shell/volume bounce analysis](BOUNCE_ANALYSIS.md).
- [Automated checks](validation/test_full_weyssenhoff.py) and [validation record](validation-results.json): 21 new cases covering both model pencils, analytical initial data, bounce/curvature identities; rerun of the previous 23 cases; existing application tests and unchanged-file manifest.

## Main findings

1. Proper rotations plus Frenkel leave only signed radial coherent spin, with \(b_{\theta\phi}=R^2\sin\theta\,b(t,r)\). Center smoothness requires \(b=O(r)\); parity invariance would exclude the coherent radial mean. An unpolarized variance is different and can be nonzero at the center.
2. Retaining all ideal linear-spin terms before reduction gives zero radial-spin derivative stress: the spatial spin divergence, acceleration contraction and shear contraction vanish separately. Thus \(q=\kappa b^2\), \(\epsilon=\rho-q\), \(P=p-q\), and \(\partial_t(BR^2b)=0\). This allows radial gradients; it does not add a stabilizing pressure or spin wave.
3. The full reduced radial pencil has a polarization/contact mode and the same acoustic pair as the earlier averaged closure. For constant \(w\), \(c_{\rm eff}^2=[w(1+w)\rho-2q]/[(1+w)\rho-2q]\). The dust obstruction remains. Extra ideal common-congruence second moments add contact modes, not a different acoustic pair.
4. A metric matching without a thin shell is weaker than requiring no delta singularity in the full torsionful Riemann tensor. Under the latter explicitly stated condition, a radial coherent spin matched to a torsion-free exterior must tend to zero at the surface. This sharpens the earlier sufficient spin-free-collar discussion; it does not reproduce general spinful surface-layer matching.
5. Recent geometric EC well-posedness and causal dissipative spin-hydrodynamics results do not establish our selected matter initial-boundary problem. They identify useful research methods, not terms to import without microscopic constitutive data.

These conclusions are conditional on the selected ideal field formulation/EOS. They do not prove that all EC matter models fail, that a pressure-driven spherical turning point is impossible, or that EC–Dirac collapse must bounce.

## Reproduce

From the repository root, use the existing Python 3.12/SymPy 1.14 and Node requirements:

~~~sh
python -m pip install -r research/ec-spherical/requirements.txt
python research/ec-spherical/full-weyssenhoff/validation/run_checks.py
bash research/ec-spherical/full-weyssenhoff/build_pdf.sh
~~~

The runner executes both research stages, runs the existing Node test suite, and verifies all 24 original FLRW files against the existing snapshot. It writes only this stage's validation record; it does not rewrite the Stage 1 results. CI runs both standalone mathematical suites plus existing application tests. Tests check algebra, analytical cases and numerical evaluations, not PDE time evolution or microscopic validity. The PDF build rejects undefined references and overfull layout.
