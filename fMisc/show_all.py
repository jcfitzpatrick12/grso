from fChunks.Chunks import Chunks

Chunks = Chunks()

for Chunk in Chunks.dict.values():
    S = Chunk.fits.load_radio_spectrogram()
    S.plot_spectrogram()