# Exact continuation after six completed cycles

## Read first

Read MASTER_STATUS.md and the end of RESEARCH_LOG.md. Completed results are in cycle01–cycle06 JSON files. The branch is codex/ec-autonomous-programme, based on audit commit 770122a9d1e69bbea123a132e98e717a300a9699. Main still supplies the original research baseline; the autonomous work is not silently merged.

Do not repeat the old audit, the homogeneous reference derivation, C02/C03 density sweeps or C04 fixed-polarization construction as new research. Existing tests can of course be run as regressions after edits. C05's expensive 33³ run took about 317 seconds; its full raw endpoint fields were not saved.

## Highest-priority new cycle: periodic spin texture

Scientific question: does the resolved focusing behavior survive a change of spin orientation, rather than only seed density, within the same massless minimal one-field action?

Use L=8,k=2 pi/L,kappa1,m0. Keep n_seed=4[1+.1 cos(kx)cos(ky)cos(kz)]. Propose a smooth periodic lower-component texture

Psi=sqrt(n_seed)(0,0,cos(theta/2),sin(theta/2)), theta=.2 sin(kx).

This is a proposed new free-data family, not an already verified result. First derive its total axial/spin bilinears and all initial stress projections from the full Dirac equation. Check the sign/orientation of each spin component explicitly. Test the proposed source relation jtilde=(curl S_seed)/4 and conformal j=chi^-6 jtilde for independent arbitrary first jets, including theta gradients. A scalar phase or complex rotation could add momentum terms; do not assume a pure curl beyond this real texture. Verify whether E remains GA n_seed² chi^-12 before reusing C04's scalar equation. Reject the ansatz/reuse if the full source disagrees.

If those identities hold, solve the zero-mean periodic vector constraint with the general solenoidal curl source, then the same positive-chi/CMC scalar normalization as C04. Check n=9/17/33 independent FD constraints and oversampled continuum residuals; tighten nonlinear tolerance to ensure it is not the observed error. Check every source component and harmonic initialization.

Only then evolve a short interval, initially t_end=.2 with 40 steps and separate time refinement as in C05. Use the full 3D engine and all complex components, not an imposed evolving polarization. Compare against the fixed-polarization data at matched n_seed/charge, resolving constraints separately. Predeclare numerical/coordinate stops and compare observables with their refinement error. A finite perturbation response is not a general stability theorem.

## Required implementation before expensive evolution

Add optional full field NPZ checkpoints (g,p,psi,physical times/units,seed parameters,grid/boundary metadata), including the initial slice, every declared diagnostic time, and any rejected final state/stop reason where safe. Do not store only resampled comparison fields. This prevents repeating a completed long run merely to evaluate new diagnostics.

Apply torsion_curvature.measure() to those checkpoints with at least two tangent difference steps; it currently assumes mass0,kappa1. Record full and metric Riemann contractions, the chosen normal-frame component maximum, torsion invariant, current conditioning and all constraints. Small full-scalar residuals can be truncation error; R_tilde=0 by itself proves nothing about regularity.

## Interpretation/decision

A convergent continued contraction, a resolved local turn, or an explicit numerical/model-domain stop are all legitimate outcomes. No bounce/oscillation should be inferred from a sign near the error floor, an oscillating spinor phase, lapse collapse or a failed elliptic solve. A candidate torsion-attributed turn requires a separate action-consistent torsion-free comparison and extended regular continuation.

After each completed cycle update all seven research records, commit the milestone, and leave exact continuation data. Do not claim a physically controlled fermion cloud, general 3D stability, finite-body bounce or baby universe from these classical periodic calculations.
