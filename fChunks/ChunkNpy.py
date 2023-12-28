import numpy as np
import os
import pickle

from fMisc.sys_vars import sys_vars


class ChunkNpy:
    def __init__(self,pseudo_start_time):
        self.sys_vars=sys_vars()
        self.pseudo_start_time=pseudo_start_time
        self.path = self.get_path()

    #find the path to the binary
    def get_path(self):
        return os.path.join(self.sys_vars.path_to_data,self.pseudo_start_time+".npy")
    
    #find out if the path exists
    def exists(self):
        return os.path.exists(self.path)
    
    def load_radio_spectrogram(self):
        if self.exists():
            # Load the array from the .npy file
            loaded_array = np.load(self.get_path(), allow_pickle=True)
            # Convert the array back to a byte stream
            byte_stream = loaded_array.tobytes()
            # Deserialize the instance from bytes using pickle
            instance = pickle.loads(byte_stream)
        else:
            raise SystemError('No file found!')
        return instance