import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


class Plotter:  
    def __init__(self):
        self.fsize_head=20
        self.fsize=15

    def plot_power(self,datetime_array,power):
        plt.stairs(10 * np.log10(power),datetime_array)
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
        plt.pcolormesh(datetime_array, freqs_MHZ, 10 * np.log10(Sxx))
        #format the datetime axis 
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=1))  # adjust the interval for your needs
        plt.gcf().autofmt_xdate()
        #assign the x and y labels
        plt.ylabel('Frequency [MHz]',size=self.fsize_head)
        plt.xlabel('Time [GMT]',size=self.fsize_head)
        #create the colorbar
        #cbar = plt.colorbar()
        #cbar.set_label('Intensity [?]', size=self.fsize_head)
        #cbar.ax.tick_params(labelsize=self.fsize)
        #format the x and y tick labels
        plt.xticks(size=self.fsize)
        plt.yticks(size=self.fsize)
        plt.show()
    
