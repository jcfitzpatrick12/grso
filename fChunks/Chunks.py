'''
Chunks deals with all the files in Pdata
'''

import os
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
import time

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
    def remove_non_fits_files_from_data(self,):
        # Loop through files in the directory
        #for each file in data [will be in some subdirectory according to its date]
        all_files = self.list_all_files()
        for file in all_files:
            fs = FileString(file)
            # If the file is not a compressed-spectrogram, delete
            if fs.type!="fits":
                file_dir = DatetimeFuncs().build_data_dir_from_pseudo_start_time(fs.pseudo_start_time)
                file_path = os.path.join(file_dir, file)
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
        all_files = self.list_all_files()
        for file in all_files:
            #create the FileString class which deals with all files saved to Pdata [hdr, bin, npy files]
            fs = FileString(file)
            #otherwise, create the DataChunkFile class! This will do all the manipulations with the hdr and bin files
            #where the bin files hold the raw IQ signal
            #hdr file contains all the metadata
            dict[fs.pseudo_start_time] = Chunk(fs.pseudo_start_time)
        #return the spectrograms
        return dict
    
    '''
    list all files regardless of subdirectories in data
    '''

    def list_all_files(self):
        all_files = []
        #walk through all the subdirectories in data
        for root, dirs, files in os.walk(self.sys_vars.path_to_data):
            for file in files:
                #full_path = os.path.join(root, file)
                all_files.append(file)  # Store the full path to the file
                # ... (rest of your code to handle each file)
        return all_files
    
    '''
    sorts the dictionaries by its keys
    '''
    def sort_dict(self):
        self.dict = {k: self.dict[k] for k in sorted(self.dict)}

    '''
    Function which returns a dictionary of all Chunks in a specified time range

    [optimise for now current data subdirectory structure]

    -return a spectrogram over a custom time range.
    -takes in start_str and end_str in the format self.sys_vars.default_time_format
    -then outputs a RadioSpectrogram over the time range specified
    '''

    def build_spectrogram_from_range(self,requested_start_str,requested_end_str):
        #loop through each Chunk in data and chop to the range
        #initiate an empty list to hold the RadiosSpectrogram objects to join
        to_join = []
        #for each Chunk in data, try and chop it to the time range
        for pseudo_start_time,Chunk in self.dict.items():
            
            requested_start_datetime = DatetimeFuncs().parse_datetime(requested_start_str)
            requested_end_datetime = DatetimeFuncs().parse_datetime(requested_end_str)
            time_array = Chunk.fits.return_info("TIME")
            pseudo_start_time = Chunk.fits.return_info("PSTIME")
            pseudo_start_datetime=DatetimeFuncs().parse_datetime(pseudo_start_time)
            datetime_array = DatetimeFuncs().build_datetime_array(pseudo_start_datetime,time_array)
            # Check if the chunk's time range intersects with the requested time range
            chunk_start_datetime = datetime_array[0]
            chunk_end_datetime = datetime_array[-1]

            if chunk_start_datetime <= requested_end_datetime and chunk_end_datetime >= requested_start_datetime:
                try:
                    #load the spectrogram from the chunk
                    S = Chunk.fits.load_radio_spectrogram()
                    #chop the spectrogram according to the requested range
                    S = S.chop(requested_start_str,requested_end_str)
                    #S.Sxx[:,0]=1000
                    #S.Sxx[:,-1]=1000
                    #if the spectrogram is in the requested range, add it to the spectrograms to join
                    to_join.append(S)
                #otherwise, we'll get an error thrown that the indices are equal. This means the spectrogram is out of range
                #and we can ignore it.
                except:
                    pass
            else:
                continue

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
    join a number of spectrograms [stored in the to_join list]

    -pads in between with zero, since there will be a couple of seconds of downtime
    -we don't need to worry about the spectrograms being time ordered as the dictionary is already sorted in Chunks
    '''

    def join_spectrograms(self,to_join):
        #find the number of spectrograms to join
        num_to_join = len(to_join)
        # Padding columns: one less than the number of spectrograms
        num_zero_cols = num_to_join - 1
        #initialise an array to hold the time dimension 
        num_time_bin_edges = []
        #create a list to hold the datetime64 array for each spectrogram
        #for each Spectrogram, in those to join.
        for i, S in enumerate(to_join):
            #if i==0, extract
            # -the pseudo_start_time
            # -the number of frequency bin edges
            # these are identical for all S in to_join, so we may take them from any
            # take from the first for convenience
            if i == 0:
                new_pseudo_start_time = S.pseudo_start_time
                num_freq_bin_edges = len(S.freqs_MHz)
            
            #keep track of the number of time_bin_edges in each spectrogram.
            num_time_bin_edges.append(len(S.time_array))

        #the total number of columns is the sum of:
        # the total number of bin edges
        # minus the number of spectrograms to join [since time dim of Sxx is the number of bin edges minus one, so each S in to_join accumulates another minus one]
        num_cols = num_zero_cols + sum(num_time_bin_edges)-num_to_join
        
        #prepping arrays to hold the joined spectrogram
        joined_Sxx = np.empty((num_freq_bin_edges-1,num_cols))

        #now for each spectrogram, place in the data with zeros padding between them
        for i,S in enumerate(to_join):
            if i==0:
                #if we are at the first spectrogram, we want to start from the 0th index, so set disp=0
                displace_index = 0
                #on the first iteration, create a joined_time array which we will concatenate hereafter
                running_concatenated_datetime_array = S.datetime64_array
            #otherwise, we displace the start index by the sum of the previous number of samples
            else:
                displace_index = sum(num_time_bin_edges[:i])-i
                #concatenate the datetimearray
                running_concatenated_datetime_array = np.concatenate([running_concatenated_datetime_array,S.datetime64_array])
            #the start index is the sum of the number of zero columns prior to the ith spectrogram [i]
            #and the displacement, disp, defined as the sum of time samples in spectrograms prior to the ith spectrogram.
            start_ind = i+(displace_index)
            #the end index is naturally the start index, plus the number of time samples in the ith spectrogram
            end_ind = start_ind + (num_time_bin_edges[i]-1)
            #raise SystemExit
            #we place in the ith spectrogram here.
            joined_Sxx[:,start_ind:end_ind]=S.Sxx

        #raise SystemExit
        
        joined_datetime_array = running_concatenated_datetime_array
               
        #convert the joined_datetimeArray into an array of seconds since t=0, so that we can construct the spectrogram object
        joined_time_array = DatetimeFuncs().datetime64_array_to_seconds(joined_datetime_array)
        
        #raise SystemExit
        return RadioSpectrogram(joined_Sxx,joined_time_array,S.freqs_MHz,S.center_freq,new_pseudo_start_time,S.is_averaged)
        