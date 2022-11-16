# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 15:51:35 2022

@author: user
"""

#importing the libraries to be used:

from collections import namedtuple

import numpy as np
import numpy.ma as ma
import pandas as pd
from pyproj import Geod
import pytest
import xarray as xr

from metpy.calc import (angle_to_direction, find_bounding_indices, find_intersections,
                        first_derivative, get_layer, get_layer_heights, gradient, laplacian,
                        lat_lon_grid_deltas, nearest_intersection_idx, parse_angle,
                        pressure_to_height_std, reduce_point_density, resample_nn_1d,
                        second_derivative)
from metpy.calc.tools import (_delete_masked_points, _get_bound_pressure_height,
                              _greater_or_close, _less_or_close, _next_non_masked_element,
                              _remove_nans, azimuth_range_to_lat_lon, BASE_DEGREE_MULTIPLIER,
                              DIR_STRS, UND)
from metpy.testing import assert_almost_equal, assert_array_almost_equal, assert_array_equal
from metpy.units import units
from metpy.xarray import grid_deltas_from_dataarray

def test_less_or_close():
    """This function tests the floating point amount which is close or less than the amount determined."""
    a = np.array([0.1, 1.2, 1.59999, 1.6, 1.4000, 1.7])
    value_for_comparisson = 1.5
    truth = np.array([True, True, False, False, True, False])
    result = _less_or_close(a, value_for_comparisson)
    assert_array_equal(result, truth)
    
    
    
    