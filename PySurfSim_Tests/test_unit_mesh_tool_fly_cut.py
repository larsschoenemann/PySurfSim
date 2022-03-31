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
@version: 1.2
@date:    2022-03-31
"""
import unittest

import numpy as np
import PySurfSim
from PySurfSim import MeshToolFlyCut


class TestMeshToolFlyCut(unittest.TestCase):
    """ Test cases for fly-cutting tool """
    def test(self):
        """ standard test case """
        x_vec = np.arange(0.0, 0.140e6, 100)
        y_vec = np.arange(0.0, 0.210e6, 100)
        surf_mesh = np.meshgrid(x_vec, y_vec)
        
        tool_mesh = MeshToolFlyCut(r_fly=80e6, delta_r_fly=0.1, r_eps=0.8e6)
        
        self.assertIsInstance(tool_mesh, PySurfSim.MeshToolFlyCut)
        
        f_p = tool_mesh.footprint([0.07e6, 0.104e6, 80e6])
        self.assertEqual(np.shape(f_p), (2, 2))

        t_z = tool_mesh.get_z(surf_mesh, [70e3, 104e3, 60e6])
        self.assertEqual(t_z.shape, (210e3 / 100, 140e3 / 100))
        

if __name__ == '__main__':
    unittest.main()
