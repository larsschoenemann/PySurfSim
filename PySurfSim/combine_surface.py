# -*- coding: utf-8 -*-
"""
Combine several patches to a common surface.

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
@date:    2022-03-31
"""
import numpy as np


def combine_surface(sliced_surface, x_div, y_div):
    """
    Combine several patches to a common surface.

    Parameters
    ----------
    sliced_surface : list of list of numpy arrays
        A list of surface patches (each patch is a list of numpy arrays).
    x_div : int
        Number of patches in X.
    y_div : int
        Number of patches in Y.

    Raises
    ------
    ValueError
        Dimension mismatch between the number of slices and the dimensions 
        provided.

    Returns
    -------
    combinedSurface : list of numpy arrays
        The combined surface (meshes for X and Y and Z heights).


    (c)2021,
    Dr.-Ing. Lars Schoenemann, schoenemann@iwt-bremen.de,
    Leibniz Institute for Materials Engineering IWT, Bremen, Germany
    v1.0, 2021-10-21: initial release
    v1.1, 2022-03-15: sort list before combination to avoid concurrency issues
    """
    if len(sliced_surface) != x_div * y_div:
        raise ValueError

    ndim, _, _ = np.shape(sliced_surface[0])
    combined_surface = list()
    
    # get x and y start points of all slices
    start_points_xy = np.array([(thisslice[0][0, 0], thisslice[1][0, 0]) 
                               for thisslice in sliced_surface])
    # build record for sorting
    record = np.core.records.fromarrays([start_points_xy[:, 0],
                                      start_points_xy[:, 1]], names='a,b')
    # sort sliced_surface list according to sorted record
    sliced_surface[:] = [sliced_surface[i] 
                        for i in record.argsort().astype(int)]
    
    for k in range(ndim):
        dslice = [d[k] for d in sliced_surface]

        rows = []  # initialize new list

        for i in range(y_div):
            # concatenate portion of slided surface
            combined = np.vstack(dslice[i * x_div:(i + 1) * x_div])
            rows.append(combined)

        combined_surface.append(np.hstack(rows))  # combine all rows
    
    return combined_surface
