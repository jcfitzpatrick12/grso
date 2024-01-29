import numpy as np
from src.utils import DatetimeFuncs

def Sxx_to_dBb(Sxx,background_vector):
    background_vector_array = np.ones(np.shape(Sxx))
    num_freqs = np.shape(Sxx)[0]
    for freq_bin_ind in range(num_freqs-1):
        background_vector_array[freq_bin_ind,:]*=background_vector[freq_bin_ind]
    Sxx_dBb = 10*np.log10(Sxx/background_vector_array)
    return Sxx_dBb

    