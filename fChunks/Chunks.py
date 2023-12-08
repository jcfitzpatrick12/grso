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
from fMisc.DatetimeFuncs import DatetimeFuncs
from fChunks.Chunk import Chunk
from fSpectrogram.RadioSpectrogram import RadioSpectrogram

#this is a child class of FileHandler!
class Chunks:
    def __init__(self):
        #super().__init__()
        #build path to pdata
        self.sys_vars=sys_vars()
        #builds the chunkDict
        self.dict = self.build_dict()
        #sorts the dictionary temporally
        self.sort_dict()


    #removes all non compressed files
    def remove_big_files(self,):
        # Loop through files in the directory
        for file in os.listdir(self.sys_vars.path_to_data):
            fs = FileString(file)
            # If the file is not a compressed-spectrogram, delete
            if fs.type!="fits":
                file_path = os.path.join(self.sys_vars.path_to_data, file)
                os.remove(file_path)
                print(f"Deleted {file}")
        pass  



    def update_dict(self):
        self.build_dict()
        pass

    '''
    build the dictionaries containing Chunk classes
    '''

    def build_dict(self):
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
    def sort_dict(self):
        self.dict = {k: self.dict[k] for k in sorted(self.dict)}

    '''
    Function which returns a dictionary of all Chunks in a specified time range

    [Will possibly be very inefficient for lots of files in data! Must be a more efficient way to check]

    - want to be able to return a spectrogram over a custom time range.

    -takes in StartString and EndString in the format self.sys_vars.default_time_format
    -then outputs a RadioSpectrogram over the time range specified by StartString and EndString
    '''

    def build_spectrogram_from_range(self,start_str,end_str):
        #loop through each Chunk in data and chop to the range
        #initiate an empty list to hold the RadiosSpectrogram objects to join
        to_join = []
        #for each Chunk in data, try and chop it to the time range
        for pseudo_start_time,Chunk in self.dict.items():
            #load the spectrogram from the chunk
            S = Chunk.fits.load_radio_spectrogram()
            try:
                #chop the spectrogram according to the requested range
                S = S.chop(start_str,end_str)
                #S.Sxx[:,0]=1000
                #S.Sxx[:,-1]=1000
                #if the spectrogram is in the requested range, add it to the spectrograms to join
                to_join.append(S)
            #otherwise, we'll get an error thrown that the indices are equal. This means the spectrogram is out of range
            #and we can ignore it.
            except:
                pass

        #if we didn't find any spectrograms to join...
        if len(to_join)==0:
            raise SystemError("No file matches! Choose a different time range.")
        #if we are looking at a single spectrogram, simple return it chopped accordingly
        if len(to_join)==1:
            return to_join[0]
        #if we more than one spectrogram to join, join them.
        elif len(to_join)>1:
            #join all the spectrograms together, padding with zeros between
            return self.join_spectrograms(to_join)   
       
    
    '''
    join a number of spectrograms [stored in the "toJoin" list]

    -pads in between with NaNs, since there will be a couple of seconds of downtime
    -we don't need to worry about the spectrograms being time ordered as the dictionary is already sorted in Chunks
    '''

    def join_spectrograms(self,to_join):

        #find the number of spectrograms to join
        num_to_join = len(to_join)
        # Padding columns: one less than the number of spectrograms
        num_zero_cols = num_to_join - 1

        #initialise an empty array to hold the number of time_samples in each spectrogram to join
        #this is necessary, as the number will naturally vary between each spectrogram [though approximately equal, out in the tens of samples]
        num_time_samples = []
        #for each Spectrogram, in those to join.
        for i, S in enumerate(to_join):
            #if we are considering the first spectrogram, extract the pseudo_start_time and the frequency bins
            #we will need the former to set the pseudo_start_time of the joined spectrogram
            #and we will need the latter for initialising the empty array to store the joined spectrograms [need to define its shape]
            if i == 0:
                new_pseudo_start_time = S.pseudo_start_time
                num_freqs = len(S.freqs_MHz)
                
            #keep track of the number of timeSamples in each spectrogram.
            num_time_samples.append(S.Sxx.shape[1])
        
        #the total number of columns is the number of zeroed columns plus the total sum of the number of samples in each spectrogram
        num_cols = num_zero_cols + sum(num_time_samples)
        
        #prepping arrays to hold the joined spectrogram
        joined_Sxx = np.zeros((num_freqs,num_cols))
        joined_datetime_array = np.empty(num_cols,dtype='datetime64[ns]')

        #now for each spectrogram, place in the data with zeros padding between them
        for i,S in enumerate(to_join):
            #if we are at the first spectrogram, we want to start from the 0th index, so set disp=0
            if i==0:
                disp = 0
            #otherwise, we displace the start index by the sum of the previous number of samples
            else:
                disp = sum(num_time_samples[:i])
    
            #the start index is the sum of the number of zero columns prior to the ith spectrogram [i]
            #and the displacement, disp, defined as the sum of time samples in spectrograms prior to the ith spectrogram.
            start_ind = i+disp
            #the end index is naturally the start index, plus the number of time samples in the ith spectrogram
            end_ind = start_ind + num_time_samples[i]
            #we place in the ith spectrogram here.
            joined_Sxx[:,start_ind:end_ind]=S.Sxx

            #the element of joined_datetimeArray indexed by (startInd-1) is responsible for telling us the width of the padding array
            #so that the padded section spans the entirety of the downtime between two neighbouring spectrograms
            #we may simple duplicate the first entry.
            if i>0:
                joined_datetime_array[start_ind-1]=S.datetime_array64[0]
            #finally, place the original datetimes of the spectrogram into the joined_datetimeArray
            joined_datetime_array[start_ind:end_ind]=S.datetime_array64

        #convert the joined_datetimeArray into an array of seconds since t=0, so that we can construct the spectrogram object
        joined_time_array = DatetimeFuncs().to_seconds(joined_datetime_array)
        
        return RadioSpectrogram(joined_Sxx,joined_time_array,S.freqs_MHz,S.center_freq,new_pseudo_start_time,S.is_compressed)
        