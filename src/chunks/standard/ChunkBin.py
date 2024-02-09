import numpy as np

from src.chunks.ChunkExt import ChunkExt

'''
The bin file contains the raw IQ data.
'''
class ChunkBin(ChunkExt):
    def __init__(self,chunk_start_time, tag):
        # there is no file extension for binary files
        super().__init__(chunk_start_time, tag, "")

    #function to convert 
    def get_IQ_data(self):
        #open the header file
        fh = open(self.get_path(), "rb")
        #extract the data
        IQ_data = np.fromfile(fh, dtype=np.complex64)
        #return the data
        return IQ_data
