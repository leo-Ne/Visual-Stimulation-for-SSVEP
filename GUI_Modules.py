#! /use/bin/env python
''' **************************************
# Author       :leo-Ne
# Last modified:2020-12-28 22:21
# Email        : leo@email.com
# Filename     :GUI_Modules.py
# Description  : 
**************************************'''
import numpy as np
import cv2  as cv
import tkinter as tk
import time
from createStimulus import *

class GUI:
    """
    This test code was programmed in Linux system, of which monitor has a 60Hz refresh.
    """
    def __init__(self,tRun=10.0, screenType='full', screenHeight=400, screenWidth=600, monitorRate=60):
        """
        screenType: 
            'full': means occuping whole screen.
            'float': means creat a floating window.
        """
        # Class properties.
        self._tRun           = int(tRun * 1000)
        self._refreshRate    = monitorRate
        self._framePeriod    = int(1000.0 / monitorRate + 0.5)   # meansurement: ms
        self._screenWidth    = None
        self._screenHeight   = None
        self._colorSpace     = r'RGB'
        self._canvas         = None
        self._displayType    = screenType
        # initialize the stimulus infomation
        self._stimulus       = Stimulus(stimulusNumber=0,monitorRate=monitorRate)
        self._stimulusSeries =  self._stimulus._stimulusSeries
        # Initial assignment for Class properties
        display        = tk.Tk()
        display_width  = display.winfo_screenwidth()
        display_height = display.winfo_screenheight()
        if screenType== 'full':
            self._screenWidth  = display_width
            self._screenHeight = display_height
        elif screenType == 'float':
            self._screenWidth  = screenWidth
            self._screenHeight = screenHeight
        else:
            print('Error:<GUI __init__()> None screenType:'+str(screenType)+'.')
        self._canvas=np.zeros([self._screenHeight, self._screenWidth], np.uint8)
        pass

    def createStimulusSquareWave(self, position:list[int], size:int,
            stiFreq=10.0, dutyfactor=0.5, tBegin=0.001, stimulusName=None):
        """
        lFrame means the mounts of the pictures inclued in one stimulus.
        This function will create a sequence of lightness. The lightness sequence should be used in method addStimuls().
        """
        self._stimulus.createStimulusSquareWave(position,size,stiFreq,dutyfactor,tBegin,stimulusName)
        return 

    def createStimulusSinWave(self, position:list[int], size:int, 
            stiFreq=10.0, amp=255, offset=0, tBegin=0.001, stimulusName=None):
        self._stimulus.createStimulusSinWave(position,size,stiFreq,amp,offset,tBegin,stimulusName)
        return 

    def showStimulusInfo(self, stimulusName=None):
        self._stimulus.showStimulusInfo(stimulusName)
        return

    def addStimuls(self, x_position, y_position, lightness, size=None):
        """
        Stimulus will alter according to lightness. The lightness is limited from 0 to 255.
        Now, this method was designed for creating square stimulus.
        """
        if  size is None:
            size = np.int(self._screenHeight / 10)
        canvas    = self._canvas
        x         = x_position
        y         = y_position
        lightness = int(lightness)
        RGB       = (lightness, lightness, lightness)
        cv.rectangle(canvas,(x, y), (x+size, y+size),RGB, -1)
        self._canvas = canvas
        del canvas, x, y, RGB
        return

    def displayGUI(self, quitKey='q'):
        height          = self._screenWidth
        width           = self._screenWidth
        canvas          = self._canvas.copy()
        stimulusSeries  = self._stimulus._stimulusSeries.copy()
        framePeriod     = self._framePeriod
        ### default setting: dispaly UI occuping the screen ###
        print("Initializing GUI....")
        displayType = self._displayType
        windowFlag  = cv.WINDOW_FULLSCREEN
        if displayType == 'float':
            windowFlag = cv.WINDOW_NORMAL
        outWin = r'UI window'
        cv.namedWindow(outWin,cv.WINDOW_NORMAL)
        cv.setWindowProperty(outWin,cv.WINDOW_NORMAL, windowFlag)
        cv.imshow(outWin, canvas)

        ### Load the stimuluses ###
        print("Loading Stimulues...")
        keys = list(stimulusSeries.keys())
        keys.remove('nStimulus')
        index = np.zeros([stimulusSeries['nStimulus']], np.int32)
        lightnessMatrix    = []
        stayTimeMatrix     = []
        positionMatrix     = []
        sizeMatrix         = []
        tBeginVector       = []
        frameStepCntVector = []
        for key in keys:
            stimulus = stimulusSeries[key]
            lightnessMatrix.append(stimulus['lightnessSeries'])
            stayTimeMatrix.append(stimulus['timeSeries'])
            positionMatrix.append(stimulus['position'])
            sizeMatrix.append(stimulus['size'])
            tBeginVector.append(stimulus['tBegin'])
            frameStepCntVector.append(stimulus['frameStepCnt'])
        nStimulus = len(keys)
        del keys, stimulusSeries
        #### debug codes, suggest that not delete it ###
        tStart = time.perf_counter_ns() 
        while True:
            # Initialize the canvas buffer
            tCurrent = int((time.perf_counter_ns() - tStart) / 1e6)
            inputKey = cv.waitKey(1) & 0xFF
            print("\rtCurrent:", tCurrent, 'ms.', flush=True, end='')
            self._canvas = np.zeros_like(canvas)
            if self._tRun > 0 and tCurrent >= self._tRun and inputKey != ord(quitKey):
                cv.imshow(outWin, self._canvas)
                continue
            # write stimuluses into screen buffer.
            for i in range(nStimulus):
                tBegin    = tBeginVector[i]
                if tCurrent < tBegin:
                    continue
                else:
                    idx          = index[i]
                    frameStepCnt = frameStepCntVector[i]
                    stayTime     = stayTimeMatrix[i][idx]
                    lightness    = lightnessMatrix[i][idx]
                    position     = positionMatrix[i]
                    size         = sizeMatrix[i]
                    self.addStimuls(position[0],position[1],lightness,size)
                    if frameStepCnt < stayTime:
                        frameStepCnt += 1
                    else:
                        frameStepCnt = 0
                        index[i] = (index[i] + 1) % len(stayTimeMatrix[i])    # next stayTime value, next series frame
                    frameStepCntVector[i] = frameStepCnt
            # display canvas on screen
            cv.imshow(outWin, self._canvas)
            cnt0 = 0
            while cnt0 < framePeriod:
                cnt0 += 1
                if inputKey == ord(quitKey):
                    print("Stimulating stopped!")
                    exit('Quit:<keycode '+quitKey+' to quit>')
        pass

