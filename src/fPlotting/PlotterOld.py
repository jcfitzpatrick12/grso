import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm
from src.fConfig import CONFIG
import os
from src.utils import SpectrogramFuncs
 

class Plotter:  
    def __init__(self):
        #plt.style.use("seaborn")
        self.fsize_head=20
        self.fsize=15
        
        self.spectrogram_plot_type = {
            "dBb": self.plot_spectrogram_dBb,
            "raw": self.plot_spectrogram_raw,
            "rawlog": self.plot_spectrogram_rawlog,
        }

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
    Spectrogram plotting functions.
    '''


    def get_plot_spectrogram_func(self, plot_type):
        try:
            return self.spectrogram_plot_type[plot_type]
        except:
            raise ValueError(f"Warning! Error fetching function. Check {plot_type} is a valid plot_type.")
    
    def plot_spectrogram_rawlog(self,freqs_MHz, datetime_array, Sxx):
        # Plot the spectrogram with LogNorm
        spectrogram = plt.pcolormesh(datetime_array, freqs_MHz, Sxx, norm=LogNorm(vmin=np.min(Sxx[Sxx > 0]), vmax=np.max(Sxx)))

        # Format the x-axis to display time in HH:MM:SS
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        plt.gca().xaxis.set_major_locator(mdates.SecondLocator(interval=CONFIG.seconds_interval))  # Adjust the interval as needed

        # Rotate date labels automatically
        plt.gcf().autofmt_xdate()

        # Assign the x and y labels with specified font size
        plt.ylabel('Frequency [MHz]', size=self.fsize_head)
        plt.xlabel('Time [GMT]', size=self.fsize_head)

        # Format the x and y tick labels with specified font size
        plt.xticks(size=self.fsize)
        plt.yticks(size=self.fsize)

        # Add a colorbar
        plt.colorbar(spectrogram, ax=plt.gca())

        # Display the plot
        plt.show()

    def plot_spectrogram_raw(self,freqs_MHz, datetime_array, Sxx):
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

    def plot_spectrogram_dBb(self, freqs_MHZ, datetime_array, Sxx):

        background_vector=np.load(os.path.join(CONFIG.path_to_background_data,"background_vector.npy"))
        #background_vector = Chunks().return_background_vector()
        Sxx = SpectrogramFuncs.Sxx_to_dBb(Sxx,background_vector)

        vmin=CONFIG.dBb_vmin
        vmax=CONFIG.dBb_vmax
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

    
