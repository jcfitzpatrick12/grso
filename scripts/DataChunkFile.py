'''
child class of the chunkFile. For code readability, primarily deals with data and headers ONCE EXTRACTED BY CHUNKFILE!
'''

'''
child class of SingleFile for operations on the saved data.
'''
import numpy as np
from ChunkFile import ChunkFile
import os
import scipy.signal as signal
from scipy.signal import spectrogram
from datetimeFuncs import datetimeFuncs
from RadioSpectrogram import RadioSpectrogram
import pmt

class DataChunkFile(ChunkFile):
    '''
    constructors for dataFile
    '''
    def __init__(self,timeStampStr):
        super().__init__(timeStampStr)
        #load the iqdata
        self.iqData = self.loadData()
        #find the number of samples
        self.num_samples = len(self.iqData)
        #extract some important variables from headerDict
        self.center_freq = pmt.to_float(self.headerDict['center_freq'])
        self.samp_rate = pmt.to_long(self.headerDict['samp_rate'])

        #compute the spectrogram for the iqData
        self.computeSpectrogram(self.sys_vars.window_type,self.sys_vars.window_size)



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
        self.Sxx = Sxx
        self.timeArray = timeArray
        self.freqsMHz = freqs*10**-6
        #build the RadioSpectrogram class
        self.RadioSpectrogram = RadioSpectrogram(self.Sxx,self.timeArray,self.freqsMHz, self.center_freq,self.pseudo_start_time,False)

        


    

        
        