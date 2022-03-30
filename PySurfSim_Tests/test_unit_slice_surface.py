# -*- coding: utf-8 -*-
"""
Unit test for surface slicing.

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
from PySurfSim import slice_surface


class TestSliceSurface(unittest.TestCase):
    """ Test cases for surface slicing """
    def test(self):
        """ standard test case """
        x_len = 0.140e6
        y_len = 0.210e6
        z_height = 40.0
        res = 100
        
        num_slice_x = 7
        num_slice_y = 10
                
        x_vec = np.arange(0.0, x_len, res)
        y_vec = np.arange(0.0, y_len, res)
        surf_mesh = np.meshgrid(x_vec, y_vec)
        surf_mesh.append(np.ones(np.shape(surf_mesh[0])) * z_height)
        
        surf_slices = slice_surface(surf_mesh, num_slice_x, num_slice_y)
        
        self.assertTrue(isinstance(surf_slices, list), 'input is not a list')
        self.assertEqual(len(surf_slices), int(num_slice_x * num_slice_y), 
                         'wrong number of elements')
        self.assertTrue(all(isinstance(item, list) 
                            for item in surf_slices),
                        'elements are not lists')
        self.assertTrue(all(all(
            isinstance(element, np.ndarray) 
            for element in item) 
            for item in surf_slices),
            'elements are not lists')


if __name__ == '__main__':
    unittest.main()
