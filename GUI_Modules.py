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

class GUI:
    """
    This test code was programmed in Linux system, of which monitor has a 60Hz refresh.
    """
    def __init__(self, screenType='full', screenHeight=400, screenWidth=600, monitorRate=60):
        """
        screenType: 
            'full': means occuping whole screen.
            'float': means creat a floating window.
        """
        # Class properties.
        self._refreshRate    = monitorRate
        self._framePeriod    = int(1000.0 / monitorRate + 0.5)   # meansurement: ms
        self._screenWidth    = None
        self._screenHeight   = None
        self._colorSpace     = r'RGB'
        self._canvas         = None
        self._displayType    = screenType
        self._stimulusSeries = {'nStimulus' : 0}
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
        # clock counter start here. Time meansurement: ms
        self._clockStartTime   = 0.0
        pass

    def addStimuls(self, x_position, y_position, lightness, size=None):
        """
        Stimulus will alter according to lightness. The lightness is limited from 0 to 255.
        Now, this method was designed for creating square stimulus.
        """
        if  size is None:
            size = np.int(self._screenHeight / 10)
        canvas = self._canvas
        x      = x_position
        y      = y_position
        RGB    = (lightness, lightness, lightness)
        cv.rectangle(canvas,(x, y), (x+size, y+size),RGB, -1)
        self._canvas = canvas
        del canvas, x, y, RGB
        return

    def creatStimulusSeries(self, position, size, stiFreq=10.0, dutyfactor=0.5, tBegin=0.001, stimulusName=None):
        """
        lFrame means the mounts of the pictures inclued in one stimulus.
        This function will create a sequence of lightness. The lightness sequence should be used in method addStimuls().
        """
        stimulusSeries  = self._stimulusSeries.copy()
        framePeriod     = self._framePeriod
        tLight          = int(dutyfactor * 1000.0 / stiFreq / framePeriod + 0.5) # ms
        tPeriod         = int(1000.0 / stiFreq / framePeriod + 0.5)        # tPeriod ms in a period of a stimulus.
        print(tPeriod)
        tDark           = int(tPeriod - tLight)
        lightness       = 255
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
        del stimulusSeries, tLight, tPeriod, tDark, lightness, lightnessSeries, timeSeries, position, size, stimulus
        return 

    def displayGUI(self):
        height          = self._screenWidth
        width           = self._screenWidth
        canvas          = self._canvas.copy()
        stimulusSeries  = self._stimulusSeries.copy()
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
        print("Loaded Stimulues:")
        for i in range(nStimulus):
            print('\t', i, 
                    '\n\tposition:',positionMatrix[i], 
                    '\n\tsize:',sizeMatrix[i],
                    '\n\tlightnessSeries:', lightnessMatrix[i],
                    '\n\ttimeSeries:',stayTimeMatrix[i])
        ### output stimulus to screen ###
        tStart = time.perf_counter_ns() 
        while True:
            # Initialize the canvas buffer
            tCurrent = int((time.perf_counter_ns() - tStart) / 1e6)
            print("\rtCurrent:", tCurrent, 'ms.', flush=True, end='')
            self._canvas = np.zeros_like(canvas)
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
                if cv.waitKey(1) & 0xFF == ord('q'):
                    print("Stimulating stopped!")
                    exit('Quit:<keycode q to quit>')
        pass

def unitTest():
    gui = GUI(screenType='float',screenHeight=200,screenWidth=200)
    gui.creatStimulusSeries([100, 100], None, 4.0, 0.5,1.0, 'Square')
    gui.creatStimulusSeries([60, 60], None, 30.0, 0.5)
    gui.displayGUI()
    return 

if __name__ == "__main__":
    unitTest()
    pass

