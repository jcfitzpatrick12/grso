from fChunks.Chunks import Chunks
from datetime import datetime
import numpy as np

Chunks = Chunks()

look_after = datetime(year=2023,month=12,day=28,hour=15,minute=30)
#look_before = datetime(year=2023,month=12,day=14,hour=17,minute=7)

for Chunk in Chunks.dict.values():
    if Chunk.pseudo_start_datetime <= look_after:
        print('skipping {}'.format(Chunk.pseudo_start_datetime))
        pass
    else:
        print('showing {}'.format(Chunk.pseudo_start_datetime))
        S = Chunk.fits.load_radio_spectrogram()
        #S = S.time_average(100)
        #print(np.mean(S.Sxx))
        #print(np.min(S.Sxx))
        #print(np.max(S.Sxx))
        S.plot_power()
        S.plot_spectrogram()
        