# -*- coding: utf-8 -*-
"""
Integration test for applying a meshed tool to a surface.

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
from PySurfSim import applyMeshToolToWorkpiece, meshToolFlyCut


class TestIntApplyMeshToolToWorkpiece(unittest.TestCase):
    """ test cases for mesh tool application """
    def test(self):
        """standard test case"""
        parameters = {
            'rasterY': 8 * 1e3,   # feed in raster direction in nm
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
        
        x_vec = np.arange(0.0, 0.140e6, 100)
        y_vec = np.arange(0.0, 0.210e6, 100)
        surf_mesh = np.meshgrid(x_vec, y_vec)
        surf_mesh.append(np.ones(np.shape(surf_mesh[0])) * 40.0)
        
        tool_mesh = np.meshgrid([70e3], [105e3])
        tool_mesh.append(np.ones(np.shape(tool_mesh[0])) * 60e6)
        
        tool = meshToolFlyCut(**parameters)
        
        new_mesh = applyMeshToolToWorkpiece(surf_mesh, tool_mesh, tool)
        
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
