# -*- coding: utf-8 -*-
"""
Generate a tool footprint.

Created on 2019-04-01

@author: Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
"""
import numpy as np


def getToolFootprint(tool_pos, rFly=60 * 1E6, deltaRfly=0,
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
