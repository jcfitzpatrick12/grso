'''
Chunks deals with all the files in Pdata
'''

import os
import numpy as np
from datetime import timedelta
import time

from src.fConfig import CONFIG, config_dicts
from src.utils import DatetimeFuncs, SpectrogramFuncs, DirFuncs
from src.fChunks.Chunk import Chunk
from collections import OrderedDict
from src.fSpectrogram.RadioSpectrogram import RadioSpectrogram


class Chunks:
    def __init__(self, tag):
        self.tag = tag
        self.chunk = config_dicts.tag_to_chunk_dict[self.tag]
        self.time_format = f"{CONFIG.default_time_format}_{self.tag}"

        self.set_all_data_files()
        self.set_dict()
        #builds the chunkDict
        self.dict = self.get_dict()
        self.sort_dict()

    def set_all_data_files(self):
        self.all_data_files = DirFuncs.list_all_files(CONFIG.path_to_data)
    
    def get_all_data_files(self):
        return self.all_data_files

    def set_dict(self):
        #create a dictionary which whill hold the key,value pairs [chunk_start_time, datachunk object]
        self.dict = OrderedDict()
        all_data_files = self.get_all_data_files()
        for file in all_data_files:
            file_name,ext = os.path.splitext(file)
            chunk_start_time, tag = file_name.split("_", 1)
            if tag==self.tag:
                self.dict[chunk_start_time] = self.chunk(chunk_start_time, tag)
        self.sort_dict()
        return

    def get_dict(self):
        if len(self.dict)==0:
            print(f"Warning, no chunks in {CONFIG.path_to_data}")
        return self.dict

    def sort_dict(self):
        self.dict = OrderedDict(sorted(self.dict.items()))

    def get_chunk_by_index(self, index):
        if index<0:
            index = len(self.dict)+index
        for i, chunk in enumerate(self.dict.values()):
            if i == index:
                return chunk
        print(f"Choose an index in range! Index {index} out of bounds of maximum index {i}. Returning None")
        return None

    def get_index_by_chunk(self, chunk_to_match):
        chunk_start_time_to_match = chunk_to_match.chunk_start_time

        for index, chunk in enumerate(self.dict.values()):
            if chunk.chunk_start_time == chunk_start_time_to_match:
                return index
    
        raise ValueError(f"No matching chunk found!")

    
    def find_nearest_chunk(self, requested_chunk_start_time):
        requested_chunk_start_time = DatetimeFuncs.strptime(requested_chunk_start_time)
        closest_chunk = None
        min_time_diff = None

        for chunk in self.dict.values():
            current_chunk_start_time = DatetimeFuncs.strptime(chunk.chunk_start_time)
            
            # Calculate the absolute time difference
            time_diff = abs(requested_chunk_start_time - current_chunk_start_time)

            # Determine if this is the closest chunk so far
            if min_time_diff is None or time_diff < min_time_diff:
                closest_chunk = chunk
                min_time_diff = time_diff

        return closest_chunk
    

    def remove_non_fits_files_from_data(self,):
        # Loop through files in the directory
        #for each file in data [will be in some subdirectory according to its date]
        all_data_files = self.get_all_data_files()
        for file in all_data_files:
            chunk_start_time,ext = os.path.splitext(file)
            # If the file is not a compressed-spectrogram, delete
            if ext!=".fits":
                file_dir = DatetimeFuncs.build_data_dir_from_chunk_start_time(CONFIG.path_to_data, chunk_start_time)
                file_path = os.path.join(file_dir, file)
                os.remove(file_path)
                print(f"Deleted {file}")
        pass  
       

    def get_background_spectrogram(self,**kwargs):
        start_background_str = kwargs.get("start_background",CONFIG.background_interval[0])
        end_background_str = kwargs.get("end_background",CONFIG.background_interval[1])
        return self.build_spectrogram_from_range(start_background_str,end_background_str)


    def build_spectrogram_from_range(self, requested_start_str,requested_end_str):
        requested_start_datetime = DatetimeFuncs.strptime(requested_start_str, CONFIG.default_time_format)
        requested_end_datetime = DatetimeFuncs.strptime(requested_end_str, CONFIG.default_time_format)

        if requested_start_datetime.day != requested_end_datetime.day:
            raise ValueError("Make sure your time interval is within one day.")

        # can now safely set the day requested
        requested_day = requested_start_datetime.day

        spectrograms_to_join = []
        for chunk_start_time,chunk in self.dict.items():
            chunk_start_datetime = DatetimeFuncs.strptime(chunk_start_time, CONFIG.default_time_format) 
            if chunk_start_datetime.day!=requested_day:
                continue

            time_array = chunk.fits.return_info("TIME")
            #chunk_start_time = chunk.fits.return_info("PSTIME")
            datetime_array = DatetimeFuncs.build_datetime_array(chunk_start_datetime,time_array)
            # Check if the chunk's time range intersects with the requested time range
            chunk_start_datetime = datetime_array[0]
            chunk_end_datetime = datetime_array[-1]

            if chunk_start_datetime <= requested_end_datetime and chunk_end_datetime >= requested_start_datetime:
                try:
                    S = chunk.fits.load_radio_spectrogram()
                    S = S.time_chop(requested_start_str,requested_end_str)
                    spectrograms_to_join.append(S)
                    # otherwise, we'll get an error thrown that the indices are equal. This means the spectrogram is out of range
                    # and we can ignore it.
                except Exception as e:
                    #raise ValueError(f"Received the following error: {e}")
                    pass
            else:
                continue
        
        #if we didn't find any spectrograms to join...
        if len(spectrograms_to_join)==0:
            raise SystemError("No file matches! Choose a different time range.")
        #if we are looking at a single spectrogram, simple return it chopped accordingly
        if len(spectrograms_to_join)==1:
            return spectrograms_to_join[0]
        #if we more than one spectrogram to join, join them.
        elif len(spectrograms_to_join)>1:
            #join all the spectrograms together, padding with zeros between
            return self.join_spectrograms(spectrograms_to_join) 

    def join_spectrograms(self, list_of_spectrograms_to_join):
        #find the number of spectrograms to join
        num_to_join = len(list_of_spectrograms_to_join)
        if num_to_join == 0:
            raise ValueError("No spectrograms to join!")
        # Padding columns: one less than the number of spectrograms
        num_zero_cols = num_to_join - 1
        #initialise an array to hold the time dimension 
        num_time_bin_edges = []
        #create a list to hold the datetime64 array for each spectrogram
        #for each Spectrogram, in those to join.
        for i, S in enumerate(list_of_spectrograms_to_join):
            #if i==0, extract
            # -the chunk_start_time
            # -the number of frequency bin edges
            # these are identical for all S in to_join, so we may take them from any
            # take from the first for convenience
            if i == 0:
                new_chunk_start_time = S.chunk_start_time
                num_freq_bin_edges = len(S.freqs_MHz)
            
            #keep track of the number of time_bin_edges in each spectrogram.
            num_time_bin_edges.append(len(S.time_array))

        #the total number of columns is the sum of:
        # the total number of bin edges
        # minus the number of spectrograms to join [since time dim of Sxx is the number of bin edges minus one, so each S in to_join accumulates another minus one]
        num_cols = num_zero_cols + sum(num_time_bin_edges)-num_to_join
        
        #prepping arrays to hold the joined spectrogram
        joined_Sxx = np.zeros((num_freq_bin_edges-1,num_cols))

        #now for each spectrogram, place in the data with zeros padding between them
        for i,S in enumerate(list_of_spectrograms_to_join):
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

            joined_Sxx[:,start_ind:end_ind]=S.Sxx
        

        joined_datetime_array = running_concatenated_datetime_array
        #convert the joined_datetimeArray into an array of seconds since t=0, so that we can construct the spectrogram object
        joined_time_array = DatetimeFuncs.datetime64_array_to_seconds(joined_datetime_array)
        
        return RadioSpectrogram(joined_Sxx, joined_time_array, S.freqs_MHz, S.center_freq, new_chunk_start_time, self.tag)






                        
                        
                    
                    
                    
                    
                    


        


    