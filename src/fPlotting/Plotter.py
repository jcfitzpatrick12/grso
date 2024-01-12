import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from src.fConfig import CONFIG


class Plotter:  
    def __init__(self):
        #plt.style.use("seaborn")
        self.fsize_head=20
        self.fsize=15

    '''
    assumes that power is normalised to integrate to unity.
    '''

    def plot_power(self,datetime_array,power):
        plt.stairs(power,datetime_array)
        plt.ylim(np.min(power)-np.min(power)*0.05,np.max(power)+np.max(power)*0.05)
        #format the datetime axis 
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=CONFIG.seconds_interval))  # adjust the interval for your needs
        plt.gcf().autofmt_xdate()
        #assign the x and y labels
        plt.ylabel('Normalised Power',size=self.fsize_head)
        plt.xlabel('Time',size=self.fsize_head)
        #format the x and y tick labels
        plt.xticks(size=self.fsize)
        plt.yticks(size=self.fsize)
        plt.show()


    '''
    assumes we are plotting the raw spectrogram data.
    '''

    def plot_raw_spectrogram(self,freqs_MHz, datetime_array, Sxx):
        # Plot the spectrogram with fixed vmin and vmax
        
        plt.pcolormesh(datetime_array, freqs_MHz, Sxx)
        #plt.pcolormesh(datetime_array, freqs_MHz, 10*np.log10(Sxx))

        # Format the x-axis to display time in HH:MM:SS
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=CONFIG.seconds_interval))  # adjust the interval for your needs

        # Rotate date labels automatically
        plt.gcf().autofmt_xdate()

        # Assign the x and y labels with specified font size
        plt.ylabel('Frequency [MHz]', size=self.fsize_head)
        plt.xlabel('Time [GMT]', size=self.fsize_head)

        # Format the x and y tick labels with specified font size
        plt.xticks(size=self.fsize)
        plt.yticks(size=self.fsize)

        # Display the plot
        plt.show()

    '''
    assumes the spectrogram is in units of dB above the background.
    '''

    def plot_spectrogram(self, freqs_MHZ, datetime_array, Sxx):

        vmin=-2
        vmax=14
        # Plot the spectrogram with fixed vmin and vmax
        plt.pcolormesh(datetime_array, freqs_MHZ, Sxx, vmin=vmin, vmax=vmax)

        # Format the x-axis to display time in HH:MM:SS
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=CONFIG.seconds_interval))  # adjust the interval for your needs

        # Rotate date labels automatically
        plt.gcf().autofmt_xdate()

        # Assign the x and y labels with specified font size
        plt.ylabel('Frequency [MHz]', size=self.fsize_head)
        plt.xlabel('Time [GMT]', size=self.fsize_head)

        # Create the colorbar with a title and fixed tick labels
        cbar = plt.colorbar()
        cbar.set_label('dB above background', size=self.fsize_head)
        cbar.set_ticks(range(vmin, vmax, 2))  # Set ticks from -2 to 14 with a step of 2

        # Format the x and y tick labels with specified font size
        plt.xticks(size=self.fsize)
        plt.yticks(size=self.fsize)

        # Display the plot
        plt.show()

    
