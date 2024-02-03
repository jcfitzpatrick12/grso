import numpy as np
from src.spectrogram.RadioSpectrogram import RadioSpectrogram
from src.utils import DatetimeFuncs, ArrayFuncs
from src.configs import GLOBAL_CONFIG


def frequency_chop(S, start_freq_MHz, end_freq_MHz):
    #find the index of the nearest matching datetime elements in the array
    startIndex = ArrayFuncs.find_closest_index(start_freq_MHz,S.freqs_MHz)
    endIndex = ArrayFuncs.find_closest_index(end_freq_MHz,S.freqs_MHz)

    if startIndex>endIndex:
        startIndex, endIndex = endIndex, startIndex
        
    chopped_Sxx=S.Sxx[startIndex:endIndex, :]
    chopped_freqs_MHz = S.freqs_MHz[startIndex:endIndex+1]
    bvect_chopped = S.background_vector[startIndex:endIndex+1]
    #return the chopped S
    return RadioSpectrogram(chopped_Sxx, S.time_array, chopped_freqs_MHz, S.center_freq, S.chunk_start_time, S.tag, bvect = bvect_chopped)
    
def time_chop(S, start_str, end_str):
    #parse the strings into datetimes
    start_dt = DatetimeFuncs.strptime(start_str, GLOBAL_CONFIG.default_time_format)
    end_dt = DatetimeFuncs.strptime(end_str, GLOBAL_CONFIG.default_time_format)
    #find the index of the nearest matching datetime elements in the array
    startIndex = DatetimeFuncs.find_closest_index(start_dt,S.datetime_array)
    endIndex = DatetimeFuncs.find_closest_index(end_dt,S.datetime_array)
    #if our start and end indices are identical, the requested range is entirely outwith the RadioSpectrom
    #return the default null spectrogram
    if startIndex==endIndex:
        raise SystemError("Start and end indices are equal! Cannot chop.")

    #chop the spectrogram and time values accordinglys
    chopped_Sxx=S.Sxx[:,startIndex:endIndex]
    chopped_timeArray = S.time_array[startIndex:endIndex+1]
    #translate the chopped_timeArray to again start at zero.
    chopped_timeArray-=chopped_timeArray[0]
    #extract the new chunk_start_time
    chopped_chunk_start_time = DatetimeFuncs.to_string(S.datetime_array[startIndex])
    #return the chopped S
    return RadioSpectrogram(chopped_Sxx,chopped_timeArray,S.freqs_MHz,S.center_freq,chopped_chunk_start_time, S.tag)

def time_average(S, average_over_int):
    if average_over_int==1:
        return S
    #find the number of frequenct samples
    num_freq_samples = np.shape(S.Sxx)[0]
    #find the number of temporal samples
    num_temporal_samples = np.shape(S.Sxx)[1]
    #print(num_temporal_samples)
    #eshorten the call of how many samples to average over
    N=average_over_int
    #find the remainder [we will average over the remaining samples if N does note exactly divide num_temporal_samples]
    remainder = num_temporal_samples % N
    
    #find the number of temporal_samples_after averaging
    num_temporal_samples_after_averaging = num_temporal_samples//N
    
    #if the remainder is non-zero, introduce a final term which we will handle uniquely [average over the remaining terms]
    if remainder:
        num_temporal_samples_after_averaging+=1

    #instantiate an array to hold the averaged spectrogram
    average_Sxx = np.empty((num_freq_samples,num_temporal_samples_after_averaging))

    #create an array to hold the decimated datetime array
    time_array_decimated = []

    #loop through the spectrogram and average the columns
    for i in range(num_temporal_samples_after_averaging):
        average_Sxx[:,i] = np.mean(S.Sxx[:,N*i:N*i+N],axis=1)
        time_array_decimated.append(S.time_array[i*N])
    
    #add the final bin edge for the decimated time array
    dt = time_array_decimated[-2]-time_array_decimated[-3]
    time_array_decimated.append(time_array_decimated[-1]+dt)

    #if there is a non-zero remainder, just cut the final entry
    if remainder:
        #average_Sxx[:,-1] = np.nanmean(S.Sxx[:,-remainder:],axis=1)
        average_Sxx=average_Sxx[:,:-1]
        time_array_decimated=time_array_decimated[:-1]
    return RadioSpectrogram(average_Sxx,time_array_decimated,S.freqs_MHz,S.center_freq,S.chunk_start_time, S.tag)

def frequency_average(S, average_over_int):
        if average_over_int==1:
            return S
        #find the number of frequenct samples
        num_freq_samples = np.shape(S.Sxx)[0]
        #find the number of temporal samples
        num_temporal_samples = np.shape(S.Sxx)[1]
        #print(num_temporal_samples)
        #eshorten the call of how many samples to average over
        N=average_over_int
        #find the remainder [we will average over the remaining samples if N does note exactly divide num_temporal_samples]
        remainder = num_temporal_samples % N
        
        #find the number of temporal_samples_after averaging
        num_frequency_samples_after_averaging = num_freq_samples//N
        
        #if the remainder is non-zero, introduce a final term which we will handle uniquely [average over the remaining terms]
        if remainder:
            num_frequency_samples_after_averaging+=1

        #instantiate an array to hold the averaged spectrogram
        average_Sxx = np.empty((num_frequency_samples_after_averaging, num_temporal_samples))

        #create an array to hold the decimated datetime array
        frequency_array_decimated = []

        #loop through the spectrogram and average the columns
        for i in range(num_frequency_samples_after_averaging):
            average_Sxx[i,:] = np.mean(S.Sxx[N*i:N*i+N,:],axis=0)
            frequency_array_decimated.append(S.freqs_MHz[i*N])
        
        #add the final bin edge for the decimated time array
        dfreq = frequency_array_decimated[-2]-frequency_array_decimated[-3]
        frequency_array_decimated.append(frequency_array_decimated[-1]+dfreq)

        #if there is a non-zero remainder, just cut the final entry
        if remainder:
            average_Sxx[-1,:] = np.nanmean(S.Sxx[-remainder:,:],axis=0)
            #average_Sxx=average_Sxx[:-1,:]
            #frequency_array_decimated=frequency_array_decimated[:-1]

        bvect_averaged = ArrayFuncs.average_every_n_elements(S.background_vector, N)
        return RadioSpectrogram(average_Sxx,S.time_array,frequency_array_decimated,S.center_freq,S.chunk_start_time, S.tag, bvect = bvect_averaged)


def join_spectrograms(list_of_spectrograms_to_join):
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
        
        return RadioSpectrogram(joined_Sxx, joined_time_array, S.freqs_MHz, S.center_freq, new_chunk_start_time, S.tag)