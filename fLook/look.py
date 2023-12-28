from fChunks.Chunks import Chunks
from fMisc.sys_vars import sys_vars
import os 
import numpy as np
#instantiate the pdata class, compute the average spectrogram and save it.
Chunks=Chunks()

#"%Y-%m-%dT%H:%M:%S"
start_string = "2023-12-28T13:11:00"
end_string = "2023-12-24T13:11:20"

S=Chunks.build_spectrogram_from_range(start_string,end_string)

#i=500
#j=530
#S.Sxx=S.Sxx[i:j,:]
#S.freqs_MHz=S.freqs_MHz[i:j+1]
S.time_average(100)
S.plot_power()
S.plot_spectrogram()
#S = S.time_average(100)


#print(S.Sxx[:,10])
#print(S_original.Sxx[:,10])

#print(np.sum(S.Sxx-S_original.Sxx))

