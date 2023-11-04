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
        #instantiate the timeStampDict which will hold the timeStamp, and it's ascociated dataFile class
        self.chunkDict = {}
        self.cspectrogramDict = {}
        #try:
        files = os.listdir(self.sys_vars.pathtoPdata)
        for file in files:
            fs = FileString(file)
            #if this file is already in the dictionary, pass
            if fs.pseudo_start_time in self.chunkDict.keys():
                pass
            #otherwise, add it to the dictionary and create the dataFile object
            else:
                #if the filename's extension notifies its a compressed spectrogram [cnpy]
                if fs.type=="compressed-spectrogram":
                    compressedSpectrogram = LoadSpectrogram().load(fs.pseudo_start_time,True)
                    self.cspectrogramDict[fs.pseudo_start_time]=compressedSpectrogram
                    pass
                else:
                    self.chunkDict[fs.pseudo_start_time] = DataChunkFile(fs.pseudo_start_time)
       
        '''
        except FileNotFoundError:
            print(f"The directory '{self.sys_vars.pathtoPdata}' was not found.")       
        '''

            
    #sort the dictionary by its keys
    def sortDicts(self):
        self.chunkDict = {k: self.chunkDict[k] for k in sorted(self.chunkDict)}
        self.cspectrogramDict = {k: self.cspectrogramDict[k] for k in sorted(self.cspectrogramDict)}



        