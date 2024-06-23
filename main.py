#!/usr/bin/env python


import sys
import time
import math
import atexit
import random
import pyautogui

import launchpad_py as launchpad
import configtester as config

# config goes here
flashTimer = 50
dimTimer = 2000

keyMap = config.getKeyMap(0)

lp = None


def millis():
    return round(time.time() * 1000)


# Timer beim Start befüllen
nextUpdate = 0
lastKey = millis()
lastFlash = 0


def updateLEDs():
    global flashTimer, lastKey, nextUpdate
    flashActive = millis() < (lastKey + flashTimer)
    timeToUpdate = millis() > nextUpdate
    # print(str(millis()) + str(flashActive) + str(timeToUpdate))
    if (not timeToUpdate) and (not flashActive):
        return

    if (flashActive):
        nextUpdate = millis() + flashTimer
        flash()
        return
    baseColorMap()
    nextUpdate = millis() + 1000


def flash():
    global lastFlash
    if (lastFlash + 50 > millis()):
        return
    lp.LedAllOn()
    lastFlash = millis()
    print("FLASH")


def baseColorMap():
    global keyMap, lp, dimTimer, lastKey
    dimmer = 0
    ledData = []
    topData = []
    rightData = []
    if (lastKey+dimTimer < millis()):
        dimmer = config.getDimmerValue()
    for rowNum, row in enumerate(keyMap):
        for colNum, col in enumerate(row):
            if (rowNum == 0):
                topData.append(lp.LedGetColor(col[0]+dimmer, col[1]+dimmer))
            else:
                if (colNum < 8):
                    ledData.append(lp.LedGetColor(col[0]+dimmer, col[1]+dimmer))
                else:
                    rightData.append(lp.LedGetColor(col[0]+dimmer, col[1]+dimmer))

    #ledData.append(topData)
    lp.LedCtrlRawRapidHome()
    lp.LedCtrlRawRapid(ledData + rightData + topData)


def pressKey(x, y):
    global keyMap, lastKey
    if (keyMap[x][y][2] == None):
        return
    if (keyMap[x][y][2].startswith('PAGE') ):
        page = int(''.join(filter(str.isdigit, keyMap[x][y][2])))
        
        print("selecting page " + str(page))
        lp.LedCtrlString(str(page+1), 0, 4, 0, 100)

        keyMap = config.getKeyMap(page)
        
    else:
        print("pressing key " + keyMap[x][y][2])
        
        pyautogui.keyDown(keyMap[x][y][2])
        lastKey = millis()


def releaseKey(x, y):
    global keyMap
    if (keyMap[x][y][2] == None):
        return
    if (keyMap[x][y][2].startswith('PAGE') ):
        return
    
    print("releasing key " + keyMap[x][y][2])
    pyautogui.keyUp(keyMap[x][y][2])


def initLaunchpad():
    global lp
    mode = None
    if launchpad.Launchpad().Check(0):
        lp = launchpad.Launchpad()
        if lp.Open(0):
            print("Launchpad Mk1/S/Mini")
            mode = "Mk1"

    if mode is None:
        print("Did not find any Launchpads, meh...")
        return


def main():
    global lp, lastKey

    initLaunchpad()
    lp.Reset()
    lp.LedCtrlString(config.getWelcomeString(), 0, 4, -1, 50)

    lastBut = (-99, -99)
    while True:
        buts = lp.ButtonStateXY()

        updateLEDs()

        if buts != []:
            # print( buts[0], buts[1], buts[2] )

            if (buts[2] == 1):
                pressKey(buts[1], buts[0])
                updateLEDs()
            else:
                releaseKey(buts[1], buts[0])


def exit_handler():
    global lp
    lp.Reset()
    print("bye ...")


atexit.register(exit_handler)

if __name__ == '__main__':
    main()
