import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm
from src.fConfig import CONFIG
import os
from src.utils import SpectrogramFuncs
 

class SpectrogramPlotter:  
    def __init__(self,S):
        self.S = S
        #plt.style.use("seaborn")
        self.fsize_head=20
        self.fsize=15

        self.plot_type_dict = {
            "power": self.plot_power,
            "dBb": self.plot_spectrogram_dBb,
            "raw": self.plot_spectrogram_raw,
            "rawlog": self.plot_spectrogram_rawlog,
        }


        
    def get_plot_func(self, plot_type):
        return self.plot_type_dict[plot_type]

    def get_plot_kwargs(self, plot_type):
        return self.plot_kwargs_dict[plot_type]
    
    def stack_plots(self, plot_types, **kwargs):
            if len(plot_types)==1:
                is_one_plot=True
            else:
                is_one_plot=False
            # Create a figure with subplots for plots and colorbars
            fig, axs = plt.subplots(len(plot_types), 2, figsize=(15,10),
                                    gridspec_kw={'width_ratios': [3, 0.1], 'wspace': 0.05})
            # Iterate over the plot types and their respective axes
            for idx, plot_type in enumerate(plot_types):

                if not is_one_plot:
                    ax = axs[idx, 0]  # Plot on the first column
                    cax = axs[idx, 1]  # Colorbar on the second column
                else:
                    ax=axs[0]
                    cax=axs[1]

                cax.axis('off')  # Initially turn off the colorbar axis; it will be turned on if needed

                # Get the plotting function
                plot_func = self.get_plot_func(plot_type)

                # Call the plotting function with its specific kwargs
                plot_func(ax=ax, cax=cax)  # Pass both plot and colorbar axes

                # Hide x-axis labels for all but the bottom plot
                if idx < len(plot_types) - 1:
                    ax.tick_params(labelbottom=False)
                
                if idx ==len(plot_types)-1 or is_one_plot:
                    ax.set_xlabel('Time [GMT]', size=self.fsize_head)

            # Automatically adjust subplot params for better layout
            plt.tight_layout()

            # Show the stacked plot
            plt.show()


    '''
    assumes that power is normalised to integrate to unity.
    '''

    def plot_power(self,ax,cax):
        datetime_array = self.S.datetime_array
        power = self.S.power
        ax.stairs(power, datetime_array)
        ax.set_ylim(np.min(power)-np.min(power)*0.05, np.max(power)+np.max(power)*0.05)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=CONFIG.seconds_interval))
        ax.tick_params(axis='x', labelsize=self.fsize)
        ax.tick_params(axis='y', labelsize=self.fsize)
        ax.set_ylabel('Normalised Power', size=self.fsize_head)


    '''
    Spectrogram plotting functions.
    '''


    def plot_spectrogram_dBb(self, ax, cax):
        datetime_array = self.S.datetime_array
        freqs_MHz = self.S.freqs_MHz
        Sxx = self.S.Sxx
        background_vector = np.load(os.path.join(CONFIG.path_to_background_data, "background_vector.npy"))
        Sxx = SpectrogramFuncs.Sxx_to_dBb(Sxx, background_vector)

        vmin = CONFIG.dBb_vmin
        vmax = CONFIG.dBb_vmax

        pcolor_plot = ax.pcolormesh(datetime_array, freqs_MHz, Sxx, vmin=vmin, vmax=vmax)

        # Format the x-axis to display time in HH:MM:SS
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=CONFIG.seconds_interval))

        # Assign the x and y labels with specified font size
        ax.set_ylabel('Frequency [MHz]', size=self.fsize_head)
        #ax.set_xlabel('Time [GMT]', size=self.fsize_head)

        # Format the x and y tick labels with specified font size
        ax.tick_params(axis='x', labelsize=self.fsize)
        ax.tick_params(axis='y', labelsize=self.fsize)
        cax.axis("On")
        cbar = plt.colorbar(pcolor_plot,ax=ax,cax=cax)
        cbar.set_label('dB above background', size=self.fsize_head)
        cbar.set_ticks(range(vmin, vmax, 2))





    
    def plot_spectrogram_rawlog(self, ax=None, cax=None):
        freqs_MHz = self.S.freqs_MHz
        datetime_array = self.S.datetime_array
        Sxx = self.S.Sxx

        # Plot the spectrogram with LogNorm
        pcolor_plot = ax.pcolormesh(datetime_array, freqs_MHz, Sxx, 
                                    norm=LogNorm(vmin=np.min(Sxx[Sxx > 0]), vmax=np.max(Sxx)))

        # Format the x-axis to display time in HH:MM:SS
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=CONFIG.seconds_interval))

        # Assign the x and y labels with specified font size
        ax.set_ylabel('Frequency [MHz]', size=self.fsize_head)

        # Format the x and y tick labels with specified font size
        ax.tick_params(axis='x', labelsize=self.fsize)
        ax.tick_params(axis='y', labelsize=self.fsize)
        cax.axis("On")
        cbar = plt.colorbar(pcolor_plot,ax=ax,cax=cax)


    def plot_spectrogram_raw(self, ax,cax):
        freqs_MHz = self.S.freqs_MHz
        datetime_array = self.S.datetime_array
        Sxx = self.S.Sxx

        # Plot the spectrogram with fixed vmin and vmax
        pcolor_plot = ax.pcolormesh(datetime_array, freqs_MHz, Sxx)

        # Format the x-axis to display time in HH:MM:SS
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=CONFIG.seconds_interval))

        # Assign the x and y labels with specified font size
        ax.set_ylabel('Frequency [MHz]', size=self.fsize_head)

        # Format the x and y tick labels with specified font size
        ax.tick_params(axis='x', labelsize=self.fsize)
        ax.tick_params(axis='y', labelsize=self.fsize)
        cax.axis("On")
        cbar = plt.colorbar(pcolor_plot,ax=ax,cax=cax)

