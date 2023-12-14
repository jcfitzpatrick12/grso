from fChunks.Chunks import Chunks
from fMisc.sys_vars import sys_vars
import os 
import numpy as np
#instantiate the pdata class, compute the average spectrogram and save it.
Chunks=Chunks()

#"%Y-%m-%dT%H:%M:%S"
start_string = "2023-12-14T18:20:00"
end_string = "2023-12-14T18:21:00"

S=Chunks.build_spectrogram_from_range(start_string,end_string)

S.time_average(10)
S.plot_power()
S.plot_spectrogram()
#S = S.time_average(100)


#print(S.Sxx[:,10])
#print(S_original.Sxx[:,10])

#print(np.sum(S.Sxx-S_original.Sxx))

