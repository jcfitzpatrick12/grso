import pmt
from gnuradio.blocks import parse_file_metadata
import numpy as np
import os
from datetime import datetime

'''
class which handles operations on the files labelled by timeStampStr
'''

class SingleFile:
    #constructor for SingleFileHandler
    def __init__(self,timeStampStr):
        #instantiate the timeStampStr field
        self.timeStampstr = timeStampStr
        #the path to the file
        self.filePath = os.path.join(os.getcwd(),"Pdata",timeStampStr)

        #convert the bin to a numpy array
        self.ConvertBinToNpy()
        #parse the Header [instantiates self.headerDict]
        self.parseHeader()
    
        #instantiate some of the header fields
        self.center_freq = pmt.to_float(self.headerDict['center_freq'])
        self.samp_rate = pmt.to_long(self.headerDict['samp_rate'])
        self.pseudo_start_time = pmt.write_string(self.headerDict['pseudo_start_time'])
        self.pseudo_start_datetime = datetime.strptime(self.pseudo_start_time,"%Y-%m-%dT%H:%M:%S")

    
    def ConvertBinToNpy(self):
        #open the header file
        fh = open(self.filePath, "rb")
        #extract the data
        data = np.fromfile(fh, dtype=np.complex64)
        np.save(os.path.join(self.filePath),data)
        pass

    def parseHeader(self):
        #find the path to that particular timeStampSr
        filePath = self.filePath+".hdr"
        #open the header file
        fh = open(filePath, "rb")
        # Reads the header of a fixed length from the current position in the file and moves the read pointer by HEADER_LENGTH bytes.
        header_str = fh.read(parse_file_metadata.HEADER_LENGTH)
        #deserailise the header_str 
        header = pmt.deserialize_str(header_str)        
        #extract the header info!
        header_info = parse_file_metadata.parse_header(header,False)

        #make a deep copy of the dictionary
        headerDict = header_info.copy()

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
                    headerDict[key]=value

        self.headerDict=headerDict