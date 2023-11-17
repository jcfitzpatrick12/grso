'''
chunkFile class deals with all files of the form [C]%Y-%m-%dT%H:%M:%S[.EXT]
'''

import numpy as np
from datetime import datetime
from sys_vars import sys_vars
from ChunkBin import ChunkBin
from ChunkHdr import ChunkHdr
from ChunkNpy import ChunkNpy
from ChunkFits import ChunkFits
#from ChunkFits import ChunkFits
from RadioSpectrogram import RadioSpectrogram
import scipy.signal as signal
from scipy.signal import spectrogram
import pmt

'''
ChunkFiles are characterised by pseudo_start_time
'''

class Chunk:
    #constructor for SingleFileHandler
    def __init__(self,pseudo_start_time):
        self.sys_vars = sys_vars()
        #instantiate the timeStampStr field
        self.pseudo_start_time = pseudo_start_time
        #type of the file
        #extract the datetime from pseudo_start_time
        self.pseudo_start_datetime = datetime.strptime(self.pseudo_start_time,"%Y-%m-%dT%H:%M:%S")
        #instantiate the ChunkBin class
        self.bin=ChunkBin(pseudo_start_time)
        #instantiate the ChunkHdr class
        self.hdr=ChunkHdr(pseudo_start_time)
        #instantiate the ChunkNpy class
        self.npy = ChunkNpy(pseudo_start_time)
        #insantiate the ChunkFits class
        self.fits = ChunkFits(pseudo_start_time)
        #instantiate the RadioSpectrogram class
        self.RadioSpectrogram = self.getRadioSpectrogram()


    '''
    other methods which I can call in Chunks class for clear 
    '''

    '''
    method which computes the RadioSpectrogram, combining data from the binary file and the header file
    '''
    def getRadioSpectrogram(self):
        IQdata = self.bin.getIQData()
        headerDict = self.hdr.parseHeader()
        #extract some important variables from headerDict
        center_freq = pmt.to_float(headerDict['center_freq'])
        samp_rate = pmt.to_long(headerDict['samp_rate'])
        # Compute the spectrogram with both positive and negative frequencies
        freqs, timeArray, Sxx = spectrogram(IQdata, fs=samp_rate, window=signal.get_window(self.sys_vars.window_type,self.sys_vars.window_size),return_onesided=False)
        # Shift the zero-frequency component to the center
        Sxx = np.fft.fftshift(Sxx, axes=0)
        freqs = np.fft.fftshift(freqs)
        # Adjust the frequency axis for the center frequency translation
        freqs += center_freq
        #convert the frequencies to MHz
        freqsMHz = freqs*10**-6
        #build the RadioSpectrogram class
        return RadioSpectrogram(Sxx,timeArray,freqsMHz, center_freq,self.pseudo_start_time,False)

    def loadRadioSpectrogram(self):
        return self.npy.load()

