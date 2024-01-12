import os 
import numpy as np
import sys

from src.fChunks.Chunks import Chunks
from src.fChunks.BackgroundChunks import BackgroundChunks
from src.fConfig import CONFIG

def main(start_string,end_string):
    background_vector = BackgroundChunks().return_background_vector()
    MyChunks = Chunks()
    S=MyChunks.build_spectrogram_from_range(start_string,end_string)
    S=S.time_average(10)
    S.plot_power()
    S.convert_to_dB_above_background(background_vector)
    S.plot_spectrogram(units_dB=True)

if __name__ == '__main__':
    start_string = sys.argv[1]
    end_string = sys.argv[2]
    main(start_string,end_string)


#print(S.Sxx[:,10])
#print(S_original.Sxx[:,10])

#print(np.sum(S.Sxx-S_original.Sxx))

