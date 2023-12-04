from fChunks.Chunks import Chunks
from fMisc.sys_vars import sys_vars
import os 
#instantiate the pdata class, compute the average spectrogram and save it.
Chunks=Chunks()

#"%Y-%m-%dT%H:%M:%S"
#startString = "2023-12-04T14:48:00"
#endString = "2023-12-04T14:49:00"

startString = "2023-12-04T18:02:43"
endString = "2023-12-04T18:02:58"
S=Chunks.buildSpectrogramFromRange(startString,endString)
S.plotSpectrogram()


    #

