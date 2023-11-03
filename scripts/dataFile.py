'''
child class of SingleFile for operations on the saved data.
'''
import numpy as np
from SingleFile import SingleFile
import os
import scipy.signal as signal
from scipy.signal import spectrogram
from datetimeFuncs import datetimeFuncs
from Plotter import Plotter
from sys_vars import sys_vars

class dataFile(SingleFile):
    #constructor for dataFile
    def __init__(self,timeStampStr):
        super().__init__(timeStampStr)
        #load the iqdata
        self.iqData = self.loadData()
        self.num_samples = len(self.iqData)

        #compute the spectrogram for the iqData
        self.computeSpectrogram(self.sys_vars.window_type,self.sys_vars.window_size)
        #build the datetime array
        self.buildDatetimes()

        #compute and save the average spectrogram
        self.computeAverageSpectrogram()
        self.computeDecimatedDatetimes()
        self.saveAveragedDataDict()


    def loadData(self):
        return np.load(os.path.join(self.filePath+".npy"))

    
    def computeSpectrogram(self,window_str,window_size):
        # Compute the spectrogram with both positive and negative frequencies
        freqs, timeArray, Sxx = spectrogram(self.iqData, fs=self.samp_rate, window=signal.get_window(window_str,window_size),return_onesided=False)

        # Shift the zero-frequency component to the center
        Sxx = np.fft.fftshift(Sxx, axes=0)
        freqs = np.fft.fftshift(freqs)

        # Adjust the frequency axis for the center frequency translation
        freqs += self.center_freq

        self.freqsMHz = freqs*10**-6
        self.timeArray = timeArray
        self.Sxx = Sxx

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

        #loop through the spectrogram and average the columns
        for i in range(num_temporal_samples_after_averaging):
            averageSxx[:,i] = np.mean(self.Sxx[:,N*i:N*i+N],axis=1)
        
        #if there is a non-zero remainder, average over the remaining terms
        if remainder:
            averageSxx[:,-1] = np.mean(self.Sxx[:,-remainder::])

        #instaniate a field to hold the averaged spectrogram
        self.averageSxx = averageSxx
        pass

    def saveAveragedDataDict(self):
        #build the averaged data dictionary
        AveragedDataDict = {}
        AveragedDataDict['Sxx']=self.averageSxx
        AveragedDataDict['datetimeArray']=self.datetimeArrayDecimated
        AveragedDataDict['center_freq']=self.center_freq
        AveragedDataDict['freqsMHz']=self.freqsMHz
        AveragedDataDict['samp_rate']=self.samp_rate
        #save the dictionary
        np.save(self.customFilePath("average"),AveragedDataDict,allow_pickle=True)
        pass
    
    #averaging will decimate the datetimes.
    #save a new datetime array to reflect this.
    def computeDecimatedDatetimes(self):

        #technically we could steal this from our averaging of the spectrogram but lets do it explicately anyway

        #find the number of temporal samples
        num_temporal_samples = len(self.datetimeArray)
        #eshorten the call of how many samples to average over
        N=self.sys_vars.averageOverInt
        #find the remainder [we will average over the remaining samples if N does note exactly divide num_temporal_samples]
        remainder = num_temporal_samples % N
        #find the number of temporal_samples_after averaging
        num_temporal_samples_after_averaging = num_temporal_samples//N


        #if there's a remainder, +=1
        if remainder:
            num_temporal_samples_after_averaging+=1

       
        #create an array to hold the decimated datetime array
        datetimeArrayDecimated = []

        #loop through the spectrogram and average the columns
        for i in range(num_temporal_samples_after_averaging):
            datetimeArrayDecimated.append(self.datetimeArray[i*N])

        #instantiate the decimated datetime array.
        self.datetimeArrayDecimated = datetimeArrayDecimated
        pass
        
    
    def buildDatetimes(self):
        #convert the times into datetimes
        self.datetimeArray = datetimeFuncs().buildDatetimeArray(self.pseudo_start_datetime,self.timeArray)
        
    def plotSpectrogram(self,**kwargs):
        defaultBoole = False
        wantAverage = kwargs.get('wantAverage',defaultBoole)
        if not wantAverage:
            Plotter().plotSpectrogram(self.freqsMHz,self.datetimeArray,self.Sxx)
        if wantAverage:
            Plotter().plotSpectrogram(self.freqsMHz,self.datetimeArrayDecimated,self.averageSxx)        
        


    

        
        
