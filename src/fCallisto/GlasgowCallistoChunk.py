'''
chunkFile class deals with all files of the form %Y-%m-%dT%H:%M:%S[.EXT]
'''

import numpy as np
from datetime import datetime
from src.fConfig import CONFIG
from src.fCallisto.GlasgowCallistoChunkFits import GlasgowCallistoChunkFits

'''
ChunkFiles are characterised by chunk_start_time
'''

class GlasgowCallistoChunk:
    #constructor for SingleFileHandler
    def __init__(self,chunk_start_time, tag):
        #instantiate the timeStampStr field
        self.chunk_start_time = chunk_start_time
        self.tag = tag
        #type of the file
        #extract the datetime from chunk_start_time
        self.chunk_start_datetime = datetime.strptime(self.chunk_start_time, CONFIG.default_time_format)
        self.fits = GlasgowCallistoChunkFits(chunk_start_time, self.tag)


