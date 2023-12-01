from fChunks.Chunks import Chunks
from fMisc.sys_vars import sys_vars
import os 
#instantiate the pdata class, compute the average spectrogram and save it.
Chunks=Chunks()
#print(sys_vars().path_to_data)

#Pdata.chunkDict contains the key_value pairs pseudo_start_time and the DataChunkFile
#DataChunkFile is so named
for pseudo_start_time,Chunk in Chunks.dict.items():
    S = Chunk.buildRadioSpectrogram()
    #S = S.timeAverage(3)
    #S.plotSpectrogram()
    S = Chunk.fits.loadRadioSpectrogram()
    S = S.timeAverage(100)
    S.plotSpectrogram()
    S.plotPower()
    


