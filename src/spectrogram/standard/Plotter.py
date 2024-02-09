from src.spectrogram.Stacker import Stacker


class Plotter(Stacker):
    def __init__(self, S):
        super().__init__(S)

        #any values specified below will override the defaults specified in BasePlotter
        self.v_min = -1
        self.v_max = 1