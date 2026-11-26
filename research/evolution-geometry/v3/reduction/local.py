"""Omitted local fiber equations on a stationary reduced Regge history."""
import numpy as np

from homogeneous import Frusta
from mesh import Slab
from regge import Regge, potential
from product_mesh import Product
from run import write


def trials():
    rows = []
    for mass in [0., .6]:
        G, L = .08, .83
        model = potential(mass)
        f = Frusta(2, G, model)
        layer = f.engine.top
        n = len(f.time)//2
        base_slab = Slab(np.array([(t, i) for t in range(3) for i in range(n)]),
                         np.vstack([layer, layer+n]), set())
        base = Regge(base_slab)
        product = Product(base, base_slab)
        for ell, h in [(1., .32), (1., .20), (1., .12), (1., .08),
                       (.75, .06), (.50, .04), (.25, .02)]:
            a = np.array([ell, .35])
            b = f.start(a, .17, h)
            c, new_h, reduced_residual = f.step(a, b, h)
            scales = np.array([a[0], b[0], c[0]])
            phi = np.repeat([a[1], b[1], c[1]], n)
            ends = base.edges//n
            u, v = scales[ends].T
            j, k = (base.edges%n).T
            offsets = (j//3 != k//3).astype(int)+(j%3 != k%3)
            dt = np.diff(np.array([0, h, h+new_h])[ends], axis=1).ravel()
            s = np.where(ends[:, 0] != ends[:, 1],
                         .25*((2-offsets)*(v-u)**2+offsets*(u+v)**2)-dt**2,
                         offsets*u**2)
            # Use canonically normalized base field in the low action, and
            # high field / sqrt(L) with G_high=L*G_base in the lifted action.
            high_model = (lambda p: model[0](p*np.sqrt(L))/L,
                          lambda p: model[1](p*np.sqrt(L))/np.sqrt(L))
            _, ds, dp, dl = product.evaluate(s, phi/np.sqrt(L), L, Gnewton=L*G,
                                            model=high_model, matter="affine")
            band = np.arange(n, 2*n)
            max_r = max(np.max(abs(ds[base.free_edges])), np.max(abs(dp[band])))
            rows.append((mass, ell, h, new_h, reduced_residual, max_r, np.max(abs(dl[band])),
                         dl[band].mean()/((h+new_h)/2*scales[1]**2), np.ptp(dl[band])))
            assert reduced_residual < 2e-8
    massless = [row for row in rows if row[0] == 0.]
    massive = [row for row in rows if row[0] > 0.]
    assert abs(massless[-1][-2]) < abs(massless[-2][-2])/3
    assert abs(massive[-1][-2] - .6**2*.35**2/.83) < .002
    write("local_fiber", "mass ell h next_h reduced_residual base_residual max_fiber_residual fiber_residual_per_volume "
          "fiber_translational_spread", rows)


if __name__ == "__main__":
    trials()
