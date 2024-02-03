'''
RadioSpectrogram class which handles, plotting, averaging, compute power etc. 
'''

import numpy as np
import pickle
import os
from astropy.io import fits

from src.configs import GLOBAL_CONFIG
from src.configs.tag_maps.tag_to_plotter import tag_to_plotter_dict
from src.utils import DatetimeFuncs, ArrayFuncs

class RadioSpectrogram:
    def __init__(self, Sxx, time_array, freqs_MHz, center_freq, chunk_start_time, tag, **kwargs):
        self.Sxx = Sxx
        #displace so that the first element of the time array is always at 0 seconds
        self.time_array = time_array-time_array[0]
        self.freqs_MHz = freqs_MHz
        self.center_freq = center_freq
        self.chunk_start_time = chunk_start_time
        self.tag = tag

        self.chunk_start_datetime=DatetimeFuncs.strptime(self.chunk_start_time, GLOBAL_CONFIG.default_time_format)
        self.datetime_array = self.build_datetime_array()
        self.datetime64_array = np.array(self.datetime_array,dtype="datetime64[ns]")
        self.data_dir=DatetimeFuncs.build_data_dir_from_chunk_start_time(GLOBAL_CONFIG.path_to_data, self.chunk_start_time)   

        bvect = kwargs.get("bvect", None)
        if bvect is None:
            try:
                self.set_background_vector_from_memory()
            except:
                self.set_background_vector(None)
        else:
            self.set_background_vector(bvect)

    def set_background_vector_from_memory(self, ):
        try:
            self.background_vector = np.load(os.path.join(GLOBAL_CONFIG.path_to_config_data, f"background_vector_{self.tag}.npy"))

        except Exception as e:
            raise SystemError(f"Error loading background vector: {e}")


    def set_background_vector(self, bvect):
        self.background_vector = bvect
    

    def get_path(self):
        return os.path.join(self.data_dir,f"{self.chunk_start_time}_{self.tag}.fits")


    def build_datetime_array(self,):
        return DatetimeFuncs.build_datetime_array(self.chunk_start_datetime,self.time_array)


    def save_to_fits(self):
        # Create a Primary HDU object with the Sxx data
        primary_hdu = fits.PrimaryHDU(self.Sxx)

        # Create a Header Data Unit (HDU) list and add the primary HDU
        hdulist = fits.HDUList([primary_hdu])

        # Add other attributes as headers in the primary HDU
        primary_hdu.header['CFREQ'] = self.center_freq
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
    

    def stack_plots(self, fig, plot_types):
        plotter = tag_to_plotter_dict[self.tag]
        plotter(self).stack_plots(fig, plot_types)


    def integrated_power(self,):
        num_freq_bins = np.shape(self.Sxx)[0]
        num_time_bins = np.shape(self.Sxx)[1]
        dfreq_Hz = (self.freqs_MHz[1]-self.freqs_MHz[0])*10**-6

        integrated_power = np.empty(num_time_bins)
        for i in range(num_time_bins):
            integrated_power[i]=np.sum(self.Sxx[:,i])*dfreq_Hz
        
        dt = self.time_array[1]-self.time_array[0]
        integrated_power/=np.trapz(integrated_power,dx=dt)
        return integrated_power


    def total_time_average(self,):
        return np.nanmean(self.Sxx,-1)