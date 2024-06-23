def getKeyMap(index):
    
    if (index == 1):
        keyMap = [
            [[1,0, "PAGE0"], [0,3, "PAGE1"], [1,0, "PAGE2"], [1,0, "PAGE3"], [1,0, "PAGE4"], [1,0, "PAGE5"], [1,0, "PAGE6"], [1,0, "PAGE7"]],
            [[0,3, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, None]],
            [[0,3, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, "PAGE3"]]
        ]
    elif (index == 2):
        keyMap = [
            [[1,0, "PAGE0"], [1,0, "PAGE1"], [0,3, "PAGE2"], [1,0, "PAGE3"], [1,0, "PAGE4"], [1,0, "PAGE5"], [1,0, "PAGE6"], [1,0, "PAGE7"]],
            [[0,0, None], [0,3, "up"], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, "x"]],
            [[0,3, "left"], [0,3, "down"], [0,3, "right"], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, "z"]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, "PAGE3"]]
        ]
    elif (index == 3):
        keyMap = [
            [[1,0, "PAGE0"], [1,0, "PAGE1"], [1,0, "PAGE2"], [0,3, "PAGE3"], [1,0, "PAGE4"], [1,0, "PAGE5"], [1,0, "PAGE6"], [1,0, "PAGE7"]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,3, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,3, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,3, "PAGE3"]]
        ]
    else:
        #STANDARD KEYMAP
        keyMap = [
            [[0,3, "PAGE0"], [1,0, "PAGE1"], [1,0, "PAGE2"], [1,0, "PAGE3"], [1,0, "PAGE4"], [1,0, "PAGE5"], [1,0, "PAGE6"], [1,0, "PAGE7"]],
            [[3,0, "q"], [0,0, "w"], [0,0, "e"], [0,0, "r"], [0,0, "t"], [0,0, "z"], [0,0, "u"], [0,3, "i"], [3,0, "1"]],
            [[0,3, "b"], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,2, None], [0,3, None], [3,3, None]],
            [[2,3, None], [2,3, None], [2,3, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None], [0,3, None], [3,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None], [3,0, None], [0,3, None]],
            [[3,0, None], [0,3, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,3, None], [2,2, None], [0,3, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None], [3,0, None], [3,0, None]],
            [[0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [0,0, None], [3,0, None], [3,0, None], [0,3, "PAGE3"]]
            
        ]
    return keyMap
def getWelcomeString():
    return "MEDDL"
def getDimmerValue():
    return -0
