import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm
from src.spectrogram.Stacker import Stacker


class Plotter(Stacker):
    def __init__(self, S):
        super().__init__(S)

        self.plot_type_dict = {
                "power": self.power,
                "dBb": self.dBb,
                "raw": self.raw,
                "rawlog": self.rawlog,
            }


    def get_plot_types(self,):
        return self.plot_type_dict.keys()

    def power(self,ax,cax):
        datetime_array = self.S.datetime_array

        power = self.S.integrated_power()
        ax.stairs(power, datetime_array)
        ax.set_ylim(np.min(power)-np.min(power)*0.05, np.max(power)+np.max(power)*0.05)
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=self.seconds_interval))
        ax.tick_params(axis='x', labelsize=self.fsize)
        ax.tick_params(axis='y', labelsize=self.fsize)
        ax.set_ylabel('Normalised Power', size=self.fsize_head)


    '''
    Spectrogram plotting functions.
    '''

    def Sxx_in_dBb(self, Sxx, bvect):
        bvect_array = np.ones(np.shape(Sxx))
        num_freqs = np.shape(Sxx)[0]
        for freq_bin_ind in range(num_freqs-1):
            bvect_array[freq_bin_ind,:]*=bvect[freq_bin_ind]
        Sxx_dBb = 10*np.log10(Sxx/bvect_array)
        return Sxx_dBb


    def dBb(self, ax, cax):
        datetime_array = self.S.datetime_array
        freqs_MHz = self.S.freqs_MHz
        Sxx = self.S.Sxx
        bvect = self.S.bvect
        Sxx = self.Sxx_in_dBb(Sxx, bvect)

        vmin = -2
        vmax = 2

        pcolor_plot = ax.pcolormesh(datetime_array, freqs_MHz, Sxx, vmin=vmin, vmax=vmax, cmap=self.cmap)
        # Format the x-axis to display time in HH:MM:SS
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=self.seconds_interval))

        # Assign the x and y labels with specified font size
        ax.set_ylabel('Frequency [MHz]', size=self.fsize_head)
        #ax.set_xlabel('Time [GMT]', size=self.fsize_head)

        # Format the x and y tick labels with specified font size
        ax.tick_params(axis='x', labelsize=self.fsize)
        ax.tick_params(axis='y', labelsize=self.fsize)
        cax.axis("On")
        cbar = plt.colorbar(pcolor_plot,ax=ax,cax=cax)
        cbar.set_label('dB above background', size=self.fsize_head)
        cbar.set_ticks(range(vmin, vmax+1, 1))

    
    def rawlog(self, ax=None, cax=None):
        freqs_MHz = self.S.freqs_MHz
        datetime_array = self.S.datetime_array
        Sxx = self.S.Sxx

        # Plot the spectrogram with LogNorm
        pcolor_plot = ax.pcolormesh(datetime_array, freqs_MHz, Sxx, 
                                    norm=LogNorm(vmin=np.min(Sxx[Sxx > 0]), vmax=np.max(Sxx))
                                    , cmap=self.cmap)

        # Format the x-axis to display time in HH:MM:SS
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=self.seconds_interval))

        # Assign the x and y labels with specified font size
        ax.set_ylabel('Frequency [MHz]', size=self.fsize_head)

        # Format the x and y tick labels with specified font size
        ax.tick_params(axis='x', labelsize=self.fsize)
        ax.tick_params(axis='y', labelsize=self.fsize)
        cax.axis("On")
        cbar = plt.colorbar(pcolor_plot,ax=ax,cax=cax)


    def raw(self, ax,cax):
        freqs_MHz = self.S.freqs_MHz
        datetime_array = self.S.datetime_array
        Sxx = self.S.Sxx

        # Plot the spectrogram with fixed vmin and vmax
        pcolor_plot = ax.pcolormesh(datetime_array, freqs_MHz, Sxx, cmap=self.cmap)

        # Format the x-axis to display time in HH:MM:SS
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))
        ax.xaxis.set_major_locator(mdates.SecondLocator(interval=self.seconds_interval))

        # Assign the x and y labels with specified font size
        ax.set_ylabel('Frequency [MHz]', size=self.fsize_head)

        # Format the x and y tick labels with specified font size
        ax.tick_params(axis='x', labelsize=self.fsize)
        ax.tick_params(axis='y', labelsize=self.fsize)