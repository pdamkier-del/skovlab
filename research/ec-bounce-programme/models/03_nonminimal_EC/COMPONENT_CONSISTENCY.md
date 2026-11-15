# P06 — a necessary covariance consistency test

The primary source is [Lucat–Prokopec, Eqs. 30–33](https://arxiv.org/html/1512.06074v1). We inspected the local Hartree/Fock structure and printed equal-time component system. This audit concerns a necessary algebraic property, not a full reproduction or refutation of its renormalized 2PI theory.

For real mass, denote a single mode's three components by f=(x,y,z), same-helicity momentum moments by X,Y,Z, and B=Σ_hZ_h−Z/4. Set c=6πG_Nξ²/a². Taking the printed component RHS as a vector field and independently differentiating its length gives

d(f·f)/dη=(c/2)z(yX−xY).

This is not identically zero. A Hermitian, collisionless Hartree–Fock generator acting on a **full** two-level covariance must instead be a commutator, hence a Bloch cross product and isospectral. The first two interaction components would require an additional third-component contribution c(xY−yX)/4 for that particular cross-product completion. This is a necessary algebraic completion, not a validated replacement for the paper's theory.

The independent SymPy identity is supplemented by two helicities and two momenta with full covariance eigenvalues strictly between zero and one. The printed generator gives a squared-length derivative up to 1.8e−6 in the declared dimensionless test; the cross-product completion gives zero within numerical precision. No time integration or bounce inference is needed for this check.

## Why this is not yet a paper-level no-go

The source describes regular/vacuum-subtracted currents and additional approximations. Such currents need not themselves be occupation matrices or evolve isospectrally. A nonzero length derivative therefore cannot by itself prove Pauli violation by the paper's actual physical state. It does show that implementing these components naively as full covariance dynamics is unjustified.

The exact subtraction identity at finite cutoff makes the missing task explicit. Write R=P⁻+C_k. From iṘ=[h0+Σ,R] and [h0,P⁻]=0,

iĊ_k=[h0+Σ,C_k]+[Σ,P⁻_k]−iṖ⁻_k.

The last term vanishes only for the fixed Minkowski reference. Omitting the reference commutator is not generally the same approximation as full Hartree–Fock. For an evolving metric the projector derivative, matching and stress counterterms must be derived together. They cannot be reconstructed merely by requiring the subtracted Bloch length to be constant.

Decision: do not use the printed component system as an exact Pauli-preserving numerical source until its subtraction map and approximation order are independently established. The matrix-functional implementation in P05 passes the corresponding unitary/energy checks in a fixed-background regulated model; it does not settle the fully renormalized cosmological source. Model 3 remains INCONCLUSIVE. Ghost/gradient spectra, B3 and B6 remain unresolved.

Artifacts: `code/component_consistency.py`, `results/07_component_consistency.json`. The algebraic defect is preserved even though its physical interpretation remains conditional.
