'''
chunkFile class deals with all files of the form %Y-%m-%dT%H:%M:%S[.EXT]
'''

import numpy as np
from datetime import datetime
import scipy.signal as signal
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
import os

from src.fChunks.ChunkBin import ChunkBin
from src.fChunks.ChunkHdr import ChunkHdr
from src.fChunks.ChunkNpy import ChunkNpy
from src.fChunks.ChunkFits import ChunkFits
from src.fSpectrogram.RadioSpectrogram import RadioSpectrogram
from src.fConfig import CONFIG
import pmt

'''
ChunkFiles are characterised by pseudo_start_time
'''

class Chunk:
    #constructor for SingleFileHandler
    def __init__(self,pseudo_start_time):
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
                                    window=signal.get_window(CONFIG.window_type,CONFIG.window_size),
                                    nperseg=CONFIG.nperseg,
                                    noverlap=CONFIG.noverlap,
                                    return_onesided=False,
                                    scaling='density',
                                    mode='psd')
            # Shift the zero-frequency component to the center
            Sxx = np.fft.fftshift(Sxx, axes=0)
            freqs = np.fft.fftshift(freqs)
            # Adjust the frequency axis for the center frequency translation
            freqs += center_freq
            '''
            We are going to modify the output of signal.spectrogram, so that time_array and freqs 
            describe the BIN EDGES!
            '''
            #append to the arrays so that we are describing the EDGES OF BINS and not the BIN CENTERS
            freqsMHz = np.empty((len(freqs)+1))
            #place in the original data
            freqsMHz[:-1]=freqs*10**-6
            dfreqMHz = freqsMHz[-2]-freqsMHz[-3]
            freqsMHz[-1]=freqsMHz[-2]+dfreqMHz
            
            extended_time_array = np.empty(len(time_array)+1,dtype='float64')
            extended_time_array[:-1]=time_array
            dt = time_array[-2]-time_array[-3]
            extended_time_array[-1] = time_array[-1]+dt
            #build the RadioSpectrogram class
            return RadioSpectrogram(Sxx,extended_time_array,freqsMHz, center_freq,self.pseudo_start_time,False)
        
        else:
            raise SystemError("Files missing! We have that .bin exists {} and .hdr exists {}".format(self.bin.exists(),self.hdr.exists()))


