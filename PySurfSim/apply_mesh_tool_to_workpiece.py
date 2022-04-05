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
from .helpers import get_surface_subset


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
        
        subset, selection = get_surface_subset(patch_xyz, (x_lim, y_lim))
        
        if subset is None:
            continue

        min_z = np.minimum(
            surf_z[selection],
            tool.get_z(subset, [tool_center_x, tool_center_y, tool_center_z])
        )
        
        # save minimum to surface
        surf_z[selection] = min_z
    
    return [patch_xyz[0], patch_xyz[1], surf_z].copy()
