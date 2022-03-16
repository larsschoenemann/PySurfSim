# -*- coding: utf-8 -*-
"""
Unit test for applying a meshed tool to a surface.

Created on Mon Mar 14 13:18:59 2022
All rights reserved.

@author:  Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
"""
import unittest
import numpy as np
from PySurfSim import applyMeshToolToWorkpiece


class test_genSurfaceMesh(unittest.TestCase):
    def test(self):
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
        
        xVec = np.arange(0.0, 0.140e6, 100)
        yVec = np.arange(0.0, 0.210e6, 100)
        surf_mesh = np.meshgrid(xVec, yVec)
        surf_mesh.append(np.ones(np.shape(surf_mesh[0])) * 40.0)
        
        tool_mesh = np.meshgrid([70e3], [105e3])
        tool_mesh.append(np.ones(np.shape(tool_mesh[0])) * 60e6)
        
        new_mesh = applyMeshToolToWorkpiece(surf_mesh, tool_mesh, p)
        
        self.assertTrue(isinstance(new_mesh, list), 'input is not a list')
        self.assertEqual(len(new_mesh), 3, 'wrong number of elements')
        self.assertTrue(all(isinstance(item, np.ndarray) 
                            for item in new_mesh),
                        'elements are not numpy arrays')
        self.assertTrue(all(item.shape == new_mesh[0].shape 
                            for item in new_mesh),
                        'elements do not have the same shape')
        

if __name__ == '__main__':
    unittest.main()
