# Verified cycles — 2026-11-16

E01: reviewed issue #9 and PR #2/#3/#5/#8 records without rerunning old trajectories. Fixed one nonzero-beta,c action and common conventions. Verified all ten original metric and 24 compatible-contortion variations, reduced stress, Ward and EC basis-transformed source limit. Result: 01_local_variation.json.

E02: derived arbitrary lapse/shift ADM system, interaction projections and scalar canonical shift. Checked geometry against independent four-metric jets and canonical equations symbolically. Results: 03_ADM_geometry.json, 05_canonical_scalar.json. No strongly hyperbolic evolution solver claimed.

E03: solved a new mixed scalar/Dirac periodic inhomogeneous constraint family and two separate counterfactual actions. Resolved collocation interpolation contamination by finer BVP mesh at unchanged physical inputs. Result: 02_initial_data.json, including reloadable collocation arrays and three-grid independent residuals.

E04: reconstructed full connection curvature from these retained data and equation-generated initial jets. Checked H=z, original trace and effective Einstein residual; recorded two tangent probes and three spatial grids. Normal congruence focuses initially. Results: 04_initial_Cartan_curvature.json and 04_initial_fields.json. This is not temporal evolution.

E05: independently checked coupled matter stress/current conservation using nonconstant all-component spinors and scalar on Minkowski. Increased spatial resolution to distinguish deliberately omitted stress from finite-difference error. Result: 06_matter_conservation.json. No physical input tuning.

E06: consolidated reproducibility runner, original-action/ADM documentation, physical falsification gates and precise handoff. Kept quantum-state validity and nonlinear time evolution explicitly unresolved. Do not repeat E01-E05 unless code/conventions change.
