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
import unittest
import numpy as np
from timeit import default_timer as timer
from joblib import Parallel, delayed, parallel_backend
# from PySurfSim import genSurfaceMesh, round_up_to_base
from PySurfSim import genSurfaceMesh
from PySurfSim import meshToolFlyCut
from PySurfSim import applyMeshToolToWorkpiece
from PySurfSim import sliceSurface
from PySurfSim import combineSurface


class test_parallel_processing(unittest.TestCase):
    def setUp(self):
        print('Setting up parallel test')
        p = {
            'rasterY': 8 * 1e3,   # feed in raster direction in nm
            'feedX': 70 * 1e3,    # feed in cutting direction in nm
            'rFly': 60 * 1E6,     # flycut radius in nm
            'rEps': 0.762 * 1E6,  # tool nose radius in nm
            # deviation in flycut radius to nominal value in nm
            'deltaRfly': 0.0,   
            # shift of tool in feed direction (necessary for second tool)
            'shiftF': 0.0,      
            'limX': 0.334833e6,   # limits of simulated surface in X in nm
            'limY': 0.334618e6,   # limits of simulated surface in Y in nm
            # initial surface height in nm (less height means less computation 
            # time, as the "footprint" of the flycutter is determined using 
            # this value
            'limZ': 100.0,       
            'raster': 100.0,    # raster spacing of simulated surface
            'numpoints': 1024,  # numer of points
            'fixedNumPoints': True,
            'visualize': True}  # do we want to plot the result?
        self.p = p
        print(p)
        self.n_jobs = 8
        print(f'Parallel jobs {self.n_jobs}')
        
        self.surf_mesh = genSurfaceMesh(
            p['limX'], p['limY'], p['limZ'], 
            p['numpoints'], fixedNumPoints=p['fixedNumPoints'])
        
        # calculate tool position
        # number of discrete tool positions in X
        numX = np.ceil(p['limX'] / p['feedX']) + 1  
        # number of discrete tool positions in Y
        numY = np.ceil(p['limY'] / p['rasterY']) + 1  

        toolCenterX = np.arange(numX) * p['feedX'] + p['shiftF']
        toolCenterY = np.arange(numY) * p['rasterY']
        toolCenterZ = p['rFly']
        
        # tool_mesh = np.meshgrid(toolCenterX, toolCenterY, toolCenterZ)
        self.tool_mesh = np.meshgrid(toolCenterX, toolCenterY)
        self.tool_mesh.append(
            np.ones(np.shape(self.tool_mesh[0])) * toolCenterZ)
        
        self.tool = meshToolFlyCut(**p)
    
    def test(self):
        """
        Test if normal and parallel processing yields the same results.

        Returns
        -------
        None.

        """
        # %% normal execution
        print('Calculating normally')
        start_time_normal = timer()
        new_mesh_normal = applyMeshToolToWorkpiece(self.surf_mesh, 
                                                   self.tool_mesh, 
                                                   self.tool)
        end_time_normal = timer()
        dt_normal = end_time_normal - start_time_normal
        print(f'Normal execution: {dt_normal:.2f} s')
        
        # %% parallel execution
        print('Calculating in parallel')
        start_time_parallel = timer()
        surf_mesh_slices = sliceSurface(
            self.surf_mesh, self.n_jobs, self.n_jobs)
        new_mesh_slices = []
        with parallel_backend('loky', n_jobs=self.n_jobs):
            new_mesh_slices = Parallel()(delayed(applyMeshToolToWorkpiece)(
                surf_mesh_slice, self.tool_mesh, self.tool) 
                for surf_mesh_slice in surf_mesh_slices)
        new_mesh_parallel = combineSurface(
            new_mesh_slices, self.n_jobs, self.n_jobs)
        
        end_time_parallel = timer()
        dt_parallel = end_time_parallel - start_time_parallel
        print(f'Parallel execution: {dt_parallel:.2f} s')
        
        # %% Test Case
        for submesh_normal, submesh_parallel, sub_dir in zip(
                new_mesh_normal, new_mesh_parallel, ['x', 'y', 'z']):
            self.assertTrue(np.array_equal(submesh_normal, submesh_parallel))
        
        
if __name__ == '__main__':
    unittest.main()
