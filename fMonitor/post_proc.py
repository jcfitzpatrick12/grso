'''
script will convert the binary and header data to fits files in data folder
'''

from fChunks.Chunks import Chunks
#instantiate the pdata class, compute the average spectrogram and save it.
Chunks=Chunks()

#DataChunkFile is so named
for pseudo_start_time,Chunk in Chunks.dict.items():
    #move all files from temp_data to data
    #if we do not have a fits file for this chunk
    if Chunk.fits.exists():
        pass
    #otherwise, the fits file exists and we can simply pass this chunk
    else:
        #build the spectrogram from the Chunk
        Spectrogram = Chunk.build_radio_spectrogram()
        Spectrogram = Spectrogram.time_average(100)
        #save the spectrogram to a fits file
        Spectrogram.save_to_fits()


#delete all non-fits files from data
Chunks.remove_non_fits_files_from_data()

exit()