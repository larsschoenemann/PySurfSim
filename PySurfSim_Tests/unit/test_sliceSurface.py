# -*- coding: utf-8 -*-
"""
Unit test for surface slicing.

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
