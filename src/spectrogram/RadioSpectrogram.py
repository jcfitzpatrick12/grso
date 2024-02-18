import numpy as np
import os

from src.configs import GLOBAL_CONFIG
from src.utils import DatetimeFuncs
from src.spectrogram.Stacker import Stacker
from src.spectrogram.Fits import Fits

class RadioSpectrogram:
    def __init__(self, Sxx, time_array, freqs_MHz, chunk_start_time, tag, **kwargs):
        self.Sxx = Sxx
        #displace so that the first element of the time array is always at 0 seconds
        self.time_array = time_array-time_array[0]
        self.freqs_MHz = freqs_MHz
        self.chunk_start_time = chunk_start_time
        self.tag = tag

        self.chunk_start_datetime = DatetimeFuncs.strptime(self.chunk_start_time, GLOBAL_CONFIG.default_time_format)
        self.datetime_array = self.build_datetime_array()
        self.datetime64_array = np.array(self.datetime_array,dtype="datetime64[ns]")
        self.data_dir=DatetimeFuncs.build_data_dir_from_chunk_start_time(GLOBAL_CONFIG.path_to_data, self.chunk_start_time) 

        bvect = kwargs.get("bvect", None)
        if bvect is None:
            try:
                self.set_bvect_from_memory()
            except:
                self.set_bvect(None)
        else:
            self.set_bvect(bvect)


    def set_bvect_from_memory(self):
        try:
            self.bvect = np.load(os.path.join(GLOBAL_CONFIG.path_to_config_data, f"bvect_{self.tag}.npy"))
        except Exception as e:
            raise SystemError(f"Error loading bvect: {e}")


    def set_bvect(self, bvect):
        self.bvect = bvect
    

    def get_path(self):
        return os.path.join(self.data_dir,f"{self.chunk_start_time}_{self.tag}.fits")


    def build_datetime_array(self,):
        return DatetimeFuncs.build_datetime_array(self.chunk_start_datetime,self.time_array)
    

    def stack_plots(self, fig, plot_types):
        Stacker(self).stack_plots(fig, plot_types)


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
    

    def save_to_fits(self):
        if self.tag in GLOBAL_CONFIG.reserved_tags:
            print(f"Warning! Cannot modify fits for the reserved tag: {tag}. File remains unchanged: {self.get_path}")
            return 
        else:
            fits = Fits()
            fits.save_spectrogram(self, self.get_path())
            print(f".fits file created at {self.get_path()}")