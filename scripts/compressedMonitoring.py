'''
script which will run to process data captured by gnuradio to obtain a compressed spectrogram,
and then save the averaged spectrograms.
'''

from pdataFuncs import pdataFuncs
#instantiate the pdata class, compute the average spectrogram and save it.
pdata = pdataFuncs()
#remove all the non-averagedFiles.
pdata.removeBigFiles()