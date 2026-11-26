"""Independent edge equations and scalar dispersion on a sheared lattice."""
import numpy as np
from scipy.linalg import null_space, qr
from scipy.integrate import solve_ivp
from scipy.optimize import brentq, least_squares

from mesh import metric_intervals, spacetime_slab
from regge import GeometryError, Regge, potential
from run import write


def derivative(fun, x, eps=2e-6):
    return np.column_stack([(fun(x+d)-fun(x-d))/(2*eps) for d in eps*np.eye(len(x))])


def slab_trials():
    slab = spacetime_slab((3, 3), 3)
    r = Regge(slab)
    x = slab.sites*np.array([.41, 1., 1.])
    eta = np.diag([-1., 1., 1.])
    sflat = metric_intervals(x, r.edges, lambda _: eta)
    E, F = r.free_edges, r.free_vertices
    a, b = r.edges.T
    displacement = np.zeros((len(a), r.nv, 3))
    displacement[np.arange(len(a)), a] = 2*(x[a]-x[b])@eta
    displacement[np.arange(len(a)), b] = -displacement[np.arange(len(a)), a]
    displacement = displacement.reshape(len(a), -1)
    motions = displacement[E] @ null_space(displacement[r.fixed_edges], rcond=1e-10)
    left, movable, _ = np.linalg.svd(motions, full_matrices=False)
    gauge = left[:, movable > 1e-9]
    zero = np.zeros(r.nv)
    model = potential(.65)
    G = .03
    def background(t, state):
        a, phi, momentum = state
        H = np.sqrt(8*np.pi*G*(.5*momentum**2+model[0](phi)))
        return [a*H, momentum, -2*H*momentum-model[1](phi)]
    ref = solve_ivp(background, (0, 2), [1., .2, .09], dense_output=True,
                    rtol=1e-12, atol=1e-14)
    s0 = metric_intervals(x, r.edges, lambda q: np.diag([-1., *([ref.sol(q[0])[0]**2]*2)]))
    p0 = ref.sol(x[:, 0])[1]
    ts = s0[E]<0

    def gravity(delta):
        s = sflat.copy()
        s[E] += delta
        return r.evaluate(s, zero, matter="affine")[1][E]

    hessian = derivative(gravity, np.zeros(len(E)))
    singular = np.linalg.svd(hessian, compute_uv=False)
    write("gauge", "mode singular_value gauge_defect induced_motion_rank",
          [(i, value, np.linalg.norm(hessian@gauge, 2) if i == 0 else "", gauge.shape[1] if i == 0 else "")
           for i, value in enumerate(singular)])
    assert np.count_nonzero(singular < 1e-7) == 9
    assert np.linalg.norm(hessian@gauge, 2) < 1e-7

    rows = []
    trace = []
    for amplitude in [0., .001, .003, .01, .02]:
        phi0 = p0+amplitude*np.cos(1.7*x[:, 1]+.8*x[:, 0])
        active = np.r_[E, len(s0)+F]
        start = np.r_[s0, phi0]

        def residual(state):
            s, phi = state[:len(s0)], state[len(s0):]
            if np.any(s*s0 <= 0) or r.temporal_norm(s, x[:, 0]).max() >= 0:
                raise GeometryError("Left initial causal branch")
            _, ds, dp, _, _ = r.evaluate(s, phi, G, model, matter="affine")
            return np.r_[ds[E], dp[F]]

        def solve(selected):
            def fun(delta):
                state = start.copy()
                state[selected] += delta
                try:
                    return residual(state)
                except GeometryError:
                    return np.full(len(active), 100.+np.linalg.norm(delta))
            sol = least_squares(fun, np.zeros(len(selected)), max_nfev=140, x_scale="jac",
                                xtol=1e-12, ftol=1e-12, gtol=1e-13)
            state = start.copy()
            state[selected] += sol.x
            return state, residual(state)

        base_state, fixed = solve(active)
        # Fix interior gauge approximately by choosing directions independent at
        # the initial configuration. Adjustable exterior edges define other data.
        candidates = np.r_[active, r.fixed_edges]
        jac = derivative(lambda d: residual(start+np.bincount(candidates, d, len(start))),
                         np.zeros(len(candidates)))
        weights = np.r_[np.ones(len(active)), np.full(len(r.fixed_edges), .7)]
        _, _, pivot = qr(jac*weights, pivoting=True, mode="economic")
        state, adjusted = solve(candidates[pivot[:len(active)]])
        for label, final, result in [("fixed", base_state, fixed), ("adjusted", state, adjusted)]:
            rows.append((amplitude, label, np.max(abs(result[:-1][~ts])),
                         np.max(abs(result[:-1][ts])), abs(result[-1]),
                         np.linalg.norm(gauge.T@result[:-1]), np.linalg.norm(result[:-1]),
                         np.max(abs(final[r.fixed_edges]-start[r.fixed_edges])),
                         np.max(abs(final-start)),
                         r.temporal_norm(final[:len(s0)], x[:, 0]).max()))
            trace.extend((amplitude, label, i, s0[i], final[i], result[j])
                         for j, i in enumerate(E))
        assert np.max(abs(adjusted)) < np.max(abs(fixed))
    write("slab", "amplitude boundary spatial_residual timelike_residual scalar_residual "
          "flat_gauge_projection edge_norm max_boundary_shift max_shift max_clock_norm", rows)
    write("independent_edges", "amplitude boundary edge initial_s final_s residual", trace)


def waves():
    slab = spacetime_slab((3, 3), 3)
    r = Regge(slab)
    center = r.free_vertices[0]
    rows = []
    for shear in [0., .25, -.25]:
        for dx in [.4, .2, .1, .05, .025]:
            dt = .37*dx
            x = slab.sites*[dt, dx, dx]
            relative = x-x[center]
            g = np.array([[-1+shear**2, shear, 0], [shear, 1, 0], [0, 0, 1]])
            s = metric_intervals(x, r.edges, lambda _: g)
            for operator in ["axial", "affine"]:
                kernel = np.array([r.evaluate(s, p, coupled=False, matter=operator)[2][center]
                                   for p in np.eye(r.nv)])
                for k in [np.array([.95, .4]), np.array([-.95, -.4])]:
                    GR = np.linalg.norm(k)-shear*k[0]
                    axial = np.sqrt(1-shear**2)*np.linalg.norm(k)
                    def symbol(omega):
                        phase = relative[:, 1:]@k-relative[:, 0]*omega
                        return kernel@np.cos(phase)
                    result = brentq(symbol, 0, 2.5)
                    rows.append((shear, dx, dt, operator, *k, result, GR, axial,
                                 abs(result-GR), abs(result-axial)))
    write("sheared_waves", "shear dx dt operator kx ky omega physical axial_limit physical_error "
          "axial_limit_error", rows)
    for shift in [.25, -.25]:
        affine = [row for row in rows if row[0] == shift and row[3] == "affine" and row[4] > 0]
        axial = [row for row in rows if row[0] == shift and row[3] == "axial" and row[4] > 0]
        assert affine[-1][-2] < affine[-2][-2]/3.8
        assert axial[-1][-2] > .1 and axial[-1][-1] < 1e-4


if __name__ == "__main__":
    slab_trials()
    waves()
