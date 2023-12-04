from datetime import datetime
from datetime import timedelta
from fMisc.sys_vars import sys_vars

class datetimeFuncs:
    def __init__(self,):
        self.sys_vars=sys_vars()

    '''
    function which takes a starting datetime, and an array of times [from 0] and builds the 
    corresponding datetime array
    '''
    def buildDatetimeArray(self,StartDatetime,timeArray):
        #create an empty list to hold the datetimes
        datetimeArray = []
        #for each time in time array, form the datetime object and append it to the list
        for time in timeArray:
            newDatetime = StartDatetime + timedelta(seconds=time)
            datetimeArray.append(newDatetime)
        #return the list
        return datetimeArray

    def toSeconds(self, datetimeArray):
        # Convert the entire array to float representing seconds
        # This retains precision for milliseconds or microseconds
        secondsArray = (datetimeArray - datetimeArray[0]).astype('timedelta64[ns]').astype(float) / 1e9
        
        return secondsArray.tolist()
    
    def parseDatetime(self,datetimeString):
        #extract the corresponding datetime
        try:
            return datetime.strptime(datetimeString,self.sys_vars.default_time_format)
        except:
            raise SystemError("Could not parse {}. Need in the format {}".format(datetimeString,self.sys_vars.default_time_format))

    def fromString(self,datetimeObj):
        return datetime.strftime(datetimeObj,self.sys_vars.default_time_format)

    def isIn(self,datetimeObj, datetimeArray):
        # Iterate through datetimeArray in pairs (t0,t1), (t1,t2), ...
        for i in range(len(datetimeArray) - 1):
            start = datetimeArray[i]
            end = datetimeArray[i + 1]

            # Check if datetimeObj falls within the current range
            if start <= datetimeObj <= end:
                return True

        # If datetimeObj is not in any range, return False
        return False

    def findClosestIndex(self,datetimeObj, datetimeArray):
        # Initialize variables to store the index of the closest match and the smallest difference
        closest_index = None
        smallest_diff = float('inf')

        # Iterate through the array to find the closest datetime
        for i, datetime_element in enumerate(datetimeArray):
            diff = abs((datetimeObj - datetime_element).total_seconds())
            
            # Update the closest match if a smaller difference is found
            if diff < smallest_diff:
                smallest_diff = diff
                closest_index = i

        return closest_index
