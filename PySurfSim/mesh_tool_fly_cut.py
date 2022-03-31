# -*- coding: utf-8 -*-
"""
Class for fly-cutting tool.

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


class MeshToolFlyCut:
    """Class for a fly-cutting tool.

    Returns:
        MeshToolFlyCut: Class for a flycutting tool.
    """
    r_fly = None
    delta_r_fly = None
    r_eps = None
    
    def __init__(self, **kwargs):
        self.r_fly = kwargs.get('r_fly', 70e6)
        self.delta_r_fly = kwargs.get('delta_r_fly', 0.0)
        self.r_eps = kwargs.get('r_eps', 0.762e6)
    
    def get_z(self, target_mesh, tool_pos):
        """Tool geometry of a fly-cutter over a given surface.

        Args:
            target_mesh (list of numpy arrays, float): support points for tool heightmap
                                                       e.g- X and Y meshes of a surface 
                                                       (only array pos [0] and [1] is considered).
            tool_pos (list of numpy arrays): Postion of the tool center points in X, Y and Z.

        Returns:
            array of float:  Tool height map.
        """
        mesh_x = target_mesh[0]
        mesh_y = target_mesh[1]
    
        x_m = tool_pos[0]
        y_m = tool_pos[1]
        z_m = tool_pos[2]
    
        # $$z_T = -\sqrt{(r_{fly}+\Delta r_{fly})^2 - (x-x_M)^2}
        #         - \sqrt{r_{\epsilon}^2-(y-y_M)^2} + r_\epsilon + z_M$$
        z_t = - np.sqrt((self.r_fly + self.delta_r_fly)**2 - (mesh_x - x_m)**2) \
              - np.sqrt(self.r_eps**2 - (mesh_y - y_m)**2) + self.r_eps + z_m
    
        # remove imagionary part, i.e. values outside of tool footprint
        # zT(imag(zT)~=0) = NaN
    
        return z_t

    def footprint(self, tool_pos, lim_z=40.0):
        """Get tool footprint.

        Args:
            tool_pos (array, float): Position of the tool in x,y,z
            lim_z (float, optional): Limiting height in z. Defaults to 40.0.

        Returns:
            float, float: limits of tool engagement in x and y
        """
        r_1 = self.r_fly + self.delta_r_fly  # first radius
        r_2 = self.r_eps  # second radius

        # calculate max height according to r1
        height = -(tool_pos[2] - r_1 - lim_z)  
        if height > 0:
            sqrt_x = np.sqrt(2 * r_1 * height - height**2)
            sqrt_y = np.sqrt(2 * r_2 * height - height**2)
            # calc. X limits
            x_lim = (-sqrt_x + tool_pos[0], sqrt_x + tool_pos[0])  
            # calc. Y limits
            y_lim = (-sqrt_y + tool_pos[1], sqrt_y + tool_pos[1])  
        else:
            x_lim = None
            y_lim = None

        return x_lim, y_lim
