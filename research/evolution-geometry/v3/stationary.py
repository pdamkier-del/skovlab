"""Unrestricted Dirichlet solve for a compact Regge slab."""
from dataclasses import dataclass

import numpy as np
from scipy.optimize import least_squares

from regge import GeometryError


@dataclass
class SlabSolve:
    intervals: np.ndarray
    field: np.ndarray
    edge_residual: np.ndarray
    field_residual: np.ndarray
    start_residual: float
    iterations: int
    stationary: bool


def solve_slab(engine,intervals,field,*,geometry_fixed=False,tolerance=1e-8,
               max_evaluations=120,clock=None,**action_options):
    """Solve all interior variations. A solver status alone cannot certify stationarity."""
    intervals=np.asarray(intervals)
    field=np.asarray(field)
    E=engine.free_edges if not geometry_fixed else np.empty(0,dtype=int)
    F=engine.free_vertices
    start=np.r_[intervals[E],field[F]]
    if not len(start):
        raise ValueError("The slab has no free degrees of freedom")
    def unpack(z):
        s=intervals.copy()
        phi=field.copy()
        s[E],phi[F]=z[:len(E)],z[len(E):]
        return s,phi
    def residual(z):
        s,phi=unpack(z)
        if clock is not None and np.max(engine.temporal_norm(s,clock))>=0:
            raise GeometryError("Supplied clock is not a time function")
        grad=engine.evaluate(s,phi,coupled=not geometry_fixed,**action_options)
        return np.r_[grad[1][E],grad[2][F]]
    initial=np.linalg.norm(residual(start),np.inf)
    def objective(z):
        try:
            return residual(z)
        except GeometryError:
            return np.full(len(z),max(50.,2*initial))
    # The numerical optimizer must not jump across a null edge into another sector.
    passed=intervals[E]
    if np.any(passed==0):
        raise GeometryError("Null free edge")
    lower=np.r_[np.where(passed>0,0.,-np.inf),np.full(len(F),-np.inf)]
    upper=np.r_[np.where(passed<0,0.,np.inf),np.full(len(F),np.inf)]
    result=least_squares(objective,start,max_nfev=max_evaluations,diff_step=1e-5,
                         bounds=(lower,upper),xtol=2e-12,gtol=2e-12,ftol=2e-12)
    values=residual(result.x)
    return SlabSolve(*unpack(result.x),values[:len(E)],values[len(E):],float(initial),
                     result.nfev,bool(np.linalg.norm(values,np.inf)<tolerance))
