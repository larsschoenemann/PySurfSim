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
from PySurfSim import sliceSurface


class test_sliceSurface(unittest.TestCase):
    def test(self):
        xLen = 0.140e6
        yLen = 0.210e6
        zHei = 40.0
        res = 100
        
        numSliceX = 7
        numSliceY = 10
                
        xVec = np.arange(0.0, xLen, res)
        yVec = np.arange(0.0, yLen, res)
        surf_mesh = np.meshgrid(xVec, yVec)
        surf_mesh.append(np.ones(np.shape(surf_mesh[0])) * zHei)
        
        surf_slices = sliceSurface(surf_mesh, numSliceX, numSliceY)
        
        self.assertTrue(isinstance(surf_slices, list), 'input is not a list')
        self.assertEqual(len(surf_slices), int(numSliceX * numSliceY), 
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
