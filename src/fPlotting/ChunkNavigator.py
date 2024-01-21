import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime
import sys

from src.fChunks.Chunks import Chunks
from src.fConfig import CONFIG

class ChunkNavigator:
    def __init__(self, master,look_for_chunk_string):
        self.master = master
        master.title("Chunk Navigator")
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Navigation buttons
        self.next_button = tk.Button(master, text="Next", command=self.next_chunk)
        self.next_button.pack(side=tk.RIGHT)
        self.prev_button = tk.Button(master, text="Previous", command=self.prev_chunk)
        self.prev_button.pack(side=tk.LEFT)

        starter_datetime = datetime.strptime(look_for_chunk_string,CONFIG.default_time_format)
        self.Chunks = Chunks()
        current_chunk = self.Chunks.find_nearest_chunk(starter_datetime)
        self.plot_data()



    def plot_data(self):
        self.ax.clear()
        self.ax.plot(self.data[self.current_chunk])
        self.canvas.draw()

    def next_chunk(self):
        self.current_index = (self.current_index + 1) % len(self.data)
        self.plot_data()

    def prev_chunk(self):
        self.current_index = (self.current_index - 1) % len(self.data)
        self.plot_data()

if __name__ == "__main__":
    starter_time_string = sys.argv[1]
    root = tk.Tk()
    app = ChunkNavigator(root,starter_time_string)
    root.mainloop()
