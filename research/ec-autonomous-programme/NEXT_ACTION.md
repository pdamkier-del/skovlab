# Exact next action after cycle 02

Latest completed: C01 homogeneous high-curvature harmonic verification and periodic charge fix; C02 continuum-constrained planar perturbation with near-second-order spatial convergence. Read the JSON records; do not repeat completed audit/sweeps without a new question.

Next C03: using periodic_data()/run() in code/planar_contraction.py, test finite epsilon and higher seed mode (start epsilon=.1,.3 and modes1,4) with n=65,129,257 and duration .8. Resolve the highest seed mode adequately, verify the BVP residual and measured physical density contrast, and refine timestep independently. Compare normal/current expansion, density contrast amplification, Hamiltonian/momentum/gauge and charge errors. Every run must respect the characteristic bound and stop before lapse<.05. In this context a constraint/gauge failure is an unresolved numerical stop, not a physical singularity or oscillation.

The C02 local tangent stress diagnostic has delta sensitivity; centered evolved-snapshot divergence has a known temporal floor. Keep both. The metric-velocity temporal ratio was 9.85 in one pair, so seek a clearer independent time-refinement sequence instead of asserting fourth order universally.

Periodicity imposes a torus. PlanarGrid retains all tensor components but removes x/y dependence; its verified full-grid lift does not test transverse perturbation stability. Use a later constrained fully 3D data family for that question.

Update all seven research records at the end of each cycle, commit milestones on codex/ec-autonomous-programme, and leave exact continuation parameters and unresolved failures.
