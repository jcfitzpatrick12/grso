import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys
import os
from datetime import datetime

# Assuming src.fChunks.Chunks and src.fConfig.CONFIG are available modules
from src.chunks.Chunks import Chunks
from src.spectrogram import SpectrogramFactory
from src.configs import GLOBAL_CONFIG
from src.configs.tag_maps import tag_to_plot_types

class LookBetween:
    def __init__(self, master, default_tag):
        self.master = master
        self.master.title("LookBetween")
        self.tag = default_tag
        self.setup_widgets()
        self.update_tag_and_chunks(default_tag)


    def setup_widgets(self):
        self.tag_entry = self.create_entry("Tag: ", self.tag, 0)
        update_tag_button = tk.Button(self.master, text="Update Tag", command=lambda: self.update_tag_and_chunks(self.tag_entry.get()))
        update_tag_button.grid(row=0, column=2, sticky="ew")

        plot_button = tk.Button(self.master, text="Plot", command=self.plot_data)
        plot_button.grid(row=8, column=0, sticky="ew")
        
        save_button = tk.Button(self.master, text="Save as PDF", command=self.save_figure_as_pdf)
        save_button.grid(row=8, column=2, sticky="ew")

        self.figure = Figure(figsize=(10, 10))
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=3)

    
    def create_entry(self, label, default, row):
        tk.Label(self.master, text=label).grid(row=row, column=0)
        entry = tk.Entry(self.master)
        entry.grid(row=row, column=1)
        entry.insert(0, default)
        return entry


    def create_checkboxes(self, label, plot_types, row):
        label_frame = tk.LabelFrame(self.master, text=label)
        label_frame.grid(row=row, column=0, columnspan=3)
        for plot_type in plot_types:
            check = tk.Checkbutton(label_frame, text=plot_type, variable=self.plot_type_vars[plot_type])
            check.pack(side=tk.LEFT)


    def update_tag_and_chunks(self, new_tag):
        self.tag = new_tag
        self.chunks = Chunks(new_tag)
        self.set_default_values()
        self.update_entry_fields()
        self.draw_plot_types()


    def set_default_values(self):
        default_chunk = self.chunks.get_chunk_by_index(-1)
        default_S = default_chunk.fits.load_radio_spectrogram()
        self.default_values = {
            'start': datetime.strftime(default_S.datetime_array[0], GLOBAL_CONFIG.default_time_format),
            'end': datetime.strftime(default_S.datetime_array[-1], GLOBAL_CONFIG.default_time_format),
            'lower_freq': round(default_S.freqs_MHz[0], 2),
            'upper_freq': round(default_S.freqs_MHz[-1], 2),
            'avg_over_int_time': 1,
            'avg_over_int_freq': 1
        }

    def get_field_titles_dict(self):
        
        field_titles_dict = {
            'start': "Start time: ",
            'end': "End time: ",
            'lower_freq': "Lower frequency [MHz]: ",
            'upper_freq': "Higher frequency [MHz]: ",
            'avg_over_int_time': "Average over int (time): ",
            'avg_over_int_freq': "Average over int (frequency): ",
        }

        return field_titles_dict


    def update_entry_fields(self):
        self.entries = {}
        fields = ['start', 'end', 'lower_freq', 'upper_freq', 'avg_over_int_time', 'avg_over_int_freq']
        field_titles_dict = self.get_field_titles_dict()
        for i, field in enumerate(fields, start=1):
            self.entries[field] = self.create_entry(field_titles_dict[field], self.default_values[field], i)


    def draw_plot_types(self):
        # Clear previous checkboxes if they exist
        if hasattr(self, 'plot_type_frame'):
            for widget in self.plot_type_frame.winfo_children():
                widget.destroy()
        else:
            self.plot_type_frame = tk.LabelFrame(self.master, text="Plot Types:")
            self.plot_type_frame.grid(row=7, column=0, columnspan=3)

        # Draw new checkboxes
        plot_types = tag_to_plot_types.tag_to_plot_types_dict[self.tag]
        self.plot_type_vars = {plot_type: tk.BooleanVar() for plot_type in plot_types}
        for plot_type in plot_types:
            check = tk.Checkbutton(self.plot_type_frame, text=plot_type, variable=self.plot_type_vars[plot_type])
            check.pack(side=tk.LEFT)

    
    def get_selected_plot_types(self):
        """Retrieve a list of selected plot types based on the checkboxes."""
        return [plot_type for plot_type, var in self.plot_type_vars.items() if var.get() == True]


    def get_spectrogram(self):
        # Input validation and error handling can be added here
        start_str = self.entries['start'].get()
        end_str = self.entries['end'].get()
        S = self.chunks.build_spectrogram_from_range(start_str, end_str)
        lower_freq = float(self.entries['lower_freq'].get())
        upper_freq = float(self.entries['upper_freq'].get())
        S = SpectrogramFactory.frequency_chop(S, lower_freq, upper_freq)
        return S


    def plot_data(self):
        self.figure.clear()
        S = self.get_spectrogram()
        
        time_avg = int(self.entries['time_avg'].get())
        freq_avg = int(self.entries['freq_avg'].get())
        
        S = SpectrogramFactory.frequency_average(S, freq_avg)
        S = SpectrogramFactory.time_average(S, time_avg)
        
        selected_plot_types = self.get_selected_plot_types()
        if selected_plot_types:
            S.stack_plots(self.figure, selected_plot_types)

        self.canvas.draw()


    def save_figure_as_pdf(self):
        if not os.path.exists(GLOBAL_CONFIG.path_to_figures):
            os.mkdir(GLOBAL_CONFIG.path_to_figures)
        save_path = os.path.join(GLOBAL_CONFIG.path_to_figures, f"figure_{self.tag}")
        self.figure.savefig(save_path, format='pdf')


    def exit_application(self):
        self.master.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    default_tag = sys.argv[1] if len(sys.argv) > 1 else "00"
    app = LookBetween(root, default_tag)
    root.mainloop()
