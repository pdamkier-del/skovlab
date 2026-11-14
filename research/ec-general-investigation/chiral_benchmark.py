"""Analytic six-field ECD reference, not a numerical collapse solution."""
from pathlib import Path
import json
import numpy as np


def normalized_solution(x):
    x=np.asarray(x,dtype=float)
    if np.any(~np.isfinite(x)):raise ValueError('Finite conformal-time coordinates required.')
    return {'a_over_ab':np.sqrt(1+x*x),
            'proper_time_q_over_ab2':(x*np.sqrt(1+x*x)+np.arcsinh(x))/2,
            'H_ab2_over_q':x/(1+x*x)**1.5,
            'volume_scale_efolds_from_bounce':np.log1p(x*x)/2,
            'acceleration_ab4_over_q2':(1-x*x)/(1+x*x)**3}


def summary():
    return {'model':'Exact six independent massless same-chirality classical Dirac fields; flat torus FLRW metric',
        'method':'Analytic field/action solution; not a numerical time integration',
        'accelerated_post_bounce_efolds':float(np.log(2)/2),
        'post_bounce_nec_violating_efolds':float(np.log(1.5)/2),
        'total_future_scale_expansion':'unbounded; asymptotically decelerated radiation-like',
        'one_particle_per_fundamental_mode_classical_density_kappa_squared':float(1024*np.pi**3/27),
        'physical_status':'Pauli-normalized amplitude illustration uses the classical source; not a renormalized quantum prediction. Bounce curvature is outside controlled classical/EFT scales.',
        'scope':'Special global cosmological benchmark, no bounded cloud, exterior matching or general perturbative stability proof.'}


if __name__=='__main__':
    Path(__file__).with_name('chiral-benchmark-results.json').write_text(json.dumps(summary(),indent=2)+'\n')
    print(json.dumps(summary(),indent=2))
