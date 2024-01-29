import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os

# Assuming src.fChunks.Chunks and src.fConfig.CONFIG are available modules
# from your project structure with the necessary methods and attributes.
from src.fChunks.Chunks import Chunks
from src.fChunks.Chunk import Chunk
from src.fConfig import CONFIG
from src.fCallisto.GlasgowCallistoChunk import GlasgowCallistoChunk

class LookBetween:
    def __init__(self, master):
        self.master = master
        self.master.title("LookBetween")
        self.default_tag = "00"
        self.chunks = Chunks(self.default_tag)
        self.setup_widgets()

    def setup_widgets(self):
        # Add entry for dynamically updating the tag
        self.tag_entry = self.create_entry("Tag String:", self.default_tag, 0)
        update_tag_button = tk.Button(self.master, text="Update Tag", command=self.update_tag_and_chunks)
        update_tag_button.grid(row=0, column=2, sticky="ew")

        # Adjust the row indices for other widgets accordingly
        default_chunk_0 = self.chunks.get_chunk_by_index(0)
        default_chunk_1 = self.chunks.get_chunk_by_index(1)
        default_S = default_chunk_0.fits.load_radio_spectrogram()

        # Set default values
        default_start = default_chunk_0.chunk_start_time
        default_end = default_chunk_1.chunk_start_time
        default_lower_freq = round(default_S.freqs_MHz[0], 2)
        default_upper_freq = round(default_S.freqs_MHz[-1], 2)

        # Entry fields for ranges, frequencies, and averaging
        self.start_entry = self.create_entry("Start Range:", default_start, 1)
        self.end_entry = self.create_entry("End Range:", default_end, 2)
        self.lower_freq_entry = self.create_entry("Lower Frequency (MHz):", default_lower_freq, 3)
        self.upper_freq_entry = self.create_entry("Upper Frequency (MHz):", default_upper_freq, 4)
        self.time_avg_entry = self.create_entry("Time Averaging (s):", CONFIG.time_average_over_before_plotting, 5)
        self.freq_avg_entry = self.create_entry("Frequency Averaging (MHz):", CONFIG.freq_average_over_before_plotting, 6)

        # Layout adjustments for checkboxes and buttons
        plot_types = ['power', 'dBb', 'raw', 'rawlog']
        self.plot_type_vars = {plot_type: tk.BooleanVar() for plot_type in plot_types}
        self.create_checkboxes("Plot Types:", plot_types, 7)

        plot_button = tk.Button(self.master, text="Plot", command=self.plot_data)
        plot_button.grid(row=8, column=0, sticky="ew")
        
        save_button = tk.Button(self.master, text="Save as PDF", command=self.save_figure_as_pdf)
        save_button.grid(row=8, column=1, sticky="ew")

        self.figure = Figure(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=2)

    def update_tag_and_chunks(self):
        """Update the chunks based on the entered tag string."""
        new_tag = self.tag_entry.get()
        self.chunks = Chunks(new_tag)
        self.refresh_gui_for_new_chunks()

    def refresh_gui_for_new_chunks(self):
        """Refresh GUI components to reflect the updated chunks."""
        # Here you would refresh the GUI components that depend on the chunks variable.
        # For demonstration, let's just update the default values for the start and end range entries.
        default_chunk_0 = self.chunks.get_chunk_by_index(0) if self.chunks.chunks else None
        default_chunk_1 = self.chunks.get_chunk_by_index(1) if len(self.chunks.chunks) > 1 else None
        if default_chunk_0 and default_chunk_1:
            self.start_entry.delete(0, tk.END)
            self.start_entry.insert(0, default_chunk_0.chunk_start_time)
            
            self.end_entry.delete(0, tk.END)
            self.end_entry.insert(0, default_chunk_1.chunk_start_time)

    def create_entry(self, label, default, row):
        tk.Label(self.master, text=label).grid(row=row, column=0)
        entry = tk.Entry(self.master)
        entry.grid(row=row, column=1)
        entry.insert(0, default)
        return entry

    # The rest of your class definition remains the same...

if __name__ == "__main__":
    root = tk.Tk()
    app = LookBetween(root)
    root.mainloop()
