from src.spectrogram.plotting.standard.Plotter import Plotter
from src.spectrogram.plotting.callisto.Plotter import Plotter as CallistoPlotter

tag_to_plotter_dict = {
            "00": Plotter, 
            "02": Plotter, 
            "03": Plotter, 
            "01": CallistoPlotter
        }