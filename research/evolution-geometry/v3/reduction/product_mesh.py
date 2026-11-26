"""Ordered prism triangulation and pullback to product metrics."""
import numpy as np

from mesh import Slab
from regge import Regge


class Product:
    def __init__(self, base, slab, segments=3, periodic=True):
        if segments < (3 if periodic else 1):
            raise ValueError("Too few segments for a simplicial fiber")
        levels = segments if periodic else segments + 1
        sites = np.array([(*x, j) for x in slab.sites for j in range(levels)])
        simplices = []
        axial = set()
        for cell in base.top:
            # A global ordering gives the same triangulation on shared facets.
            ordered = np.sort(cell)
            for j in range(segments):
                lower = levels * ordered + j
                upper = levels * ordered + (j + 1) % levels
                for k in range(len(ordered)):
                    simplices.append(np.r_[lower[:k + 1], upper[k:]])
                axial.update(tuple(sorted((a, b))) for a, b in zip(lower, upper))
        for a, b in slab.axial_edges:
            axial.update(tuple(sorted((levels*a+j, levels*b+j))) for j in range(levels))
        self.slab = Slab(sites, np.asarray(simplices), axial)
        self.engine = Regge(self.slab)
        self.segments = segments
        self.base = base
        self.vertex_map = np.arange(len(sites)) // levels
        a, b = self.engine.edges.T
        self.endpoints = self.vertex_map[self.engine.edges]
        index = {tuple(e): i for i, e in enumerate(base.edges)}
        self.edge_map = np.array([index.get((i, j), -1) for i, j in self.endpoints])
        self.cross = (a % levels) != (b % levels)

    def lift(self, s, phi, length):
        """At nonconstant length this is a midpoint ansatz for interval data."""
        length = np.broadcast_to(length, (self.base.nv,))
        if np.any(length <= 0):
            raise ValueError("Fiber length must be positive")
        middle = length[self.endpoints].mean(axis=1)
        lifted = np.r_[s, 0.][self.edge_map] + self.cross * (middle/self.segments)**2
        return lifted, phi[self.vertex_map]

    def evaluate(self, s, phi, length, **kwargs):
        lifted, field = self.lift(s, phi, length)
        action, ds, dp, _, _ = self.engine.evaluate(lifted, field, **kwargs)
        base_edges = self.edge_map >= 0
        edge_gradient = np.bincount(self.edge_map[base_edges], ds[base_edges],
                                    minlength=len(s))
        field_gradient = np.bincount(self.vertex_map, dp, minlength=len(phi))
        ends = self.endpoints[self.cross]
        lengths = np.broadcast_to(length, (self.base.nv,))
        weight = ds[self.cross] * lengths[ends].mean(axis=1) / self.segments**2
        length_gradient = np.bincount(ends.ravel(), np.repeat(weight, 2),
                                      minlength=self.base.nv)
        return action, edge_gradient, field_gradient, length_gradient
