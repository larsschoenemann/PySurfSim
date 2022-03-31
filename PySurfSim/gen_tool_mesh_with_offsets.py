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
@version: 1.2.1
@date:    2022-03-31
"""
import numpy as np


def gen_tool_mesh_with_offsets(*args):
    """Generate a milling tool mesh including live axis offsets

    Args:
        lim_x (float): _description_
        feed_x (float): _description_
        shift_f (float): _description_
        lim_y (float): _description_
        raster_y (float): _description_
        shift_r (float): _description_
        r_fly (float): _description_
        x0_pos (float): _description_
        tool_offsets (float): _description_

    Returns:
        _type_: _description_
    """
    if len(args) != 9:
        raise ValueError('Incorrect number of args')
    
    feed_x = {'lim': args[0],
              'feed': args[1],
              'feed_shift': args[2]}
    raster_y = {'lim': args[3],
                'raster': args[4],
                'raster_shift': args[5]}
    
    r_fly = args[6]
    x0_pos = args[7]
    tool_offsets = args[8]

    # calculate tool position
    num_x = np.min((np.ceil(feed_x['lim'] / feed_x['feed']) + 1,
                   len(tool_offsets['z'])))  
    # no discrete tool pos. in X
    
    if raster_y['raster'] > 0:
        # no discrete tool pos. in Y
        num_y = np.ceil(raster_y['lim'] / raster_y['raster']) + 1  
    else:
        num_y = 1
    
    tool_center_x = np.arange(num_x) * feed_x['feed'] + feed_x['feed_shift']
    tool_center_y = np.arange(num_y) * raster_y['raster'] + raster_y['raster_shift']
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
