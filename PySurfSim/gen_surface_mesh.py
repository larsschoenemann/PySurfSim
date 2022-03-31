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
@version: 1.2
@date:    2022-03-31
"""
import numpy as np


def gen_surface_mesh(d_x, d_y, z_height=40.0,
                     resolution=100.0, fixed_num_points=False):
    """Generate a surface mesh.

    Args:
        d_x (float): Dimension in x.
        d_y (float): Dimension in y.
        z_height (float, optional): Initial surface height. Defaults to 40.0.
        resolution (float, optional): treated as interval (fixedNumPoints=False)
                                      or as number of points (fixedNumPoints=True).
                                      Defaults to 100.0.
        fixed_num_points (bool, optional): Use fixed number of points (False) or resolution (True). 
                                           Defaults to False.

    Raises:
        ValueError: Error if wrong resolution was passed.

    Returns:
        meshgrid: Generated surface mesh.
    """
    
    r_shape = np.shape(resolution)
    if r_shape == (2,):
        r_x = resolution[0]
        r_y = resolution[1]
    elif r_shape == ():
        r_x = r_y = resolution
    else:
        raise ValueError('Resolution should be single value or tuple, '
                         f'is {r_shape}')
    
    if fixed_num_points:
        x_vec = np.linspace(0.0, d_x, r_x)
        y_vec = np.linspace(0.0, d_y, r_y)
    else:
        x_vec = np.arange(0.0, d_x + r_x, r_x)
        y_vec = np.arange(0.0, d_y + r_y, r_y)
    mygrid = np.meshgrid(x_vec, y_vec)
    mygrid.append(np.ones(np.shape(mygrid[0])) * z_height)
    return mygrid