def unitTest():
    gui = GUI(tRun=-1.0, screenType='float',screenHeight=200,screenWidth=200)
    gui.createStimulusSquareWave(
            position=[10,10],
            size=10,
            stiFreq=10.0,
            dutyfactor=0.5,
            tBegin=0.001,
            stimulusName='SquareWave1')
    gui.createStimulusSinWave(
            position=[100,100],
            size=10,
            stiFreq=5.4,
            amp=255,
            offset=0,
            tBegin=0.001,
            stimulusName='SinWave1')
    gui.displayGUI('q')
    return 

def demo():
    freq = [8., 9., 10., 11., 12., 13.]
    position1 = []
    position2 = []
    width    = 1920
    height   = 1080
    nFreq    = len(freq)
    size     = int(min(height/(2*nFreq+1), width/5))
    for i in range(nFreq):
        pos1 = [int((2*i+1)*width/(2*nFreq + 1)), int(height/5)] 
        pos2 = [int((2*i+1)*width/(2*nFreq + 1)), int(height*3/5)]
        position1.append(pos1)
        position2.append(pos2)
    # game begins here !!!!
    gui = GUI(tRun=-1.0,
            screenType='float',
            monitorRate=60.0,
            screenHeight=600,
            screenWidth=800)
    for i in range(nFreq):
        gui.createStimulusSquareWave(
                position=position1[i],
                size=size,
                stiFreq=freq[i],
                dutyfactor=0.5,
                tBegin=0.001,
                stimulusName='SquareWave'+str(i+1))
        gui.createStimulusSinWave(
                position=position2[i],
                size=size,
                stiFreq=freq[i],
                amp=255,
                offset=0,
                tBegin=0.001,
                stimulusName='SinWave'+str(i+1))
    gui.showStimulusInfo()
    gui.displayGUI(quitKey='q')
    return

if __name__ == "__main__":
#    unitTest()
    demo()
    pass

