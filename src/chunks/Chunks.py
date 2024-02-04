'''
Chunks deals with all the files in Pdata
'''

import os
import numpy as np
from datetime import timedelta
import time
from collections import OrderedDict

from src.configs import GLOBAL_CONFIG
from src.configs.tag_maps.tag_to_chunk import tag_to_chunk_dict

from src.utils import DatetimeFuncs, DirFuncs

from src.spectrogram import SpectrogramFactory


class Chunks:
    def __init__(self, tag):
        self.tag = tag
        self.chunk = tag_to_chunk_dict[tag]
        self.time_format = f"{GLOBAL_CONFIG.default_time_format}_{self.tag}"
        self.set_all_data_files()
        self.set_dict()
        self.sort_dict()


    def set_all_data_files(self):
        self.all_data_files = DirFuncs.list_all_files(GLOBAL_CONFIG.path_to_data)
    
    
    def get_all_data_files(self):
        return self.all_data_files


    def set_dict(self):
        self.dict = OrderedDict()
        all_data_files = self.get_all_data_files()
        for file in all_data_files:
            file_name,ext = os.path.splitext(file)
            chunk_start_time, tag = file_name.split("_", 1)
            if tag==self.tag:
                self.dict[chunk_start_time] = self.chunk(chunk_start_time, tag)
        self.sort_dict()


    def get_dict(self):
        if len(self.dict)==0:
            print(f"Warning, no chunks in {GLOBAL_CONFIG.path_to_data}")
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
            file_name, ext = os.path.splitext(file)
            chunk_start_time, tag = file_name.split("_", 1)
            # If the file is not a compressed-spectrogram, delete
            if ext!=".fits":
                file_dir = DatetimeFuncs.build_data_dir_from_chunk_start_time(GLOBAL_CONFIG.path_to_data, chunk_start_time)
                file_path = os.path.join(file_dir, file)
                os.remove(file_path)
                print(f"Deleted {file}")
        pass  


    def build_spectrogram_from_range(self, requested_start_str,requested_end_str):
        requested_start_datetime = DatetimeFuncs.strptime(requested_start_str, GLOBAL_CONFIG.default_time_format)
        requested_end_datetime = DatetimeFuncs.strptime(requested_end_str, GLOBAL_CONFIG.default_time_format)

        if requested_start_datetime.day != requested_end_datetime.day:
            raise ValueError("Make sure your time interval is within one day.")

        # can now safely set the day requested
        requested_day = requested_start_datetime.day

        spectrograms_to_join = []
        for chunk_start_time,chunk in self.dict.items():
            chunk_start_datetime = DatetimeFuncs.strptime(chunk_start_time, GLOBAL_CONFIG.default_time_format) 
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
                    S = SpectrogramFactory.time_chop(S, requested_start_str,requested_end_str)
                    spectrograms_to_join.append(S)
                    # otherwise, we'll get an error thrown that the indices are equal. This means the spectrogram is out of range
                    # and we can ignore it.
                except Exception as e:
                    raise ValueError(f"Received the following error: {e}")
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
            return SpectrogramFactory.join_spectrograms(spectrograms_to_join) 







                        
                        
                    
                    
                    
                    
                    


        


    