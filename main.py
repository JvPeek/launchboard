#!/usr/bin/env python


import sys
import time
import math
import atexit
import random
import pyautogui
import pygame

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
                topData.append(lp.LedGetColor(col["r"]+dimmer, col["g"]+dimmer))
            else:
                if (colNum < 8):
                    ledData.append(lp.LedGetColor(col["r"]+dimmer, col["g"]+dimmer))
                else:
                    rightData.append(lp.LedGetColor(col["r"]+dimmer, col["g"]+dimmer))

    #ledData.append(topData)
    lp.LedCtrlRawRapidHome()
    lp.LedCtrlRawRapid(ledData + rightData + topData)

def blink():
    global lastKey
    lastKey = millis()
    updateLEDs()

def pressKey(key):
    
    if (key == None):
        return
    pyautogui.keyDown(key)
    blink()

def releaseKey(key):
    if (key == None):
        return
    pyautogui.keyUp(key)
    
def changePage(page):
    global keyMap, lp
    lp.LedCtrlString(str(page+1), 0, 4, 0, 100)
    keyMap = config.getKeyMap(page)
def playSound(sound):
    pygame.mixer.Sound("sounds/" + str(sound)).play()
    blink()

    

# def pressKey(x, y):
#     global keyMap, lastKey
#     if (keyMap[x][y][2] == None):
#         return
#     if (keyMap[x][y][2].startswith('PAGE') ):
#         page = int(''.join(filter(str.isdigit, keyMap[x][y][2])))
        
#         print("selecting page " + str(page))
#         lp.LedCtrlString(str(page+1), 0, 4, 0, 100)

#         keyMap = config.getKeyMap(page)
        
#     else:
#         print("pressing key " + keyMap[x][y][2])
        
#         pyautogui.keyDown(keyMap[x][y][2])
#         lastKey = millis()


# def releaseKey(x, y):
#     global keyMap
#     if (keyMap[x][y][2] == None):
#         return
#     if (keyMap[x][y][2].startswith('PAGE') ):
#         return
    
#     print("releasing key " + keyMap[x][y][2])
#     pyautogui.keyUp(keyMap[x][y][2])


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
    pygame.mixer.init()
                    
    initLaunchpad()
    lp.Reset()
    lp.LedCtrlString(config.getWelcomeString(), 0, 4, -1, 50)

    lastBut = (-99, -99)
    while True:
        buts = lp.ButtonStateXY()

        updateLEDs()

        if buts != []:
            #print( buts[0], buts[1], buts[2] )
            thisConfig = keyMap[buts[1]][buts[0]]

            if (thisConfig["keyEnabled"]):
                if (buts[2] == 1):
                    pressKey(thisConfig["key"])
                    
                else:
                    releaseKey(thisConfig["key"])

            if (thisConfig["pageEnabled"]):
                if (buts[2] == 1):
                    print("change page")
                    changePage(thisConfig["page"]-1)

            
            if (thisConfig["soundEnabled"]):
                if (buts[2] == 1):

                    print("play sound")
                    playSound(thisConfig["sound"])

                


def exit_handler():
    global lp
    lp.Reset()
    print("bye ...")


atexit.register(exit_handler)

if __name__ == '__main__':
    main()
