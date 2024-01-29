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
from src.utils import DatetimeFuncs, ArrayFuncs

import matplotlib.pyplot as plt 

class RadioSpectrogram:
    '''
    constructor functions
    '''

    def __init__(self, Sxx, time_array, freqs_MHz, center_freq, chunk_start_time, tag, **kwargs):
        self.Sxx = Sxx
        #displace so that the first element of the time array is at 0 seconds
        self.time_array = time_array-time_array[0]
        self.freqs_MHz = freqs_MHz
        self.center_freq = center_freq
        self.chunk_start_time = chunk_start_time
        self.tag = tag

        self.chunk_start_datetime=DatetimeFuncs.strptime(self.chunk_start_time, CONFIG.default_time_format)
        self.datetime_array = self.build_datetime_array()
        self.datetime64_array = np.array(self.datetime_array,dtype="datetime64[ns]")
        self.data_dir=DatetimeFuncs.build_data_dir_from_chunk_start_time(CONFIG.path_to_data, self.chunk_start_time)

        self.set_power()    
        #note, if this radiospectrogram was generated via frequency averaging or chopping, we no longer want to load the background
        #vector from memory.
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
            self.background_vector = np.load(os.path.join(CONFIG.path_to_background_data, f"background_vector_{self.tag}.npy"))

        except Exception as e:
            raise SystemError(f"Error loading background vector: {e}")

    def set_background_vector(self, bvect):
        self.background_vector = bvect

    def set_power(self):
        num_freq_bins = np.shape(self.Sxx)[0]
        num_time_bins = np.shape(self.Sxx)[1]
        power = np.empty(num_time_bins)
        dfreq_Hz = (self.freqs_MHz[1]-self.freqs_MHz[0])*10**-6
        for i in range(num_time_bins):
            power[i]=np.sum(self.Sxx[:,i])*dfreq_Hz
        
        dt = self.time_array[1]-self.time_array[0]
        power/=np.trapz(power,dx=dt)
        self.power = power

    
    def total_time_average(self,):
        return np.nanmean(self.Sxx,-1)


    def build_datetime_array(self,):
        #convert the times into datetimes
        return DatetimeFuncs.build_datetime_array(self.chunk_start_datetime,self.time_array)


    #find the path to temporary_data
    def get_temp_data_path(self):
        return os.path.join(CONFIG.path_to_temp_data,self.chunk_start_time)
    
    #find the path to data
    def get_path(self):
        return os.path.join(self.data_dir,f"{self.chunk_start_time}_{self.tag}.fits")

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
        primary_hdu.header['PSTIME'] = self.chunk_start_time

        col_time = fits.Column(name='TIME', array=self.time_array, format='D')
        col_freq = fits.Column(name='FREQ', array=self.freqs_MHz, format='D')

        tb_hdu_time = fits.BinTableHDU.from_columns([col_time])
        tb_hdu_freq = fits.BinTableHDU.from_columns([col_freq])

        hdulist.append(tb_hdu_time)
        hdulist.append(tb_hdu_freq)

        #name the path according to the chunk_start_time
        fpath = os.path.join(self.get_path()+".fits")
        # Write the FITS file
        hdulist.writeto(fpath, overwrite=True)
        pass

    '''
    factory functions
    '''

    def frequency_chop(self, start_freq_MHz, end_freq_MHz):
        #find the index of the nearest matching datetime elements in the array
        startIndex = ArrayFuncs.find_closest_index(start_freq_MHz,self.freqs_MHz)
        endIndex = ArrayFuncs.find_closest_index(end_freq_MHz,self.freqs_MHz)

        if startIndex>endIndex:
            startIndex, endIndex = endIndex, startIndex
            
        chopped_Sxx=self.Sxx[startIndex:endIndex, :]
        chopped_freqs_MHz = self.freqs_MHz[startIndex:endIndex+1]
        bvect_chopped = self.background_vector[startIndex:endIndex+1]
        #return the chopped RadioSpectrogram
        return RadioSpectrogram(chopped_Sxx, self.time_array, chopped_freqs_MHz, self.center_freq, self.chunk_start_time, self.tag, bvect = bvect_chopped)
        
    def time_chop(self,start_str,end_str):
        #parse the strings into datetimes
        start_dt = DatetimeFuncs.strptime(start_str, CONFIG.default_time_format)
        end_dt = DatetimeFuncs.strptime(end_str, CONFIG.default_time_format)
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
        #extract the new chunk_start_time
        chopped_chunk_start_time = DatetimeFuncs.to_string(self.datetime_array[startIndex])
        #return the chopped RadioSpectrogram
        return RadioSpectrogram(chopped_Sxx,chopped_timeArray,self.freqs_MHz,self.center_freq,chopped_chunk_start_time, self.tag)

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
        return RadioSpectrogram(average_Sxx,time_array_decimated,self.freqs_MHz,self.center_freq,self.chunk_start_time, self.tag)
    
    def frequency_average(self,average_over_int):
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
            num_frequency_samples_after_averaging = num_freq_samples//N
            
            #if the remainder is non-zero, introduce a final term which we will handle uniquely [average over the remaining terms]
            if remainder:
                num_frequency_samples_after_averaging+=1

            #instantiate an array to hold the averaged spectrogram
            average_Sxx = np.empty((num_frequency_samples_after_averaging, num_temporal_samples))

            #create an array to hold the decimated datetime array
            frequency_array_decimated = []

            #loop through the spectrogram and average the columns
            for i in range(num_frequency_samples_after_averaging):
                average_Sxx[i,:] = np.mean(self.Sxx[N*i:N*i+N,:],axis=0)
                frequency_array_decimated.append(self.freqs_MHz[i*N])
            
            #add the final bin edge for the decimated time array
            dfreq = frequency_array_decimated[-2]-frequency_array_decimated[-3]
            frequency_array_decimated.append(frequency_array_decimated[-1]+dfreq)

            #if there is a non-zero remainder, just cut the final entry
            if remainder:
                #average_Sxx[:,-1] = np.nanmean(self.Sxx[:,-remainder:],axis=1)
                average_Sxx=average_Sxx[:-1,:]
                frequency_array_decimated=frequency_array_decimated[:-1]

            bvect_averaged = ArrayFuncs.average_every_n_elements(self.background_vector, N)
            return RadioSpectrogram(average_Sxx,self.time_array,frequency_array_decimated,self.center_freq,self.chunk_start_time, self.tag, bvect = bvect_averaged)
    
    '''
    Plotting functions
    '''

    def stack_plots(self,fig,plot_types):
        SpectrogramPlotter(self).stack_plots(fig, plot_types)