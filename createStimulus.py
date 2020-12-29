#! /use/bin/env python
''' **************************************
# Author       :leo-Ne
# Last modified:2020-12-29 14:45
# Email        : leo@email.com
# Filename     :createStimulus.py
# Description  : 
**************************************'''
import cv2 as cv
import numpy as np 
import time as time 
import matplotlib.pyplot as plt

class Stimulus:

    def __init__(self, stimulusNumber=0, monitorRate=60):
        self._nStimulus = stimulusNumber
        self._monitorRate = monitorRate
        self._framePeriod = int(1000.0 / monitorRate + 0.5)   # meansurement: ms
        self._stimulusSeries = {'nStimulus': stimulusNumber}
        pass

    def createStimulusSquareWave(self, position:list[int], size:int, 
            stiFreq=10.0, dutyfactor=0.5, tBegin=0.001, stimulusName=None):
        stimulusSeries  = self._stimulusSeries.copy()
        framePeriod     = self._framePeriod
        tLight          = int(dutyfactor * 1000.0 / stiFreq / framePeriod + 0.5) # ms
        tPeriod         = int(1000.0 / stiFreq / framePeriod + 0.5)        
        tDark           = int(tPeriod - tLight)
        lightnessSeries = [255, 0]
        timeSeries      = [tLight, tDark]
        position        = position
        size            = size
        tBegin          = int(1000 * tBegin)

        stimulus        = {
                'timeSeries'     : timeSeries,
                'lightnessSeries': lightnessSeries,
                'position'       : position,
                'size'           : size,
                'tBegin'         : tBegin,              # stimulus firstly start. ms
                'frameStepCnt'   : 0
                         }
        if stimulusName is None:
            stimulusName                = str(stimulusSeries['nStimulus'])
        stimulusSeries['nStimulus'] = stimulusSeries['nStimulus']+ 1
        stimulusSeries.update({stimulusName: stimulus})
        self._stimulusSeries        = stimulusSeries.copy()
        del stimulusSeries, tLight, tPeriod, tDark, lightnessSeries, timeSeries, position, size, stimulus
        self._nStimulus += 1
        pass

    def createStimulusSinWave(self, position:list[int], size:int, 
            stiFreq=10.0, amp=255, offset=0, tBegin=0.001, stimulusName=None):

        stimulusSeries  = self._stimulusSeries.copy()
        framePeriod     = self._framePeriod
        # timeSeriesLength defined as fellowed.
        timeSeriesLength= int(stiFreq * 5 * framePeriod)
        n               = np.arange(0, timeSeriesLength,step=1,dtype=np.int16)
        lightness_n     = (amp / 2) * np.sin(2*np.pi*stiFreq * framePeriod * n / 1000.0 - np.pi/2) + (amp / 2)
        lightness_n     = np.uint8(lightness_n)
        lightnessSeries = lightness_n.copy()

        timeSeries      = np.ones_like(lightness_n)
        position        = position
        size            = size
        tBegin          = int(1000 * tBegin)

        stimulus        = {
                'timeSeries'     : timeSeries,
                'lightnessSeries': lightnessSeries,
                'frequency'      : stiFreq,
                'nFrame'         : timeSeriesLength,
                'position'       : position,
                'size'           : size,
                'tBegin'         : tBegin,
                'frameStepCnt'   : 0
                         }
        if stimulusName is None:
            stimulusName                = str(stimulusSeries['nStimulus'])
        stimulusSeries['nStimulus'] = stimulusSeries['nStimulus']+ 1
        stimulusSeries.update({stimulusName: stimulus})
        self._stimulusSeries        = stimulusSeries.copy()
        del stimulusSeries, framePeriod, timeSeriesLength, n, lightness_n
        del lightnessSeries, timeSeries, position, size, tBegin, stimulus
        self._nStimulus += 1
        pass
    
    def showStimulusInfo(self, stimulusName=None):
        """
        Method to show the infomation of stimuluses ceated.
        """
        stimulusSeries  = self._stimulusSeries.copy()
        framePeriod     = self._framePeriod
        print("<==================================================>")
        print('Monitor refresh rate:\t', self._monitorRate, 'Hz')
        print('framePeriod:\t\t', self._framePeriod, 'ms')
        print("<==================================================>")
        keys = list(stimulusSeries.keys())
        keys.remove('nStimulus')
        for i, key in enumerate(keys):
            outputInfo = r''
            stimulus = stimulusSeries[key]
            print("\tStimulus No:", i, ',\tStimulusName:', key)
            if len(stimulus['timeSeries']) != 2 :
                print('\t\tposition:\t', stimulus['position'], '\t[x, y]')
                print('\t\tsize:\t\t', stimulus['size'], '\t\tpixels.')
                print('\t\tfrequency:\t', stimulus['frequency'], '\t\tHz.')
                print('\t\tframe length:\t', stimulus['nFrame'], '\t\tframe.')
                print('\t\ttBegin:\t\t', stimulus['tBegin'], '\t\tms.')
            else:
                print('\t\tposition:\t', stimulus['position'], '\t[x, y]')
                print('\t\tsize:\t\t', stimulus['size'], '\t\tpixels.')
                print('\t\tlightnessSeries:', stimulus['lightnessSeries'], '\tper frame.')
                print('\t\ttimeSeries:\t', stimulus['timeSeries'], '\tframePeriod.')
                print('\t\ttBegin:\t\t', stimulus['tBegin'], '\t\tms.')
            print('\t==========================================')
        pass

def UnitTest():
    stimulus = Stimulus()
    stimulus.createStimulusSquareWave([1, 1], 10, 10, stimulusName='SquareWave1')
    stimulus.createStimulusSinWave([1, 1], 10, 5.4, stimulusName='SinWave1')
    stimulus.showStimulusInfo()
    pass

if __name__ == "__main__":
    UnitTest()

