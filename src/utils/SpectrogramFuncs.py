import numpy as np
from src.utils import DatetimeFuncs
from src.fSpectrogram.RadioSpectrogram import RadioSpectrogram
'''
join a number of spectrograms [stored in the to_join list]

-pads in between with zero, since there will be a couple of seconds of downtime
-we don't need to worry about the spectrograms being time ordered as the dictionary is already sorted in Chunks
'''

def join_spectrograms(list_of_spectrograms_to_join):
    #find the number of spectrograms to join
    num_to_join = len(list_of_spectrograms_to_join)
    # Padding columns: one less than the number of spectrograms
    num_zero_cols = num_to_join - 1
    #initialise an array to hold the time dimension 
    num_time_bin_edges = []
    #create a list to hold the datetime64 array for each spectrogram
    #for each Spectrogram, in those to join.
    for i, S in enumerate(list_of_spectrograms_to_join):
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
    
    return RadioSpectrogram(joined_Sxx,joined_time_array,S.freqs_MHz,S.center_freq,new_pseudo_start_time,S.is_averaged)
    