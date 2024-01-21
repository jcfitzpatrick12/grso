# general variables to change

import os

'''
variables for gnuradio
'''
#the central frequency you wish to observe around [Hz]
#center_freq = 57.5e6
center_freq = 62.5e6
#center_freq = 95.8e6
#the sampling rate of the SDR [samples per second]
samp_rate = 5e6
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
noverlap=int(nperseg/2)
#average over this many integer samples [so that the final spectrograms have a sample rate
# of samp_rate/average_over_int]
average_over_int = 100
#average_over_int=2

'''
Interval overwhich to evaluate the background vector over frequency.
'''
background_interval = ["2024-01-21T16:30:00","2024-01-21T16:31:00"]

'''
plotting  params
'''
seconds_interval=360
dBb_vmin = -2
dBb_vmax = 4
average_over_before_plotting = 100

'''
global config variables
'''
#the default string format for defining the string format for the pseudo_start_time
default_time_format="%Y-%m-%dT%H:%M:%S"
#the path to the data folder
path_to_data = os.path.join(os.environ['GRSOPARENTPATH'],"data")
#the path to the temp_data folder
path_to_temp_data = os.path.join(os.environ['GRSOPARENTPATH'],"temp_data")
#the path to the background_data folder
path_to_background_data = os.path.join(os.environ['GRSOPARENTPATH'],"background_data")










    