from Chunks import Chunks
#instantiate the pdata class, compute the average spectrogram and save it.
Chunks=Chunks()

#Pdata.chunkDict contains the key_value pairs pseudo_start_time and the DataChunkFile
#DataChunkFile is so named
for pseudo_start_time,Chunk in Chunks.dict.items():
    Spectrogram = Chunk.buildRadioSpectrogram()
    compressedSpectrogram = Spectrogram.timeAverage(2)
    compressedSpectrogram.plotSpectrogram()
