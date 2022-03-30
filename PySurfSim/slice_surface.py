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


def slice_surface(surface_to_slice, x_div, y_div):
    """
    Split a meshed surface into smaller patches.

    Parameters
    ----------
    surface_to_slice : list of arrays, float
        A list of 3 numpy arrays (X, Y and Z) with X and Y defining the surface
        grid and Z defining the height at each point of the grid.
    x_div : int
        No of patches in X-direction.
    y_div : int
        No of patches in Y-direction.

    Returns
    -------
    sliced_surface : list of arrays, float
        Returns a list of xDiv*yDiv patches containing slices of the original
        meshed surface.


    (c)2021,
    Dr.-Ing. Lars Schoenemann, schoenemann@iwt-bremen.de,
    Leibniz Institute for Materials Engineering IWT, Bremen, Germany
    v1.0, 2021-10-21
    """
    if x_div <= 0:
        raise ValueError(f'division in x cannot be 0 or negative (is {x_div})')
    if y_div <= 0:
        raise ValueError(f'division in y cannot be 0 or negative (is {y_div})')

    sliced_surface = []
    # get dim. of surface to slice
    [_, x_len, y_len] = np.shape(surface_to_slice)
    
    if x_div > x_len:
        raise ValueError(f'more divisions than length in x ({x_div} > {x_len})')
    if y_div > y_len:
        raise ValueError(f'more divisions than length in y ({y_div} > {y_len})')
    
    # create divions in 1st dim.
    div_a = np.floor(np.linspace(0, x_len, x_div + 1)).astype(int)
    # create divions in 2nd dim.
    div_b = np.floor(np.linspace(0, y_len, y_div + 1)).astype(int)

    for (b_1, b_2) in pairwise(div_b):    
        for (a_1, a_2) in pairwise(div_a):
            thisslice = [sliceElement[a_1:a_2, b_1:b_2]
                         for sliceElement in surface_to_slice]
            sliced_surface.append(thisslice)
    return sliced_surface
