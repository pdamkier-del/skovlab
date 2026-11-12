# EC spherical-collapse derivation and audit

**Stage 2:** [GSM + averaged versus full Weyssenhoff: equations, bounce and viability analysis](full-weyssenhoff/README.md) continues this audit. The original derivation and its recorded validation results below are preserved.

This is the mathematical deliverable requested before any new spherical simulation features. It extends the prior FLRW documentation without replacing or duplicating the existing implementation. **No application or solver files were changed.**

## Deliverables

- **[derivation.pdf](derivation.pdf)** — compiled LaTeX derivation, explicit metric components, action/torsion conventions, three source formulations, constraints/evolution, symmetry restrictions, initial/boundary data, outcome definitions and literature audit.
- **[derivation.tex](derivation.tex)** and [sections/](sections/) — editable, documented derivation. Equations are derived in the text; symbolic output is a separate check.
- **[COMPATIBILITY.md](COMPATIBILITY.md)** — the six geometry–matter combinations and independent-variable/constraint tables.
- **[PDE_SPEC.md](PDE_SPEC.md)** — implementation plan, data model, acceptance tests and explicit mathematical gates. This is not a PDE solver.
- **[UNRESOLVED.md](UNRESOLVED.md)** — missing closures, possible contradictions, boundary assumptions and parts that must remain unimplemented.
- **[SOURCE_LEDGER.md](SOURCE_LEDGER.md)** — primary references, versions, coefficient/notation differences and access/reproduction limits.
- **[validation/](validation/)** and [validation-results.json](validation-results.json) — automated symbolic, analytical and numerical-evaluation checks with a read-only bridge to existing FLRW samples.
- **[baseline-flrw.sha256](baseline-flrw.sha256)** — snapshot manifest of the existing `ec-flrw/` files from commit `6d9e7ff95b11160afa869d6cd9f6da73bb2dc8e4`.

## Main conclusions

1. The spherical Einstein components, general flux/anisotropy conservation equations, Misner–Sharp balance laws, ADM constraints and FLRW reduction are independently verified.
2. A local averaged Hashemi source can be described by an explicit effective-fluid action **only under stated coarse-graining and conserved-spin assumptions**. Algebraic closure is not sufficient for a well-posed initial-value problem.
3. For that local constant-w model, the fixed-composition sound speed is

   `c_eff² = [w(1+w)ρ − 2q] / [(1+w)ρ − 2q]`, with `q=κ S_H²/4`.

   Ordinary dust has negative c_eff² for 0<q<ρ/2. Enthalpy vanishes at q/ρ=(1+w)/2. A flat homogeneous bounce reaches q/ρ=1. These facts block an unqualified promotion of the regular homogeneous ODE to a generic causal spherical Euler solver; they do not invalidate the FLRW ODE or prove that every EC theory/matter model fails.
4. **Metric symmetry and full-field symmetry differ.** Nonzero coherent convective Frenkel spin cannot inherit all FLRW symmetries. A verified flat FLRW *metric* with homogeneous aligned spin is a weaker, symmetry-noninheriting case; it is not an isotropic torsion configuration. A coherent SO(3)-invariant spherical spin tensor must be radial; in the selected ideal BHL formulation its retained linear-spin stress cancels. Parity and center conditions matter. A broader averaged correlation-retaining source still lacks closure.
5. A finite comoving no-flux boundary matched smoothly to vacuum must have zero effective pressure. Homogeneous ordinary dust with nonzero spin at that boundary does not automatically meet this condition. Full spinful surface-layer matching remains unresolved; a scalar spin zero is not proof of matching.
6. No novelty, global event horizon, eternal expansion, eternal oscillation or completed black-hole spacetime is claimed.

## Reproduce the audit

From the repository root, with Python 3.12, Node available and SymPy installed:

```sh
python -m venv /tmp/ec-spherical-audit-venv
/tmp/ec-spherical-audit-venv/bin/pip install -r research/ec-spherical/requirements.txt
/tmp/ec-spherical-audit-venv/bin/python research/ec-spherical/validation/run_checks.py
npm test
```

The audit runner records the actual test inventory and tool versions in `validation-results.json`. It checks the snapshot manifest as a record that this task left the prior FLRW files intact. A later intentional application change requires a reviewed new baseline for that snapshot comparison; the standalone mathematical test suite does not freeze the application forever:

```sh
python -m unittest discover -s research/ec-spherical/validation -v
sha256sum -c research/ec-spherical/baseline-flrw.sha256
```

The checks cover 23 test cases, including full coordinate Einstein calculation, a separately entered hand derivation, FLRW/vacuum/LTB limits, general stress conservation, Bianchi identities, mass/ADM relations, spin symmetry/transport, contortion and auxiliary torsion elimination, acoustic-sign obstruction, matching-pressure obstruction, Schwarzschild Riemann contraction and a read-only FLRW trajectory comparison. The LTB and nonspherical spin controls are manufactured analytical tests, not proposed EC initial profiles. These checks are not a PDE evolution or proof of well-posedness.

Compile the document using `pdflatex` and `ripgrep`:

```sh
bash research/ec-spherical/build_pdf.sh
```

The script compiles three passes in a temporary directory, rejects unresolved cross-references or overfull layout and writes only the final PDF into this research directory. TeX toolchain versions can affect the PDF's byte representation; scientific source/tests and the prescribed build are versioned.

## What is deliberately not implemented

No spherical PDE, full correlation closure, new spin action, spin relaxation, particle production, artificial spin window, pressure floor, exterior matching algorithm or new simulator mode was added. The full Weyssenhoff branch is specified using the published BHL field-equation formulation; its complete constrained microscopic matter-action derivation and the general spinful junction problem are identified as unresolved rather than filled with unsupported equations.
