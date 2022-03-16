# -*- coding: utf-8 -*-
"""
Unit test for tool footprint determination.

Created on Mon Mar 14 13:18:59 2022
All rights reserved.

@author:  Dr.-Ing. Lars Schönemann
@contact: schoenemann@iwt.uni-bremen.de
@address: LFM Laboratory for Precision Machining
          Leibniz-Institut für Werkstofforientierte Technologien IWT
          Badgasteiner Straße 2
          28359 Bremen
          Germany
"""
import unittest
from PySurfSim import getToolFootprint


class test_getToolFootprint(unittest.TestCase):
    def test(self):
        xLim, yLim = getToolFootprint(tool_pos={'x': 70000.0,
                                                'y': 104000.0,
                                                'z': 60000000.0},
                                      rFly=60 * 1E6,
                                      deltaRfly=0.0,
                                      rEps=0.762 * 1E6)
        
        self.assertIsInstance(xLim, tuple)
        self.assertIsInstance(yLim, tuple)


if __name__ == '__main__':
    unittest.main()
