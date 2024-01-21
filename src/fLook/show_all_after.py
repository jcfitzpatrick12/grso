import os 
import numpy as np
import sys

from src.fChunks.Chunks import Chunks
from src.fChunks.BackgroundChunks import BackgroundChunks
from src.fConfig import CONFIG
from datetime import datetime


def main(look_after_string, requested_plot_type):
    from src.fBackground import set_background_vector

    look_after = datetime.strptime(look_after_string,CONFIG.default_time_format)
    MyChunks = Chunks()
    for Chunk in MyChunks.dict.values():

        if Chunk.pseudo_start_datetime <= look_after:
            #print('skipping {}'.format(Chunk.pseudo_start_datetime))
            pass

        else:
            print('Showing chunk: {}'.format(Chunk.pseudo_start_datetime))
            S = Chunk.fits.load_radio_spectrogram()
            S = S.time_average(CONFIG.average_over_before_plotting)
            S.plot_power()
            S.convert_to_dB_above_background(background_vector)
            S.plot_spectrogram(units_dB=True)
    
if __name__ == '__main__':
    look_after_string = sys.argv[1]
    requested_plot_type = sys.argv[2]
    main(look_after_string, requested_plot_type)