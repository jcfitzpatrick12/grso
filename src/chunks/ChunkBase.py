from datetime import datetime

from src.configs import GLOBAL_CONFIG

class ChunkBase:
    #constructor for SingleFileHandler
    def __init__(self,chunk_start_time, tag):
        #instantiate the timeStampStr field
        self.chunk_start_time = chunk_start_time
        self.tag = tag
        self.time_format = f"{GLOBAL_CONFIG.default_time_format}_{tag}"
        self.chunk_start_datetime = datetime.strptime(self.chunk_start_time, GLOBAL_CONFIG.default_time_format)