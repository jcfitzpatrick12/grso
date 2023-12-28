import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from fMisc.sys_vars import sys_vars


class Plotter:  
    def __init__(self):
        #plt.style.use("seaborn")
        self.fsize_head=20
        self.fsize=15
        self.sys_vars=sys_vars()

    def plot_power(self,datetime_array,power):
        plt.stairs(power,datetime_array)
        plt.ylim(np.min(power)-np.min(power)*0.05,np.max(power)+np.max(power)*0.05)
        #format the datetime axis 
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=10))  # adjust the interval for your needs
        plt.gcf().autofmt_xdate()
        #assign the x and y labels
        plt.ylabel('Power [?]',size=self.fsize_head)
        plt.xlabel('Time',size=self.fsize_head)
        #format the x and y tick labels
        plt.xticks(size=self.fsize)
        plt.yticks(size=self.fsize)
        plt.show()


    def plot_spectrogram(self,freqs_MHZ, datetime_array, Sxx):
        # Plot the spectrogram
        
        plt.pcolormesh(datetime_array, freqs_MHZ, Sxx)
        #plt.pcolormesh(datetime_array, freqs_MHZ, 10*np.log10(Sxx))
        #format the datetime axis 
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=10))  # adjust the interval for your needs
        plt.gcf().autofmt_xdate()
        #assign the x and y labels
        plt.ylabel('Frequency [MHz]',size=self.fsize_head)
        plt.xlabel('Time [GMT]',size=self.fsize_head)
        #create the colorbar
        #cbar = plt.colorbar(min=1e-17,max=1e-19)
        #cbar.set_label('dB above the [?]', size=self.fsize_head)
        #cbar.ax.tick_params(labelsize=self.fsize)
        #format the x and y tick labels
        plt.xticks(size=self.fsize)
        plt.yticks(size=self.fsize)
        plt.show()
    
