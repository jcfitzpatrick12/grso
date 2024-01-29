'''
script will convert the binary and header data to fits files in data folder
'''
from src.fChunks.Chunks import Chunks
from src.fChunks.Chunk import Chunk
from src.fConfig import CONFIG

def main():
    #instantiate the pdata class, compute the average spectrogram and save it.
    my_chunks=Chunks(CONFIG.path_to_data, Chunk)
    #DataChunkFile is so named
    for chunk_start_time,chunk in my_chunks.dict.items():
        #move all files from temp_data to data
        #if we do not have a fits file for this chunk
        if chunk.fits.exists():
            pass
        #otherwise, the fits file exists and we can simply pass this chunk
        else:
            try:
                #build the spectrogram from the Chunk
                Spectrogram = chunk.build_radio_spectrogram()
                Spectrogram = Spectrogram.time_average(CONFIG.average_over_int)
                #save the spectrogram to a fits file
                Spectrogram.save_to_fits()
            except Exception as e:
                print(f"Couldn't make spectrogram for this Chunk! {e}")


    #delete all non-fits files from data
    my_chunks.remove_non_fits_files_from_data()

if __name__ == '__main__':
    main()