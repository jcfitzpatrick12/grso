'''
Class which deals with multiple files in Pdata
Lists all those available
Organises in date order
Multiple header parsing [sorts into a dictionary with file name, and headerDict as the value?]
Another dictionary with the file name and the asociated IQ signal array.

ect.
'''

import os

from dataFile import dataFile
from dataFileCompressed import dataFileCompressed

#this is a child class of FileHandler!
class pdataFuncs:
    def __init__(self):
        super().__init__()
        #build path to pdata
        self.pathPdata = os.path.join(os.getcwd(),"Pdata")
        #build dataDict which contains {key: value} where key is pseudo_start_time, value is dataFile class for that pseudo_start_time
        self.buildDicts()
        #sorts the dictionary temporally
        self.sortDict()

    #removes all non compressed files
    def removeBigFiles(self,):
        # Loop through files in the directory
        for filename in os.listdir(self.pathPdata):
            print(filename)
            # If "average" is not in the filename, delete it
            if "average" not in filename:
                file_path = os.path.join(self.pathPdata, filename)
                os.remove(file_path)
                print(f"Deleted {filename}")

        print("Operation completed.")

    '''
    #builds the long data over all the 
    def buildLongData(self,):
        #loop over all dataFiles
        for pseudo_start_time, dataFile in self.dataDict.items():
            print(dataFile.pseudo_start_time)
        pass   
    '''


    #build the dictionaries containing dataFile classes and dataFileCompressed classes

    def buildDicts(self):
        #instantiate the timeStampDict which will hold the timeStamp, and it's ascociated dataFile class
        self.dataDict = {}
        self.dataCompressedDict = {}
        
        try:
            #list all the files in os.listdir (will be bin, npy, hdr)
            #we will basically loop through them all, if we encounter a file with a so-far unique timeStampStr
            #we will make a new key value pair in timeStampDict, where the value is a dataFile class!
            files = os.listdir(os.path.join(os.getcwd(),"Pdata"))
            for fileName in files:
                #ignore averaged files
                if "average" in fileName:
                    pseudo_start_time = fileName.split('e')[-1].split('.')[0]
                    self.dataCompressedDict[pseudo_start_time]=dataFileCompressed(pseudo_start_time)
                    continue

                #extract the pseudo_start_time from the file extensions
                pseudo_start_time, _ = os.path.splitext(fileName)
                #if this file is in the dictionary, pass
                if pseudo_start_time in self.dataDict.keys():
                    pass
                #otherwise, add it to the dictionary and create the dataFile object
                else:
                    self.dataDict[pseudo_start_time]=dataFile(pseudo_start_time)

        except FileNotFoundError:
            print(f"The directory '{self.pathPdata}' was not found.")
            
    #sort the dictionary by its keys
    def sortDict(self):
        self.dataDict = {k: self.dataDict[k] for k in sorted(self.dataDict)}



        