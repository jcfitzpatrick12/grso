'''
script which will run to process data captured by gnuradio to obtain a compressed spectrogram,
and then save the averaged spectrograms.
'''

from Chunks import Chunks
#instantiate the pdata class, compute the average spectrogram and save it.
Chunks=Chunks()

#Pdata.chunkDict contains the key_value pairs pseudo_start_time and the DataChunkFile
#DataChunkFile is so named
for pseudo_start_time,Chunk in Chunks.dict.items():
    compressedSpectrogram = Chunk.computeAverageSpectrogram()
    compressedSpectrogram.savetoFits()
#remove all the non-averaged files.
Chunks.removeBigFiles()