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


class meshToolFlyCut:
    """Class for a fly-cutting tool."""
    
    rFly = None
    deltaRfly = None
    rEps = None
    
    def __init__(self, **kwargs):
        self.rFly = kwargs.get('rFly', 70e6)
        self.deltaRfly = kwargs.get('deltaRfly', 0.0)
        self.rEps = kwargs.get('rEps', 0.762e6)
    
    def getZ(self, surf_mesh, tool_pos):
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
        meshX = surf_mesh[0]
        meshY = surf_mesh[1]
    
        xM = tool_pos[0]
        yM = tool_pos[1]
        zM = tool_pos[2]
    
        # $$z_T = -\sqrt{(r_{fly}+\Delta r_{fly})^2 - (x-x_M)^2}
        #         - \sqrt{r_{\epsilon}^2-(y-y_M)^2} + r_\epsilon + z_M$$
        zT = - np.sqrt((self.rFly + self.deltaRfly)**2 - (meshX - xM)**2) \
             - np.sqrt(self.rEps**2 - (meshY - yM)**2) + self.rEps + zM
    
        # remove imagionary part, i.e. values outside of tool footprint
        # zT(imag(zT)~=0) = NaN
    
        return zT

    def footprint(self, tool_pos, limZ=40.0):
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
        r1 = self.rFly + self.deltaRfly  # first radius
        r2 = self.rEps  # second radius

        # calculate max height according to r1
        h = -(tool_pos['z'] - r1 - limZ)  
        if h > 0:
            sqrX = np.sqrt(2 * r1 * h - h**2)
            sqrY = np.sqrt(2 * r2 * h - h**2)
            # calc. X limits
            xLim = (-sqrX + tool_pos['x'], sqrX + tool_pos['x'])  
            # calc. Y limits
            yLim = (-sqrY + tool_pos['y'], sqrY + tool_pos['y'])  
        else:
            xLim = None
            yLim = None

        return xLim, yLim
