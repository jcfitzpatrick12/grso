import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys

from src.fChunks.Chunks import Chunks
from src.fChunks.Chunk import Chunk
from src.fConfig import CONFIG

class ChunkNavigator:
    def __init__(self, master, tag):
        self.master = master
        master.title("Chunk Navigator")

        self.Chunks = Chunks(tag)
        self.current_chunk_index = len(self.Chunks.dict)-1
        self.current_chunk = self.Chunks.get_chunk_by_index(self.current_chunk_index)

        # Set default values
        self.chunk_start_time = self.current_chunk.chunk_start_time
        self.current_chunk = None
        self.plot_types = ['power', 'dBb', 'raw', 'rawlog']
        self.plot_type_vars = {}

        self.setup_ui()
        self.set_initial_chunk()
        self.plot_data()

    def setup_ui(self):
        self.figure = Figure(figsize=(15, 10))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.prev_button = tk.Button(self.master, text="Previous", command=self.prev_chunk).pack(side=tk.LEFT)
        self.next_button = tk.Button(self.master, text="Next", command=self.next_chunk).pack(side=tk.LEFT)

        self.goto_chunk = tk.Entry(self.master)
        self.goto_chunk.pack(side=tk.LEFT)
        self.goto_button = tk.Button(self.master, text="Go To", command=self.go_to_chunk).pack(side=tk.LEFT)

        self.update = tk.Button(self.master, text="Update", command=self.plot_data).pack(side=tk.LEFT)

        self.exit_button = tk.Button(self.master, text="Exit", command=self.exit_application).pack(side=tk.RIGHT)

        self.create_plot_type_checkboxes()


    def create_plot_type_checkboxes(self):
        self.plot_type_frame = tk.Frame(self.master)
        self.plot_type_frame.pack(side=tk.BOTTOM, fill=tk.X)

        for plot_type in self.plot_types:
            if plot_type in ["power", "dBb"]:
                var = tk.BooleanVar(value=True)
            else: 
                var = tk.BooleanVar(value=False)
            cb = tk.Checkbutton(self.plot_type_frame, text=plot_type, variable=var)
            cb.pack(side=tk.LEFT)
            self.plot_type_vars[plot_type] = var

    def set_initial_chunk(self):
        self.current_chunk = self.Chunks.get_chunk_by_index(self.current_chunk_index)
        self.goto_chunk.insert(0, self.current_chunk.chunk_start_time)

    def get_selected_plot_types(self):
        return [plot_type for plot_type, var in self.plot_type_vars.items() if var.get()]
    
    def update(self):
        self.Chunks = Chunks(CONFIG.path_to_data, Chunk)
        self.plot_data()

    def plot_data(self):
        self.figure.clear()

        if self.current_chunk:
            S = self.current_chunk.fits.load_radio_spectrogram()  
            S = S.time_average(CONFIG.time_average_over_before_plotting) 
            S = S.frequency_average(CONFIG.freq_average_over_before_plotting) 
            selected_plot_types = self.get_selected_plot_types()
            S.stack_plots(self.figure, selected_plot_types)

        self.canvas.draw()

    def change_chunk(self, direction):
        new_index = self.current_chunk_index + direction
        new_chunk = self.Chunks.get_chunk_by_index(new_index)
        if new_chunk:
            self.current_chunk = new_chunk
            self.current_chunk_index = new_index
            self.plot_data()

    def next_chunk(self):
        self.change_chunk(1)

    def prev_chunk(self):
        self.change_chunk(-1)

    def go_to_chunk(self):
        chunk_start_time = self.goto_chunk.get()
        target_chunk = self.Chunks.find_nearest_chunk(chunk_start_time)
        if target_chunk:
            self.current_chunk = target_chunk
            self.current_chunk_index = self.Chunks.get_index_by_chunk(self.current_chunk)
            self.plot_data()

    def exit_application(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    try:
        default_tag = sys.argv[1]
    except:
        default_tag = "00"
    app = ChunkNavigator(root, default_tag)
    root.mainloop()
