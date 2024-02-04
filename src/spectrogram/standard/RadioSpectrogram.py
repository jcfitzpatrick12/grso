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

    def save_to_fits(self):
        # Create a Primary HDU object with the Sxx data
        primary_hdu = fits.PrimaryHDU(self.Sxx)

        # Create a Header Data Unit (HDU) list and add the primary HDU
        hdulist = fits.HDUList([primary_hdu])

        primary_hdu.header['PSTIME'] = self.chunk_start_time

        col_time = fits.Column(name='TIME', array=self.time_array, format='D')
        col_freq = fits.Column(name='FREQ', array=self.freqs_MHz, format='D')

        tb_hdu_time = fits.BinTableHDU.from_columns([col_time])
        tb_hdu_freq = fits.BinTableHDU.from_columns([col_freq])

        hdulist.append(tb_hdu_time)
        hdulist.append(tb_hdu_freq)

        #name the path according to the chunk_start_time
        fpath = os.path.join(self.get_path())
        # Write the FITS file
        hdulist.writeto(fpath, overwrite=True)
        pass