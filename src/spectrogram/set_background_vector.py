import numpy as np
import os
import sys

from src.chunks.plural.Chunks import Chunks
from src.configs import GLOBAL_CONFIG


def save_background(tag):
    background_interval = ["2024-01-31T15:27:00","2024-01-31T15:27:20"]

    chunks = Chunks(tag)
    background_spectrogram = chunks.build_spectrogram_from_range(background_interval[0], background_interval[1])
    background_vector = background_spectrogram.total_time_average()
    
    # Check if the path exists, if not create it
    if not os.path.exists(GLOBAL_CONFIG.path_to_config_data):
        os.makedirs(GLOBAL_CONFIG.path_to_config_data)
        
    np.save(os.path.join(GLOBAL_CONFIG.path_to_config_data,f"background_vector_{tag}"), background_vector)

    try:
        np.load(os.path.join(GLOBAL_CONFIG.path_to_config_data, f"background_vector_{tag}.npy"))
        print(f"Succesfully constructed background vector for tag {tag}.")
    except Exception as e:
        raise SystemError(f"Error making background vector for tag {tag}: {e}")


if __name__=="__main__":
    tags = sys.argv[1:]
    for tag in tags:
        save_background(f"{tag}")



