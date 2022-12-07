import numpy as np
import xarray as xr

from metpy.interpolate import interpolate_to_slice
from metpy.units import units

data_temp = np.linspace(250, 300, 5 * 6 * 7).reshape((5, 6, 7)) * units.kelvin

ds = xr.Dataset(
        {
            'temperature': (['isobaric', 'lat', 'lon'], data_temp),
        },
        coords={
            'isobaric': xr.DataArray(
                np.linspace(1000, 500, 5),
                name='isobaric',
                dims=['isobaric'],
                attrs={'units': 'hPa'}
            ),
            'lat': xr.DataArray(
                np.linspace(30, 45, 6),
                name='lat',
                dims=['lat'],
                attrs={'units': 'degrees_north'}
            ),
            'lon': xr.DataArray(
                np.linspace(255, 275, 7),
                name='lon',
                dims=['lon'],
                attrs={'units': 'degrees_east'}
            )
        }
    )

data = ds.metpy.parse_cf()['temperature']

path = np.array([[10.0, 30.],
                    [30.0, 40.],
                    [40.0, 30.],
                    [45.0, 30.]])
test_slice = interpolate_to_slice(data, path)
print("Distance : ")
print(test_slice["distance"].data)
