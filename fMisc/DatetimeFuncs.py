from datetime import datetime
from datetime import timedelta
from fMisc.sys_vars import sys_vars

class DatetimeFuncs:
    def __init__(self,):
        self.sys_vars=sys_vars()

    '''
    function which takes a starting datetime, and an array of times [from 0] and builds the 
    corresponding datetime array
    '''
    def build_datetime_array(self,start_datetime,time_array):
        #create an empty list to hold the datetimes
        datetime_array = []
        #for each time in time array, form the datetime object and append it to the list
        for time in time_array:
            new_datetime = start_datetime + timedelta(seconds=time)
            datetime_array.append(new_datetime)
        #return the list
        return datetime_array

    def to_seconds(self, datetime_array):
        # Convert the entire array to float representing seconds
        # This retains precision for milliseconds or microseconds
        seconds_array = (datetime_array - datetime_array[0]).astype('timedelta64[ns]').astype(float) / 1e9
        return seconds_array.tolist()
    
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
