'''
chunkFile class deals with all files of the form %Y-%m-%dT%H:%M:%S[.EXT]
'''

import numpy as np
from datetime import datetime
from src.configs import GLOBAL_CONFIG
from src.chunks.singular.callisto.ChunkFits import ChunkFits as CallistoChunkFits

'''
ChunkFiles are characterised by chunk_start_time
'''

class Chunk:
    #constructor for SingleFileHandler
    def __init__(self,chunk_start_time, tag):
        #instantiate the timeStampStr field
        self.chunk_start_time = chunk_start_time
        self.tag = tag
        #type of the file
        #extract the datetime from chunk_start_time
        self.chunk_start_datetime = datetime.strptime(self.chunk_start_time, GLOBAL_CONFIG.default_time_format)
        self.fits = CallistoChunkFits(chunk_start_time, self.tag)


