'''
RadioSpectrogram class which handles, plotting, averaging, compute power etc. 
'''

import numpy as np
import pickle
import os
from astropy.io import fits
from datetime import timedelta

from src.fPlotting.SpectrogramPlotter import SpectrogramPlotter
from src.fConfig import CONFIG
from src.utils import DatetimeFuncs 

import matplotlib.pyplot as plt 

class RadioSpectrogram:
    '''
    constructor functions
    '''
    def __init__(self, Sxx, time_array, freqs_MHz, center_freq, pseudo_start_time,is_averaged):
        self.Sxx = Sxx
        #displace so that the first element of the time array is at 0 seconds
        self.time_array = time_array-time_array[0]
        self.freqs_MHz = freqs_MHz
        self.center_freq = center_freq
        self.is_averaged = is_averaged

        self.pseudo_start_time = pseudo_start_time
        self.pseudo_start_datetime=DatetimeFuncs.parse_datetime(self.pseudo_start_time)
        self.datetime_array = self.build_datetime_array()
        self.datetime64_array = np.array(self.datetime_array,dtype="datetime64[ns]")
        self.power = self.build_power()
        self.data_dir=DatetimeFuncs.build_data_dir_from_pseudo_start_time(self.pseudo_start_time)


    def build_datetime_array(self,):
        #convert the times into datetimes
        return DatetimeFuncs.build_datetime_array(self.pseudo_start_datetime,self.time_array)
    '''
    returns a vector of length (len(freqs_MHz)) so that each element is the time average over that frequency bin
    of the entire spectrogram
    '''

    def total_time_average(self,):
        return np.nanmean(self.Sxx,-1)

    def build_power(self):
        num_freq_bins = np.shape(self.Sxx)[0]
        num_time_bins = np.shape(self.Sxx)[1]
        power = np.empty(num_time_bins)
        dfreq_Hz = (self.freqs_MHz[1]-self.freqs_MHz[0])*10**-6
        for i in range(num_time_bins):
            power[i]=np.sum(self.Sxx[:,i])*dfreq_Hz
        
        dt = self.time_array[1]-self.time_array[0]
        power/=np.trapz(power,dx=dt)
        return power

    '''
    file functions
    '''
    #find the path to temporary_data
    def get_temp_data_path(self):
        return os.path.join(CONFIG.path_to_temp_data,self.pseudo_start_time)
    
    #find the path to data
    def get_path(self):
        return os.path.join(self.data_dir,self.pseudo_start_time)

    def save_self(self):
        # Serialize the instance to bytes using pickle
        serialized_instance = pickle.dumps(self)
        # Convert the byte stream to a NumPy uint8 array
        instance_array = np.frombuffer(serialized_instance, dtype=np.uint8)
        np.save(self.get_path(), instance_array)

    def save_to_fits(self):
        # Create a Primary HDU object with the Sxx data
        primary_hdu = fits.PrimaryHDU(self.Sxx)

        # Create a Header Data Unit (HDU) list and add the primary HDU
        hdulist = fits.HDUList([primary_hdu])

        # Add other attributes as headers in the primary HDU
        primary_hdu.header['CFREQ'] = self.center_freq
        primary_hdu.header['PSTIME'] = self.pseudo_start_time
        primary_hdu.header['ISAVR'] = self.is_averaged

        col_time = fits.Column(name='TIME', array=self.time_array, format='D')
        col_freq = fits.Column(name='FREQ', array=self.freqs_MHz, format='D')

        tb_hdu_time = fits.BinTableHDU.from_columns([col_time])
        tb_hdu_freq = fits.BinTableHDU.from_columns([col_freq])

        hdulist.append(tb_hdu_time)
        hdulist.append(tb_hdu_freq)

        #name the path according to the pseudo_start_time
        fpath = os.path.join(self.get_path()+".fits")
        # Write the FITS file
        hdulist.writeto(fpath, overwrite=True)
        pass

    '''
    factory functions
    '''

    def chop(self,start_str,end_str):
        #parse the strings into datetimes
        start_dt = DatetimeFuncs.parse_datetime(start_str)
        end_dt = DatetimeFuncs.parse_datetime(end_str)
        #find the index of the nearest matching datetime elements in the array
        startIndex = DatetimeFuncs.find_closest_index(start_dt,self.datetime_array)
        endIndex = DatetimeFuncs.find_closest_index(end_dt,self.datetime_array)

        #if our start and end indices are identical, the requested range is entirely outwith the RadioSpectrom
        #return the default null spectrogram
        if startIndex==endIndex:
            raise SystemError("Start and end indices are equal! Cannot chop.")
        #chop the spectrogram and time values accordinglys
        chopped_Sxx=self.Sxx[:,startIndex:endIndex]
        chopped_timeArray = self.time_array[startIndex:endIndex+1]
        #translate the chopped_timeArray to again start at zero.
        chopped_timeArray-=chopped_timeArray[0]
        #extract the new pseudo_start_time
        chopped_pseudo_start_time = DatetimeFuncs.to_string(self.datetime_array[startIndex])
        #return the chopped RadioSpectrogram
        return RadioSpectrogram(chopped_Sxx,chopped_timeArray,self.freqs_MHz,self.center_freq,chopped_pseudo_start_time,self.is_averaged)


    '''
    function which RETURNS the average spectrogram, and (necessarily) decimated timeArray
    '''

    def to_dBb(self,background_vector):
        Sxx_dBb=SpectrogramFuncs.Sxx_to_dBb(self.Sxx)
        return RadioSpectrogram(Sxx_dBb,self.time_array, self.freqs_MHz, self.center_freq, self.pseudo_start_time, self.is_averaged)


    def time_average(self,average_over_int):
        if average_over_int==1:
            return self
        #find the number of frequenct samples
        num_freq_samples = np.shape(self.Sxx)[0]
        #find the number of temporal samples
        num_temporal_samples = np.shape(self.Sxx)[1]
        #print(num_temporal_samples)
        #eshorten the call of how many samples to average over
        N=average_over_int
        #find the remainder [we will average over the remaining samples if N does note exactly divide num_temporal_samples]
        remainder = num_temporal_samples % N
        
        #find the number of temporal_samples_after averaging
        num_temporal_samples_after_averaging = num_temporal_samples//N
        
        #if the remainder is non-zero, introduce a final term which we will handle uniquely [average over the remaining terms]
        if remainder:
            num_temporal_samples_after_averaging+=1

        #instantiate an array to hold the averaged spectrogram
        average_Sxx = np.empty((num_freq_samples,num_temporal_samples_after_averaging))

        #create an array to hold the decimated datetime array
        time_array_decimated = []

        #loop through the spectrogram and average the columns
        for i in range(num_temporal_samples_after_averaging):
            average_Sxx[:,i] = np.mean(self.Sxx[:,N*i:N*i+N],axis=1)
            time_array_decimated.append(self.time_array[i*N])
        
        #add the final bin edge for the decimated time array
        dt = time_array_decimated[-2]-time_array_decimated[-3]
        time_array_decimated.append(time_array_decimated[-1]+dt)

        #if there is a non-zero remainder, just cut the final entry
        if remainder:
            #average_Sxx[:,-1] = np.nanmean(self.Sxx[:,-remainder:],axis=1)
            average_Sxx=average_Sxx[:,:-1]
            time_array_decimated=time_array_decimated[:-1]
        return RadioSpectrogram(average_Sxx,time_array_decimated,self.freqs_MHz,self.center_freq,self.pseudo_start_time,True)
    

    '''
    Plotting functions
    '''

    # def plot_spectrogram(self,**kwargs):
    #     plot_type = kwargs.get("plot_type", None)
    #     if not plot_type:
    #         raise ValueError(f"Specify plot type to be one of {Plotter().spectrogram_plot_type}")
    #     plot_spectrogram = Plotter().get_plot_spectrogram_func(plot_type)
    #     plot_spectrogram(self.freqs_MHz,self.datetime_array,self.Sxx)
    #     pass

    # def plot_power(self):
    #     Plotter().plot_power(self.datetime_array,self.power)
    #     pass

    def stack_plots(self,plot_types,**kwargs):
        SpectrogramPlotter(self).stack_plots(plot_types,**kwargs)