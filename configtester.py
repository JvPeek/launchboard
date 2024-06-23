import config
from constants import CONFIG_FILE, PAGES
import json
import math

configData = None
def getWelcomeString():
    return "MEDDL"
def getDimmerValue():
    return -0

def loadConfig():
    global configData
    with open(CONFIG_FILE, 'r') as file:
        configData = json.load(file)



def getKeyMap(index):
    if (index == None):
        index = 0
    if (configData == None):
        loadConfig()

    print("getting keymap")
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
            rowData.append(colData)
        outputData.append(rowData)



        
    return outputData
