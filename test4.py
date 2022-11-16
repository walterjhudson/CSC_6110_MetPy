# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 19:07:54 2022

@author: user
"""
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

def test_get_layer_heights_no_interpolation():
    """This function tests the function get_layer_heights without having interpolation."""
    heights = np.arange(10) * units.km
    data = heights.m * 2 * units.degC
    heights, data = get_layer_heights(heights, 5000 * units.m, data,
                                      bottom=1500 * units.m, interpolate=False)
    heights_true = np.array([2, 3, 4, 5, 6]) * units.km
    data_true = heights_true.m * 2 * units.degC
    assert_array_almost_equal(heights_true, heights, 6)
    assert_array_almost_equal(data_true, data, 6)