

from PdataFuncs import PdataFuncs
#instantiate the pdata class

Pdata = PdataFuncs()

for pseudo_start_time,DataChunkFile in Pdata.chunkDict.items():
    rawSpectrogram=DataChunkFile.RadioSpectrogram
    rawSpectrogram.plotSpectrogram()
    rawSpectrogram.saveToFile()
    compressedSpectrogram = rawSpectrogram.computeAverageSpectrogram()
    #print(compressedSpectrogram.isCompressed)
    compressedSpectrogram.plotSpectrogram()
    compressedSpectrogram.saveToFile()

Pdata.updateDicts()

for compressedSpectrogram in Pdata.cspectrogramDict.values():
    compressedSpectrogram.plotSpectrogram()





    