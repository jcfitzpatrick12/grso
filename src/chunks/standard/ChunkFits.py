from astropy.io import fits

from src.chunks.ChunkExt import ChunkExt
from src.spectrogram.standard.RadioSpectrogram import RadioSpectrogram

class ChunkFits(ChunkExt):
    def __init__(self,chunk_start_time, tag):
        super().__init__(chunk_start_time, tag, ".fits")
        self.valid_request_strings = ["TIME"]


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
                        return data['TIME']
        pass

    
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
                time_array = data['TIME']
                freqs_MHz = data['FREQUENCY']
                return RadioSpectrogram(Sxx, time_array, freqs_MHz, self.chunk_start_time, self.tag)
    