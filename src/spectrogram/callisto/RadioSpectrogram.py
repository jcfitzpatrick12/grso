import numpy as np

from src.spectrogram.BaseSpectrogram import BaseSpectrogram



class RadioSpectrogram(BaseSpectrogram):
    def __init__(self, Sxx, time_array, freqs_MHz, chunk_start_time, tag, **kwargs):
        super().__init__(Sxx, time_array, freqs_MHz, chunk_start_time, tag, **kwargs)
