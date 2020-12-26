#! /use/bin/env python
''' **************************************
# Author       :leo-Ne
# Last modified:2020-12-25 15:17
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
    def __init__(self, screenType='full', screenHeight=400, screenWidth=600):
        """
        screenType: 
            'full': means occuping whole screen.
            'float': means creat a floating window.
        """
        # Class properties.
        self._refresh        = 60
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
        print('<addStimuls()>, lightness:', lightness)
        cv.rectangle(canvas,(x, y), (x+size, y+size),RGB, -1)
        self._canvas = canvas
        del canvas, x, y, RGB
        return

    def creatStimulusSeries(self, position, size, stiFreq=10.0, dutyfactor=0.5, alterType=None):
        """
        lFrame means the mounts of the pictures inclued in one stimulus.
        This function will create a sequence of lightness. The lightness sequence should be used in method addStimuls().
        """
        stimulusSeries  = self._stimulusSeries.copy()
        tLight          = dutyfactor / stiFreq
        tPeriod         = 1.0 / stiFreq
        tDark           = tPeriod - tLight
        lightness       = 255
        lightnessSeries = [255, 0]
        timeSeries      = [tLight, tDark]
        position        = position
        size            = size
        stimulus        = {
                'timeSeries'     : timeSeries,
                'lightnessSeries': lightnessSeries,
                'position'       : position,
                'size'           : size
                         }
        stimulusName                = stimulusSeries['nStimulus']
        stimulusSeries['nStimulus'] = stimulusName + 1
        stimulusSeries.update({stimulusName: stimulus})
        self._stimulusSeries        = stimulusSeries.copy()
        del stimulusSeries, tLight, tPeriod, tDark, lightness, lightnessSeries, timeSeries, position, size, stimulus
        return 

    def displayGUI(self):
        height          = self._screenWidth
        width           = self._screenWidth
        canvas          = self._canvas.copy()
        stimulusSeries  = self._stimulusSeries.copy()
        # default setting: dispaly UI occuping the screen
        print("Initializing GUI....")
        displayType = self._displayType
        windowFlag  = cv.WINDOW_FULLSCREEN
        if displayType == 'float':
            windowFlag = cv.WINDOW_NORMAL
        outWin = r'UI window'
        cv.namedWindow(outWin,cv.WINDOW_NORMAL)
        cv.setWindowProperty(outWin,cv.WINDOW_NORMAL, windowFlag)
        cv.imshow(outWin, canvas)
        # Load the stimuluses
        print("Loading Stimulues...")
        keys = list(stimulusSeries.keys())
        keys.remove('nStimulus')
        index = np.zeros([stimulusSeries['nStimulus']], np.int32)
        lightnessMatrix = []
        stayTimeMatrix  = []
        positionMatrix  = []
        sizeMatrix      = []
        for key in keys:
            stimulus = stimulusSeries[key]
            lightnessMatrix.append(stimulus['lightnessSeries'])
            stayTimeMatrix.append(stimulus['timeSeries'])
            positionMatrix.append(stimulus['position'])
            sizeMatrix.append(stimulus['size'])
        nStimulus = len(keys)
        del keys, stimulusSeries
        #### debug codes, suggest that not delete it ###
        print("Loaded Stimulues:")
        for i in range(nStimulus):
            print('\t', i, 
                    '\tposition:',        positionMatrix[i], 
                    '\tsize:',            sizeMatrix[i],
                    '\tlightnessSeries:', lightnessMatrix[i],
                    '\ttimeSeries:',      stayTimeMatrix[i])
        ### output stimulus to screen ###
        while True:
            for i in range(nStimulus):
                idx       = index[i]
                lightness = lightnessMatrix[i][idx]
                stayTime  = int(stayTimeMatrix[i][idx] * 1000)
                position  = positionMatrix[i]
                size      = sizeMatrix[i]
                self.addStimuls(position[0],position[1],lightness,size)
                index[i] = (index[i] + 1) % len(stayTimeMatrix[i])
            # display canvas on screen
            """" Here is time-synchronization problem """
            cv.imshow(outWin, self._canvas)
            if cv.waitKey(1000) & 0xFF == ord('q'):
                print("Stimulating stopped!")
                break
            # clear buffer
#            self._canvas = np.zeros_like(canvas)
        pass

def unitTest():
    gui = GUI(screenType='full',screenHeight=200,screenWidth=200)
    gui.creatStimulusSeries([40, 40], None, 0.5, 0.5)
    gui.creatStimulusSeries([160, 160], None, 4.0, 0.5)
    gui.creatStimulusSeries([360, 360], None, 20.0, 0.5)
#    gui.creatStimulusSeries(60.0,0.5)
    gui.displayGUI()
    return 

if __name__ == "__main__":
    unitTest()
    pass

