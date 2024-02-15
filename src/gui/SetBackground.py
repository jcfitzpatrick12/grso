import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import sys

from src.spectrogram.Bvect import save_bvect, load_bvect

class SetBackground:
    def __init__(self, master, default_tag):
        self.master = master
        self.master.title("SetBackground")
        self.tag = default_tag
        self.entries = {}  # Initialize the entries dictionary
        self.setup_widgets()
        self.update_tag(default_tag)


    def setup_widgets(self):
        self.tag_entry = self.create_entry("Tag: ", self.tag, 0)
        update_tag_button = tk.Button(self.master, text="Update Tag", command=lambda: self.update_tag(self.tag_entry.get()))
        update_tag_button.grid(row=0, column=2, sticky="ew")

        # Initialize start_background and end_background entry fields
        self.entries['start_background'] = self.create_entry("Start Background: ", "", 1)
        self.entries['end_background'] = self.create_entry("End Background: ", "", 2)

        save_button = tk.Button(self.master, text="Save", command=self.save_background_to_memory)
        save_button.grid(row=8, column=0, sticky="ew")

        plot_button = tk.Button(self.master, text="Load from memory", command=self.plot_data)
        plot_button.grid(row=8, column=2, sticky="ew")

        self.figure = Figure(figsize=(10, 4))  # Adjusted for a more standard aspect ratio
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.master)
        self.canvas.get_tk_widget().grid(row=9, column=0, columnspan=3)


    def update_tag(self, new_tag):
        self.tag = new_tag
        self.set_default_values()
        self.update_entry_fields()

    
    def set_default_values(self):
            try:
                freqs_MHz, bvect, bvect_interval = self.load_background_from_memory()
            except:
                bvect_interval = ["", ""]
            self.default_values = {
                'start_background': bvect_interval[0],
                'end_background': bvect_interval[1],
            }


    def get_field_titles_dict(self):
        field_titles_dict = {
                    'start_background': "Start Background: ",
                    'end_background': "End Background: ",
                }
        return field_titles_dict


    def update_entry_fields(self):
        self.entries = {}
        fields = ['start_background', 'end_background']
        field_titles_dict = self.get_field_titles_dict()
        for i, field in enumerate(fields, start=1):
            self.entries[field] = self.create_entry(field_titles_dict[field], self.default_values[field], i)


    def create_entry(self, label, default, row):
        tk.Label(self.master, text=label).grid(row=row, column=0)
        entry = tk.Entry(self.master)
        entry.grid(row=row, column=1)
        entry.insert(0, default)
        return entry


    def save_background_to_memory(self):
        start_background = self.entries['start_background'].get()
        end_background = self.entries['end_background'].get()
        # Assuming save_background function exists and works as expected
        save_bvect(self.tag, start_background, end_background)


    def load_background_from_memory(self):
        # Input validation and error handling can be added here
        start_background = self.entries['start_background'].get()
        end_background = self.entries['end_background'].get()
        # Assuming load_background function exists and returns the expected data
        freqs_MHz, bvect, bvect_interval = load_bvect(self.tag)
        return freqs_MHz, bvect, bvect_interval

        
    def plot_data(self):
        self.figure.clear()
        freqs_MHz, bvect, bvect_interval = self.load_background_from_memory()
        ax = self.figure.add_subplot(111)
        ax.plot(freqs_MHz, bvect)
        ax.set_xlabel('Frequency [MHz]')
        
        self.canvas.draw()

    def exit_application(self):
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()

    try:
        tag = Tags.get_tag_from_args()
    except:
        print("Using default tag 00")
        tag = "00"
        
    app = SetBackground(root, default_tag)
    root.mainloop()
