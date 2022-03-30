# -*- coding: utf-8 -*-
"""
Apply a tool pass with given tool offsets.

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

@author:  Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
"""
import numpy as np


def gen_tool_mesh_with_offsets(
    lim_x, feed_x, shift_f, 
    lim_y, raster_y, shift_r, 
    r_fly,
    x0_pos, tool_offsets):
    """
    .

    Parameters
    ----------
    surf_mesh : TYPE
        DESCRIPTION.
    p : TYPE
        DESCRIPTION.
    x0_pos : TYPE
        DESCRIPTION.
    tool_offsets : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.
    tool_mesh : TYPE
        DESCRIPTION.

    """
    # calculate tool position
    num_x = np.min((np.ceil(lim_x / feed_x) + 1,
                   len(tool_offsets['z'])))  
    # no discrete tool pos. in X
    
    if raster_y > 0:
        # no discrete tool pos. in Y
        num_y = np.ceil(lim_y / raster_y) + 1  
    else:
        num_y = 1
    
    tool_center_x = np.arange(num_x) * feed_x + shift_f
    tool_center_y = np.arange(num_y) * raster_y + shift_r
    tool_center_z = r_fly
    
    tool_mesh = np.meshgrid(tool_center_x, tool_center_y)
    tool_mesh.append(np.ones(np.shape(tool_mesh[0])) * tool_center_z)
    # for iP in range(np.min((len(tool_mesh[0]), len(x0_pos_um)))):
    #     tool_mesh[0][iP] = tool_mesh[0][iP] + x0_pos_um[iP] * um2nm
    tool_mesh[0] = tool_mesh[0] + x0_pos
    for i in range(np.shape(tool_mesh)[2]):
        # tool_mesh[0][0][iZ] = tool_mesh[0][0][iZ] - x_off_w1_nm[groove][iZ]
        tool_mesh[0][0][i] = tool_mesh[0][0][i] - tool_offsets['x'][i]
        tool_mesh[1][0][i] = tool_mesh[1][0][i] - tool_offsets['y'][i]
        tool_mesh[2][0][i] = tool_mesh[2][0][i] - tool_offsets['z'][i]
    
    return tool_mesh
