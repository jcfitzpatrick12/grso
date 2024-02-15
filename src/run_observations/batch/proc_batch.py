'''
script will convert the binary and header data to fits files in data folder
'''
from src.utils import Tags

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
                print(f"Couldn't make spectrogram for this Chunk! Received the following error: \n{e}")

    my_chunks.remove_non_fits_files_from_data()

if __name__ == '__main__':
    tag = Tags.get_tag_from_args(disable_reserved_tags = True)
    main(tag)