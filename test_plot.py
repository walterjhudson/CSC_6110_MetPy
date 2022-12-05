#Reference: https://github.com/Unidata/MetPy/issues/2460
# Tested with a different dataset, figure size and add logo parameters.


import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import pandas as pd
import pytest

import metpy.calc as mpcalc
from metpy.cbook import get_test_data
from metpy.plots import add_metpy_logo, Hodograph, SkewT
from metpy.units import units

def test_skewt_api():

        col_names = ['pressure', 'height', 'temperature', 'dewpoint', 'direction', 'speed']

        df = pd.read_fwf(get_test_data('dec9_sounding.txt', as_file_obj=False),
                        skiprows=5, usecols=[0, 1, 2, 3, 6, 7], names=col_names)

        # Drop any rows with all NaN values for T, Td, winds
        df = df.dropna(subset=('temperature', 'dewpoint', 'direction', 'speed'
                            ), how='all').reset_index(drop=True)

        p = df['pressure'].values * units.hPa
        T = df['temperature'].values * units.degC
        Td = df['dewpoint'].values * units.degC
        wind_speed = df['speed'].values * units.knots
        wind_dir = df['direction'].values * units.degrees
        u, v = mpcalc.wind_components(wind_speed, wind_dir)


        # Create a new figure. The dimensions here give a good aspect ratio
        fig = plt.figure(figsize=(14, 8))
        add_metpy_logo(fig, 1950, 150, size='large')

        #skew = SkewT(fig, aspect='auto')
        skew = SkewT(fig,rotation=45, rect=(0.1, 0.1, 0.55, 0.85))


        # Plot the data using normal plotting functions, in this case using
        # log scaling in Y, as dictated by the typical meteorological plot
        skew.plot(p, T, 'r')
        skew.plot(p, Td, 'g')
        skew.plot_barbs(p, u, v)

        # Change to adjust data limits and give it a semblance of what we want
        skew.ax.set_adjustable('datalim')
        skew.ax.set_ylim(1000, 100)
        skew.ax.set_xlim(-20, 30)

        # Add the relevant special lines
        skew.plot_dry_adiabats()
        skew.plot_moist_adiabats()
        skew.plot_mixing_lines()

        ax = plt.axes((0.7, 0.75, 0.2, 0.2))
        h = Hodograph(ax, component_range=60.)
        h.add_grid(increment=20)
        h.plot(u, v)
        #plt.show()
        return fig
