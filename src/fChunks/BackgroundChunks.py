from src.fChunks.Chunk import Chunk
from src.fChunks.Chunks import Chunks
from src.fConfig import CONFIG
from src.utils import SpectrogramFuncs

import numpy as np

class BackgroundChunks:
    def return_background_vector(self):
        num_background_times = len(CONFIG.background_times)
        if num_background_times==0:
            raise SystemExit("Please indicate background chunks in self.background_chunk field in CONFIG")
        else:
            background_frequency_vectors =[]
            for pseudo_start_time in CONFIG.background_times:
                background_chunk = Chunk(pseudo_start_time)
                S = background_chunk.fits.load_radio_spectrogram()
                background_frequency_vector = S.total_time_average()
                background_frequency_vectors.append(background_frequency_vector)
            background_frequency_vectors = np.array(background_frequency_vectors)
            return np.mean(background_frequency_vectors,axis=0)
