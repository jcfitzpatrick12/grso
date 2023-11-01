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

class dataFile(SingleFile):
    #constructor for dataFile
    def __init__(self,timeStampStr):
        super().__init__(timeStampStr)
        self.iqData = self.loadData()

        #compute the spectrogram for the iqData
        self.computeSpectrogram("blackmanharris",1024)
        #build the datetime array
        self.buildDatetimes()

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
    
    def buildDatetimes(self):
        #convert the times into datetimes
        self.datetimeArray = datetimeFuncs().buildDatetimeArray(self.pseudo_start_datetime,self.timeArray)
        
    def plotSpectrogram(self):
        Plotter().plotSpectrogram(self.freqsMHz,self.datetimeArray,self.Sxx)

        
        
