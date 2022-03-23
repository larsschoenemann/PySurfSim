# -*- coding: utf-8 -*-
"""
Unit test for surface mesh generation.

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
from PySurfSim import genSurfaceMesh


class test_genSurfaceMesh(unittest.TestCase):
    """ Things to check :
        - the return value should be a list of 3 numpy arrays with equal shape
        - all values in mesh[2] (surface height) should be equal 
          (to custom zHeight)
        - the number of elements is
           fixedNumPoints=False -> (yLen/res, xLen/res)
           fixedNumPoints=True and resolution=(val) ->(val, val)
           fixedNumPoints=True and resolution=(val1, val2) -> (val1, val2)
    """
    
    def _check_list_equal_shaped_elements(self, mylist):
        self.assertTrue(isinstance(mylist, list), 'input is not a list')
        self.assertEqual(len(mylist), 3, 'wrong number of elements')
        self.assertTrue(all(isinstance(item, np.ndarray) for item in mylist),
                        'elements are not numpy arrays')
        self.assertTrue(all(item.shape == mylist[0].shape for item in mylist),
                        'elements do not have the same shape')

    def test_minimal(self):
        print('check mwe')
        mesh = genSurfaceMesh(0.210e6, 0.105e6)
        self._check_list_equal_shaped_elements(mesh)
        
        self.assertTrue(np.array_equal(element, mesh[2][0, 0]) 
                        for element in mesh[2])
        
    def test_zheight(self):
        print('check setting of custom zHeight')
        cust_zHeight = 50.0
        mesh = genSurfaceMesh(0.210e6, 0.210e6, zHeight=cust_zHeight)
        
        self._check_list_equal_shaped_elements(mesh)
        
        self.assertTrue(np.array_equal(element, cust_zHeight) 
                        for element in mesh[2])
    
    def test_zheight_and_res(self):
        print('check setting zHeight and resolution')
        xLen = 0.140e6
        yLen = 0.210e6
        zH = 50.0
        res = 70.0
        mesh = genSurfaceMesh(xLen, yLen, zH, res)
        
        self._check_list_equal_shaped_elements(mesh)
        self.assertTrue(all(item.shape == (int((yLen + res) / res), 
                                           int((xLen + res) / res)) 
                            for item in mesh),
                        'element shape does not match size and resolution')
        self.assertTrue(np.array_equal(element, zH) 
                        for element in mesh[2])
        
    def test_zheight_and_res_tuple(self):
        print('check setting zHeight and resolution tuple')
        xLen = 0.140e6
        yLen = 0.210e6
        zH = 50.0
        res = (70.0, 30.0)
        mesh = genSurfaceMesh(xLen, yLen, zH, res)
        
        self._check_list_equal_shaped_elements(mesh)
        self.assertTrue(all(item.shape == (int((yLen + res[1]) / res[1]), 
                                           int((xLen + res[0]) / res[0])) 
                            for item in mesh),
                        'element shape does not match size and resolution')
        self.assertTrue(np.array_equal(element, zH) 
                        for element in mesh[2])
        
    def test_fixedNumPoints_single(self):
        print('check fixed number of points and resolution')
        res = 1024
        mesh = genSurfaceMesh(0.140e6, 0.210e6, 40.0, 
                              res, fixedNumPoints=True)
        
        self._check_list_equal_shaped_elements(mesh)
        self.assertTrue(all(item.shape == (res, res)
                            for item in mesh), 
                        'element shape does not match fixed number of points')
        
    def test_fixedNumPoints_tuple(self):
        print('check fixed number of points and resolution tuple')
        res = (1024, 512)
        mesh = genSurfaceMesh(0.210e6, 0.105e6, 40.0, 
                              res, fixedNumPoints=True)
        
        self._check_list_equal_shaped_elements(mesh)
        self.assertTrue(all(item.shape == tuple(reversed(res))
                            for item in mesh), 
                        'element shape does not match fixed number of points')
        
        
if __name__ == '__main__':
    unittest.main()
