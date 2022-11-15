## Reference
## https://github.com/Unidata/MetPy
#Made changes in the function inputs and expected output and more assertions

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import numpy.ma as ma
import pytest
import xarray as xr
from collections import namedtuple
from pyproj import Geod


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

from metpy.testing import assert_array_almost_equal, assert_array_equal, assert_nan
from metpy.units import *
from metpy.units import (check_units, concatenate,
                         pandas_dataframe_to_unit_arrays, units)

FULL_CIRCLE_DEGREES = np.arange(0, 360, BASE_DEGREE_MULTIPLIER.m) * units.degree

def test_Nan_removal():
    #Tested the two implications of removing Nan in an array
    p = np.array([1, 2, np.nan, 3, 4, 5, 6, np.nan])
    q = np.arange(0, len(p))
    i = np.array([1, 2, 3])
    j = np.arange(0, len(i))
    i_test, j_test = _remove_nans(i, j)
    q_test, p_test = _remove_nans(q, p)
    p_expected = np.array([1, 2, 3, 4, 5, 6])
    q_expected = np.array([0, 1, 2, 3, 4, 5])
    i_expected = np.array([1, 2, 3])
    j_expected = np.array([0, 1, 2])
    assert_array_almost_equal(p_expected, p_test, 0)
    assert_almost_equal(q_expected, q_test, 0)
    assert_array_almost_equal(i_expected, i_test,0)
    assert_almost_equal(j_expected, j_test,0)



def test_invalid_bound_units():
    #Test invalid bound units as well as when the height is out of bound
    p = np.arange(20, 57, 100) * units.hPa
    h = np.arange(1, 9) * units.kilometer
    with pytest.raises(ValueError):
        _get_bound_pressure_height(p, 100 * units.meter)
    with pytest.raises(ValueError):
        _get_bound_pressure_height(p, 8 * units.kilometer, height=h)
    with pytest.raises(ValueError):
        _get_bound_pressure_height(p, 100 * units.meter, height=h)
    

def test_all_level_direction_angle():
    #Test array of angles in degree based on the different levels#
    desired_output1 =[
        'N', 'N', 'N', 'E', 'E', 'E', 'E', 'S', 'S', 'S', 'S',
        'W', 'W', 'W', 'W', 'N']
    desired_output2 = [
        'N', 'N', 'NE', 'NE', 'E', 'E', 'SE', 'SE',
       'S', 'S', 'SW', 'SW', 'W', 'W', 'NW', 'NW'
    ]
    desired_output3 =[
        'N', 'NNE', 'NE', 'ENE',
    'E', 'ESE', 'SE', 'SSE',
    'S', 'SSW', 'SW', 'WSW',
    'W', 'WNW', 'NW', 'NNW']
    output1 = angle_to_direction(FULL_CIRCLE_DEGREES, level=1)
    assert_array_equal(output1, desired_output1)
    output2 = angle_to_direction(FULL_CIRCLE_DEGREES, level=2)
    assert_array_equal(output2, desired_output2)
    output3 = angle_to_direction(FULL_CIRCLE_DEGREES, level=3)
    assert_array_equal(output3,desired_output3)


def test_delete_points_with_mask():
    """Test to delete masked points from array for easy calculation"""
    i = ma.masked_array(np.arange(8), mask=[True, True, False, True, False, False, False, False])
    j = ma.masked_array(np.arange(8), mask=[True, True, False, True, False, False, True, False])
    desired_output = np.array([2, 4, 5, 7)
    i, j = _delete_masked_points(i, j)
    assert_array_equal(i, desired_output)
    assert_array_equal(j, desired_output)


def test_value_unit_concatenation():
    #Test to check if the unit attached to an array is proper for cocatenation.
    result = concatenate((67.8 * units.inches, 78.5*units.inches))
    result1= concatenate((35 , 50 *units.inches))
    assert_array_equal(result, np.array([67.8, 78.5]) * units.inches)
    assert not isinstance(result.m, np.ma.MaskedArray)
    assert_array_equal(result1, np.array([35, 50]) * units.inches)
    assert not isinstance(result1.m, np.ma.MaskedArray)

    

def test_is_quantity():
    #Test if an array is a quantity
    assert is_quantity(np.array([4.]) * units.degree)
    assert not is_quantity(np.arraynp.array([4.]))