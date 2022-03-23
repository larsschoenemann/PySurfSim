# -*- coding: utf-8 -*-
"""
Generate a surface mesh for numerical simulation.

Copyright (C) 2022  Lars Schönemann

This library is free software; you can redistribute it and/or modify 
it under the terms of the GNU Lesser General Public License as published by 
the Free Software Foundation; either version 2.1 of the License, or 
(at your option) any later version.

This library is distributed in the hope that it will be useful, 
but WITHOUT ANY WARRANTY; without even the implied warranty of 
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the 
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License 
along with this library; if not, write to the Free Software Foundation, Inc., 
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

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
    Generate a surface mesh.

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
