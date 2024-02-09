import numpy as np
from astropy.io import fits
from datetime import datetime

from src.spectrogram.BaseSpectrogram import BaseSpectrogram

class RadioSpectrogram(BaseSpectrogram):
    def __init__(self, Sxx, time_array, freqs_MHz, chunk_start_time, tag, **kwargs):
        super().__init__(Sxx, time_array, freqs_MHz, chunk_start_time, tag, **kwargs)


    # Function to create a FITS file with the specified structure
    def save_to_fits(self,):
        # Primary HDU with data
        primary_data = self.Sxx.astype(dtype=np.float64) 
        primary_hdu = fits.PrimaryHDU(primary_data)

        primary_hdu.header.set('SIMPLE', True, 'file does conform to FITS standard')
        primary_hdu.header.set('BITPIX', -64, 'number of bits per data pixel')
        primary_hdu.header.set('NAXIS', 2, 'number of data axes')
        primary_hdu.header.set('NAXIS1', self.get_NAXIS1(), 'length of data axis 1')
        primary_hdu.header.set('NAXIS2', self.get_NAXIS2(), 'length of data axis 2')
        primary_hdu.header.set('EXTEND', True, 'FITS dataset may contain extensions')

        # Add comments
        comments = [
            "FITS (Flexible Image Transport System) format defined in Astronomy and",
            "Astrophysics Supplement Series v44/p363, v44/p371, v73/p359, v73/p365.",
            "Contact the NASA Science Office of Standards and Technology for the",
            "FITS Definition document #100 and other FITS information."
        ]
        # The comments section remains unchanged since add_comment is the correct approach
        for comment in comments:
            primary_hdu.header.add_comment(comment)

        primary_hdu.header.set('DATE', self.get_DATE(), 'time of observation')
        primary_hdu.header.set('CONTENT', f'{self.get_DATE()} power spectral density, grso (GLASGOW)', 'title of image')
        primary_hdu.header.set('ORIGIN', 'UK', 'organization name')
        primary_hdu.header.set('TELESCOP', f'SDRplay RSP1A, tag: {self.tag}', 'type of instrument')
        primary_hdu.header.set('INSTRUME', 'grso (GLASGOW)', 'name of the spectrometer') # Corrected keyword INSTRUMEN to INSTRUME
        primary_hdu.header.set('OBJECT', 'Sun', 'object description')

        primary_hdu.header.set('DATE-OBS', self.get_DATE_OBS(), 'date observation starts')
        primary_hdu.header.set('TIME-OBS', self.get_TIME_OBS(), 'time observation starts')
        primary_hdu.header.set('DATE-END', self.get_DATE_END(), 'date observation ends')
        primary_hdu.header.set('TIME-END', self.get_TIME_END(), 'time observation ends')

        primary_hdu.header.set('BZERO', 0, 'scaling offset')
        primary_hdu.header.set('BSCALE', 1, 'scaling factor')
        primary_hdu.header.set('BUNIT', " ... ", 'z-axis title') # This should be specified with the actual unit

        primary_hdu.header.set('DATAMIN', self.get_DATA_MIN(), 'minimum element in image')
        primary_hdu.header.set('DATAMAX', self.get_DATA_MAX(), 'maximum element in image')

        primary_hdu.header.set('CRVAL1', self.get_CRVAL1(), 'value on axis 1 at reference pixel [sec of day]')
        primary_hdu.header.set('CRPIX1', 0, 'reference pixel of axis 1')
        primary_hdu.header.set('CTYPE1', 'TIME [UT]', 'title of axis 1')
        primary_hdu.header.set('CDELT1', self.get_CDELT1(), 'step between first and second element in x-axis')

        primary_hdu.header.set('CRVAL2', 0, 'value on axis 2 at reference pixel')
        primary_hdu.header.set('CRPIX2', 0, 'reference pixel of axis 2')
        primary_hdu.header.set('CTYPE2', 'Frequency [MHz]', 'title of axis 2')
        primary_hdu.header.set('CDELT2', self.get_CDELT2(), 'step between first and second element in axis')

        primary_hdu.header.set('OBS_LAT', '55.78088', 'observatory latitude in degree')
        primary_hdu.header.set('OBS_LAC', 'N', 'observatory latitude code {N,S}')
        primary_hdu.header.set('OBS_LON', '4.31770', 'observatory longitude in degree')
        primary_hdu.header.set('OBS_LOC', 'W', 'observatory longitude code {E,W}')
        primary_hdu.header.set('OBS_ALT', '100', 'observatory altitude in meter asl')


 
        # Binary Table HDU (extension)
        col1 = fits.Column(name='TIME', format='D', array=self.time_array.astype(np.float64))
        col2 = fits.Column(name='FREQUENCY', format='D', array=self.freqs_MHz.astype(np.float64))
        cols = fits.ColDefs([col1, col2])

        bin_table_hdu = fits.BinTableHDU.from_columns(cols)

        bin_table_hdu.header.set('PCOUNT', 0, 'size of special data area')
        bin_table_hdu.header.set('GCOUNT', 1, 'one data group (required keyword)')
        bin_table_hdu.header.set('TFIELDS', 2, 'number of fields in each row')
        bin_table_hdu.header.set('TTYPE1', 'TIME', 'label for field 1')
        bin_table_hdu.header.set('TFORM1', 'D', 'data format of field: 8-byte DOUBLE')
        bin_table_hdu.header.set('TTYPE2', 'FREQUENCY', 'label for field 2')
        bin_table_hdu.header.set('TFORM2', 'D', 'data format of field: 8-byte DOUBLE')
        bin_table_hdu.header.set('TSCAL1', 1, '')
        bin_table_hdu.header.set('TZERO1', 0, '')
        bin_table_hdu.header.set('TSCAL2', 1, '')
        bin_table_hdu.header.set('TZERO2', 0, '')

        # Create HDU list and write to file
        hdul = fits.HDUList([primary_hdu, bin_table_hdu])
        hdul.writeto(self.get_path(), overwrite=True)


    def get_NAXIS1(self):
        # Assuming self.Sxx is a 2D numpy array with shape (rows, columns)
        return self.Sxx.shape[1]

    def get_NAXIS2(self):
        # Assuming self.Sxx is a 2D numpy array with shape (rows, columns)
        return self.Sxx.shape[0]
    

    def get_DATE(self):
        return self.datetime_array[0].strftime("%Y-%m-%d")


    def get_DATE_OBS(self):
        return self.datetime_array[0].strftime("%Y-%m-%d")
    
    
    def get_TIME_OBS(self):
        return self.datetime_array[0].strftime("%H:%M:%S.%f")
    
    
    def get_DATE_END(self):
        return self.datetime_array[-1].strftime("%Y-%m-%d")
    

    def get_TIME_END(self):
        return self.datetime_array[-1].strftime("%H:%M:%S.%f")
    

    def get_DATA_MIN(self):
        return np.nanmin(self.Sxx)
    

    def get_DATA_MAX(self):
        return np.nanmax(self.Sxx)
    

    def get_CRVAL1(self):
        now = datetime.now()
        start_of_day = datetime(now.year, now.month, now.day)
        return (now - start_of_day).total_seconds()
    
    
    def get_CDELT1(self):
        return (self.datetime_array[1] - self.datetime_array[0]).total_seconds()
    

    def get_CDELT2(self):
        return self.freqs_MHz[1] - self.freqs_MHz[0]
    
    
    def get_bintable_NAXIS1(self):
        # Assuming time_array and freqs_MHz are 1D numpy arrays and the only two columns in the binary table
        # Calculate the width in bytes of a single row in the table
        return (len(self.time_array) + len(self.freqs_MHz)) * 8

    # def save_to_fits(self):
    #     # Create a Primary HDU object with the Sxx data
    #     primary_hdu = fits.PrimaryHDU(self.Sxx)

    #     # Create a Header Data Unit (HDU) list and add the primary HDU
    #     hdulist = fits.HDUList([primary_hdu])

    #     primary_hdu.header['PSTIME'] = self.chunk_start_time

    #     col_time = fits.Column(name='TIME', array=self.time_array, format='D')
    #     col_freq = fits.Column(name='FREQ', array=self.freqs_MHz, format='D')

    #     tb_hdu_time = fits.BinTableHDU.from_columns([col_time])
    #     tb_hdu_freq = fits.BinTableHDU.from_columns([col_freq])

    #     hdulist.append(tb_hdu_time)
    #     hdulist.append(tb_hdu_freq)

    #     #name the path according to the chunk_start_time
    #     fpath = os.path.join(self.get_path())
    #     # Write the FITS file
    #     hdulist.writeto(fpath, overwrite=True)
    #     p
    # s