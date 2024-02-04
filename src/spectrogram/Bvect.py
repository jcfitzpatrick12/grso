from src.chunks.Chunks import Chunks
import os
from src.configs import GLOBAL_CONFIG
import numpy as np

def save_bvect(tag, start_background, end_background):
    chunks = Chunks(tag)
    background_spectrogram = chunks.build_spectrogram_from_range(start_background, end_background)
    freqs_MHz = background_spectrogram.freqs_MHz
    background_vector = background_spectrogram.total_time_average()
    
    # Check if the path exists, if not create it
    if not os.path.exists(GLOBAL_CONFIG.path_to_config_data):
        os.makedirs(GLOBAL_CONFIG.path_to_config_data)
        
    try: 
        np.save(os.path.join(GLOBAL_CONFIG.path_to_config_data,f"bvect_{tag}"), background_vector)
        np.save(os.path.join(GLOBAL_CONFIG.path_to_config_data,f"bvect_freqs_MHz_{tag}"), freqs_MHz)
        print(f"Succesfully saved background vector for tag {tag}.")

    except Exception as e:
        raise SystemError(f"Error saving bvect for tag {tag}: {e}")

def load_bvect(tag):
    try:
        freqs_MHz = np.load(os.path.join(GLOBAL_CONFIG.path_to_config_data, f"bvect_freqs_MHz_{tag}.npy"))
        background_vector = np.load(os.path.join(GLOBAL_CONFIG.path_to_config_data, f"bvect_{tag}.npy"))
        return freqs_MHz, background_vector
    except Exception as e:
        raise SystemError(f"Error loading bvect for tag {tag}: {e}")