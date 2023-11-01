from pdataFuncs import pdataFuncs
#instantiate the pdata class
pdata = pdataFuncs()

#for each dataFile in the timeStampDict
for timeStampStr,dataFile in pdata.dataDict.items():
    print(timeStampStr)
    dataFile.plotSpectrogram()

#print((dataFile.freqsMHz[-1]-dataFile.freqsMHz[0])*10**3)





