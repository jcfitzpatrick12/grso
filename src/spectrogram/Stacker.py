import matplotlib.pyplot as plt

from src.spectrogram.BasePlotter import BasePlotter
 

class Stacker(BasePlotter):  
    def __init__(self, S):
        super().__init__(S)
    
    def stack_plots(self, fig, plot_types):
            
            if len(plot_types)==1:
                is_one_plot=True
            else:
                is_one_plot=False
            
            # # Create a figure with subplots for plots and colorbars
            axs = fig.subplots(len(plot_types), 2, gridspec_kw={'width_ratios': [3, 0.1], 'wspace': 0.05})
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
            # plt.show()

        

