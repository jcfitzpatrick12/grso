from src.fCallisto.GlasgowCallistoChunk import GlasgowCallistoChunk
from src.fChunks.Chunks import Chunks
from src.fChunks.Chunk import Chunk
from src.fConfig import CONFIG


### Deal with multiple backgrounds! Include a tag or something and save in background data.
### then at instantiation can specify a tag for the backgroud vector for RadioSpectrogram
def main():
    callisto_chunks = Chunks(CONFIG.path_to_glasgow_callisto_data, CONFIG.glasgow_callisto_time_format, GlasgowCallistoChunk)
    for chunk_start_time, chunk in callisto_chunks.dict.items():
        S = chunk.fits.load_radio_spectrogram()
        break
    pass

if __name__ == "__main__":
    main()