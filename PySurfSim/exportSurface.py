# -*- coding: utf-8 -*-
"""
Export a simulated surface to a SPIP-readable ASCII file.

Created on Mon Nov  8 08:48:30 2021

@author: Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
@version: 1.0
@date: 2021-11-08
"""
import numpy as np


def exportSurface(filename, surfMesh):
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
    with open(filename, 'w', newline='\r\n') as fid:  # open file for writing
        shapeZ = np.shape(surfMesh)
        # Write header
        fid.write('# File Format = ASCII\n')
        fid.write('# Created by Python\n')
        fid.write('# Original file: \n')
        fid.write('# forcecurve = 0\n')
        # number of pixel in X:
        fid.write('# x-pixels = {}\n'.format(shapeZ[2]))
        # number of pixel in Y:
        fid.write('# y-pixels = {}\n'.format(shapeZ[1]))
        # length in X, i.e. last point of meshX:
        fid.write('# x-length = {:0.0f}\n'.format(surfMesh[0][-1][-1]))
        # length in Y, i.e. last point of meshY
        fid.write('# y-length = {:0.0f}\n'.format(surfMesh[1][-1][-1]))
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
        for i in range(shapeZ[1]):
            for j in range(shapeZ[2]):
                # write surface point
                fid.write('{:.8f}\t'.format(surfMesh[2][i, j]))

            fid.write('\n')  # write EOL
