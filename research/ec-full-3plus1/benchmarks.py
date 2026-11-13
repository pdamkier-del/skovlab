"""Analytic harmonic gauge wave and convergence of the actual 3D operator."""
import numpy as np
from ecd import minkowski,rk4,Grid


def gauge_wave(grid,t=0.,amplitude=.02):
    k=np.pi/grid.half_width;phase=k*(grid.xyz[...,0]-t);h=np.exp(amplitude*np.sin(phase));ht=-k*amplitude*np.cos(phase)*h
    g,p,psi=minkowski(grid);g[...,0,0]=-h;g[...,1,1]=h;p[...,0,0]=-ht;p[...,1,1]=ht
    return g,p,psi


def run_wave(n=9,duration=.1,steps=8):
    grid=Grid(n,2.,'periodic');state=gauge_wave(grid)
    for _ in range(steps):state=rk4(grid,state,duration/steps)
    exact=gauge_wave(grid,duration)
    return float(np.sqrt(np.mean((state[0]-exact[0])**2))),state


if __name__=='__main__':
    for n in [7,11,15]:print(n,run_wave(n)[0])
