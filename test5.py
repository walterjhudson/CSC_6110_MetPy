# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 19:07:59 2022

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

def test_get_layer_heights_agl():
    """This function tests the get_layer_heights with having interpolation."""
    heights = np.arange(300, 1200, 100) * units.m
    data = heights.m * 0.1 * units.degC
    heights, data = get_layer_heights(heights, 500 * units.m, data, with_agl=True)
    heights_true = np.array([0, 0.1, 0.2, 0.3, 0.4, 0.5]) * units.km
    data_true = np.array([30, 40, 50, 60, 70, 80]) * units.degC
    assert_array_almost_equal(heights_true, heights, 6)
    assert_array_almost_equal(data_true, data, 6)