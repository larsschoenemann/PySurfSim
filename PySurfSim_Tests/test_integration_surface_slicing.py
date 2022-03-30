# -*- coding: utf-8 -*-
"""
Integration test for parallel execution of surface simulation framework.

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
import random
import unittest

import numpy as np
from PySurfSim import combine_surface, gen_surface_mesh, slice_surface


class TestSurfaceSlicing(unittest.TestCase):
    """ Test cases for surface slicing """
    def setUp(self):
        self.surf_mesh = gen_surface_mesh(
            100e3, 75e3, 40.0, 
            (1000, 500), fixed_num_points=False)
    
    def test(self):
        """
        Test if normal and parallel processing yields the same results.
        (First test case with unaltered list)

        Returns
        -------
        None.

        """
        surf_mesh_slices = slice_surface(
            self.surf_mesh, 5, 10)
        combined_mesh = combine_surface(
            surf_mesh_slices, 5, 10)
        
        self.assertTrue(np.array_equal(org_mesh_part, com_mesh_part)
                        for org_mesh_part, com_mesh_part 
                        in zip(self.surf_mesh, combined_mesh))
        
    def test_randomized(self):
        """
        Test if normal and parallel processing yields the same results.
        (Second test case with randomized list)

        Returns
        -------
        None.

        """
        surf_mesh_slices = slice_surface(
            self.surf_mesh, 5, 10)
        # randomize slice order
        surf_mesh_slices = random.sample(surf_mesh_slices, 
                                         k=len(surf_mesh_slices))
        combined_mesh = combine_surface(
            surf_mesh_slices, 5, 10)
        
        self.assertTrue(np.array_equal(org_mesh_part, com_mesh_part)
                        for org_mesh_part, com_mesh_part 
                        in zip(self.surf_mesh, combined_mesh))
        
        
if __name__ == '__main__':
    unittest.main()
