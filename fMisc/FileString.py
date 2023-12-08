'''
class which handles the fileName stuff

convention is 

%Y-%m-%dT%H:%M:%S[.EXT]

[.EXT] can be:
-null, raw SDR outputted binary file
-.hdr, header file
-.npy numpy array

'''

import os 


class FileString:
    def __init__(self,file):
        #split the file into its fileName and the ascociated extension
        self.file_name,self.file_ext = os.path.splitext(file)
        #find the type of file
        self.type = self.find_type()
        #find the pseudo_start_time
        self.pseudo_start_time = self.find_pseudo_start_time()

    #find the type of file. 
    def find_type(self):
        #if there is no file extension, the file must be a binary file
        if not self.file_ext:
            return "bin"
        #if we have a numpy file, and the first character is NOT C, then we have a 
        elif self.file_ext == ".npy":
            return "spectrogram"
        #if the file extension is .hdr then we have a header file
        elif self.file_ext==".hdr":
            return "header"
        elif self.file_ext==".fits":
            return "fits"

    #extract pseudo_start_time from the filename [careful! if we have a compressed file]
    def find_pseudo_start_time(self):
        #if the file begins with a C, take the rest of the filename [without the extension]
        if self.file_name[0]=="C":
            return self.file_name[1:]
        else:
            return self.file_name
        




