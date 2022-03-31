# -*- coding: utf-8 -*-
"""
Helping functions for PySurfSim.

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
from itertools import tee


def round_up_to_base(num, base=10.0):
    """Round a number up to a specified base.

    Args:
        num (float): the number.
        base (float, optional): the base. Defaults to 10.0.

    Returns:
        float: rounded number.
    """
    return num + (base - num) % base


def pairwise(iterable):
    """pairwise('ABCDEFG') --> AB BC CD DE EF FG."""
    el1, el2 = tee(iterable)
    next(el2, None)
    return zip(el1, el2)


def default_parameters():
    """Return default parameters for surface generation."""
    nm = 1.0  #pylint: disable=C0103
    um = 1e3  #pylint: disable=C0103
    mm = 1e6  #pylint: disable=C0103
    
    return {
        'raster_y': 8 * um,   # feed in raster direction in nm
        'feed_x': 70 * um,    # feed in cutting direction in nm
        'r_fly': 60 * mm,     # flycut radius in nm
        'r_eps': 0.762 * mm,  # tool nose radius in nm
        # deviation in flycut radius to nominal value in nm
        'delta_r_fly': 0.0 * nm,   
        # shift of tool in feed direction (necessary for second tool)
        'shift_f': 0.0 * nm,      
        'lim_x': 0.334833 * mm,   # limits of simulated surface in X in nm
        'lim_y': 0.334618 * mm,   # limits of simulated surface in Y in nm
        # initial surface height in nm (less height means less computation 
        # time, as the "footprint" of the flycutter is determined using 
        # this value
        'lim_z': 100.0 * nm,       
        'raster': 100.0 * nm,    # raster spacing of simulated surface
        'numpoints': 1024,  # numer of points
        'fixed_num_points': True,
        'visualize': True}  # do we want to plot the result?
