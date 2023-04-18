# -*- coding: utf-8 -*-
"""
Visual test case for apply_mesh_tool_to_workpiece using matplotlib (slow).

Copyright (C) 2023  Lars Schönemann

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
@version: 1.0
@date:    2023-04-18
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import ticker
from matplotlib import cm
from PySurfSim import (MeshToolFlyCut, apply_mesh_tool_to_workpiece,
                       default_parameters, gen_surface_mesh, round_up_to_base)


if __name__ == '__main__':
    # Visual test case
    p = default_parameters().copy()
   
    surf_mesh = gen_surface_mesh(p['lim_x'], p['lim_y'], p['lim_z'], 
                                 p['numpoints'], 
                                 fixed_num_points=p['fixed_num_points'])

    # calculate tool position
    # number of discrete tool positions in X
    numX = np.ceil(p['lim_x'] / p['feed_x']) + 1  
    # number of discrete tool positions in Y
    numY = np.ceil(p['lim_y'] / p['raster_y']) + 1  

    tc_x = np.arange(numX) * p['feed_x'] + p['shift_f']
    tc_y = np.arange(numY) * p['raster_y']
    TC_Z = p['r_fly']
    
    tool_mesh = np.meshgrid(tc_x, tc_y)
    tool_mesh.append(np.ones(np.shape(tool_mesh[0])) * TC_Z)
    
    test_tool = MeshToolFlyCut(**p)
    
    new_mesh = apply_mesh_tool_to_workpiece(surf_mesh, tool_mesh, test_tool)
    
    # plotting from here
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    
    ax.xaxis.set_major_formatter(lambda x, pos: f'{(x/1000):.0f}')
    ax.set_xlabel('x in µm')
    ax.yaxis.set_major_formatter(lambda x, pos: f'{(x/1000):.0f}')
    ax.set_ylabel('y in µm')
    ax.set_zlabel('z in nm')
    ax.set_box_aspect((1,1,0.1))
    ax.plot_surface(new_mesh[0].T, new_mesh[1].T, new_mesh[2].T, 
                    vmin=new_mesh[2].min()*2, cmap=cm.afmhot,
                    rstride=1, cstride=1)
    
    plt.show(block=True)
