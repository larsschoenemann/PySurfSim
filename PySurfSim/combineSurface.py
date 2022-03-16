# -*- coding: utf-8 -*-
"""
Combine several patches to a common surface.

Created on Fri Nov 19 13:47:44 2021

@author: Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
"""
import numpy as np


def combineSurface(slicedSurface, xDiv, yDiv):
    """
    Combine several patches to a common surface.

    Parameters
    ----------
    slicedSurface : list of list of numpy arrays
        A list of surface patches (each patch is a list of numpy arrays).
    xDiv : int
        Number of patches in X.
    yDiv : int
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
    if len(slicedSurface) != xDiv * yDiv:
        raise ValueError

    ndim, _, _ = np.shape(slicedSurface[0])
    combinedSurface = list()
    
    # get x and y start points of all slices
    startPointsXY = np.array([(thisslice[0][0, 0], thisslice[1][0, 0]) 
                              for thisslice in slicedSurface])
    # build record for sorting
    r = np.core.records.fromarrays([startPointsXY[:, 0],
                                    startPointsXY[:, 1]], names='a,b')
    # sort slicedSurface list according to sorted record
    slicedSurface[:] = [slicedSurface[i] for i in r.argsort().astype(int)]
    
    for nd in range(ndim):
        dslice = [d[nd] for d in slicedSurface]

        rows = list()  # initialize new list

        for i in range(yDiv):
            # concatenate portion of slided surface
            combined = np.vstack(dslice[i * xDiv:(i + 1) * xDiv])
            rows.append(combined)

        combinedSurface.append(np.hstack(rows))  # combine all rows
    
    return combinedSurface