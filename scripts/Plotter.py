import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import scipy.signal as signal
from datetimeFuncs import datetimeFuncs
import matplotlib.dates as mdates


class Plotter:  
    def __init__(self):
        self.fsize_head=20
        self.fsize=15

    def plotSpectrogram(self,frequenciesMHZ, datetimeArray, Sxx):

        # Plot the spectrogram
        plt.pcolormesh(datetimeArray, frequenciesMHZ, 10 * np.log10(Sxx), shading='gouraud')
        #format the datetime axis 
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=1))  # adjust the interval for your needs
        plt.gcf().autofmt_xdate()
        #assign the x and y labels
        plt.ylabel('Frequency [MHz]',size=self.fsize_head)
        plt.xlabel('Time [sec]',size=self.fsize_head)
        #create the colorbar
        cbar = plt.colorbar()
        cbar.set_label('Intensity [dB]', size=self.fsize_head)
        cbar.ax.tick_params(labelsize=self.fsize)
        #format the x and y tick labels
        plt.xticks(size=self.fsize)
        plt.yticks(size=self.fsize)
        plt.show()
    
