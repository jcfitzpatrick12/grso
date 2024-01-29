# import numpy as np
# import os
# import pickle

# from src.fConfig import CONFIG
# from src.utils import DatetimeFuncs


# class ChunkNpy:
#     def __init__(self,chunk_start_time):
#         self.chunk_start_time=chunk_start_time
#         self.data_dir=DatetimeFuncs.build_data_dir_from_chunk_start_time(CONFIG.path_to_data, self.chunk_start_time)

#     #find the path to the binary
#     def get_path(self):
#         return os.path.join(self.data_dir,self.chunk_start_time+".npy")
    
#     #find out if the path exists
#     def exists(self):
#         return os.path.exists(self.get_path())
    
#     def load_radio_spectrogram(self):
#         if self.exists():
#             # Load the array from the .npy file
#             loaded_array = np.load(self.get_path(), allow_pickle=True)
#             # Convert the array back to a byte stream
#             byte_stream = loaded_array.tobytes()
#             # Deserialize the instance from bytes using pickle
#             instance = pickle.loads(byte_stream)
#         else:
#             raise SystemError('No file found!')
#         return instance