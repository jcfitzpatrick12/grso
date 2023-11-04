'''
class which handles the fileName stuff

convention is 

[C]%Y-%m-%dT%H:%M:%S[.EXT]

[.EXT] can be:
-null, raw SDR outputted binary file
-.hdr, header file
-.npy numpy array

[C] indicates whether the file is the final compressed
'''

import os 
from datetime import datetime


class FileString:
    def __init__(self,file):
        #split the file into its fileName and the ascociated extension
        self.fileName,self.fileExt = os.path.splitext(file)
        #find the type of file
        self.findType()
        #find the pseudo_start_time
        self.pseudo_start_time = self.findPseudoStartTime()

    #find the type of file. 
    def findType(self):
        if not self.fileExt:
            self.type = "bin"
        elif self.fileExt == ".npy" and self.fileName[0]=="C":
            self.type = "compressed-spectrogram"
        elif self.fileExt == ".npy" and self.fileName[0]!="C":
            self.type = "spectrogram"
        elif self.fileExt==".hdr":
            self.type="header"

    
    def findPseudoStartTime(self):
        if self.fileName[0]=="C":
            return self.fileName[1:]
        else:
            return self.fileName
        




