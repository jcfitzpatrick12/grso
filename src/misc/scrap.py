from src.chunks.plural.Chunks import Chunks
from src.spectrogram import SpectrogramFactory
from src.configs import GLOBAL_CONFIG
from src.configs.BatchConfig import load_config
from matplotlib.figure import Figure
import sys

def main(tag):
    # batch_config = load_config(tag)
    # print(batch_config.get_center_freq())

    chunks = Chunks(tag)

    for chunk_start_time, chunk in chunks.dict.items():
        print(chunk_start_time)
    

if __name__ == "__main__":
    try:
        tag = str(sys.argv[1])
    except:
        raise ValueError("Please specify the tag by passing in through the command line.")
    
    if tag not in GLOBAL_CONFIG.defined_tags:
        raise ValueError(f"Please specify a valid tag. Received {tag}, need one of {GLOBAL_CONFIG.defined_tags}")
        
    main(tag)