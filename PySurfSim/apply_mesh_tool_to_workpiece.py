# -*- coding: utf-8 -*-
# flake8: noqa=W291, W293
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
"""

import numpy as np


def apply_mesh_tool_to_workpiece(patch_xyz, tool_pos, tool):
    """
    Apply a meshed tool to a surface patch.

    Parameters
    ----------
    patchXYZ : list of arrays
        Surface patches (X- & Y-Meshes and Z-height).
    tool_pos : list of arrays
        Tool positions to be simulated.
    p : dict
        Processing parameters.

    Returns
    -------
    newPatchXYZ : list of arrays
        Modified surface patches (X- & Y-Meshes and Z-height).

    """
    patch_x = patch_xyz[0]
    patch_y = patch_xyz[1]
    surf_z = patch_xyz[2].copy()

    tool_pos_x = tool_pos[0].flatten()
    tool_pos_y = tool_pos[1].flatten()
    tool_pos_z = tool_pos[2].flatten()
    
    # sequentially iterate number of steps in raster direction
    for tool_center_x, tool_center_y, tool_center_z \
            in zip(tool_pos_x, tool_pos_y, tool_pos_z):
        
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
        else:
            mask = np.bitwise_and.reduce((patch_x >= x_lim[0],
                                          patch_x <= x_lim[1],
                                          patch_y >= y_lim[0],
                                          patch_y <= y_lim[1]))
            # apply mask to surface patch (X-coordinates)
            subset_x = patch_x[mask]
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
            subset_y = patch_y[mask] 
            # reshape subset to original mask shape
            subset_y = np.reshape(subset_y, 
                                 (in_x_end - in_x_start + 1, 
                                  in_y_end - in_y_start + 1))
            
            # apply tool function to subset
            z_t = tool.get_z([subset_x, subset_y],
                           [tool_center_x, tool_center_y, tool_center_z])
            
            # calculate minimum of result zT and given surface height surfZ
            z_s = np.reshape(surf_z[mask], 
                             (in_x_end - in_x_start + 1, 
                              in_y_end - in_y_start + 1))
            min_z = np.minimum(z_s, z_t)
            
            # save minimum to surface
            surf_z[in_x_start:in_x_end + 1, in_y_start:in_y_end + 1] = min_z
    
    return [patch_x, patch_y, surf_z].copy()


if __name__ == '__main__':
    # Visual test case
    from PySurfSim import gen_surface_mesh
    from PySurfSim.helpers import round_up_to_base
    from PySurfSim.mesh_tool_fly_cut import MeshToolFlyCut
    from mayavi import mlab

    p = {'raster_y': 8 * 1e3,   # feed in raster direction in nm
         'feed_x': 70 * 1e3,    # feed in cutting direction in nm
         'r_fly': 60 * 1E6,     # flycut radius in nm
         'r_eps': 0.762 * 1E6,  # tool nose radius in nm
         # deviation in flycut radius to nominal value in nm
         'delta_r_fly': 0.0,   
         # shift of tool in feed direction (necessary for second tool)
         'shift_f': 0.0,      
         'lim_x': 0.334833e6,   # limits of simulated surface in X in nm
         'lim_y': 0.334618e6,   # limits of simulated surface in Y in nm
         # initial surface height in nm (less height means less computation 
         # time, as the "footprint" of the flycutter is determined using 
         # this value
         'lim_z': 100.0,       
         'raster': 100.0,    # raster spacing of simulated surface
         'numpoints': 1024,  # numer of points
         'fixed_num_points': True,
         'visualize': True}  # do we want to plot the result?
    
    surf_mesh = gen_surface_mesh(p['lim_x'], p['lim_y'], p['lim_z'], 
                                 p['numpoints'], 
                                 fixed_num_points=p['fixed_num_points'])

    # calculate tool position
    # number of discrete tool positions in X
    numX = np.ceil(p['lim_x'] / p['feed_x']) + 1  
    # number of discrete tool positions in Y
    numY = np.ceil(p['lim_y'] / p['raster_y']) + 1  

    tc_x = np.arange(numX) * p['feed_x'] + p['shift_f']
    tc_y = np.arange(numY) * p['raster_y']
    TC_Z = p['r_fly']
    
    tool_mesh = np.meshgrid(tc_x, tc_y)
    tool_mesh.append(np.ones(np.shape(tool_mesh[0])) * TC_Z)
    
    test_tool = MeshToolFlyCut(**p)
    
    new_mesh = apply_mesh_tool_to_workpiece(surf_mesh, tool_mesh, test_tool)
    
    mlab.options.backend = 'auto'

    mlab.surf(new_mesh[0].T, new_mesh[1].T, new_mesh[2].T,
              warp_scale=1000, colormap='afmhot')
    mlab.axes(xlabel='feed', ylabel='raster', zlabel='height',
              ranges=[0, np.ceil(p['lim_x'] / 1000) * 1000,
                      0, np.ceil(p['lim_y'] / 1000) * 1000,
                      0, round_up_to_base(np.max(new_mesh[2]), 5)])
    cb = mlab.colorbar(orientation='vertical')
    cb.data_range = (0, 25)
    cb.number_of_labels = int(np.ceil(25 / 5) + 1)
    cb.label_text_property.font_size = 10
    mlab.view(azimuth=-135, elevation=66, distance='auto')
    mlab.show()
