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

#this is a child class of FileHandler!
class pdataFuncs:
    def __init__(self):
        super().__init__()
        self.buildDict()
        self.sortDict()

    #build a list of all unique timestamps in Pdata
    def buildDict(self):
        #instantiate the timeStampDict which will hold the timeStamp, and it's ascociated dataFile class
        self.dataDict = {}
        try:
            #list all the files in os.listdir (will be bin, npy, hdr)
            #we will basically loop through them all, if we encounter a file with a so-far unique timeStampStr
            #we will make a new key value pair in timeStampDict, where the value is a dataFile class!
            files = os.listdir(os.path.join(os.getcwd(),"Pdata"))
            for file in files:
                #seperate the timeStampStr from the datafile
                timeStampStr, _ = os.path.splitext(file)
                #does the timeStampDict have a key with timeStampStr?
                if timeStampStr in self.dataDict.keys():
                    pass
                else:
                    self.dataDict[timeStampStr]=dataFile(timeStampStr)

        except FileNotFoundError:
            print(f"The directory '{self.pathPdata}' was not found.")
            
    #sort the dictionary by its keys
    def sortDict(self):
        self.dataDict = {k: self.dataDict[k] for k in sorted(self.dataDict)}



        