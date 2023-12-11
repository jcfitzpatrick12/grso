from fChunks.Chunks import Chunks
from fMisc.sys_vars import sys_vars
import os 
import numpy as np
#instantiate the pdata class, compute the average spectrogram and save it.
Chunks=Chunks()

#"%Y-%m-%dT%H:%M:%S"
start_string = "2023-12-11T20:18:03"
end_string = "2023-12-11T20:18:10"

S=Chunks.build_spectrogram_from_range(start_string,end_string)

#S.time_average(100)
#print(S.pseudo_start_time)
S.plot_spectrogram()
#S = S.time_average(100)
#S.plot_power()

#print(S.Sxx[:,10])
#print(S_original.Sxx[:,10])

#print(np.sum(S.Sxx-S_original.Sxx))

