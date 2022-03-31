# -*- coding: utf-8 -*-
"""
Apply a mesh tool to a given workpiece.

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


def apply_mesh_tool_to_workpiece(patch_xyz, tool_pos, tool):
    """Apply a meshed tool to a surface patch.

    Args:
        patch_xyz (list of arrays): Surface patches (X- & Y-Meshes and Z-height).
        tool_pos (list of arrays): Tool positions to be simulated.
        tool (tool class): Tool class to apply.

    Returns:
        list of arrays: Modified surface patches (X- & Y-Meshes and Z-height).
    """
    surf_z = patch_xyz[2].copy()

    # sequentially iterate number of steps in raster direction
    for tool_center_x, tool_center_y, tool_center_z \
            in zip(tool_pos[0].flatten(), 
                   tool_pos[1].flatten(), 
                   tool_pos[2].flatten()):
        
        # caluclate footprint of tool for given height
        [x_lim, y_lim] = tool.footprint([tool_center_x,
                                         tool_center_y,
                                         tool_center_z],
                                        lim_z=np.max(surf_z))
        # generate mask with footprint limits
        if x_lim is None or y_lim is None:
            print((
                f'X{tool_center_x:.6f} '
                f'Y{tool_center_y:.6f} '
                f'Z{tool_center_z:.6f}: tool not engaged'))
            continue
        
        mask = np.bitwise_and.reduce((patch_xyz[0] >= x_lim[0],
                                      patch_xyz[0] <= x_lim[1],
                                      patch_xyz[1] >= y_lim[0],
                                      patch_xyz[1] <= y_lim[1]))
        
        # apply mask to surface patch (X-coordinates)
        subset_x = patch_xyz[0][mask]
        if len(subset_x) == 0:
            continue
                        
        # get start and end indices of rectangular mask
        # [inXstart, inYstart] = find(mask, 1, 'first')
        indices = np.where(mask)
        [in_x_start, in_y_start] = [indices[0][0], indices[1][0]]
        # [inXend, inYend] = find(mask, 1, 'last')
        [in_x_end, in_y_end] = [indices[0][-1], indices[1][-1]]
        
        # reshape subset to original mask shape
        subset_x = np.reshape(subset_x, 
                              (in_x_end - in_x_start + 1, 
                               in_y_end - in_y_start + 1))
        
        # apply mask to surface patch (Y-coordinates)
        # should not be empty as subsetX was not empty
        subset_y = patch_xyz[1][mask] 
        # reshape subset to original mask shape
        subset_y = np.reshape(subset_y, 
                              (in_x_end - in_x_start + 1, 
                               in_y_end - in_y_start + 1))
        
        # calculate minimum of result zT and given surface height surfZ
        min_z = np.minimum(
            np.reshape(surf_z[mask], 
                       (in_x_end - in_x_start + 1, 
                        in_y_end - in_y_start + 1)), 
            tool.get_z([subset_x, subset_y],
                       [tool_center_x, tool_center_y, tool_center_z]))
        
        # save minimum to surface
        surf_z[in_x_start:in_x_end + 1, in_y_start:in_y_end + 1] = min_z
    
    return [patch_xyz[0], patch_xyz[1], surf_z].copy()
