# -*- coding: utf-8 -*-
"""
Apply a tool pass with given tool offsets.

Created on Fri Feb 18 10:08:21 2022
All rights reserved.

@author:  Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
"""
import numpy as np
from PySurfSim.applyMeshToolToWorkpiece import applyMeshToolToWorkpiece


def applyToolPassWithOffset(surf_mesh, p, x0_pos, tool_offsets):
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
    numX = np.min((np.ceil(p['limX'] / p['feedX']) + 1,
                   len(tool_offsets['z'])))  
    # no discrete tool pos. in X
    
    if p['rasterY'] > 0:
        # no discrete tool pos. in Y
        numY = np.ceil(p['limY'] / p['rasterY']) + 1  
    else:
        numY = 1
    
    toolCenterX = np.arange(numX) * p['feedX'] + p['shiftF']
    toolCenterY = np.arange(numY) * p['rasterY'] + p['shiftR']
    toolCenterZ = p['rFly']
    
    tool_mesh = np.meshgrid(toolCenterX, toolCenterY)
    tool_mesh.append(np.ones(np.shape(tool_mesh[0])) * toolCenterZ)
    # for iP in range(np.min((len(tool_mesh[0]), len(x0_pos_um)))):
    #     tool_mesh[0][iP] = tool_mesh[0][iP] + x0_pos_um[iP] * um2nm
    tool_mesh[0] = tool_mesh[0] + x0_pos
    for iZ in range(np.shape(tool_mesh)[2]):
        # tool_mesh[0][0][iZ] = tool_mesh[0][0][iZ] - x_off_w1_nm[groove][iZ]
        tool_mesh[0][0][iZ] = tool_mesh[0][0][iZ] - tool_offsets['x'][iZ]
        tool_mesh[1][0][iZ] = tool_mesh[1][0][iZ] - tool_offsets['y'][iZ]
        tool_mesh[2][0][iZ] = tool_mesh[2][0][iZ] - tool_offsets['z'][iZ]
    
    return applyMeshToolToWorkpiece(surf_mesh, tool_mesh, p), tool_mesh
