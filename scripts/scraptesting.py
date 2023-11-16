

from PdataFuncs import PdataFuncs
#instantiate the pdata class

#instantiate Pdata
Pdata = PdataFuncs()

'''
#Pdata.chunkDict contains the key_value pairs pseudo_start_time and the DataChunkFile
#DataChunkFile is so named
for pseudo_start_time,DataChunkFile in Pdata.chunkDict.items():
    rawSpectrogram=DataChunkFile.RadioSpectrogram
    #rawSpectrogram.plotSpectrogram()
    #rawSpectrogram.saveToFile()
    compressedSpectrogram = rawSpectrogram.computeAverageSpectrogram()
    #print(compressedSpectrogram.isCompressed)
    compressedSpectrogram.plotSpectrogram()
    compressedSpectrogram.saveToFile()

Pdata.updateDicts()
'''

#print(Pdata.cspectrogramDict.values())
for compressedSpectrogram in Pdata.cspectrogramDict.values():
    compressedSpectrogram = compressedSpectrogram.computeAverageSpectrogram()
    compressedSpectrogram.plotSpectrogram()
    #compressedSpectrogram.plotPower()





    











    