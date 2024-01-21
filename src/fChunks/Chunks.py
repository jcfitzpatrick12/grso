'''
Chunks deals with all the files in Pdata
'''

import os
import numpy as np
from datetime import timedelta
import time

from src.fConfig import CONFIG
from src.utils import DatetimeFuncs, SpectrogramFuncs
from src.fChunks.Chunk import Chunk




class Chunks:
    def __init__(self):
        self.set_dict()
        #builds the chunkDict
        self.dict = self.get_dict()

    def set_dict(self):
        #create a dictionary which whill hold the key,value pairs [pseudo_start_time, dataChunk object]
        self.dict = {}
        #for each file in Pdata folder
        all_files = self.list_all_files()
        for file in all_files:
            #create the FileString class which deals with all files saved to Pdata [hdr, bin, npy files]
            pseudo_start_time,ext = os.path.splitext(file)
            #otherwise, create the DataChunkFile class! This will do all the manipulations with the hdr and bin files
            #where the bin files hold the raw IQ signal
            #hdr file contains all the metadata
            self.dict[pseudo_start_time] = Chunk(pseudo_start_time)
        #sorts the dictionary temporally
        self.sort_dict()

    def get_dict(self):
        return self.dict

    def sort_dict(self):
        self.dict = {k: self.dict[k] for k in sorted(self.dict)}

    def list_all_files(self):
        all_files = []
        #walk through all the subdirectories in data
        for root, dirs, files in os.walk(CONFIG.path_to_data):
            for file in files:
                #full_path = os.path.join(root, file)
                all_files.append(file)  # Store the full path to the file
                # ... (rest of your code to handle each file)
        return all_files
    

    def build_spectrogram_from_range(self,requested_start_str,requested_end_str):
            requested_start_datetime = DatetimeFuncs.parse_datetime(requested_start_str)
            requested_end_datetime = DatetimeFuncs.parse_datetime(requested_end_str)

            try:
                assert requested_start_datetime.day == requested_end_datetime.day
                requested_day = requested_start_datetime.day
            except:
                raise ValueError("Make sure your time interval is within one day.")

            #loop through each Chunk in data and chop to the range
            #initiate an empty list to hold the RadiosSpectrogram objects to join
            to_join = []

            for pseudo_start_time,Chunk in self.dict.items():
                pseudo_start_datetime=DatetimeFuncs.parse_datetime(pseudo_start_time)
                if pseudo_start_datetime.day!=requested_day:
                    continue

                time_array = Chunk.fits.return_info("TIME")
                #pseudo_start_time = Chunk.fits.return_info("PSTIME")
                datetime_array = DatetimeFuncs.build_datetime_array(pseudo_start_datetime,time_array)
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
                return SpectrogramFuncs.join_spectrograms(to_join) 

    def remove_non_fits_files_from_data(self,):
        # Loop through files in the directory
        #for each file in data [will be in some subdirectory according to its date]
        all_files = self.list_all_files()
        for file in all_files:
            pseudo_start_time,ext = os.path.splitext(file)
            # If the file is not a compressed-spectrogram, delete
            if ext!=".fits":
                file_dir = DatetimeFuncs.build_data_dir_from_pseudo_start_time(pseudo_start_time)
                file_path = os.path.join(file_dir, file)
                os.remove(file_path)
                print(f"Deleted {file}")
        pass  
       
    def find_nearest_chunk(self,look_after_datetime):
        for Chunk in self.dict.values():
            if Chunk.pseudo_start_datetime <= look_after_datetime:
                pass
            else:
                return Chunk

    def get_background_spectrogram(self,**kwargs):
        start_background_str = kwargs.get("start_background",CONFIG.background_interval[0])
        end_background_str = kwargs.get("end_background",CONFIG.background_interval[1])
        return self.build_spectrogram_from_range(start_background_str,end_background_str)

    # def find_neighbouring_chunk(self,Chunk,**kwargs):
    #     go_backwards = kwargs.get("go_backwards",False)

        


    