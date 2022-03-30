# -*- coding: utf-8 -*-
"""
Unit test for surface mesh combination.

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
from PySurfSim import combine_surface, pairwise


class TestCombineSurface(unittest.TestCase):
    """ Test cases for combination of surface patches """
    def test(self):
        """ standard test case """
        limits = {'x': 0.140e6,
                  'y': 0.210e6,
                  'z': 40.0,
                  'res': 100}
        
        num_slice_x = 10
        num_slice_y = 7
        
        x_vec = np.arange(0.0, limits['x'] + limits['res'], limits['res'])
        y_vec = np.arange(0.0, limits['y'] + limits['res'], limits['res'])
        surf_mesh_org = np.meshgrid(x_vec, y_vec)
        surf_mesh_org.append(np.ones(np.shape(surf_mesh_org[0])) * limits['z'])
        
        sliced_surface = []
        # get dim. of surface to slice
        [_, num_x, num_y] = np.shape(surf_mesh_org)
        
        # create divions in 1st dim.
        div_a = np.floor(np.linspace(0, num_x, num_slice_x + 1)).astype(int)
        # create divions in 2nd dim.
        div_b = np.floor(np.linspace(0, num_y, num_slice_y + 1)).astype(int)

        for (b_1, b_2) in pairwise(div_b):    
            for (a_1, a_2) in pairwise(div_a):
                thisslice = [sliceElement[a_1:a_2, b_1:b_2]
                             for sliceElement in surf_mesh_org]
                sliced_surface.append(thisslice)
        
        surf_mesh = combine_surface(sliced_surface, num_slice_x, num_slice_y)
        
        self.assertTrue(isinstance(surf_mesh, list), 'input is not a list')
        self.assertEqual(len(surf_mesh), 3, 
                         'wrong number of elements')
        self.assertTrue(all(isinstance(item, np.ndarray) 
                            for item in surf_mesh),
                        'elements are not arrays')
        self.assertTrue(all(item.shape == (num_x, num_y)
                            for item in surf_mesh),
                        'elements are not arrays')


if __name__ == '__main__':
    unittest.main()
