'''
Class which deals with multiple files in Pdata
Lists all those available
Organises in date order
Multiple header parsing [sorts into a dictionary with file name, and headerDict as the value?]
Another dictionary with the file name and the asociated IQ signal array.

ect.
'''

import os
from FileString import FileString
from DataChunkFile import DataChunkFile
from sys_vars import sys_vars
from LoadSpectrogram import LoadSpectrogram
from RadioSpectrogram import RadioSpectrogram
import numpy as np

#this is a child class of FileHandler!
class PdataFuncs:
    def __init__(self):
        #super().__init__()
        #build path to pdata
        self.sys_vars=sys_vars()
        #builds the dataDicts
        self.buildDicts()
        #sorts the dictionary temporally
        self.sortDicts()

    '''
    ## takes all the files in self.cspectrogramDict and builds one big RadioSpectrogram class [shows the dead time inbetween collection]
    def buildBigSpectrogram(self,):
        #extract the number of spectrograms
        numSpectrograms = len(self.cspectrogramDict.items())
        print(numSpectrograms)
        for pseudo_start_time, compressedSpectrogram in self.cspectrogramDict.items():
            print(pseudo_start_time)
            print(np.shape(compressedSpectrogram.Sxx))
            #compressedSpectrogram.plotSpectrogram()
        pass  
    '''

    #removes all non compressed files
    def removeBigFiles(self,):
        # Loop through files in the directory
        for file in os.listdir(self.sys_vars.pathtoPdata):
            fs = FileString(file)
            # If the file is not a compressed-spectrogram, delete
            if fs.type!="compressed-spectrogram":
                file_path = os.path.join(self.sys_vars.pathtoPdata, file)
                os.remove(file_path)
                print(f"Deleted {file}")
        pass

    def updateDicts(self):
        self.buildDicts()
        pass

    #build the dictionaries containing dataFile classes
    #dataFile classes are used 
    #dataFileCompressed classes
    def buildDicts(self):
        #create a dictionary which whill hold the key,value pairs [key, pseudo_start_time, dataChunk object]
        self.chunkDict = {}
        #create a dictionary which will
        self.cspectrogramDict = {}
        #for each file in Pdata folder
        files = os.listdir(self.sys_vars.pathtoPdata)
        for file in files:
            #create the FileString class which deals with all files saved to Pdata [hdr, bin, npy files]
            fs = FileString(file)
            #if this file is already in the dictionary, pass
            if fs.pseudo_start_time in self.chunkDict.keys():
                pass
            #otherwise, add it to the dictionary and create the dataFile object
            else:
                #if the filename's extension notifies its a compressed spectrogram [cnpy]
                if fs.type=="compressed-spectrogram":
                    #if thefiletype is a compressedspcetrogram, load the [compressed] spectrogram class]
                    compressedSpectrogram = LoadSpectrogram().load(fs.pseudo_start_time,True)
                    self.cspectrogramDict[fs.pseudo_start_time]=compressedSpectrogram
                    pass
                else:
                    #otherwise, create the DataChunkFile class! This will do all the manipulations with the hdr and bin files
                    #where the bin files hold the raw IQ signal
                    #hdr file contains all the metadata
                    self.chunkDict[fs.pseudo_start_time] = DataChunkFile(fs.pseudo_start_time)
       

            
    #sort the dictionary by its keys
    def sortDicts(self):
        self.chunkDict = {k: self.chunkDict[k] for k in sorted(self.chunkDict)}
        self.cspectrogramDict = {k: self.cspectrogramDict[k] for k in sorted(self.cspectrogramDict)}



        