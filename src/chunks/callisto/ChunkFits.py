import numpy as np
import os
from astropy.io import fits
import matplotlib.pyplot as plt

from src.utils import DatetimeFuncs
from src.configs import GLOBAL_CONFIG
from src.spectrogram.callisto.RadioSpectrogram import RadioSpectrogram


class ChunkFits:
    def __init__(self,chunk_start_time, tag):
        self.chunk_start_time=chunk_start_time
        self.tag = tag
        self.data_dir=DatetimeFuncs.build_data_dir_from_chunk_start_time(GLOBAL_CONFIG.path_to_data, self.chunk_start_time)
        self.valid_request_strings = ["TIME"]

    #find the path to data
    def get_path(self):
        return os.path.join(self.data_dir,f"{self.chunk_start_time}_{self.tag}.fits")
    
    #find out if the path exists
    def exists(self):
        return os.path.exists(self.get_path())

    #function which returns requested information about a Chunk.
    def return_info(self,request_string):
        if self.exists():
            with fits.open(self.get_path(), mode='readonly') as hdulist:
                # Access the primary HDU
                primary_hdu = hdulist['PRIMARY']
                # Access the data part of the primary HDU
                Sxx = primary_hdu.data
                # The index of the BINTABLE varies; commonly, it's the first extension, hence hdul[1]
                bintable_hdu = hdulist[1]
                # Access the data within the BINTABLE
                data = bintable_hdu.data
                #make sure we have a valid request string
                if request_string in self.valid_request_strings:
                    if request_string == "TIME":
                        return data['TIME'][0]
        pass

    def print_header_info(self):
        if self.exists():
            # Open the FITS file
            with fits.open(self.get_path(), mode='readonly') as hdulist:
                 # hdul is a list-like collection of HDU (Header/Data Unit) objects
                for hdu in hdulist:
                    print('Header for HDU:', hdu.name)
                    print(repr(hdu.header))
                    print('\n\n') 
        else:
            print(f"Warning! No fits file for this chunk: {self.chunk_start_time}")

    
    #load the RadioSpectrogram from the fits file.
    def load_radio_spectrogram(self):
        if self.exists():
            # Open the FITS file
            with fits.open(self.get_path(), mode='readonly') as hdulist:
                # Access the primary HDU
                primary_hdu = hdulist['PRIMARY']
                
                # Access the data part of the primary HDU
                Sxx = primary_hdu.data
                                
                # The index of the BINTABLE varies; commonly, it's the first extension, hence hdul[1]
                bintable_hdu = hdulist[1]

                # Access the data within the BINTABLE
                data = bintable_hdu.data

                # Extract the time and frequency arrays
                # The column names ('TIME' and 'FREQUENCY') must match those in the FITS file
                time_array = data['TIME'][0]
                freqs_MHz = data['FREQUENCY'][0]

            #truncate the 2D array to follow shape conventions
            Sxx = Sxx[:-1,:-1]

            Sxx = np.array(Sxx, dtype = 'float')
            return RadioSpectrogram(Sxx, time_array, freqs_MHz, self.chunk_start_time, self.tag)

        else:
            print(f"Warning! No fits file for this chunk: {self.chunk_start_time}")

                


                