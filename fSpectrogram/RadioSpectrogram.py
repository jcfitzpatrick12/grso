'''
RadioSpectrogram class which handles, plotting, averaging, compute power etc. 
'''

import numpy as np
import pickle
import os
from astropy.io import fits
from datetime import timedelta

from fPlotting.Plotter import Plotter
from fMisc.sys_vars import sys_vars
from fMisc.DatetimeFuncs import DatetimeFuncs


class RadioSpectrogram:
    '''
    constructor functions
    '''
    def __init__(self, Sxx, time_array, freqs_MHz, center_freq, pseudo_start_time,is_averaged):
        self.sys_vars = sys_vars()
        self.Sxx = Sxx
        #displace so that the first element of the time array is at 0 seconds
        self.time_array = time_array-time_array[0]
        self.freqs_MHz = freqs_MHz
        self.center_freq = center_freq
        self.is_averaged = is_averaged

        self.pseudo_start_time = pseudo_start_time
        self.pseudo_start_datetime=DatetimeFuncs().parse_datetime(self.pseudo_start_time)
        self.datetime_array = self.build_datetime_array()
        self.datetime64_array = np.array(self.datetime_array,dtype="datetime64[ns]")
        self.power = self.build_power()
        self.sys_vars = sys_vars()


    def build_datetime_array(self,):
        #convert the times into datetimes
        return DatetimeFuncs().build_datetime_array(self.pseudo_start_datetime,self.time_array)

    def build_power(self):
        num_freq_bins = np.shape(self.Sxx)[0]
        num_time_bins = np.shape(self.Sxx)[1]
        power = np.empty(num_time_bins)
        dfreq_Hz = (self.freqs_MHz[1]-self.freqs_MHz[0])*10**-6
        for i in range(num_time_bins):
            power[i]=np.sum(self.Sxx[:,i])*dfreq_Hz

        return power
        pass

    '''
    Plotting functions
    '''
    def plot_power(self):
        Plotter().plot_power(self.datetime_array,self.power)
        pass

    def plot_spectrogram(self):
        Plotter().plot_spectrogram(self.freqs_MHz,self.datetime_array,self.Sxx)
        pass
    '''
    file functions
    '''
    #find the path to temporary_data
    def get_temp_data_path(self):
        return os.path.join(self.sys_vars.path_to_temp_data,self.pseudo_start_time)
    
    #find the path to data
    def get_data_path(self):
        return os.path.join(self.sys_vars.path_to_data,self.pseudo_start_time)
    
    '''
    function which saves the current instance to file
    '''
    def save_self(self):
        # Serialize the instance to bytes using pickle
        serialized_instance = pickle.dumps(self)
        # Convert the byte stream to a NumPy uint8 array
        instance_array = np.frombuffer(serialized_instance, dtype=np.uint8)
        np.save(self.get_path(), instance_array)
    '''
    function which saves the relevent data to rebuild the instance to a fits file!
    '''
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
        fpath = os.path.join(self.sys_vars.path_to_data,self.pseudo_start_time+".fits")
        # Write the FITS file
        hdulist.writeto(fpath, overwrite=True)
        pass

    '''
    function which returns a chopped spectrogram based on the time range

    startRange and endRange are both datetime Objects
    '''
    def chop(self,start_str,end_str):
        #parse the strings into datetimes
        start_dt = DatetimeFuncs().parse_datetime(start_str)
        end_dt = DatetimeFuncs().parse_datetime(end_str)
        #find the index of the nearest matching datetime elements in the array
        startIndex = DatetimeFuncs().find_closest_index(start_dt,self.datetime_array)
        endIndex = DatetimeFuncs().find_closest_index(end_dt,self.datetime_array)

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
        chopped_pseudo_start_time = DatetimeFuncs().to_string(self.datetime_array[startIndex])
        #return the chopped RadioSpectrogram
        return RadioSpectrogram(chopped_Sxx,chopped_timeArray,self.freqs_MHz,self.center_freq,chopped_pseudo_start_time,self.is_averaged)


    '''
    function which RETURNS the average spectrogram, and (necessarily) decimated timeArray
    '''

    def time_average(self,AverageOverInt):
        '''
        average in time over averageOver samples in the full spectrogram, create fields and save to a numpy array
        ''' 
        #find the number of frequenct samples
        num_freq_samples = np.shape(self.Sxx)[0]
        #find the number of temporal samples
        num_temporal_samples = np.shape(self.Sxx)[1]
        #print(num_temporal_samples)
        #eshorten the call of how many samples to average over
        N=AverageOverInt
        #find the remainder [we will average over the remaining samples if N does note exactly divide num_temporal_samples]
        remainder = num_temporal_samples % N
        
        #find the number of temporal_samples_after averaging
        num_temporal_samples_after_averaging = num_temporal_samples//N
        
        #if the remainder is non-zero, introduce a final term which we will handle uniquely [average over the remaining terms]
        if remainder:
            num_temporal_samples_after_averaging+=1

        #print(num_temporal_samples_after_averaging)

        #instantiate an array to hold the averaged spectrogram
        averageSxx = np.empty((num_freq_samples,num_temporal_samples_after_averaging))

        #create an array to hold the decimated datetime array
        timeArrayDecimated = []

        #loop through the spectrogram and average the columns
        for i in range(num_temporal_samples_after_averaging):
            averageSxx[:,i] = np.mean(self.Sxx[:,N*i:N*i+N],axis=1)
            timeArrayDecimated.append(self.time_array[i*N])
        
        #add the final bin edge for the decimated time array
        dt = timeArrayDecimated[-2]-timeArrayDecimated[-3]
        timeArrayDecimated.append(timeArrayDecimated[-1]+dt)

        #if there is a non-zero remainder, average over the remaining terms
        if remainder:
            averageSxx[:,-1] = np.mean(self.Sxx[:,-remainder::])
        
        averageRadioSpectrogram = RadioSpectrogram(averageSxx,timeArrayDecimated,self.freqs_MHz,self.center_freq,self.pseudo_start_time,True)
        return averageRadioSpectrogram



