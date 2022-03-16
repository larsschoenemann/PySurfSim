# -*- coding: utf-8 -*-
"""
Unit test for tool mesh generation.

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
from PySurfSim import meshToolFlyCut


class test_meshToolFlyCut(unittest.TestCase):
    def test(self):
        xVec = np.arange(0.0, 0.140e6, 100)
        yVec = np.arange(0.0, 0.210e6, 100)
        surf_mesh = np.meshgrid(xVec, yVec)
        
        tool_mesh = meshToolFlyCut(surf_mesh, [70e3, 104e3, 60e6],
                                   60e6, 0, 762e3)
        
        self.assertIsInstance(tool_mesh, np.ndarray)
        self.assertEqual(tool_mesh.shape, (210e3 / 100, 140e3 / 100))
        

if __name__ == '__main__':
    unittest.main()
