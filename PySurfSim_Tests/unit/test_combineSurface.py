# -*- coding: utf-8 -*-
"""
Unit test for surface mesh combination.

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
from PySurfSim import combineSurface
from PySurfSim import pairwise


class test_combineSurface(unittest.TestCase):
    def test(self):
        xLen = 0.140e6
        yLen = 0.210e6
        zHei = 40.0
        res = 100
        numSliceX = 10
        numSliceY = 7
        
        xVec = np.arange(0.0, xLen + res, res)
        yVec = np.arange(0.0, yLen + res, res)
        surf_mesh_org = np.meshgrid(xVec, yVec)
        surf_mesh_org.append(np.ones(np.shape(surf_mesh_org[0])) * zHei)
        
        slicedSurface = list()
        # get dim. of surface to slice
        [_, numX, numY] = np.shape(surf_mesh_org)
        
        # create divions in 1st dim.
        a = np.floor(np.linspace(0, numX, numSliceX + 1)).astype(int)
        # create divions in 2nd dim.
        b = np.floor(np.linspace(0, numY, numSliceY + 1)).astype(int)

        for (b1, b2) in pairwise(b):    
            for (a1, a2) in pairwise(a):
                thisslice = [sliceElement[a1:a2, b1:b2]
                             for sliceElement in surf_mesh_org]
                slicedSurface.append(thisslice)
        
        surf_mesh = combineSurface(slicedSurface, numSliceX, numSliceY)
        
        self.assertTrue(isinstance(surf_mesh, list), 'input is not a list')
        self.assertEqual(len(surf_mesh), 3, 
                         'wrong number of elements')
        self.assertTrue(all(isinstance(item, np.ndarray) 
                            for item in surf_mesh),
                        'elements are not arrays')
        self.assertTrue(all(item.shape == (numX, numY)
                            for item in surf_mesh),
                        'elements are not arrays')


if __name__ == '__main__':
    unittest.main()
