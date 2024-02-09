import os

from src.utils import DatetimeFuncs
from src.configs import GLOBAL_CONFIG

class ChunkExt:
    def __init__(self,chunk_start_time, tag, ext):
        self.chunk_start_time=chunk_start_time
        self.tag = tag
        self.ext = ext
        self.data_dir=DatetimeFuncs.build_data_dir_from_chunk_start_time(GLOBAL_CONFIG.path_to_data, self.chunk_start_time)

    #find the path to data
    def get_path(self):
        return os.path.join(self.data_dir,f"{self.chunk_start_time}_{self.tag}{self.ext}")
    
    #find out if the path exists
    def exists(self):
        return os.path.exists(self.get_path())
    