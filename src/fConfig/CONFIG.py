# general variables to change

import os

'''
variables for gnuradio
'''
#the central frequency you wish to observe around [Hz]
center_freq = 50.95e6
#center_freq = 440e6
#the sampling rate of the SDR [samples per second]
samp_rate = 1e6
#samp_rate = 300e3
#value of IF_gain [dB]
#IF_gain = -50
IF_gain=-25

'''
signal.spectrogram params
'''
window_type = "hann"
window_size = 2048
nperseg = int(window_size)
noverlap = int(nperseg/2)
#average over this many integer samples [so that the final spectrograms have a sample rate
# of samp_rate/average_over_int]
average_over_int = 100

'''
Interval overwhich to evaluate the background vector over frequency.
'''

background_interval = ["2024-01-29T14:00:00","2024-01-29T14:01:00"]

'''
plotting  params
'''

seconds_interval = 10
dBb_vmin = -1
dBb_vmax = 1
time_average_over_before_plotting = 10
freq_average_over_before_plotting = 20

'''
callisto fetching data variables
'''

max_range_days = 7

'''
chunk_start_time formats
'''

#the default string format for defining the string format for the chunk_start_time
default_time_format = "%Y-%m-%dT%H:%M:%S"
glasgow_callisto_time_format = "GLASGOW_%Y%m%d_%H%M%S_01"


'''
global config variables
'''

#the path to the data folder
path_to_data = os.path.join(os.environ['GRSOPARENTPATH'],"data")
#the path to the temp_data folder
path_to_temp_data = os.path.join(os.environ['GRSOPARENTPATH'],"temp_data")
#the path to the background_data folder
path_to_background_data = os.path.join(os.environ['GRSOPARENTPATH'],"background_data")
#the path to the glasgow_callisto_data folder
path_to_glasgow_callisto_data = os.path.join(os.environ['GRSOPARENTPATH'],"glasgow_callisto_data")
#the path to figures
path_to_figures = os.path.join(os.environ['GRSOPARENTPATH'],"figures")








    