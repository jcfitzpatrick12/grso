'''
chunkFile class deals with all files of the form %Y-%m-%dT%H:%M:%S[.EXT]
'''

import numpy as np
import scipy.signal as signal
from scipy.signal import spectrogram
import matplotlib.pyplot as plt
import os

from src.chunks.ChunkBase import ChunkBase
from src.chunks.standard.ChunkBin import ChunkBin
from src.chunks.standard.ChunkHdr import ChunkHdr
from src.chunks.standard.ChunkFits import ChunkFits
from src.spectrogram.standard.RadioSpectrogram import RadioSpectrogram
from src.configs import GLOBAL_CONFIG
import pmt

'''
ChunkFiles are characterised by chunk_start_time
'''

class Chunk(ChunkBase):
    #constructor for SingleFileHandler
    def __init__(self,chunk_start_time, tag):
        super().__init__(chunk_start_time, tag)
        #instantiate the ChunkBin class
        self.bin=ChunkBin(chunk_start_time, self.tag)
        #instantiate the ChunkHdr class
        self.hdr=ChunkHdr(chunk_start_time, self.tag)
        #insantiate the ChunkFits class
        self.fits = ChunkFits(chunk_start_time, self.tag)


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
            freqs_MHz = freqs*10**-6

            Sxx = Sxx.astype(np.float64)
            time_array = time_array.astype(np.float64)
            freqs_MHz = freqs_MHz.astype(np.float64)
            return RadioSpectrogram(Sxx, time_array, freqs_MHz, self.chunk_start_time, self.tag)
        else:
            raise SystemError(f"Files missing! We have that .bin exists is {self.bin.exists()} and .hdr exists is {self.hdr.exists()}")


