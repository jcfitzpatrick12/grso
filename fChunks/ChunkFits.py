import numpy as np
import os
from astropy.io import fits

from fMisc.sys_vars import sys_vars
from fSpectrogram.RadioSpectrogram import RadioSpectrogram

class ChunkFits:
    def __init__(self,pseudo_start_time):
        self.sys_vars=sys_vars()
        self.pseudo_start_time=pseudo_start_time
        self.path = self.getPath()

    #find the path to the binary
    def getPath(self):
        return os.path.join(self.sys_vars.path_to_data,self.pseudo_start_time+".fits")
    
    #find out if the path exists
    def exists(self):
        return os.path.exists(self.path)
    
    #load the RadioSpectrogram from the fits file.
    def loadRadioSpectrogram(self):
        if self.exists():
                # Open the FITS file
            with fits.open(self.getPath(), mode='readonly') as hdulist:
                # Extract the primary HDU data (Sxx spectrogram)
                primary_hdu = hdulist[0]
                Sxx = primary_hdu.data

                # Extract other necessary attributes from the header
                center_freq = primary_hdu.header['CFREQ']
                pseudo_start_time = primary_hdu.header['PSTIME']
                isCompressed = primary_hdu.header['ISCOMPR']

                # Assuming timeArray and freqsMHz are stored in a binary table in the second HDU
                timeArray = hdulist[1].data['Time']
                freqsMHz = hdulist[2].data['Frequency']


                    # Create a new instance of RadioSpectrogram
            return RadioSpectrogram(Sxx, timeArray, freqsMHz, center_freq, pseudo_start_time, isCompressed)

        else:
            raise SystemError('No file found!!')