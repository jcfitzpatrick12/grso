import numpy as np
import os
from astropy.io import fits

from src.utils import DatetimeFuncs
from src.configs import GLOBAL_CONFIG
from src.spectrogram.RadioSpectrogram import RadioSpectrogram

class ChunkFits:
    def __init__(self,chunk_start_time, tag):
        self.chunk_start_time=chunk_start_time
        self.tag = tag
        self.data_dir=DatetimeFuncs.build_data_dir_from_chunk_start_time(GLOBAL_CONFIG.path_to_data, self.chunk_start_time)
        self.valid_request_strings = ['Sxx','CFREQ','PSTIME','ISCOMPR','TIME','FREQ']

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
                # Extract the primary HDU data (Sxx spectrogram)
                primary_hdu = hdulist[0]
                Sxx = primary_hdu.data
                #make sure we have a valid request string
                if request_string in self.valid_request_strings:
                    if request_string == "TIME":
                        return(hdulist[1].data[request_string])
                    elif request_string == "Sxx":
                        return(primary_hdu.data)
                    elif request_string in ["CFREQ", "PSTIME", "ISCOMPR"]:
                        return primary_hdu.header[request_string]
                    elif request_string=="FREQ":
                        return(hdulist[2].data[request_string])
                    else:
                        raise SystemError("Error in the code! We shouldn't make it to here if the previous if statement caught an invalid input.")
                #if it is not valid, throw an error.
                else:
                    raise SystemError('Please enter a valid RequestString. {} is not one of {}'.format(request_string,self.valid_request_strings))


        else:
            raise SystemError('No file found!!')
    
    #load the RadioSpectrogram from the fits file.
    def load_radio_spectrogram(self):
        if self.exists():
                # Open the FITS file
            with fits.open(self.get_path(), mode='readonly') as hdulist:
                # Extract the primary HDU data (Sxx spectrogram)
                primary_hdu = hdulist[0]
                Sxx = primary_hdu.data

                # Extract other necessary attributes from the header
                center_freq = primary_hdu.header['CFREQ']
                chunk_start_time = primary_hdu.header['PSTIME']

                # Assuming timeArray and freqsMHz are stored in a binary table in the second HDU
                time_array = hdulist[1].data['TIME']
                freqs_MHz = hdulist[2].data['FREQ']


                    # Create a new instance of RadioSpectrogram
            return RadioSpectrogram(Sxx, time_array, freqs_MHz, center_freq, chunk_start_time, self.tag)

        else:
            raise SystemError('No file found!!')