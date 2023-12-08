from fChunks.Chunks import Chunks
from fMisc.sys_vars import sys_vars
import os 
import numpy as np
#instantiate the pdata class, compute the average spectrogram and save it.
Chunks=Chunks()


for pseudo_start_time,Chunk in Chunks.dict.items():
    print(pseudo_start_time)
    S_original = Chunk.fits.load_radio_spectrogram()

#"%Y-%m-%dT%H:%M:%S"
start_string = "2023-12-08T17:27:01"
end_string = "2023-12-08T17:27:09"

#startString = "2023-12-04T18:02:43"
#endString = "2023-12-04T18:02:58"
S=Chunks.build_spectrogram_from_range(start_string,end_string)

#S.time_average(2)
#print(S.pseudo_start_time)
S.plot_spectrogram()

#S.plot_power()

#print(S.Sxx[:,10])
#print(S_original.Sxx[:,10])

#print(np.sum(S.Sxx-S_original.Sxx))

