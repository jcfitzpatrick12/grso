import pmt
from gnuradio.blocks import parse_file_metadata
import os

from src.utils import DatetimeFuncs
from src.fConfig import CONFIG


'''
The header file contains all the header data associated with the bin file.
'''

class ChunkHdr:
    def __init__(self,pseudo_start_time):
        self.pseudo_start_time = pseudo_start_time
        self.data_dir=DatetimeFuncs.build_data_dir_from_pseudo_start_time(self.pseudo_start_time)

    #find the path to data
    def get_path(self):
        return os.path.join(self.data_dir,self.pseudo_start_time+".hdr")
    
    def exists(self):
        return os.path.exists(self.get_path())
    
    def parse_header(self):
        #open the header file
        fh = open(self.get_path(), "rb")
        # Reads the header of a fixed length from the current position in the file and moves the read pointer by HEADER_LENGTH bytes.
        header_str = fh.read(parse_file_metadata.HEADER_LENGTH)
        #deserailise the header_str 
        header = pmt.deserialize_str(header_str)        
        #extract the header info!
        header_info = parse_file_metadata.parse_header(header,False)

        #make a deep copy of the dictionary [Why?]
        header_dict = header_info.copy()
        
        #extra length in the header, these lines are necessary to move the reading pointer to the start of the next segment
        if header_info["extra_len"] > 0:
            extra_str = fh.read(header_info["extra_len"])
            if len(extra_str) != 0:
                extra = pmt.deserialize_str(extra_str)
                extra_info = parse_file_metadata.parse_extra_dict(extra, header_info, False)

                '''
                for each element in extra info, append to header_info dict
                '''
                for key,value in extra_info.items():
                    header_dict[key]=value

        return header_dict