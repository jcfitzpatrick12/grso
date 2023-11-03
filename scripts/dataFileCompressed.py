'''
class which deals with a single compressed dataFile
'''

import os
import numpy as np
from Plotter import Plotter

class dataFileCompressed:
    def __init__(self,pseudo_start_time):
        self.pseudo_start_time=pseudo_start_time
        #build the data file dict
        self.buildAveragedDataDict()
        self.Sxx = self.AveragedDataDict['Sxx']
        self.datetimeArray = self.AveragedDataDict['datetimeArray']
        self.center_freq = self.AveragedDataDict['center_freq']
        self.freqsMHz = self.AveragedDataDict['freqsMHz']
        self.dfreqHz = (self.freqsMHz[1]-self.freqsMHz[0])*10**6
        self.samp_rate = self.AveragedDataDict['samp_rate']

        #build the total power
        self.buildPower()

    def customFilePath(self,customString):
        return os.path.join(os.getcwd(),"Pdata",customString+self.pseudo_start_time)
    
    def buildAveragedDataDict(self):
        self.customFilePath("average")
        AveragedDataDict = np.load(self.customFilePath("average")+".npy",allow_pickle=True).item()
        self.AveragedDataDict=AveragedDataDict
        pass


    def buildPower(self):
        num_freq_bins = np.shape(self.Sxx)[0]
        num_time_bins = np.shape(self.Sxx)[1]
        power = np.empty(num_time_bins)

        for i in range(num_time_bins):
            power[i]=np.sum(self.Sxx[:,i])*self.dfreqHz

        self.power=power
        pass

    def plotSpectrogram(self,**kwargs):
        Plotter().plotSpectrogram(self.freqsMHz,self.datetimeArray,self.Sxx)
        pass

    def plotPower(self):
        Plotter().plotPower(self.datetimeArray,self.power)
        pass





        