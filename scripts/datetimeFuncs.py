from datetime import datetime
from datetime import timedelta

class datetimeFuncs:
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