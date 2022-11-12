import warnings

import matplotlib
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt
import numpy as np
import pytest

from metpy.plots import Hodograph, SkewT
from metpy.units import units

def test_skewt_tight_bbox():

    fig = plt.figure(figsize=(8, 14))
    SkewT(fig)
    return fig

def test_skewt_subplot():

    fig = plt.figure(figsize=(9, 12))
    SkewT(fig, subplot=(4, 3, 1))
    return fig
def test_skewt_gridspec():

    fig = plt.figure(figsize=(9, 12))
    gs = GridSpec(5, 2)
    SkewT(fig, subplot=gs[0, 1])
    return fig
def test_skewt_arbitrary_rect():

    fig = plt.figure(figsize=(9, 12))
    SkewT(fig, rect=(0.1, 0.1, 0.55, 0.85))
    return fig

def test_hodograph_range_with_units():
    """Tests making a hodograph with a range with units."""
    fig = plt.figure(figsize=(12, 4))
    ax = fig.add_subplot(4, 3, 1)
    Hodograph(ax, component_range=30. * units.knots)

def test_skewt_with_grid_enabled():
    with plt.rc_context(rc={'axes.grid': False}):
        SkewT()
