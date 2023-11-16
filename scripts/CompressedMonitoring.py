'''
script which will run to process data captured by gnuradio to obtain a compressed spectrogram,
and then save the averaged spectrograms.
'''

from PdataFuncs import PdataFuncs
#instantiate the pdata class, compute the average spectrogram and save it.
Pdata = PdataFuncs()

#for each DataChunkFile, copute the average spectrogram and save it
for DataChunkFile in Pdata.chunkDict.values():
    #extract the averaged spectrogram
    compressedSpectrogram = DataChunkFile.RadioSpectrogram.computeAverageSpectrogram()
    #save this to file in Pdata
    compressedSpectrogram.saveToFile()
#remove all the non-averaged files.
Pdata.removeBigFiles()