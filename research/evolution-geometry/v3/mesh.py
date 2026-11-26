"""Combinatorics only. Integer labels do not assign physical lengths."""
from collections import Counter
from dataclasses import dataclass
from itertools import combinations, permutations, product

import numpy as np


def axial_complex(shape, masks=None):
    """All axis-aligned cubes supported by actual reciprocal axial edges."""
    nodes = tuple(product(*(range(n) for n in shape)))
    axes = set(range(len(shape)))
    if masks is None:
        masks = {node: axes for node in nodes}
    if set(masks) != set(nodes) or any(not set(mask) <= axes for mask in masks.values()):
        raise ValueError("Invalid axis masks")
    edges = set()
    for node in nodes:
        for axis in masks[node]:
            other = tuple(x+(i == axis) for i,x in enumerate(node))
            if other in masks and axis in masks[other]:
                edges.add((node,other))
    cubes=[]
    for node in nodes:
        active=sorted(masks[node])
        for dimension in range(len(active)+1):
            for directions in combinations(active,dimension):
                vertices = {bits:tuple(x + (bits[directions.index(k)] if k in directions else 0)
                                       for k,x in enumerate(node))
                            for bits in product([0,1],repeat=dimension)}
                if not all(v in masks for v in vertices.values()):
                    continue
                if not all((v,vertices[bits[:j]+(1,)+bits[j+1:]]) in edges
                           for bits,v in vertices.items() for j in range(dimension) if bits[j]==0):
                    continue
                cubes.append((node,directions,tuple(vertices.values())))
    return nodes,edges,cubes


def maximal_cubes(cubes):
    covered=set()
    maximal=[]
    for node,axes,verts in sorted(cubes,key=lambda c:-len(c[1])):
        key=(node,axes)
        if key in covered:
            continue
        maximal.append((node,axes,verts))
        for length in range(len(axes)):
            for keep in combinations(axes,length):
                removed=tuple(a for a in axes if a not in keep)
                for bits in product([0,1],repeat=len(removed)):
                    lower=tuple(x+(bits[removed.index(i)] if i in removed else 0)
                                for i,x in enumerate(node))
                    covered.add((lower,keep))
    return maximal


@dataclass
class Slab:
    sites: np.ndarray
    simplices: np.ndarray
    axial_edges: set


def spacetime_slab(shape,time_count,masks=None):
    """Freudenthal triangulation, with time first and exactly one axial leg per step."""
    if time_count<2 or any(side<1 for side in shape):
        raise ValueError("Need at least one time interval and a nonempty spatial lattice")
    nodes,axial,cubes=axial_complex(shape,masks)
    maximal=maximal_cubes(cubes)
    dims={len(axes) for _,axes,_ in maximal}
    if len(dims)!=1:
        raise ValueError(f"Non-pure complex: maximal spatial dimensions {sorted(dims)}")
    n=dims.pop()
    if n<1:
        raise ValueError("Need a spatial direction")
    sites=[(t,*node) for t in range(time_count) for node in nodes]
    lookup={node:i for i,node in enumerate(sites)}
    top=[]
    for t in range(time_count-1):
        for node,axes,_ in maximal:
            directions=(0,*(axis+1 for axis in axes))
            for order in permutations(directions):
                point=list((t,*node))
                chain=[lookup[tuple(point)]]
                for axis in order:
                    point[axis]+=1
                    chain.append(lookup[tuple(point)])
                top.append(chain)
    axial_ids={tuple(sorted((lookup[t,*a],lookup[t,*b]))) for t in range(time_count) for a,b in axial}
    axial_ids.update((lookup[t,*a],lookup[t+1,*a]) for t in range(time_count-1) for a in nodes)
    return Slab(np.asarray(sites),np.asarray(top),axial_ids)


def boundary_facets(simplices):
    counts=Counter(tuple(sorted(f)) for simplex in simplices for f in combinations(simplex,len(simplex)-1))
    if max(counts.values(),default=0)>2:
        raise ValueError("A facet has more than two incident top simplices")
    return {facet for facet,count in counts.items() if count==1}


def metric_intervals(sites,edges,metric):
    """Initialize with one symmetric midpoint metric per edge."""
    u,v=sites[edges.T]
    dx=v-u
    g=np.asarray([metric(x) for x in (u+v)/2])
    return np.einsum("bi,bij,bj->b",dx,g,dx)
