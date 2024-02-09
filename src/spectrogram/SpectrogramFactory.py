import numpy as np

from src.utils import DatetimeFuncs, ArrayFuncs
from src.configs import GLOBAL_CONFIG
from src.configs.tag_maps.tag_to_radio_spectrogram import tag_to_radio_spectrogram_dict


def frequency_chop(S, start_freq_MHz, end_freq_MHz):
    #find the index of the nearest matching datetime elements in the array
    startIndex = ArrayFuncs.find_closest_index(start_freq_MHz,S.freqs_MHz)
    endIndex = ArrayFuncs.find_closest_index(end_freq_MHz,S.freqs_MHz)

    if startIndex>endIndex:
        startIndex, endIndex = endIndex, startIndex
        
    chopped_Sxx=S.Sxx[startIndex:endIndex+1, :]
    chopped_freqs_MHz = S.freqs_MHz[startIndex:endIndex+1]

    if S.bvect is None:
        bvect = None
    else:
        bvect = S.bvect[startIndex:endIndex+1]
    
    RadioSpectrogram = tag_to_radio_spectrogram_dict[S.tag]
    return RadioSpectrogram(chopped_Sxx, S.time_array, chopped_freqs_MHz, S.chunk_start_time, S.tag, bvect = bvect)
    

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
    chopped_Sxx=S.Sxx[:,startIndex:endIndex+1]
    chopped_timeArray = S.time_array[startIndex:endIndex+1]
    #translate the chopped_timeArray to again start at zero.
    chopped_timeArray-=chopped_timeArray[0]
    #extract the new chunk_start_time
    chopped_chunk_start_time = DatetimeFuncs.to_string(S.datetime_array[startIndex])

    RadioSpectrogram = tag_to_radio_spectrogram_dict[S.tag]
    return RadioSpectrogram(chopped_Sxx,chopped_timeArray,S.freqs_MHz, chopped_chunk_start_time, S.tag, bvect = S.bvect)


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
    
    # #add the final bin edge for the decimated time array
    # dt = time_array_decimated[-2]-time_array_decimated[-3]
    # time_array_decimated.append(time_array_decimated[-1]+dt)

    #if there is a non-zero remainder, just cut the final entry
    if remainder:
        #average_Sxx[:,-1] = np.nanmean(S.Sxx[:,-remainder:],axis=1)
        average_Sxx=average_Sxx[:,:-1]
        time_array_decimated=time_array_decimated[:-1]

    RadioSpectrogram = tag_to_radio_spectrogram_dict[S.tag]
    return RadioSpectrogram(average_Sxx, time_array_decimated, S.freqs_MHz, S.chunk_start_time, S.tag, bvect = S.bvect)


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
        
        # #add the final bin edge for the decimated time array
        # dfreq = frequency_array_decimated[-2]-frequency_array_decimated[-3]
        # frequency_array_decimated.append(frequency_array_decimated[-1]+dfreq)

        #if there is a non-zero remainder, just cut the final entry
        if remainder:
            average_Sxx[-1,:] = np.nanmean(S.Sxx[-remainder:,:],axis=0)
            #average_Sxx=average_Sxx[:-1,:]
            #frequency_array_decimated=frequency_array_decimated[:-1]

        if S.bvect is None:
            bvect = None
        else:
            bvect = ArrayFuncs.average_every_n_elements(S.bvect, N)

        RadioSpectrogram = tag_to_radio_spectrogram_dict[S.tag]
        return RadioSpectrogram(average_Sxx, S.time_array, frequency_array_decimated, S.chunk_start_time, S.tag, bvect = bvect)



def join_spectrograms(list_of_spectrograms_to_join):
    # Check if the list is empty
    if not list_of_spectrograms_to_join:
        raise ValueError("No spectrograms to join!")

    # Initialize variables
    total_time_samples = 0
    num_freq_samples = len(list_of_spectrograms_to_join[0].freqs_MHz)
    new_chunk_start_time = list_of_spectrograms_to_join[0].chunk_start_time

    # Determine the total number of time samples across all spectrograms
    time_arrays = [S.time_array for S in list_of_spectrograms_to_join]
    total_time_samples = sum(map(len, time_arrays))

    # num_spectrograms_to_join = len(list_of_spectrograms_to_join)
    # Since we're dealing with bin centres, no need for padding zeros between spectrograms
    joined_Sxx = np.zeros((num_freq_samples, total_time_samples))
    joined_datetime_array = np.concatenate([S.datetime64_array for S in list_of_spectrograms_to_join])

    # Fill in the joined spectrogram array
    start_index = 0
    for S in list_of_spectrograms_to_join:
        end_index = start_index + len(S.time_array)

        #for clean plotting only [ensures whitespace at the joins]
        S.Sxx[:,0] = 0
        S.Sxx[:,-1] = 0

        joined_Sxx[:, start_index:end_index] = S.Sxx
        start_index = end_index

    # Convert datetime array to seconds since the first chunk's start time
    joined_time_array = DatetimeFuncs.datetime64_array_to_seconds(joined_datetime_array)

    # Create and return the new RadioSpectrogram object
    RadioSpectrogram = tag_to_radio_spectrogram_dict[list_of_spectrograms_to_join[0].tag]
    return RadioSpectrogram(joined_Sxx, joined_time_array, list_of_spectrograms_to_join[0].freqs_MHz, new_chunk_start_time, list_of_spectrograms_to_join[0].tag)
