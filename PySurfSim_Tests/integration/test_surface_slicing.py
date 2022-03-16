# -*- coding: utf-8 -*-
"""
Integration test for parallel execution of surface simulation framework.

Created on Fri Mar  4 13:12:34 2022
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
import random
from PySurfSim import genSurfaceMesh
from PySurfSim import sliceSurface
from PySurfSim import combineSurface


class test_surface_slicing(unittest.TestCase):
    def setUp(self):
        self.surf_mesh = genSurfaceMesh(
            100e3, 75e3, 40.0, 
            (1000, 500), fixedNumPoints=False)
    
    def test(self):
        """
        Test if normal and parallel processing yields the same results.
        (First test case with unaltered list)

        Returns
        -------
        None.

        """
        surf_mesh_slices = sliceSurface(
            self.surf_mesh, 5, 10)
        combined_mesh = combineSurface(
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
        surf_mesh_slices = sliceSurface(
            self.surf_mesh, 5, 10)
        # randomize slice order
        surf_mesh_slices = random.sample(surf_mesh_slices, 
                                         k=len(surf_mesh_slices))
        combined_mesh = combineSurface(
            surf_mesh_slices, 5, 10)
        
        self.assertTrue(np.array_equal(org_mesh_part, com_mesh_part)
                        for org_mesh_part, com_mesh_part 
                        in zip(self.surf_mesh, combined_mesh))
        
        
if __name__ == '__main__':
    unittest.main()
