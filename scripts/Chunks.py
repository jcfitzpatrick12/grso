'''
Chunks deals with all the files in Pdata
'''

import os
from FileString import FileString
from sys_vars import sys_vars
from Chunk import Chunk

#this is a child class of FileHandler!
class Chunks:
    def __init__(self):
        #super().__init__()
        #build path to pdata
        self.sys_vars=sys_vars()
        #builds the chunkDict
        self.dict = self.buildDict()
        #sorts the dictionary temporally
        self.sortDicts()


    #removes all non compressed files
    def removeBigFiles(self,):
        # Loop through files in the directory
        for file in os.listdir(self.sys_vars.path_to_data):
            fs = FileString(file)
            # If the file is not a compressed-spectrogram, delete
            if fs.type!="fits":
                file_path = os.path.join(self.sys_vars.path_to_data, file)
                os.remove(file_path)
                print(f"Deleted {file}")
        pass  



    def updateDict(self):
        self.buildDict()
        pass

    #build the dictionaries containing dataFile classes
    #dataFile classes are used 
    #dataFileCompressed classes
    def buildDict(self):
        #create a dictionary which whill hold the key,value pairs [key, pseudo_start_time, dataChunk object]
        dict = {}
        #for each file in Pdata folder
        files = os.listdir(self.sys_vars.path_to_data)
        for file in files:
            #create the FileString class which deals with all files saved to Pdata [hdr, bin, npy files]
            fs = FileString(file)
            #otherwise, create the DataChunkFile class! This will do all the manipulations with the hdr and bin files
            #where the bin files hold the raw IQ signal
            #hdr file contains all the metadata
            dict[fs.pseudo_start_time] = Chunk(fs.pseudo_start_time)
        #return the spectrograms
        return dict
            
    #sort the dictionary by its keys
    def sortDicts(self):
        self.dict = {k: self.dict[k] for k in sorted(self.dict)}



        