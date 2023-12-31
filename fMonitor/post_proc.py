'''
script will convert the binary and header data to fits files in data folder
'''
from fChunks.Chunks import Chunks
from fMisc.sys_vars import sys_vars

def main():
    sv = sys_vars()
    #instantiate the pdata class, compute the average spectrogram and save it.
    MyChunks=Chunks()
    #DataChunkFile is so named
    for pseudo_start_time,Chunk in MyChunks.dict.items():
        #move all files from temp_data to data
        #if we do not have a fits file for this chunk
        if Chunk.fits.exists():
            pass
        #otherwise, the fits file exists and we can simply pass this chunk
        else:
            try:
            #build the spectrogram from the Chunk
                Spectrogram = Chunk.build_radio_spectrogram()
                Spectrogram = Spectrogram.time_average(sv.average_over_int)
                #save the spectrogram to a fits file
                Spectrogram.save_to_fits()
            except:
                print("Couldn't make spectrogram for this Chunk!")
                pass


    #delete all non-fits files from data
    MyChunks.remove_non_fits_files_from_data()
    exit()

if __name__ == '__main__':
    main()