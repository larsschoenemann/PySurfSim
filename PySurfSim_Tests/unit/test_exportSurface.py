# -*- coding: utf-8 -*-
"""
Test for surface mesh generation.

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
from PySurfSim import exportSurface
from pathlib import Path


class test_genSurfaceMesh(unittest.TestCase):
    def setUp(self):
        if Path('test.asc').is_file():
            Path('test.asc').unlink()
            
        self.xLen = 0.001e6
        self.yLen = 0.002e6
        self.zHei = 40.0
        self.res = 100
        
    def tearDown(self):
        if Path('test.asc').is_file():
            Path('test.asc').unlink()
    
    def test(self):
        xVec = np.arange(0.0, self.xLen + self.res, self.res)
        yVec = np.arange(0.0, self.yLen + self.res, self.res)
        surf_mesh = np.meshgrid(xVec, yVec)
        surf_mesh.append(np.ones(np.shape(surf_mesh[0])) * self.zHei)

        exportSurface('test.asc', surf_mesh)
        
        self.assertTrue(Path('test.asc').is_file(), 'no file created')
        
        import csv
        header = []
        rows = []
        r_numX = -1
        r_numY = -1
        r_xLen = -1.0
        r_yLen = -1.0
        with open('test.asc', 'r') as file:
            csvreader = csv.reader(file, delimiter='\t')
            while True:
                line = next(csvreader)
                header.append(line)
                if line == ['# Start of Data:']:
                    break
                pline = line[0].partition(' = ')
                if pline[0] == '# x-pixels':
                    r_numX = int(pline[-1])
                if pline[0] == '# y-pixels':
                    r_numY = int(pline[-1])
                if pline[0] == '# x-length':
                    r_xLen = float(pline[-1])
                if pline[0] == '# y-length':
                    r_yLen = float(pline[-1])
            for row in csvreader:
                if row[-1] == '':
                    row = row[:-1]
                rows.append(row)
        surf_mesh_read = np.array(rows).astype(float)
        
        self.assertEqual(self.xLen, r_xLen, 'wrong xLen')
        self.assertEqual(self.yLen, r_yLen, 'wrong yLen')
        self.assertEqual(len(xVec), r_numX, 'wrong number of elements (x)')
        self.assertEqual(len(yVec), r_numY, 'wrong number of elements (y)')
        self.assertTrue(np.array_equal(surf_mesh_read, surf_mesh[2]),
                        'z values not equal')
        

if __name__ == '__main__':
    unittest.main()
