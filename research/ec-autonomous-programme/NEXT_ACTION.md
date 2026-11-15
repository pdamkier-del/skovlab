# Exact continuation after cycle 07

Branch: codex/ec-autonomous-programme. Completed C01–C07 records are committed. Do not repeat the old density-only sweeps or source derivations as new research. C07 establishes the real spin-texture source identities and periodic constrained data; it does not establish stability or a bounce.

## Next C08 experiment

Use spin_texture_data.construct(): L8,n_seed=4[1+.1 cos(kx)cos(ky)cos(kz)], theta=.2 sin(kx), real lower pair, m0,kappa1, tolerance1e-11. Evolve the original full 3D ECD equations to harmonic t=.2 with 40 steps on n=9,17,33. Refine time separately at n17 with 20/40/80 steps. Do not impose a frozen evolving polarization. Preserve 5% relative-Hamiltonian, lapse .1, spacelike metric, timelike current and characteristic-step guards; every guard exit is inconclusive rather than a singularity/bounce result.

Before expensive runs use checkpoints.save_checkpoint/load_checkpoint for full fields at t=0,.1,.2 and any finite rejected state, with reasons and last accepted state. Save NPZ files under checkpoints/cycle08, commit them as binary blobs and put relative paths, whole-file SHA256 and field hashes in the result manifest. Record actual runtime and code hashes. A restart must reproduce arrays and the next RK step exactly; these tests already pass.

At each persisted diagnostic time evaluate torsion_curvature.measure() at delta1e-4 and5e-5, reload from disk before probing, and record full/metric curvature, current conditioning, all constraints, charge and stress divergence. Full scalar zero alone is not regularity evidence. Keep the separate spatial/time/diagnostic-step errors visible.

Use the C05 JSON as the fixed-polarization comparator at matched density seed/charge with separately resolved constraints, not as a torsion-free run. Report differences against their convergence uncertainty. A finite-time bounded response does not prove arbitrary-perturbation or long-time stability.

Persist code/results/status at every completed cycle. If a numerical stop or an unverified source identity prevents progress, retain the failure evidence and select the next question; do not change the physical action to force a desired outcome.
