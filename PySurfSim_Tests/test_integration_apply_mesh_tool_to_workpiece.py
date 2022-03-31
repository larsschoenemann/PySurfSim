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
@version: 1.2
@date:    2022-03-31
"""
import unittest

import numpy as np
from PySurfSim import MeshToolFlyCut, apply_mesh_tool_to_workpiece, default_parameters


class TestIntApplyMeshToolToWorkpiece(unittest.TestCase):
    """ test cases for mesh tool application """
    def test_correct_type_and_shape(self):
        """standard test case"""
        parameters = default_parameters().copy()
       
        x_vec = np.arange(0.0, 0.140e6, 100)
        y_vec = np.arange(0.0, 0.210e6, 100)
        surf_mesh = np.meshgrid(x_vec, y_vec)
        surf_mesh.append(np.ones(np.shape(surf_mesh[0])) * 40.0)
        
        tool_mesh = np.meshgrid([70e3], [105e3])
        tool_mesh.append(np.ones(np.shape(tool_mesh[0])) * 60e6)
        
        tool = MeshToolFlyCut(**parameters)
        
        new_mesh = apply_mesh_tool_to_workpiece(surf_mesh, tool_mesh, tool)
        
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
