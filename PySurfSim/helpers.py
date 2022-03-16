# -*- coding: utf-8 -*-
"""
Helping functions.

Created on Fri Nov 19 13:51:51 2021

@author: Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
"""
from itertools import tee


def round_up_to_base(x, base=10):
    """
    Round a number up to a specified base.

    Parameters
    ----------
    x : float
        the number.
    base : float, optional
        the base. The default is 10.

    Returns
    -------
    float
        rounded number.

    """
    return x + (base - x) % base


def pairwise(iterable):
    """pairwise('ABCDEFG') --> AB BC CD DE EF FG."""
    el1, el2 = tee(iterable)
    next(el2, None)
    return zip(el1, el2)


def default_parameters():
    """Return default parameters for surface generation."""
    nm = 1.0
    um = 1e3
    mm = 1e6
    
    p = {'rasterY': 8 * um,   # feed in raster direction in nm
         'feedX': 70 * um,    # feed in cutting direction in nm
         'rFly': 60 * mm,     # flycut radius in nm
         'rEps': 0.762 * mm,  # tool nose radius in nm
         # deviation in flycut radius to nominal value in nm
         'deltaRfly': 0.0 * nm,   
         # shift of tool in feed direction (necessary for second tool)
         'shiftF': 0.0 * nm,      
         'limX': 0.334833 * mm,   # limits of simulated surface in X in nm
         'limY': 0.334618 * mm,   # limits of simulated surface in Y in nm
         # initial surface height in nm (less height means less computation 
         # time, as the "footprint" of the flycutter is determined using 
         # this value
         'limZ': 100.0 * nm,       
         'raster': 100.0 * nm,    # raster spacing of simulated surface
         'numpoints': 1024,  # numer of points
         'fixedNumPoints': True,
         'visualize': True}  # do we want to plot the result?
