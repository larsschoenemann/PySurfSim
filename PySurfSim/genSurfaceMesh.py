# -*- coding: utf-8 -*-
"""
Generates a surface mesh according input values.

Created on 2021-10-20
All rights reserved.

@author: Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
"""
import numpy as np


def genSurfaceMesh(dX, dY, zHeight=40.0,
                   resolution=100.0, fixedNumPoints=False):
    """
    Generate a surface mesh according input values.

    Parameters
    ----------
    dX : float
        Dimension in x.
    dY : float
        Dimension in y.
    zHeight : float, optional
        Initial surface height. The default is 40.0.
    resolution : float, optional
        resolution is either treated as interval (fixedNumPoints=False)
        or as number of points (fixedNumPoints=True). The default is 100.0.
    fixedNumPoints : bool, optional
        Use fixed number of points (False) or resolution (True). 
        The default is False.

    Returns
    -------
    mygrid : meshgrid
        Generated surface mesh.

    """
    rShape = np.shape(resolution)
    if rShape == (2,):
        rX = resolution[0]
        rY = resolution[1]
    elif rShape == ():
        rX = rY = resolution
    else:
        raise ValueError('Resolution should be single value or tuple, '
                         f'is {rShape}')
    
    if fixedNumPoints:
        xVec = np.linspace(0.0, dX, rX)
        yVec = np.linspace(0.0, dY, rY)
    else:
        xVec = np.arange(0.0, dX + rX, rX)
        yVec = np.arange(0.0, dY + rY, rY)
    mygrid = np.meshgrid(xVec, yVec)
    mygrid.append(np.ones(np.shape(mygrid[0])) * zHeight)
    return mygrid

# tests are not in unittest directory
