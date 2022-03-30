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
"""
import numpy as np


class MeshToolFlyCut:
    """Class for a fly-cutting tool."""
    
    r_fly = None
    delta_r_fly = None
    r_eps = None
    
    def __init__(self, **kwargs):
        self.r_fly = kwargs.get('r_fly', 70e6)
        self.delta_r_fly = kwargs.get('delta_r_fly', 0.0)
        self.r_eps = kwargs.get('r_eps', 0.762e6)
    
    def get_z(self, surf_mesh, tool_pos):
        """
        Tool geometry of a fly-cutter over a given surface.
    
        Parameters
        ----------
        surf_mesh : list of numpy arrays, float
            X and Y meshes of a surface (Z mesh is ignored).
        tool_pos : list of numpy arrays
            Postion of the tool center points in X, Y and Z.
        rFly : float
            Nominal fly-cut radius (r_{fly}).
        drFly : float
            Deviation to nominal flycut radius (Delta r_{fly}).
        rEps : float
            Nose radius (r_epsilon).
    
        Returns
        -------
        zT : array of float
            Tool height map (z_T).
    
    
        (c)2021,
        Dr.-Ing. Lars Schoenemann, schoenemann@iwt-bremen.de,
        Leibniz Institute for Materials Engineering IWT, Bremen, Germany
        v1.0, 2021-10-21
        """
        mesh_x = surf_mesh[0]
        mesh_y = surf_mesh[1]
    
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
        """
        Generate a tool footprint.

        Parameters
        ----------
        tool_pos : TYPE
            DESCRIPTION.
        rFly : TYPE, optional
            DESCRIPTION. The default is 60*1E6.
        deltaRfly : TYPE, optional
            DESCRIPTION. The default is 0.
        rEps : TYPE, optional
            DESCRIPTION. The default is 0.762*1E6.
        limZ : TYPE, optional
            DESCRIPTION. The default is 40.0.

        Returns
        -------
        xLim : TYPE
            DESCRIPTION.
        yLim : TYPE
            DESCRIPTION.

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
