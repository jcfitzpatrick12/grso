from fChunks.Chunks import Chunks
from fMisc.sys_vars import sys_vars
import os 
import numpy as np
import sys

def main(start_string,end_string):
    MyChunks = Chunks()
    S=MyChunks.build_spectrogram_from_range(start_string,end_string)

    #i=500
    #j=530
    #S.Sxx=S.Sxx[i:j,:]
    #S.freqs_MHz=S.freqs_MHz[i:j+1]
    S.time_average(100)
    S.plot_power()
    S.plot_spectrogram()
    #S = S.time_average(100)

if __name__ == '__main__':
    start_string = sys.argv[1]
    end_string = sys.argv[2]
    main(start_string,end_string)


#print(S.Sxx[:,10])
#print(S_original.Sxx[:,10])

#print(np.sum(S.Sxx-S_original.Sxx))

