'''
script which will run to process data captured by gnuradio to obtain a compressed spectrogram,
and then save the averaged spectrograms.
'''

from fChunks.Chunks import Chunks
#instantiate the pdata class, compute the average spectrogram and save it.
Chunks=Chunks()

#Pdata.chunkDict contains the key_value pairs pseudo_start_time and the DataChunkFile
#DataChunkFile is so named
for pseudo_start_time,Chunk in Chunks.dict.items():
    #if we do not have a fits file for this chunk
    if Chunk.fits.exists():
        pass
    #otherwise, the fits file exists and we can simply pass this chunk
    else:
        #build the spectrogram from the Chunk
        Spectrogram = Chunk.buildRadioSpectrogram()
        Spectrogram = Spectrogram.timeAverage(100)
        #save the spectrogram to a fits file
        Spectrogram.savetoFits()

#remove all the non-fits files.
Chunks.removeBigFiles()