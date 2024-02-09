'''
chunkFile class deals with all files of the form %Y-%m-%dT%H:%M:%S[.EXT]
'''

from src.chunks.callisto.ChunkFits import ChunkFits as CallistoChunkFits
from src.chunks.ChunkBase import ChunkBase

class Chunk(ChunkBase):
    #constructor for SingleFileHandler
    def __init__(self,chunk_start_time, tag):
        super().__init__(chunk_start_time, tag)
        self.fits = CallistoChunkFits(chunk_start_time, self.tag)


