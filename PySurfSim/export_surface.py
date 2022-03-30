# -*- coding: utf-8 -*-
"""
Export a simulated surface to a SPIP-readable ASCII file.

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

@author: Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
@version: 1.2
@date: 2021-11-08
"""
import numpy as np


def export_surface(filename, surf_mesh):
    """
    Export a simulated surface to a SPIP-readable ASCII file.

    Parameters
    ----------
    filename :  string/path
        filename or path to which the surface shall be exported as ASCII.
    surfMesh : list of meshes
        Meshes of the surface to be exported (X- & Y-meshes plus heights in Z).

    Returns
    -------
    None.

    """
    with open(filename, 'w', newline='\r\n',
              encoding='utf-8') as fid:  # open file for writing
        shape_z = np.shape(surf_mesh)
        # Write header
        fid.write('# File Format = ASCII\n')
        fid.write('# Created by Python\n')
        fid.write('# Original file: \n')
        fid.write('# forcecurve = 0\n')
        # number of pixel in X:
        fid.write(f'# x-pixels = {shape_z[2]}\n')
        # number of pixel in Y:
        fid.write(f'# y-pixels = {shape_z[1]}\n')
        # length in X, i.e. last point of meshX:
        fid.write(f'# x-length = {surf_mesh[0][-1][-1]:0.0f}\n')
        # length in Y, i.e. last point of meshY
        fid.write(f'# y-length = {surf_mesh[1][-1][-1]:0.0f}\n')
        fid.write('# x-offset = 0\n')
        fid.write('# y-offset = 0\n')
        fid.write('# z-unit = nm\n')  # alles values in nm!
        fid.write('# scanspeed = 0\n')
        fid.write('# forcecurve = 0\n')
        fid.write('# voidpixels =0\n')
        fid.write('# description =\n')
        fid.write('Operator:  \n')
        fid.write('# Start of Data:\n')

        # iterate over rows and columns of surface
        for i in range(shape_z[1]):
            for j in range(shape_z[2]):
                # write surface point
                fid.write(f'{surf_mesh[2][i, j]:.8f}\t')

            fid.write('\n')  # write EOL
