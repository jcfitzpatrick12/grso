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
                "raw": self.raw,
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