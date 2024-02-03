import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os

# Assuming src.fChunks.Chunks and src.fConfig.CONFIG are available modules
# from your project structure with the necessary methods and attributes.
from src.chunks.plural.Chunks import Chunks
from src.spectrogram import SpectrogramFactory
from src.configs import GLOBAL_CONFIG
from src.configs.tag_maps import tag_to_plot_types

class LookBetween:
    def __init__(self, master, default_tag):
        self.master = master
        self.master.title("LookBetween")
        self.tag = default_tag
        self.chunks = Chunks(self.tag)
        self.setup_widgets()

    def setup_widgets(self):
        # Add entry for dynamically updating the tag
        self.set_default_values()
        
        self.tag_entry = self.create_entry("Tag: ", self.tag, 0)
        update_tag_button = tk.Button(self.master, text="Update Tag", command=self.update_tag_and_chunks)
        update_tag_button.grid(row=0, column=2, sticky="ew")

        # Entry fields for ranges, frequencies, and averaging
        self.start_entry = self.create_entry("Start Range:", self.default_start, 1)
        self.end_entry = self.create_entry("End Range:", self.default_end, 2)
        self.lower_freq_entry = self.create_entry("Lower Frequency (MHz):", self.default_lower_freq, 3)
        self.upper_freq_entry = self.create_entry("Upper Frequency (MHz):", self.default_upper_freq, 4)
        self.time_avg_entry = self.create_entry("Average over n bins (time):", self.default_time_avg_entry, 5)
        self.freq_avg_entry = self.create_entry("Average over n bins (frequency):", self.default_freq_avg_entry, 6)

        self.draw_plot_types()

        plot_button = tk.Button(self.master, text="Plot", command=self.plot_data)
        plot_button.grid(row=8, column=0, sticky="ew")
        
        save_button = tk.Button(self.master, text="Save as PDF", command=self.save_figure_as_pdf)
        save_button.grid(row=8, column=1, sticky="ew")

        self.figure = Figure(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=2)

    def draw_plot_types(self):
        # Layout adjustments for checkboxes and buttons
        plot_types = tag_to_plot_types.tag_to_plot_types_dict[self.tag]
        self.plot_type_vars = {plot_type: tk.BooleanVar() for plot_type in plot_types}
        self.create_checkboxes("Plot Types:", plot_types, 7)


    def set_default_values(self):
        # Adjust the row indices for other widgets accordingly
        default_chunk_0 = self.chunks.get_chunk_by_index(-2)
        default_chunk_1 = self.chunks.get_chunk_by_index(-1)
        default_S = default_chunk_0.fits.load_radio_spectrogram()
        # Set default values
        self.default_start = default_chunk_0.chunk_start_time
        self.default_end = default_chunk_1.chunk_start_time
        self.default_lower_freq = round(default_S.freqs_MHz[0], 2)
        self.default_upper_freq = round(default_S.freqs_MHz[-1], 2)
        self.default_time_avg_entry = 1
        self.default_freq_avg_entry = 1


    def update_tag_and_chunks(self):
        """Update the chunks based on the entered tag string."""
        new_tag = self.tag_entry.get()
        self.tag = new_tag

        self.chunks = Chunks(new_tag)
        self.draw_plot_types()


    def get_selected_plot_types(self):
        """Retrieve a list of selected plot types based on the checkboxes."""
        return [plot_type for plot_type, var in self.plot_type_vars.items() if var.get() == True]

    def create_entry(self, label, default, row):
        tk.Label(self.master, text=label).grid(row=row, column=0)
        entry = tk.Entry(self.master)
        entry.grid(row=row, column=1)
        entry.insert(0, default)
        return entry

    def create_checkboxes(self, label, plot_types, row):
        label_frame = tk.LabelFrame(self.master, text=label)
        label_frame.grid(row=row, column=0, columnspan=2)
        for plot_type in plot_types:
            check = tk.Checkbutton(label_frame, text=plot_type, variable=self.plot_type_vars[plot_type])
            check.pack(side=tk.LEFT)

    def get_spectrogram(self):
        start_str = self.start_entry.get()
        end_str = self.end_entry.get()
        lower_freq = float(self.lower_freq_entry.get())
        upper_freq = float(self.upper_freq_entry.get())
        S = self.chunks.build_spectrogram_from_range(start_str, end_str)
        S = SpectrogramFactory.frequency_chop(S, lower_freq, upper_freq)
        return S

    def plot_data(self):
        self.figure.clear()
        S = self.get_spectrogram()
        
        time_avg = int(self.time_avg_entry.get())
        freq_avg = int(self.freq_avg_entry.get())
        S = SpectrogramFactory.time_average(S, time_avg)
        S = SpectrogramFactory.frequency_average(S, freq_avg)

        selected_plot_types = self.get_selected_plot_types()
        if selected_plot_types:
            S.stack_plots(self.figure, selected_plot_types)
        self.canvas.draw()

    def save_figure_as_pdf(self):
        if not os.path.exists(GLOBAL_CONFIG.path_to_figures):
            os.mkdir(GLOBAL_CONFIG.path_to_figures)
        save_path = os.path.join(GLOBAL_CONFIG.path_to_figures, "figure.pdf")  # Updated to a generic name for demonstration
        self.figure.savefig(save_path, format='pdf')

    def exit_application(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    try:
        default_tag = sys.argv[1]
    except:
        default_tag = "00"
    app = LookBetween(root, default_tag)
    root.mainloop()
