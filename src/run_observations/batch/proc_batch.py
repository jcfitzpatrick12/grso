'''
script will convert the binary and header data to fits files in data folder
'''
import sys

from src.chunks.Chunks import Chunks
from src.spectrogram import SpectrogramFactory
from src.configs import GLOBAL_CONFIG
from src.configs.JsonConfig import load_config

def main(tag):
    config_dict = load_config("batch", tag)
    my_chunks=Chunks(tag)
    for chunk in my_chunks.dict.values():
        if chunk.fits.exists():
            pass
        else:
            try:
                S = chunk.build_radio_spectrogram()
                average_over_int = config_dict['average_over_int']
                S = SpectrogramFactory.time_average(S, average_over_int)
                S.save_to_fits()
            except Exception as e:
                print(f"Couldn't make spectrogram for this Chunk! {e}")

    my_chunks.remove_non_fits_files_from_data()

if __name__ == '__main__':
    try:
        tag = str(sys.argv[1])
    except:
        raise ValueError("Please specify the tag by passing in through the command line.")
    
    if tag not in GLOBAL_CONFIG.defined_tags:
        raise ValueError(f"Please specify a valid tag. Received {tag}, need one of {GLOBAL_CONFIG.defined_tags}")

    main(tag)