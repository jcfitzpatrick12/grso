from src.spectrogram.BaseSpectrogram import BaseSpectrogram
import numpy as np
import pickle
import os
from astropy.io import fits

from src.configs import GLOBAL_CONFIG
from src.configs.tag_maps.tag_to_plotter import tag_to_plotter_dict
from src.utils import DatetimeFuncs, ArrayFuncs

class RadioSpectrogram(BaseSpectrogram):
    def __init__(self, Sxx, time_array, freqs_MHz, chunk_start_time, tag, **kwargs):
        super().__init__(Sxx, time_array, freqs_MHz, chunk_start_time, tag, **kwargs)
