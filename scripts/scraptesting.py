from pdataFuncs import pdataFuncs
#instantiate the pdata class
pdata = pdataFuncs()


'''
#for each dataFile in the timeStampDict
for pseudo_start_time,dataFile in pdata.dataDict.items():
    print(pseudo_start_time)
    dataFile.plotSpectrogram(wantAverage=True)
    break
    #dataFile.plotSpectrogram(wantAverage=True)
'''




for pseudo_start_time,dataFileCompressed in pdata.dataCompressedDict.items():
    print(pseudo_start_time)
    dataFileCompressed.plotSpectrogram()
    dataFileCompressed.plotPower()




    