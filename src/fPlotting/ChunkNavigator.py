import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime
import sys

from src.fChunks.Chunks import Chunks
from src.fConfig import CONFIG

class ChunkNavigator:
    def __init__(self, master, starter_pseudo_start_time):
        self.master = master
        master.title("Chunk Navigator")
        
        # Initialize the figure for plotting
        self.figure = Figure(figsize=(15, 10))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Navigation buttons
        self.next_button = tk.Button(master, text="Next", command=self.next_chunk)
        self.next_button.pack(side=tk.RIGHT)
        self.prev_button = tk.Button(master, text="Previous", command=self.prev_chunk)
        self.prev_button.pack(side=tk.LEFT)

        # Go To button and entry
        self.goto_entry = tk.Entry(master)
        self.goto_entry.pack(side=tk.LEFT)
        self.goto_entry.insert(0, starter_pseudo_start_time)  # Initialize with starter_pseudo_start_time
        self.goto_button = tk.Button(master, text="Go To", command=self.go_to_chunk)
        self.goto_button.pack(side=tk.LEFT)

        self.Chunks = Chunks()
        self.current_chunk = self.Chunks.find_nearest_chunk(starter_pseudo_start_time)
        self.plot_data()

        # Exit button
        self.exit_button = tk.Button(master, text="Exit", command=self.exit_application)
        self.exit_button.pack(side=tk.BOTTOM)

    def plot_data(self):
        # Clear the figure before plotting new data
        self.figure.clear()

        # Load and process the data for the current chunk
        S = self.current_chunk.fits.load_radio_spectrogram()  
        S = S.time_average(CONFIG.average_over_before_plotting)  
        S.stack_plots(self.figure, ["power", "raw"])

        # Redraw the canvas with the new plot
        self.canvas.draw()

    def next_chunk(self):
        next_chunk = self.Chunks.find_nearest_neighbour(self.current_chunk)
        if next_chunk:
            self.current_chunk = next_chunk
            self.plot_data()

    def prev_chunk(self):
        prev_chunk = self.Chunks.find_nearest_neighbour(self.current_chunk, go_backwards=True)
        if prev_chunk:
            self.current_chunk = prev_chunk
            self.plot_data()

    def go_to_chunk(self):
        pseudo_start_time = self.goto_entry.get()
        target_chunk = self.Chunks.find_nearest_chunk(pseudo_start_time)
        if target_chunk:
            self.current_chunk = target_chunk
            self.plot_data()

    def exit_application(self):
        self.master.destroy()

if __name__ == "__main__":
    starter_pseudo_start_time = sys.argv[1]
    root = tk.Tk()
    app = ChunkNavigator(root, starter_pseudo_start_time)
    root.mainloop()
