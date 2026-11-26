"""Reproduce the V3 product and extra-direction benchmarks."""
import csv
from pathlib import Path

import numpy as np

from mesh import boundary_facets, metric_intervals, spacetime_slab
from regge import Regge, potential
from product_mesh import Product
from radion import evolve

OUT = Path(__file__).resolve().parent / "results"


def write(name, columns, rows):
    with (OUT / (name + ".csv")).open("w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(columns.split())
        writer.writerows(rows)


def product_trials():
    rows = []
    for shape in [(3,), (3, 3), (2, 2, 2)]:
        slab = spacetime_slab(shape, 3 if len(shape) < 3 else 2)
        base = Regge(slab)
        x = slab.sites * [.37, *([1] * len(shape))]
        eta = np.diag([-1., *([1.] * len(shape))])
        s = metric_intervals(x, base.edges, lambda _: eta)
        rng = np.random.default_rng(173)
        p = .07*rng.normal(size=base.nv)
        curved = s + .006*rng.normal(size=len(s))
        for periodic, matter, s0 in [(True, "affine", s), (True, "axial", curved),
                                     (True, "affine", curved), (False, "affine", curved)]:
            prod = Product(base, slab, periodic=periodic)
            L = .83
            config = dict(Gnewton=.24, matter=matter, cosmological=.021, model=potential(.3, .6))
            A, dS, dP, deficit, _ = base.evaluate(s0, p, **config)
            B, dU, dQ, dL = prod.evaluate(s0, p, L, **config)
            eps = 1e-5
            direction = rng.normal(size=base.nv)
            Ap = prod.evaluate(s0, p, L+eps*direction, **config)[0]
            Am = prod.evaluate(s0, p, L-eps*direction, **config)[0]
            joints = 0.
            if not periodic:
                hs = np.asarray(prod.engine.hinges)
                lifted, _ = prod.lift(s0, p, L)
                area, timelike, *_ = prod.engine.geometry(
                    prod.engine.gram(prod.engine.unpack(lifted, prod.engine.h_slots)))
                coordinate = prod.slab.sites[hs, -1]
                mask = prod.engine.exterior & timelike & (
                    (coordinate == 0).all(axis=1) | (coordinate == prod.segments).all(axis=1))
                boundary = boundary_facets(base.top)
                mask &= np.array([tuple(sorted(prod.vertex_map[h])) in boundary for h in hs])
                joints = area[mask].sum()/(16*config["Gnewton"])
                assert abs(B-L*A-joints) < 2e-10
            rows.append((base.D, periodic, matter, s0 is curved, np.max(abs(deficit[~base.exterior])),
                         A, B, B-L*A, np.max(abs(dU-L*dS)), np.max(abs(dQ-L*dP)),
                         dL.sum()-A, joints, abs((Ap-Am)/(2*eps)-dL@direction)))
    write("product", "D periodic matter perturbed interior_deficit A_base A_high action_error "
          "edge_error field_error length_error joints local_length_fd_error", rows)
    for D, periodic, matter, curved, deficit, A, B, err, ds, dp, dl, joints, fd in rows:
        if periodic:
            assert max(abs(err), ds, dp, abs(dl), fd) < 2e-7, (D, matter, curved, err, ds, dp, dl, fd)


def double_product():
    slab = spacetime_slab((2,), 2)
    base = Regge(slab)
    s = metric_intervals(slab.sites*[.39, 1.], base.edges, lambda _: np.diag([-1., 1.]))
    p = np.linspace(-.13, .23, base.nv)
    first = Product(base, slab)
    second = Product(first.engine, first.slab, segments=4)
    L1, L2 = .87, .96
    config = dict(Gnewton=.2, model=potential(.3, .7), matter="affine")
    s1, p1 = first.lift(s, p, L1)
    A = base.evaluate(s, p, **config)[0]
    B = second.evaluate(s1, p1, L2, **config)[0]
    assert abs(B-L1*L2*A) < 1e-11
    write("double_product", "L1 L2 A_base A_high error", [(L1, L2, A, B, B-L1*L2*A)])


def radion_trials():
    rows = []
    times = np.linspace(0, 2, 81)
    for n in [2, 3, 4]:
        for scenario, mass, cosmological in [("massless", 0., 0.), ("massive", .6, 0.),
                                              ("vacuum_offset", 0., .02)]:
            result = evolve(n, .08, potential(mass), times, cosmological=cosmological)
            assert max(abs(result[:, 7])) < 2e-11
            if scenario == "massless":
                assert max(abs(result[:, 2]-.8)) < 2e-12
            rows.extend((n, scenario, *row) for row in result)
    write("radion", "n scenario time a L H H_L phi momentum constraint frozen_source", rows)


if __name__ == "__main__":
    product_trials()
    double_product()
    radion_trials()
