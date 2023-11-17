'''
RadioSpectrogram class which handles, plotting, averaging, compute power etc. 
'''

import numpy as np
from Plotter import Plotter
from datetimeFuncs import datetimeFuncs
import pickle
import os
from sys_vars import sys_vars
from astropy.io import fits

class RadioSpectrogram:
    '''
    constructor functions
    '''
    def __init__(self, Sxx, timeArray, freqsMHz, center_freq, pseudo_start_time,isCompressed):
        self.sys_vars = sys_vars()
        self.Sxx = Sxx
        self.timeArray = timeArray
        self.freqsMHz = freqsMHz
        self.center_freq = center_freq
        self.pseudo_start_time = pseudo_start_time
        self.pseudo_start_datetime=datetimeFuncs().parseDatetime(self.pseudo_start_time)
        self.isCompressed = isCompressed
        self.datetimeArray = self.build_datetimeArray()
        self.power = self.buildPower()
        self.sys_vars = sys_vars()


    def build_datetimeArray(self,):
        #convert the times into datetimes
        return datetimeFuncs().buildDatetimeArray(self.pseudo_start_datetime,self.timeArray)

    def buildPower(self):
        num_freq_bins = np.shape(self.Sxx)[0]
        num_time_bins = np.shape(self.Sxx)[1]
        power = np.empty(num_time_bins)
        dfreqHz = (self.freqsMHz[1]-self.freqsMHz[0])*10**-6
        for i in range(num_time_bins):
            power[i]=np.sum(self.Sxx[:,i])*dfreqHz

        return power
        pass

    '''
    Plotting functions
    '''
    def plotPower(self):
        Plotter().plotPower(self.datetimeArray,self.power)
        pass

    def plotSpectrogram(self):
        Plotter().plotSpectrogram(self.freqsMHz,self.datetimeArray,self.Sxx)
        pass
    '''
    file functions
    '''
    def getPath(self):
        fpath = os.path.join(self.sys_vars.path_to_data,self.pseudo_start_time)
        return fpath
    
    '''
    function which saves the current instance to file
    '''
    def saveSelf(self):
        # Serialize the instance to bytes using pickle
        serialized_instance = pickle.dumps(self)
        # Convert the byte stream to a NumPy uint8 array
        instance_array = np.frombuffer(serialized_instance, dtype=np.uint8)
        np.save(self.getPath(), instance_array)
    '''
    function which saves the relevent data to rebuild the instance to a fits file!
    '''
    def savetoFits(self):
        # Create a Primary HDU object with the Sxx data
        primary_hdu = fits.PrimaryHDU(self.Sxx)

        # Create a Header Data Unit (HDU) list and add the primary HDU
        hdulist = fits.HDUList([primary_hdu])

        # Add other attributes as headers in the primary HDU
        primary_hdu.header['CFREQ'] = self.center_freq
        primary_hdu.header['PSTIME'] = self.pseudo_start_time
        primary_hdu.header['ISCOMPR'] = self.isCompressed

        col_time = fits.Column(name='Time', array=self.timeArray, format='D')
        col_freq = fits.Column(name='Frequency', array=self.freqsMHz, format='D')

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
    function which RETURNS the average spectrogram, and decimated timeArray
    '''

    def computeAverageSpectrogram(self):
        '''
        average in time over averageOver samples in the full spectrogram, create fields and save to a numpy array
        ''' 
        #find the number of frequenct samples
        num_freq_samples = np.shape(self.Sxx)[0]
        #find the number of temporal samples
        num_temporal_samples = np.shape(self.Sxx)[1]
        #print(num_temporal_samples)
        #eshorten the call of how many samples to average over
        N=self.sys_vars.averageOverInt
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
            timeArrayDecimated.append(self.timeArray[i*N])
        
        #if there is a non-zero remainder, average over the remaining terms
        if remainder:
            averageSxx[:,-1] = np.mean(self.Sxx[:,-remainder::])
        
        averageRadioSpectrogram = RadioSpectrogram(averageSxx,timeArrayDecimated,self.freqsMHz,self.center_freq,self.pseudo_start_time,True)
        return averageRadioSpectrogram


