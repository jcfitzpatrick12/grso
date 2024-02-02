import numpy as np
import os
import matplotlib.pyplot as plt

from src.fChunks.Chunks import Chunks
from src.fChunks.Chunk import Chunk
from src.fConfig import CONFIG
from src.fCallisto.GlasgowCallistoChunk import GlasgowCallistoChunk
from src.utils import ArrayFuncs


def build_background(tag):
    chunks = Chunks(tag)
    background_spectrogram = chunks.get_background_spectrogram()
    background_vector = background_spectrogram.total_time_average()
    
    # Check if the path exists, if not create it
    if not os.path.exists(CONFIG.path_to_background_data):
        os.makedirs(CONFIG.path_to_background_data)
        
    np.save(os.path.join(CONFIG.path_to_background_data,f"background_vector_{tag}"), background_vector)

    try:
        np.load(os.path.join(CONFIG.path_to_background_data, f"background_vector_{tag}.npy"))
        print(f"Succesfully constructed background vector for tag {tag}.")
    except Exception as e:
        raise SystemError(f"Error making background vector for tag {tag}: {e}")


if __name__=="__main__":
    build_background("00")
    build_background("01")



