import os 
import numpy as np
import sys
from src.fChunks.Chunks import Chunks
from src.fConfig import CONFIG

def main(requested_start_str,requested_end_str,requested_plot_types):
    from src.fBackground import set_background_vector
    MyChunks = Chunks()
    S = MyChunks.build_spectrogram_from_range(requested_start_str,requested_end_str)
    S = S.time_average(CONFIG.average_over_before_plotting)
    S.stack_plots(requested_plot_types)


if __name__ == '__main__':
    start_string = sys.argv[1]
    end_string = sys.argv[2]
    requested_plot_type = sys.argv[3:]
    main(start_string,end_string,requested_plot_type)



