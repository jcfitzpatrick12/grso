'''
Chunks deals with all the files in Pdata
'''

import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from fMisc.FileString import FileString
from fMisc.sys_vars import sys_vars
from fChunks.Chunk import ChunkFits
from fMisc.datetimeFuncs import datetimeFuncs
from fChunks.Chunk import Chunk
from fSpectrogram.RadioSpectrogram import RadioSpectrogram

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

    '''
    build the dictionaries containing Chunk classes
    '''

    def buildDict(self):
        #create a dictionary which whill hold the key,value pairs [pseudo_start_time, dataChunk object]
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
    
    '''
    sorts the dictionaries by its keys
    '''
    def sortDicts(self):
        self.dict = {k: self.dict[k] for k in sorted(self.dict)}

    '''
    Function which returns a dictionary of all Chunks in a specified time range
    - want to be able to return a spectrogram over a custom time range.

    -takes in StartString and EndString in the format self.sys_vars.default_time_format
    -then outputs a RadioSpectrogram over the time range specified by StartString and EndString
    '''

    def buildSpectrogramFromRange(self,startString,endString):
        #loop through each Chunk in data and chop to the range
        #create a list of spectrogram objects to joint
        toJoin = []
        for pseudo_start_time,Chunk in self.dict.items():
            #load the spectrogram from the chunk
            S = Chunk.fits.loadRadioSpectrogram()
            try:
                #chop the spectrogram according to the requested range
                S = S.chop(startString,endString)
                #if the spectrogram is in the requested range, add it to the spectrograms to join
                toJoin.append(S)
            #otherwise, we'll get an error thrown that the indices are equal. This means the spectrogram is out of range
            #and we can ignore it.
            except:
                pass

        #if we have spectrograms to join, join them 
        if len(toJoin)>1:
            #join all the spectrograms together, padding with zeros between
            return self.joinSpectrograms(toJoin)   
        #if we are looking at a single spectrogram, simple return it chopped accordingly
        else:
            return toJoin[0]
    
    '''
    join a number of spectrograms in the form of a list.
    '''

    def joinSpectrograms(self,toJoin):

        #find the number of spectrograms to join
        num_toJoin = len(toJoin)
        # Padding columns: one less than the number of spectrograms
        numZeroCols = num_toJoin - 1

        #the number of time bins for each spectrogram.
        num_timeBins = []
        for i, S in enumerate(toJoin):
            #if we are considering the first spectrogram, extract the pseudo_start_time and the frequency bins
            if i == 0:
                new_pseudo_start_time = S.pseudo_start_time
                numFreqs = len(S.freqsMHz)
                
            #keep track of the number of time bins
            num_timeBins.append(S.Sxx.shape[1])
        
        #the total number of columns is the number of zeroed columns plus the total sum of the number of timebins in each spectrogram
        numCols = numZeroCols + sum(num_timeBins)
        
        #prepping arrays to hold the joined spectrogram
        joined_Sxx = np.zeros((numFreqs,numCols))
        joined_datetimeArray = np.empty(numCols,dtype='datetime64[ms]')

        #now for each spectrogram, place in the data with zeros padding between them
        for i,S in enumerate(toJoin):
            #if we are at the first spectrogram start from the start
            if i==0:
                disp = 0
            #otherwise, we displace the start index by the sum of the previous number of bins
            else:
                disp = sum(num_timeBins[:i])
    
            #and finally we displace by the number of zero columns
            startInd = i+disp
            endInd = startInd + num_timeBins[i]
            joined_Sxx[:,startInd:endInd]=S.Sxx
      
            if i>0:
                joined_datetimeArray[startInd-1]=S.datetimeArray64[0]

            joined_datetimeArray[startInd:endInd]=S.datetimeArray64

        joined_timeArray = datetimeFuncs().toSeconds(joined_datetimeArray)
        
        return RadioSpectrogram(joined_Sxx,joined_timeArray,S.freqsMHz,S.center_freq,new_pseudo_start_time,S.isCompressed)
        