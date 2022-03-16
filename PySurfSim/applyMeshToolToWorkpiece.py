"""
Apply a mesh tool to a given workpiece.

@author: Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
"""
import numpy as np
from PySurfSim.getToolFootprint import getToolFootprint
from PySurfSim.meshToolFlyCut import meshToolFlyCut


def applyMeshToolToWorkpiece(patchXYZ, tool_pos, p, 
                             toolFunction=None):
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
    if not callable(toolFunction):
        toolFunction = meshToolFlyCut
    
    patchX = patchXYZ[0]
    patchY = patchXYZ[1]
    surfZ = patchXYZ[2].copy()

    toolPosX = tool_pos[0].flatten()
    toolPosY = tool_pos[1].flatten()
    toolPosZ = tool_pos[2].flatten()
    
    # sequentially iterate number of steps in raster direction
    for toolCenterX, toolCenterY, toolCenterZ \
            in zip(toolPosX, toolPosY, toolPosZ):
        
        # caluclate footprint of tool for given height
        [xLim, yLim] = getToolFootprint({'x': toolCenterX,
                                         'y': toolCenterY,
                                         'z': toolCenterZ},
                                        rFly=p['rFly'],
                                        deltaRfly=p['deltaRfly'],
                                        rEps=p['rEps'],
                                        limZ=np.max(surfZ))
        # generate mask with footprint limits
        if xLim is None or yLim is None:
            print('X{:.6f} Y{:.6f} Z{:.6f}: tool not engaged'.format
                  (toolCenterX, 
                   toolCenterY, 
                   toolCenterZ))
            continue
        else:
            mask = np.bitwise_and.reduce((patchX >= xLim[0],
                                          patchX <= xLim[1],
                                          patchY >= yLim[0],
                                          patchY <= yLim[1]))
            # apply mask to surface patch (X-coordinates)
            subsetX = patchX[mask]
            if(len(subsetX) == 0):
                continue
                        
            # get start and end indices of rectangular mask
            # [inXstart, inYstart] = find(mask, 1, 'first')
            indices = np.where(mask)
            [inXstart, inYstart] = [indices[0][0], indices[1][0]]
            # [inXend, inYend] = find(mask, 1, 'last')
            [inXend, inYend] = [indices[0][-1], indices[1][-1]]
            
            # reshape subset to original mask shape
            subsetX = np.reshape(subsetX, 
                                 (inXend - inXstart + 1, 
                                  inYend - inYstart + 1))
            
            # apply mask to surface patch (Y-coordinates)
            # should not be empty as subsetX was not empty
            subsetY = patchY[mask] 
            # reshape subset to original mask shape
            subsetY = np.reshape(subsetY, 
                                 (inXend - inXstart + 1, 
                                  inYend - inYstart + 1))
            
            # apply tool function to subset
            zT = toolFunction([subsetX, subsetY],
                              [toolCenterX, toolCenterY, toolCenterZ],
                              p['rFly'], p['deltaRfly'], p['rEps'])
            
            # calculate minimum of result zT and given surface height surfZ
            zS = np.reshape(surfZ[mask], 
                            (inXend - inXstart + 1, 
                             inYend - inYstart + 1))
            minZ = np.minimum(zS, zT)
            
            # save minimum to surface
            surfZ[inXstart:inXend + 1, inYstart:inYend + 1] = minZ
    
    return [patchX, patchY, surfZ].copy()


if __name__ == '__main__':
    # Visual test case
    from PySurfSim.genSurfaceMesh import genSurfaceMesh
    from PySurfSim.helpers import round_up_to_base
    from mayavi import mlab

    p = {'rasterY': 8 * 1e3,   # feed in raster direction in nm
         'feedX': 70 * 1e3,    # feed in cutting direction in nm
         'rFly': 60 * 1E6,     # flycut radius in nm
         'rEps': 0.762 * 1E6,  # tool nose radius in nm
         # deviation in flycut radius to nominal value in nm
         'deltaRfly': 0.0,   
         # shift of tool in feed direction (necessary for second tool)
         'shiftF': 0.0,      
         'limX': 0.334833e6,   # limits of simulated surface in X in nm
         'limY': 0.334618e6,   # limits of simulated surface in Y in nm
         # initial surface height in nm (less height means less computation 
         # time, as the "footprint" of the flycutter is determined using 
         # this value
         'limZ': 100.0,       
         'raster': 100.0,    # raster spacing of simulated surface
         'numpoints': 1024,  # numer of points
         'fixedNumPoints': True,
         'visualize': True}  # do we want to plot the result?
    
    surf_mesh = genSurfaceMesh(p['limX'], p['limY'], p['limZ'], 
                               p['numpoints'], 
                               fixedNumPoints=p['fixedNumPoints'])

    # calculate tool position
    # number of discrete tool positions in X
    numX = np.ceil(p['limX'] / p['feedX']) + 1  
    # number of discrete tool positions in Y
    numY = np.ceil(p['limY'] / p['rasterY']) + 1  

    toolCenterX = np.arange(numX) * p['feedX'] + p['shiftF']
    toolCenterY = np.arange(numY) * p['rasterY']
    toolCenterZ = p['rFly']
    
    # tool_mesh = np.meshgrid(toolCenterX, toolCenterY, toolCenterZ)
    tool_mesh = np.meshgrid(toolCenterX, toolCenterY)
    tool_mesh.append(np.ones(np.shape(tool_mesh[0])) * toolCenterZ)
    
    new_mesh = applyMeshToolToWorkpiece(surf_mesh, tool_mesh, p)
    
    # import matplotlib
    # import matplotlib.pyplot as plt
    # from matplotlib import cm
    # fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
    # ax.scatter3D(new_mesh[0], new_mesh[1], new_mesh[2], c=new_mesh[2],
    #              cmap=cm.inferno, edgecolor='none')
    # ax.set_box_aspect(aspect = (1,1,1/10))
    # ax.azim = -125
    
    # mlab.options.backend = 'envisage'
    mlab.options.backend = 'auto'
    # f = mlab.figure(fgcolor=(0., 0., 0.), bgcolor=(1, 1, 1))
    mlab.surf(new_mesh[0].T, new_mesh[1].T, new_mesh[2].T,
              warp_scale=1000, colormap='afmhot')
    mlab.axes(xlabel='feed', ylabel='raster', zlabel='height',
              ranges=[0, np.ceil(p['limX'] / 1000) * 1000,
                      0, np.ceil(p['limY'] / 1000) * 1000,
                      0, round_up_to_base(np.max(new_mesh[2]), 5)])
    cb = mlab.colorbar(orientation='vertical')
    cb.data_range = (0, 25)
    cb.number_of_labels = int(np.ceil(25 / 5) + 1)
    cb.label_text_property.font_size = 10
    mlab.view(azimuth=-135, elevation=66, distance='auto')
