'''
chunkFile class deals with all files of the form %Y-%m-%dT%H:%M:%S[.EXT]
'''

import numpy as np
from datetime import datetime
import scipy.signal as signal
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
import os

from src.chunks.singular.standard.ChunkBin import ChunkBin
from src.chunks.singular.standard.ChunkHdr import ChunkHdr
from src.chunks.singular.standard.ChunkFits import ChunkFits
from src.spectrogram.standard.RadioSpectrogram import RadioSpectrogram
from src.configs import GLOBAL_CONFIG
import pmt

'''
ChunkFiles are characterised by chunk_start_time
'''

class Chunk:
    #constructor for SingleFileHandler
    def __init__(self,chunk_start_time, tag):
        #instantiate the timeStampStr field
        self.chunk_start_time = chunk_start_time
        self.tag = tag
        self.time_format = f"{GLOBAL_CONFIG.default_time_format}_{tag}"
        #extract the datetime from chunk_start_time
        self.chunk_start_datetime = datetime.strptime(self.chunk_start_time, GLOBAL_CONFIG.default_time_format)
        #instantiate the ChunkBin class
        self.bin=ChunkBin(chunk_start_time, self.tag)
        #instantiate the ChunkHdr class
        self.hdr=ChunkHdr(chunk_start_time, self.tag)
        #insantiate the ChunkFits class
        self.fits = ChunkFits(chunk_start_time, self.tag)


    '''
    build the original RadioSpectrogram object from the bin and header files [no compression]
    '''

    def build_radio_spectrogram(self):
        #check that the binary and header files both exist for the chunk.
        if self.bin.exists() and self.hdr.exists():
            #otherwise, create from the original data and save it to memory.
            IQ_data = self.bin.get_IQ_data()
            headerDict = self.hdr.parse_header()
            #extract some important variables from headerDict
            center_freq = pmt.to_float(headerDict['center_freq'])
            samp_rate = pmt.to_long(headerDict['samp_rate'])
            # Compute the spectrogram with both positive and negative frequencies
            freqs, time_array, Sxx = spectrogram(IQ_data, 
                                    fs=samp_rate, # Replace with your actual sampling rate
                                    window=signal.get_window("hann",2048),
                                    nperseg=2048,
                                    noverlap=1024,
                                    return_onesided=False,
                                    scaling='density',
                                    mode='psd')
            # Shift the zero-frequency component to the center
            Sxx = np.fft.fftshift(Sxx, axes=0)
            freqs = np.fft.fftshift(freqs)
            # Adjust the frequency axis for the center frequency translation
            freqs += center_freq


            #pad frequency and time arrays
            freqsMHz = np.empty((len(freqs)+1))
            #place in the original data
            freqsMHz[:-1]=freqs*10**-6
            dfreqMHz = freqsMHz[-2]-freqsMHz[-3]
            freqsMHz[-1]=freqsMHz[-2]+dfreqMHz
            
            extended_time_array = np.empty(len(time_array)+1,dtype='float64')
            extended_time_array[:-1]=time_array
            dt = time_array[-2]-time_array[-3]
            extended_time_array[-1] = time_array[-1]+dt
            
            return RadioSpectrogram(Sxx, extended_time_array, freqsMHz, self.chunk_start_time, self.tag)
        
        else:
            raise SystemError("Files missing! We have that .bin exists {} and .hdr exists {}".format(self.bin.exists(),self.hdr.exists()))


