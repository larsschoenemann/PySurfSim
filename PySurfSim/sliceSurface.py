# -*- coding: utf-8 -*-
"""
Split a meshed surface into smaller patches.

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
from PySurfSim.helpers import pairwise


def sliceSurface(surfaceToSlice, xDiv, yDiv):
    """
    Split a meshed surface into smaller patches.

    Parameters
    ----------
    surfaceToSlice : list of arrays, float
        A list of 3 numpy arrays (X, Y and Z) with X and Y defining the surface
        grid and Z defining the height at each point of the grid.
    xDiv : int
        No of patches in X-direction.
    yDiv : int
        No of patches in Y-direction.

    Returns
    -------
    slicedSurface : list of arrays, float
        Returns a list of xDiv*yDiv patches containing slices of the original
        meshed surface.


    (c)2021,
    Dr.-Ing. Lars Schoenemann, schoenemann@iwt-bremen.de,
    Leibniz Institute for Materials Engineering IWT, Bremen, Germany
    v1.0, 2021-10-21
    """
    if xDiv <= 0:
        raise ValueError(f'division in x cannot be 0 or negative (is {xDiv})')
    if yDiv <= 0:
        raise ValueError(f'division in y cannot be 0 or negative (is {yDiv})')

    slicedSurface = list()
    # get dim. of surface to slice
    [_, xLen, yLen] = np.shape(surfaceToSlice)
    
    if xDiv > xLen:
        raise ValueError(f'more divisions than length in x ({xDiv} > {xLen})')
    if yDiv > yLen:
        raise ValueError(f'more divisions than length in y ({yDiv} > {yLen})')
    
    # create divions in 1st dim.
    a = np.floor(np.linspace(0, xLen, xDiv + 1)).astype(int)
    # create divions in 2nd dim.
    b = np.floor(np.linspace(0, yLen, yDiv + 1)).astype(int)

    for (b1, b2) in pairwise(b):    
        for (a1, a2) in pairwise(a):
            thisslice = [sliceElement[a1:a2, b1:b2]
                         for sliceElement in surfaceToSlice]
            slicedSurface.append(thisslice)
    return slicedSurface
