from src.fChunks.Chunks import Chunks
from src.utils import SpectrogramFuncs
import matplotlib.pyplot as plt
import numpy as np

def main():
    chunks = Chunks("00")

    n,m = 40, 20
    for chunk_start_time, chunk in chunks.dict.items():        
        # print(chunk_start_time, chunk)
        S = chunk.fits.load_radio_spectrogram()
        S = S.time_average(10)
        S = S.frequency_average(10)
        tar = S.datetime_array
        Sxx = S.Sxx
        bvect = S.background_vector
        dBb = SpectrogramFuncs.Sxx_to_dBb(Sxx, bvect)
        # Sxx_val = Sxx[n,m]
        # bvect_val = bvect[n]
        # dBb = 10*np.log10(Sxx_val/bvect_val)
        # print(tar[0], tar[-1])
        # print(S.Sxx)
        # print(bvect)
        # print(dBb)
        plt.plot(dBb[:,50])
        plt.ylim(-3,3)
        plt.show()
        exit()
        # exit()
    pass

if __name__=="__main__":
    main()