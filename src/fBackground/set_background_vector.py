from src.fChunks.Chunks import Chunks
from src.fConfig import CONFIG
import numpy as np
import os

MyChunks = Chunks()
try:
    background_spectrogram = MyChunks.get_background_spectrogram()
except:
    raise ValueError("Choose a valid background interval.")
background_vector = background_spectrogram.total_time_average()

# Check if the path exists, if not create it
if not os.path.exists(CONFIG.path_to_background_data):
    os.makedirs(CONFIG.path_to_background_data)

np.save(os.path.join(CONFIG.path_to_background_data,"background_vector"), background_vector)



