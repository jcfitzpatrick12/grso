from src.chunks.standard.Chunk import Chunk
from src.chunks.callisto.Chunk import Chunk as CallistoChunk

tag_to_chunk_dict =  {
            "00": Chunk,
            "02": Chunk,
            "03": Chunk, 
            "01": CallistoChunk, 
        }