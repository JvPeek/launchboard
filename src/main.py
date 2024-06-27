#!/usr/bin/env python


import sys
import time
import math
import atexit
import random
import pyautogui
import pygame
from paho.mqtt import client as mqtt_client
from queue import Queue
from threading import Thread


import launchpad_py as launchpad
import configtester as config
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSystemTrayIcon, QApplication, QMenu, QAction
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
    lp.LedCtrlRawRapidHome()
    lp.LedCtrlRawRapid(ledData + rightData + topData)

def blink():
    global lastKey
    lastKey = millis()
    updateLEDs()
def keyPresser(keyQueue):
    while True:
        keyToPress = keyQueue.get()
        if (keyToPress):
            print(keyToPress)
            if (keyToPress[0]):
                pressKey(keyToPress[1])
            else:
                releaseKey(keyToPress[1])

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
    lp.LedCtrlString(str(page+1), 0, 3, 1, 20)
    keyMap = config.getKeyMap(page)



def soundPlayer(soundQueue):
    while True:
        soundToPlay = soundQueue.get()
        if (soundToPlay):
            playSound(soundToPlay)

def playSound(sound):
    try:
        pygame.mixer.Sound("sounds/" + str(sound)).play()
    except:
        print("sound not found")
    blink()

    

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
    app = QApplication([])
    app.setQuitOnLastWindowClosed(True)


    icon = QIcon("icon.png")
    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)
    menu = QMenu()
    


    # Add a Quit option to the menu.
    quit = QAction("Quit")
    quit.triggered.connect(app.quit)
    menu.addAction(quit)

    # Add the menu to the tray
    tray.setContextMenu(menu)
    pygame.mixer.init()

    initLaunchpad()
    lp.Reset()
    lp.LedCtrlString(config.getWelcomeString(), 0, 4, -1, 50)

    soundQueue = Queue()
    keyQueue = Queue()
    pageQueue = Queue()
    mqttQueue = Queue()
    
    soundThread = Thread(target = soundPlayer, args =(soundQueue, )) 
    soundThread.start()

    keyThread = Thread(target = keyPresser, args =(keyQueue, )) 
    keyThread.start()

    lastBut = (-99, -99)
    while True:

        buts = lp.ButtonStateXY()

        updateLEDs()

        if buts != []:
            #print( buts[0], buts[1], buts[2] )
            thisConfig = keyMap[buts[1]][buts[0]]

            if (thisConfig["keyEnabled"]):
                keyQueue.put([buts[2], thisConfig["key"]])
                
            if (thisConfig["pageEnabled"]):
                if (buts[2] == 1):
                    
                    changePage(thisConfig["page"]-1)

            
            if (thisConfig["soundEnabled"]):
                if (buts[2] == 1):
                    soundQueue.put(thisConfig["sound"])
                    
        time.sleep(0.01)
                


def exit_handler():
    global lp
    if (lp == None):
        return
    lp.Reset()
    print("bye ...")


atexit.register(exit_handler)

if __name__ == '__main__':
    
    main()
