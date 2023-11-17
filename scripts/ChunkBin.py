import numpy as np
import os
from sys_vars import sys_vars

'''
The bin file contains the raw IQ data.
'''
class ChunkBin:
    def __init__(self,pseudo_start_time):
        self.sys_vars=sys_vars()
        self.pseudo_start_time=pseudo_start_time
        self.path = self.getPath()

    #find the path to the binary
    def getPath(self):
        return os.path.join(self.sys_vars.path_to_data,self.pseudo_start_time)
    
    def exists(self):
        return os.path.exists(self.path)

    #function to convert 
    def getIQData(self):
        #open the header file
        fh = open(self.path, "rb")
        #extract the data
        IQdata = np.fromfile(fh, dtype=np.complex64)
        #return the data
        return IQdata
