from src.spectrogram.standard.Plotter import Plotter
from src.spectrogram.callisto.Plotter import Plotter as CallistoPlotter

tag_to_plotter_dict = {
            "00": Plotter, 
            "02": Plotter, 
            "03": Plotter, 
            "01": CallistoPlotter
        }