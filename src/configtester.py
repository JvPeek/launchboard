import config
from constants import CONFIG_FILE, PAGES
import json
import math

configData = None
currentPage = 1
def getWelcomeString():
    return "MEDDL"
def getDimmerValue():
    return -0
def getMqttCredentials():
    return {"broker": "192.168.2.11", "port": 1883, "user": None, "pass": None}
def getCurrentPage():
    return currentPage
def loadConfig():
    global configData
    with open(CONFIG_FILE, 'r') as file:
        configData = json.load(file)



def getKeyMap(index:int)->list:
    global currentPage
    if (index == None):
        index = 0
    if (configData == None):
        loadConfig()
    currentPage = index+1
    outputData = []
    configPage = configData['tab_' + str(index+1)]

    for i in range(9):
        rowData = []

        for j in range(9):
            colData = []
            key = configPage[i*9+j]['key']
            if (key == "" or key == "None"):
                key = None
            colData = [configPage[i*9+j]['r'],configPage[i*9+j]['g'],key]
            rowData.append(configPage[i*9+j])

        outputData.append(rowData)



        
    return outputData
