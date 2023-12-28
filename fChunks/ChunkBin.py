import numpy as np
import os

from fMisc.sys_vars import sys_vars
from fMisc.DatetimeFuncs import DatetimeFuncs 

'''
The bin file contains the raw IQ data.
'''
class ChunkBin:
    def __init__(self,pseudo_start_time):
        self.sys_vars=sys_vars()
        self.pseudo_start_time=pseudo_start_time
        self.data_dir=DatetimeFuncs().build_data_dir_from_pseudo_start_time(self.pseudo_start_time)

    #find the path to data
    def get_path(self):
        return os.path.join(self.data_dir,self.pseudo_start_time)
    
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
