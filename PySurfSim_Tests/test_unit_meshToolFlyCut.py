# -*- coding: utf-8 -*-
"""
Unit test for tool mesh generation.

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
import PySurfSim
from PySurfSim import meshToolFlyCut



class test_meshToolFlyCut(unittest.TestCase):
    def test(self):
        xVec = np.arange(0.0, 0.140e6, 100)
        yVec = np.arange(0.0, 0.210e6, 100)
        surf_mesh = np.meshgrid(xVec, yVec)
        
        tool_mesh = meshToolFlyCut(rFly=80e6, deltaRfly=0.1, rEps=0.8e6)
        
        self.assertIsInstance(tool_mesh, PySurfSim.meshToolFlyCut)
        
        fp = tool_mesh.footprint([0.07e6, 0.104e6, 80e6])
        self.assertEqual(np.shape(fp), (2, 2))

        tz = tool_mesh.getZ(surf_mesh, [70e3, 104e3, 60e6])
        self.assertEqual(tz.shape, (210e3 / 100, 140e3 / 100))
        

if __name__ == '__main__':
    unittest.main()
