"""Continuum homogeneous torus data for the extra Einstein equation."""
import numpy as np
from scipy.integrate import solve_ivp


def evolve(n, gravity, potential, times, phi=.35, momentum=.17, length=.8, cosmological=0.):
    kappa = 8*np.pi*gravity
    V, dV = potential
    density = .5*momentum**2 + V(phi)
    H = np.sqrt(2*(kappa*density+cosmological)/(n*(n-1)))

    def rhs(t, state):
        a, L, H, J, q, p = state
        expansion = n*H+J
        source = 2*(cosmological+kappa*V(q))/n
        return [a*H, L*J, source-expansion*H, source-expansion*J, p,
                -expansion*p-dV(q)]

    result = solve_ivp(rhs, (times[0], times[-1]), [1, length, H, 0, phi, momentum],
                       t_eval=times, rtol=2e-12, atol=2e-14)
    if not result.success:
        raise RuntimeError(result.message)
    a, L, H, J, q, p = result.y
    constraint = n*(n-1)*H**2/2+n*H*J-kappa*(.5*p**2+V(q))-cosmological
    missing = 4*(cosmological+kappa*V(q))/(n-1)
    return np.column_stack([times, a, L, H, J, q, p, constraint, missing])
