"""
SuperPlots Generator
====================
A Python tool for generating SuperPlots to visualize cell biology data
with proper statistical representation of biological replicates.

Author: Christina (牧濑红莉栖)
License: MIT
"""

from .core import SuperPlot
from .statistics import StatisticalTest
from .visualization import plot_superplot

__version__ = "0.1.0"
__author__ = "Christina"

__all__ = ["SuperPlot", "StatisticalTest", "plot_superplot"]