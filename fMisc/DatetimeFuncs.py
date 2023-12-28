from datetime import datetime
from datetime import timedelta
import numpy as np
from fMisc.sys_vars import sys_vars
import os

class DatetimeFuncs:
    def __init__(self,):
        self.sys_vars=sys_vars()

    '''
    function which builds the data directory for the current day
    '''

    def build_data_dir_today(self):
        # Get the current date
        current_date = datetime.now()
        # Format the date to YYYY/mm/dd with leading zeros for month and day
        date_path_today = current_date.strftime("%Y/%m/%d")
        return os.path.join(self.sys_vars.path_to_data, date_path_today)

    '''
    function which builds the data directory for a particular pseudo_start_time [in the default format]
    '''
    
    def build_data_dir_from_pseudo_start_time(self,pseudo_start_time):
        # Parse the datetime string to a datetime object
        dt_obj = datetime.strptime(pseudo_start_time, self.sys_vars.default_time_format)
        # Format the datetime object to the desired string format
        formatted_date = dt_obj.strftime("%Y/%m/%d")
        return os.path.join(self.sys_vars.path_to_data, formatted_date)
    
    '''
    function which takes a starting datetime, and an array of times [from 0] and builds the 
    corresponding datetime array
    '''
    
    def build_datetime_array(self,start_datetime,time_array):
        #create an empty list to hold the datetimes
        datetime_array = []
        #for each time in time array, form the datetime object and append it to the list
        for i in range(0,len(time_array)):
            new_datetime = start_datetime + timedelta(seconds=time_array[i])
            datetime_array.append(new_datetime)
        #return the list
        return datetime_array

    def datetime64_array_to_seconds(self, datetime64_array):
        # Convert the entire array to float representing seconds
        # This retains precision for milliseconds or microseconds
        seconds_array = (datetime64_array-datetime64_array[0]).astype('timedelta64[ns]').astype(float) / 1e9
        #displace by the sample rate
        return seconds_array
    
    def parse_datetime(self,datetime_string):
        #extract the corresponding datetime
        try:
            return datetime.strptime(datetime_string,self.sys_vars.default_time_format)
        except:
            raise SystemError("Could not parse {}. Need in the format {}".format(datetime_string,self.sys_vars.default_time_format))

    def to_string(self,datetime_obj):
        return datetime.strftime(datetime_obj,self.sys_vars.default_time_format)

    def is_in(self,datetime_obj, datetime_array):
        # Iterate through datetimeArray in pairs (t0,t1), (t1,t2), ...
        for i in range(len(datetime_array) - 1):
            start = datetime_array[i]
            end = datetime_array[i + 1]

            # Check if datetimeObj falls within the current range
            if start <= datetime_obj <= end:
                return True

        # If datetimeObj is not in any range, return False
        return False

    def find_closest_index(self,datetime_obj, datetime_array):
        # Initialize variables to store the index of the closest match and the smallest difference
        closest_index = None
        smallest_diff = float('inf')

        # Iterate through the array to find the closest datetime
        for i, datetime_element in enumerate(datetime_array):
            diff = abs((datetime_obj - datetime_element).total_seconds())
            
            # Update the closest match if a smaller difference is found
            if diff < smallest_diff:
                smallest_diff = diff
                closest_index = i

        return closest_index
