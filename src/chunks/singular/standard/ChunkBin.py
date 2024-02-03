import numpy as np
import os

from src.utils import DatetimeFuncs
from src.configs import GLOBAL_CONFIG

'''
The bin file contains the raw IQ data.
'''
class ChunkBin:
    def __init__(self,chunk_start_time, tag):
        self.chunk_start_time=chunk_start_time
        self.tag = tag
        self.data_dir=DatetimeFuncs.build_data_dir_from_chunk_start_time(GLOBAL_CONFIG.path_to_data, self.chunk_start_time)

    #find the path to data
    def get_path(self):
        return os.path.join(self.data_dir,f"{self.chunk_start_time}_{self.tag}")
    
    def exists(self):
        return os.path.exists(self.get_path())

    #function to convert 
    def get_IQ_data(self):
        #open the header file
        fh = open(self.get_path(), "rb")
        #extract the data
        IQ_data = np.fromfile(fh, dtype=np.complex64)
        #return the data
        return IQ_data
