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
import csv
import unittest
from pathlib import Path

import numpy as np
from PySurfSim import exportSurface


class TestUnitExportSurface(unittest.TestCase):
    """ Test Cases for exporting surfaces """
    def setUp(self):
        if Path('test.asc').is_file():
            Path('test.asc').unlink()
            
        self.x_len = 0.001e6
        self.y_len = 0.002e6
        self.z_height = 40.0
        self.res = 100
        
    def tearDown(self):
        if Path('test.asc').is_file():
            Path('test.asc').unlink()
    
    def test_export_surface(self):
        """ test export of surfaces to ASCII """
        x_vec = np.arange(0.0, self.x_len + self.res, self.res)
        y_vec = np.arange(0.0, self.y_len + self.res, self.res)
        surf_mesh = np.meshgrid(x_vec, y_vec)
        surf_mesh.append(np.ones(np.shape(surf_mesh[0])) * self.z_height)

        exportSurface('test.asc', surf_mesh)
        
        self.assertTrue(Path('test.asc').is_file(), 'no file created')
        
        header = []
        rows = []
        r_num = {'x': -1, 'y': -1}
        r_len = {'x': -1.0, 'y': -1.0}
        
        with open('test.asc', 'r', encoding='utf-8') as file:
            csvreader = csv.reader(file, delimiter='\t')
            while True:
                line = next(csvreader)
                header.append(line)
                if line == ['# Start of Data:']:
                    break
                pline = line[0].partition(' = ')
                if pline[0] == '# x-pixels':
                    r_num['x'] = int(pline[-1])
                if pline[0] == '# y-pixels':
                    r_num['y'] = int(pline[-1])
                if pline[0] == '# x-length':
                    r_len['x'] = float(pline[-1])
                if pline[0] == '# y-length':
                    r_len['y'] = float(pline[-1])
            for row in csvreader:
                if row[-1] == '':
                    row = row[:-1]
                rows.append(row)
        surf_mesh_read = np.array(rows).astype(float)
        
        self.assertEqual(self.x_len, r_len['x'], 'wrong xLen')
        self.assertEqual(self.y_len, r_len['y'], 'wrong yLen')
        self.assertEqual(len(x_vec), r_num['x'], 'wrong number of elements (x)')
        self.assertEqual(len(y_vec), r_num['y'], 'wrong number of elements (y)')
        self.assertTrue(np.array_equal(surf_mesh_read, surf_mesh[2]),
                        'z values not equal')
        

if __name__ == '__main__':
    unittest.main()
