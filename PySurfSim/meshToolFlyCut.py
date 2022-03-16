# -*- coding: utf-8 -*-
"""
Tool geometry of a fly-cutter over a given surface.

Created on Fri Nov 19 13:51:51 2021

@author: Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
"""
import numpy as np


def meshToolFlyCut(surf_mesh, tool_pos, rFly, drFly, rEps):
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
    zT = - np.sqrt((rFly + drFly)**2 - (meshX - xM)**2) \
         - np.sqrt(rEps**2 - (meshY - yM)**2) + rEps + zM

    # remove imagionary part, i.e. values outside of tool footprint
    # zT(imag(zT)~=0) = NaN

    return zT

    def footprint(tool_pos, rFly=60 * 1E6, deltaRfly=0,
                         rEps=0.762 * 1E6, limZ=40.0):
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
        r1 = rFly + deltaRfly  # first radius
        r2 = rEps  # second radius

        h = -(tool_pos['z'] - r1 - limZ)  # calculate max height according to r1
        if h > 0:
            sqrX = np.sqrt(2 * r1 * h - h**2)
            sqrY = np.sqrt(2 * r2 * h - h**2)
            xLim = (-sqrX + tool_pos['x'], sqrX + tool_pos['x'])  # calc. X limits
            yLim = (-sqrY + tool_pos['y'], sqrY + tool_pos['y'])  # calc. Y limits
        else:
            xLim = None
            yLim = None

        return xLim, yLim
