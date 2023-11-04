'''
single method class to load a spectrogram
'''

import pickle
import numpy as np
from sys_vars import sys_vars
import os

class LoadSpectrogram:
    def __init__(self):
        self.sys_vars = sys_vars()

    def load(self,pseudo_start_time,wantCompressed):
        # Load the array from the .npy file
        loaded_array = np.load(self.returnPath(pseudo_start_time,wantCompressed), allow_pickle=True)
        # Convert the array back to a byte stream
        byte_stream = loaded_array.tobytes()
        # Deserialize the instance from bytes using pickle
        instance = pickle.loads(byte_stream)
        return instance

    def returnPath(self,pseudo_start_time,wantCompressed):
        if wantCompressed:
            fpath = os.path.join(self.sys_vars.pathtoPdata,"C"+pseudo_start_time+".npy")
        else:
            fpath = os.path.join(self.sys_vars.pathtoPdata,pseudo_start_time+".npy")
        return fpath

