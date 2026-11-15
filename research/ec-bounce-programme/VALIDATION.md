# Reproduction and integrity

From `research/ec-bounce-programme/`, install the versions in `requirements.txt` if needed, then run:

```bash
OPENBLAS_NUM_THREADS=1 python code/validate_programme.py
```

The validator reruns four small investigations and the separate source-parameter arithmetic and verifies their evidence. It writes versions and SHA256 of source/evidence to `results/validation.json`. Run scripts individually as `python code/finite_fock.py`, `python code/thermal_bounds.py`, `python code/stress_and_mass.py`, `python code/nonrelativistic_loophole.py`, `python code/source_scale_check.py`.

- **Operator check:** fresh sparse CAR matrices, full quartic vacuum ordering versus an independent analytic coincident Wick formula; 17 ensembles, 256-dimensional space. Error ≤3.56e−15. Finite-mode variance is not a continuum stress-noise validation.
- **Thermal check:** eight adaptive momentum quadratures to infinity, relative/absolute requested tolerance 2e−11, compared with independent analytical FD polynomials. Quadrature estimates are not rigorous interval error bounds; agreement and limiting/symmetry checks are retained.
- **Pauli check:** 800 seeded random piecewise-constant particle/antiparticle spectra. Shell integrals are exact polynomials at double precision. The sharp theorem is proved analytically; random tests alone would not prove it. Full-sea saturation is independently asserted.
- **Stress check:** explicit thermodynamic susceptibility/Legendre transform, symbolic massless conservation, and fresh gamma trace for massive unpolarized Dirac matter. The low-momentum bound is compared with actual integrals.
- **Cold-state falsification:** nine mass/temperature checks and a bracketed radiation-only root, followed by inclusion of the independently integrated positive fermion energy. No state or gravitational trajectory is evolved.

All reference quantities use κ=1 unless a symbolic κ is shown. Dimensional example values do not automatically certify a physically controlled EFT. No prior classical engine is imported. Gaussian factorization is an explicit state assumption, including exchange, rather than replacing a current composite by its mean square. The root is a deliberately incomplete-source counterexample, not a bounce result.

There is no new PDE/ODE spacetime evolution, spatial stencil, boundary discretization, dynamic field checkpoint, temporal refinement or inhomogeneous stability result. These are not omitted tests of an accepted candidate: the physical-source gate failed before such an evolution was justified. The previous branches retain their own numerical evidence and limitations.
