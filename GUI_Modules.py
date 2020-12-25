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
        self._refresh      = 60
        self._screenWidth  = None
        self._screenHeight = None
        self._colorSpace   = r'RGB'
        self._canvas       = None
        self._displayType  = screenType
        # Initial assignment for Class properties
        display = tk.Tk()
        display_width=display.winfo_screenwidth()
        display_height=display.winfo_screenheight()
        if screenType== 'full':
            self._screenWidth = display_width
            self._screenHeight = display_height
        elif screenType == 'float':
            self._screenWidth = screenWidth
            self._screenHeight= screenHeight
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
        x = x_position
        y = y_position
        RGB = (lightness, lightness, lightness)
        cv.rectangle(canvas,(x, y), (x+size, y+size),RGB, -1)
        self._canvas = canvas
        del canvas, x, y, RGB
        return

    def creatStimulusSeries(self, stiFreq=10.0, dutyfactor=0.5, alterType=None):
        """
        lFrame means the mounts of the pictures inclued in one stimulus.
        This function will create a sequence of lightness. The lightness sequence should be used in method addStimuls().
        """
        refreshRate = self._refresh
        framePeriod = 1.0 / refreshRate
        nPeriod     = refreshRate / stiFreq
        dutyfactor  = 


        # create stimulus block
        return sequence
        

    def displayGUI(self):
        height = self._screenWidth
        width = self._screenWidth
        canvas = self._canvas.copy()
        # default setting: dispaly UI occuping the screen
        displayType = self._displayType
        windowFlag  = cv.WINDOW_FULLSCREEN
        if displayType == 'float':
            windowFlag = cv.WINDOW_NORMAL
        outWin = r'UI window'
        cv.namedWindow(outWin,cv.WINDOW_NORMAL)
        cv.setWindowProperty(outWin,cv.WINDOW_NORMAL, windowFlag)
        cv.imshow(outWin, canvas)
        k = cv.waitKey(0)
        return
        # key to close the UI
        while k != ord("q"):
            cv.imshow(outWin, canvas)
            k = cv.waitKey(0)
        pass


def unitTest():
    gui = GUI(screenType='full',screenHeight=200,screenWidth=300)
    gui.addStimuls(40, 40, 100)
    gui.displayGUI()
    return 

if __name__ == "__main__":
    unitTest()
    pass

