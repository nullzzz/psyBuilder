import copy
import datetime
import os
import re
import shutil

from app.func import Func
from app.info import Info

cIndents = 0
isPreLineSwitch = 0
haveGaborStim = False
haveSnowStim = False
enabledKBKeysSet = set()
isDummyPrint = False
spFormatVarDict = dict()
inputDevNameIdxDict = dict()
outputDevNameIdxDict = dict()
historyPropDict = dict()
cInfoDict = dict()
queueDevIdxValueStr = str()
stimWidgetTypesList = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH]


def throwCompileErrorInfo(inputStr):
    Func.printOut(inputStr, 3)
    raise Exception("compile failed: see info above for details.")


def debugPrint(inputStr: str):
    isDebug = False
    if isDebug:
        print(inputStr)


def pyStr2MatlabStr(inputStr):
    if isinstance(inputStr, str):
        if isSingleQuotedStr(inputStr):
            inputStr = inputStr[1:-1]

        inputStr = re.sub("'", "''", inputStr)
        # replace the \n with \\n so that we could print it with \n to matlab
        inputStr = "\\n".join(inputStr.split("\n"))
        # inputStr = re.sub(r"\\\%","%",inputStr)
    return inputStr


# def dataStrConvert(dataStr, isRef=False, transMATStr=False, transPercent=True) -> str or float or int:
def dataStrConvert(dataStr, isRef=False, transMATStr=False, transPercent=True):
    # convert string to neither a string or a num
    # e.g.,
    # 1） "2"    to 2
    # 2） "2.00" to 2.0
    # 3） "abcd" to "'abcd'"
    # 4） "[12,12,12]" to "[12,12,12]"
    # 5） "12,12,12"  to "[12,12,12]"
    # 6） is a referred value will do nothing
    if isinstance(dataStr, str):

        if dataStr:

            if isPercentStr(dataStr):
                if transPercent:
                    outData = parsePercentStr(dataStr)
                else:
                    outData = addSingleQuotes(dataStr)

            elif isRgbWithBracketsStr(dataStr):
                outData = dataStr

            elif isRgbaWithBracketsStr(dataStr):
                outData = dataStr

            elif isRgbStr(dataStr):
                outData = addSquBrackets(dataStr)

            elif isRgbaStr(dataStr):
                outData = addSquBrackets(dataStr)

            elif isIntStr(dataStr):
                outData = int(dataStr)

            elif isFloatStr(dataStr):
                outData = float(dataStr)

            elif isRefStr(dataStr):
                outData = dataStr  # maybe a bug

            else:
                if isRef:
                    outData = dataStr  # maybe a bug
                else:
                    if transMATStr:
                        outData = addSingleQuotes(pyStr2MatlabStr(dataStr))  # maybe a bug
                    else:
                        outData = addSingleQuotes(dataStr)  # maybe a bug
        else:
            outData = "[]"

    else:  # in case there is something wrong
        # raise Exception(f"the input dataStr:{dataStr} is not a string!")
        outData = dataStr

    return outData


def addedTransparentToRGBStr(RGBStr, transparentStr):
    transparentValue = parsePercentStr(transparentStr)

    if isinstance(transparentValue, (int, float)):
        if transparentValue == -1:  # for 100%
            return RGBStr
        else:
            transparentValue = transparentValue * -255
    else:
        if transparentValue != '[]':
            transparentValue = f"{transparentValue}*-255"

    if transparentValue != '[]':
        if isRgbStr(RGBStr):
            RGBStr = f"[{RGBStr},{transparentValue}]"
        elif isRgbWithBracketsStr(RGBStr):
            RGBStr = re.sub("]", f",{transparentValue}]", RGBStr)
        elif isRefStr(RGBStr):
            RGBStr = f"[{RGBStr},{transparentStr}]"
        else:
            raise Exception(
                f"the input parameter 'RGBStr' is not a RGB format String\n should be of R,G,B, [R,G,B], or referred values!")

    return RGBStr


# add curly brackets
def addCurlyBrackets(inputStr):
    # outputStr = "{"+str(inputStr)+"}"
    outputStr = f"{{{inputStr}}}"
    return outputStr


# add single quotes
def addSingleQuotes(inputStr: str) -> str:
    outputStr = f"'{inputStr}'"
    return outputStr


# add square brackets
def addSquBrackets(inputStr: str) -> str:
    outputStr = f"[{inputStr}]"
    return outputStr


def removeSingleQuotes(inputStr: str) -> str:
    if isinstance(inputStr, str):
        if re.fullmatch("'.+'", inputStr):  # any character except a new line
            inputStr = inputStr[1:-1]
    return inputStr


def removeSquBrackets(inputStr: str) -> str:
    if isinstance(inputStr, str):
        if re.fullmatch(r"\[.+\]", inputStr):  # any character except a new line
            inputStr = inputStr[1:-1]
    return inputStr


def isSubWidgetOfIfOrSwitch(widgetOrId) -> bool:
    isSubWidget = False
    if isinstance(widgetOrId, str):
        cWidgetId = widgetOrId
    else:
        cWidgetId = widgetOrId.widget_id

    parentWid = Func.getParentWid(cWidgetId)

    if parentWid:
        if getWidgetType(parentWid) in [Info.IF, Info.SWITCH]:
            isSubWidget = True

    return isSubWidget


def updateSpFormatVarDict(propertyValue, formatTypeStr, cSpecialFormatVarDict):
    if isRefStr(propertyValue):
        propertyValue = propertyValue[1:-1]  # remove the square brackets
        allRefedCycleAttrs = getAllNestedVars(propertyValue, [])

        for cAttrName in allRefedCycleAttrs:

            if cAttrName in cSpecialFormatVarDict:
                if cSpecialFormatVarDict[cAttrName] != formatTypeStr:
                    throwCompileErrorInfo(
                        f"attribute: {cAttrName} are not allowed to be both {formatTypeStr} or {cSpecialFormatVarDict[cAttrName]}")
            else:
                cSpecialFormatVarDict.update({cAttrName: formatTypeStr})


def isContainChStr(inputStr):
    # :param check_str: {str}
    # :return: {bool} True and False for have and have not chinese characters respectively
    for ch in inputStr:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def isSoundRelatedWidget(cWidget) -> bool:
    haveSound = False
    cWidgetType = getWidgetType(cWidget)

    if Info.SOUND == cWidgetType:
        haveSound = True
    elif Info.COMBO == cWidgetType:
        itemIds = getSliderItemIds(cWidget)

        if isContainItemType(itemIds, Info.ITEM_SOUND):
            haveSound = True

    return haveSound


def isSingleQuotedStr(inputStr):
    if inputStr.startswith("'") and inputStr.endswith("'"):
        return True
    return False


def isRgbStr(inputStr):
    isRgbFormat = re.fullmatch(r"^\d+,\d+,\d+$", inputStr)
    return isRgbFormat


def isRgbaStr(inputStr):
    isRgbaFormat = re.fullmatch(r"^\d+,\d+,\d+,\d+$", inputStr)
    return isRgbaFormat


def isRectStr(inputStr):
    if len(inputStr) == 0:
        return None
    isRectFormat = re.fullmatch(r"^\d+,\d+,\d+,\d+$", inputStr)
    return isRectFormat


def isRgbaWithBracketsStr(inputStr):
    if len(inputStr) == 0:
        return None
    isRgbaFormat = re.fullmatch(r"^\[\d+,\d+,\d+,\d+\]$", inputStr)
    return isRgbaFormat


def isRectWithBracketsStr(inputStr):
    if len(inputStr) == 0:
        return None
    isRectFormat = re.fullmatch(r"^\[\d+,\d+,\d+,\d+\]$", inputStr)
    return isRectFormat


def isRgbWithBracketsStr(inputStr):
    if len(inputStr) == 0:
        return None
    isRgbFormat = re.fullmatch(r'^\[\d+,\d+,\d+\]$', inputStr)
    return isRgbFormat


def isNumStr(inputStr):
    if isinstance(inputStr, str):
        if len(inputStr) == 0:
            return False

        return re.fullmatch(r"([\d]*\.[\d$]+)|\d*", inputStr)

    return False


def isIntStr(inputStr):
    if isinstance(inputStr, str):
        if len(inputStr) == 0:
            return False

        return re.fullmatch(r"\d*", inputStr)

    return False


def isFloatStr(inputStr):
    if isinstance(inputStr, str):
        if len(inputStr) == 0:
            return False
        return re.fullmatch(r"([\d]*\.[\d$]+)", inputStr)

    return False


def isPercentStr(inputStr):
    if isinstance(inputStr, str):
        if len(inputStr) == 0:
            return False

        return re.fullmatch(r"([\d]*\.[\d]+%$)|(\d*%$)", inputStr)

    return False


def isRefStr(inputStr):
    isRef = False

    if isinstance(inputStr, str):
        # if isRgbWithBracketsStr(inputStr):
        #     return False
        if len(inputStr) == 0:
            return False

        # special chars lose their special meaning inside sets [], so . inside [] just means the char '.'
        if re.fullmatch(r'\[[A-Za-z]+[a-zA-Z._0-9]*\]', inputStr):
            isRef = True

    return isRef


def isContainCycleTL(widgetId) -> bool:
    cTimelineWidgetIds = Func.getWidgetIDInTimeline(widgetId)

    for cWidgetId in cTimelineWidgetIds:
        if Func.isWidgetType(cWidgetId, Info.LOOP):
            return True
    return False


def isVideoRelatedWidget(cWidget) -> bool:
    if Func.isWidgetType(cWidget.widget_id, Info.VIDEO):
        return True
    elif Func.isWidgetType(cWidget.widget_id, Info.COMBO):
        return isContainItemType(getSliderItemIds(cWidget), Info.ITEM_VIDEO)
    else:
        return False


def isContainItemType(itemIds: list, itemType: str) -> bool:
    haveItemType = False

    for cItemId in itemIds:
        if getItemType(cItemId) == itemType:
            haveItemType = True
            break

    return haveItemType


def isFirstStimWidgetInTL(widget_id: str) -> bool:
    global stimWidgetTypesList

    if isSubWidgetOfIfOrSwitch(widget_id):
        return isFirstStimWidgetInTL(Func.getParentWid(widget_id))

    isFirstEvent = True

    preWidgetId = getPreWID(widget_id)

    while preWidgetId:
        if getWidgetIdType(preWidgetId) in stimWidgetTypesList:
            isFirstEvent = False
            break
        else:
            preWidgetId = getPreWID(widget_id)

    return isFirstEvent


def isLastStimWidgetInTL(widget_id: str) -> bool:
    global stimWidgetTypesList
    isLastEvent = True

    nextWidgetId = getNextWID(widget_id)
    while nextWidgetId:
        if getWidgetIdType(nextWidgetId) in stimWidgetTypesList:
            isLastEvent = False
            break
        else:
            nextWidgetId = getNextWID(nextWidgetId)

    return isLastEvent


def keyNameToCodes(keyNameList: list) -> list:
    """
    :type keyNameList: list of key names
    """
    keyCodesDict = {'any': '1:255', 'left_mouse': 1, 'right_mouse': 2, 'middle_mouse': 4, 'backspace': 8,
                    'tab': 9, 'clear': 12, 'return': 13, 'shift': 16, 'control': 17,
                    'alt': 18, 'pause': 19, 'capslock': 20, 'escape': 27, 'space': 32,
                    'pageup': 33, 'pagedown': 34, 'end': 35, 'home': 36, 'leftarrow': 37,
                    'uparrow': 38, 'rightarrow': 39, 'downarrow': 40, 'printscreen': 44,
                    'insert': 45, 'delete': 46, 'help': 47, '0)': 48, '1!': 49, '2@': 50,
                    '3#': 51, '4$': 52, '5%': 53, '6^': 54, '7&': 55, '8*': 56, '9(': 57, 'a': 65,
                    'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70, 'g': 71, 'h': 72, 'i': 73, 'j': 74,
                    'k': 75, 'l': 76, 'm': 77, 'n': 78, 'o': 79, 'p': 80, 'q': 81, 'r': 82, 's': 83,
                    't': 84, 'u': 85, 'v': 86, 'w': 87, 'x': 88, 'y': 89, 'z': 90, 'leftgui': 91,
                    'rightgui': 92, 'application': 93, '0': 96, '1': 97, '2': 98, '3': 99, '4': 100,
                    '5': 101, '6': 102, '7': 103, '8': 104, '9': 105, '*': 106, '+': 107, 'seperator': 108,
                    '-': 109, '.': 110, '/': 111, 'f1': 112, 'f2': 113, 'f3': 114, 'f4': 115, 'f5': 116, 'f6': 117,
                    'f7': 118, 'f8': 119, 'f9': 120, 'f10': 121, 'f11': 122, 'f12': 123, 'f13': 124, 'f14': 125,
                    'f15': 126,
                    'f16': 127, 'f17': 128, 'f18': 129, 'f19': 130, 'f20': 131, 'f21': 132, 'f22': 133, 'f23': 134,
                    'f24': 135, 'numlock': 144, 'scrolllock': 145, 'leftshift': 160, 'rightshift': 161,
                    'leftcontrol': 162, 'rightcontrol': 163, 'leftalt': 164, 'rightalt': 165, ';': 186,
                    '=+': 187, ',<': 188, '-_': 189, '.>': 190, '/?': 191, '`~': 192, '[{': 219, '\\\\': 220,
                    ']}': 221, "'": 222, 'attn': 246, 'crsel': 247, 'exsel': 248, 'play': 251, 'zoom': 252, 'pa1': 254}
    keyCodes = []

    for keyName in keyNameList:
        cKeyCode = keyCodesDict[keyName.lower()]
        if cKeyCode:
            keyCodes.append(cKeyCode)

    return keyCodes


def replaceDot(screenNameStr, newSplitStr="_") -> str:
    return newSplitStr.join(screenNameStr.split('.'))


def genAppropriatePathSplitter(filename:str, isForWin:bool = False) -> str:

    if isForWin:
        filename = re.sub(r'[\\/]',r'\\',filename)
    else:
        filename = re.sub(r'[\\/]', r'/', filename)

    return filename


def makeInputDevIndexValueStr(devType: str, indexStr: str, isOrderNum=True) -> [str, int]:
    if Info.DEV_KEYBOARD == devType:
        devIndexesVarName = "kbIndices"
        cDevType = 1
    elif Info.DEV_MOUSE == devType:
        devIndexesVarName = "miceIndices"
        cDevType = 2

    elif Info.DEV_GAMEPAD == devType:
        devIndexesVarName = "gamepadIndices"
        cDevType = 3

    elif Info.DEV_RESPONSE_BOX == devType:
        devIndexesVarName = "rbIndices"
        cDevType = 4
    elif Info.DEV_EYE_ACTION == devType:
        devIndexesVarName = "eyetrackerIndices"
        cDevType = 82
    else:
        cDevType = -1
        devIndexesVarName = "un_supportedInputDevs"

    if isOrderNum:
        inputDevIndexValue = f"{devIndexesVarName}({indexStr})"
    else:
        inputDevIndexValue = indexStr

    return inputDevIndexValue, cDevType


def shouldNotBeCitationCheck(keyStr, value):
    if isRefStr(value):
        throwCompileErrorInfo(f"'{keyStr}': the value should NOT be a citation!")


def shouldNotBeEmptyCheck(keyStr, value):
    if value == '':
        throwCompileErrorInfo(f"'{keyStr}'should NOT be empty!")


def copyYanglabFiles(beCopyFilenames: list):
    for cFile in beCopyFilenames:
        copyYanglabFile(cFile)
    return 0


def copyYanglabFile(filename: str):
    destinationDir = os.path.dirname(os.path.abspath(Info.FILE_NAME))

    # if isinstance(filename, list):
    #     for cFile in filename:
    #         copyYanglabFile(cFile)
    #     return 0

    destinationFile = os.path.join(destinationDir, filename)

    cPyFullFile = os.path.abspath(__file__)

    for iLevel in range(3):
        cPyFullFile, _ = os.path.split(cPyFullFile)

    sourceFile = os.path.join(cPyFullFile, 'yanglabMFuns', filename)

    shutil.copyfile(sourceFile, destinationFile)

    return 0


def outPutTriggerCheck(cWidget) -> dict:
    """
    : force the pulse dur to be 10 ms if the ppl device will be used to send responses triggers
    """
    cOutPutDevices = cWidget.getOutputDevice()
    cInputDevices = cWidget.getInputDevice()

    respTriggerDevNames = set()
    for cInputDevInfo in cInputDevices.values():
        cRespTriggerDevName = cInputDevInfo['Output Device']

        shouldNotBeCitationCheck('Resp Trigger Device', cRespTriggerDevName)

        respTriggerDevNames.update([cRespTriggerDevName])

    shortPulseDurParallelsDict = dict()

    for cOpDevInfo in cOutPutDevices.values():
        if cOpDevInfo['Device Type'] == Info.DEV_PARALLEL_PORT:
            if cOpDevInfo['Device Name'] in respTriggerDevNames:
                shortPulseDurParallelsDict.update({cOpDevInfo['Device Id']: 10})
                Func.printOut('Currently we will force the pulse duration to be 10 ms', False)

    return shortPulseDurParallelsDict


def updateEnableKbKeysList(allowKeyStr):
    global enabledKBKeysSet

    if len(allowKeyStr) > 0:
        if allowKeyStr.startswith('[') and allowKeyStr.endswith(']'):
            enabledKBKeysSet.add(allowKeyStr[1:-1])
        else:
            enabledKBKeysSet.add(allowKeyStr)


def parseRectStr(inputStr: str, isRef=False) -> str:
    if isinstance(inputStr, str):
        if not isRef:
            if isRectStr(inputStr):
                inputStr = addSquBrackets(inputStr)
            elif isRectWithBracketsStr(inputStr):
                pass
            elif len(inputStr) == 0:
                inputStr = addSquBrackets(inputStr)
            else:
                throwCompileErrorInfo(
                    f"the value {inputStr} is not a rect format in PTB ('x0,y0,x1,y1' or '[x0,y0,x1,y1]')!")

    return inputStr


def parseBooleanStr(inputStr, isRef=False):
    if isinstance(inputStr, str):
        if not isRef:
            if inputStr.lower() in ["'yes'", "'true'", 'yes', 'true', '0', '1']:
                inputStr = "1"
            elif inputStr.lower() in ["'no'", "'false'", 'no', 'false', '0', '1']:
                inputStr = "0"
            else:
                throwCompileErrorInfo(
                    f"the value of '{inputStr}' should be of ['False','True','Yes','No','1', or '0'] ")
    elif isinstance(inputStr, bool):
        if inputStr:
            inputStr = "1"
        else:
            inputStr = "0"

    return inputStr


def parseDontClearAfterStr(inputStr):
    if isinstance(inputStr, str):
        inputStr = removeSingleQuotes(inputStr)

        if inputStr == "clear_0":
            inputStr = '0'
        elif inputStr == "notClear_1":
            inputStr = '1'
        elif inputStr == "doNothing_2":
            inputStr = '2'
    return inputStr


def parseDurationStr(inputStr):
    if isinstance(inputStr, str):
        inputStr = removeSingleQuotes(inputStr)

        if inputStr == "(Infinite)":
            inputStr = "999000"  # an extremely impossible value maximum of 1000 second
        elif re.fullmatch(r"\d+~\d+", inputStr):
            cDurRange = inputStr.split('~')
            inputStr = f"{cDurRange[0]},{cDurRange[1]}"

    return inputStr


def parseEndActionStr(endActionStr):
    if endActionStr == 'Terminate':
        endActionStr = '1'
    elif endActionStr == 'Terminate Till Release':
        endActionStr = '2'
    else:
        endActionStr = '0'

    return endActionStr


def trans2relativePath(fullFileName:str):
    if fullFileName:
        beSavedDir = os.path.dirname(Info.FILE_NAME)
        try:
            commonPath = os.path.commonpath([fullFileName,beSavedDir])
            # re.sub(r'[\\/]', r'\\', filename)
            if len(commonPath) > 0 and re.sub(r'[\\/]', r'\\', commonPath) != re.sub(r'[\\/]', r'\\', beSavedDir):
                raise Exception

            fullFileName = fullFileName[len(commonPath):]
        except:
            if not fullFileName.startswith("["):
                throwCompileErrorInfo(f"All experimental materials should be put under the folder: {beSavedDir}")

    return fullFileName


def formatPathSplitter(inputStr):

    # toBeSavedDir = os.path.dirname(Info.FILE_NAME)
    #
    # if not isRef:
    #
    #     if len(toBeSavedDir) <= len(inputStr):
    #         if inputStr[:len(toBeSavedDir)] == toBeSavedDir:
    #             inputStr = inputStr[len(toBeSavedDir):]

    inputStr = genAppropriatePathSplitter(inputStr, Info.PLATFORM == 'windows')

    return inputStr


def parsePhysicSize(inputStr: str) -> list:
    return re.split(r'[,xX\s]\s*', inputStr)


def parseStartEndTimeStr(inputStr, isRef=False) -> str:
    if not isRef:
        inputStr = inputStr

    return inputStr


def parseFontStyleStr(inputStr):
    if isinstance(inputStr, str):
        inputStr = removeSingleQuotes(inputStr)
        if inputStr == "normal_0":
            inputStr = '0'
        elif inputStr == "bold_1":
            inputStr = '1'
        elif inputStr == "italic_2":
            inputStr = '2'
        elif inputStr == "underline_4":
            inputStr = '4'
        elif inputStr == "outline_8":
            inputStr = '8'
        elif inputStr == "overline_16":
            inputStr = '16'
        elif inputStr == "condense_32":
            inputStr = '32'
        elif inputStr == "extend_64":
            inputStr = '64'
    return inputStr


def parseKbCorRespStr(kbCorRespStr, isRefValue, devType) -> str:
    if isRefValue:
        kbCorRespCodesStr = kbCorRespStr
    else:
        if len(kbCorRespStr) > 0:
            if devType == Info.DEV_KEYBOARD:
                splittedStrs = re.split(r'({\w*})', kbCorRespStr)
                kbNameList = []
                for item in splittedStrs:
                    if item.startswith('{') and item.endswith('}'):
                        item = item[1:-1]
                        kbNameList.append(item)
                    else:
                        for char in item:
                            kbNameList.append(char)

                kbCorRespCodes = keyNameToCodes(kbNameList)
            else:
                kbCorRespCodes = kbCorRespStr

            kbCorRespCodesStr = "".join(f"{value}, " for value in kbCorRespCodes[0:-1])
            kbCorRespCodesStr = "[" + kbCorRespCodesStr + f"{kbCorRespCodes[-1]}" + "]"

        else:
            kbCorRespCodesStr = "[0]"

    return kbCorRespCodesStr


def parsePercentStr(inputStr):
    if isinstance(inputStr, str):
        if isPercentStr(inputStr):
            if float(inputStr[:-1]) == 0:
                outputValue = float(inputStr[:-1])
            else:
                outputValue = float(inputStr[:-1]) / -100
        elif isNumStr(inputStr):
            outputValue = float(inputStr)
        else:
            outputValue = inputStr
    else:
        outputValue = inputStr

    return outputValue


def parseRTWindowStr(inputStr):
    if isinstance(inputStr, str):
        if inputStr == "(Same as duration)":
            inputStr = '-1'
        elif inputStr == "(End of timeline)":
            inputStr = '-2'
        # else:
        #
    return inputStr


def parseAspectRationStr(inputStr, isRef=False):
    # ""、Both、Horizontal、Vertical、[attr]
    if not isRef:
        if isinstance(inputStr, str):
            if inputStr == "Default":
                inputStr = "0"
            elif inputStr == "Ignore":
                inputStr = "1"
            elif inputStr == "keep":
                inputStr = "2"
            elif inputStr == "KeepByExpanding":
                inputStr = "3"
            else:
                inputStr = "0"

    return inputStr


def parseStretchModeStr(inputStr, isRef=False):
    # ""、Both、Horizontal、Vertical、[attr]
    if not isRef:
        if isinstance(inputStr, str):
            if inputStr == "Both":
                inputStr = "3"
            elif inputStr == "Horizontal":
                inputStr = "1"
            elif inputStr == "Vertical":
                inputStr = "2"
            else:
                inputStr = "0"

    return inputStr


def parseTextContentStrNew(inputStr) -> str:
    """
    new fun to support citation within current_text
    :param inputStr:
    :return:
    """
    # inputStr = pyStr2MatlabStr(inputStr)

    # if inputStr.startswith("'") and inputStr.endswith("'"):
    #     pass
    # else:
    #     pass

    if isContainChStr(inputStr):
        inputStr = "double(" + inputStr + ")"

    return inputStr


def parseTextContentStr(inputStr, isRef=False) -> str:
    if not isRef:
        if isContainChStr(inputStr):
            # inputStr = "double(" + inputStr + ")"
            inputStr = "[" + "".join(f"{ord(value)} " for value in inputStr) + "]"
        else:
            # cinputStr = '\\n'.join(inputStr.split('\n')) have down in pyStr2MatlabStr
            inputStr = addSingleQuotes(pyStr2MatlabStr(inputStr))

    return inputStr


def printOutList(f,inputList:list):

    for cRowStr in inputList:
        cRowStr = "{{".join(cRowStr.split('{'))
        cRowStr = "}}".join(cRowStr.split('}'))
        printAutoInd(f, cRowStr)
    
    return


# noinspection PyStringFormat
def printAutoInd(f, inputStr, *argins):
    global cIndents, isPreLineSwitch, isDummyPrint

    if isDummyPrint:
        # DO nothing
        return

    if isinstance(f, list):
        f.append(inputStr.format(*argins))
        return

    incrAfterStr = ('if', 'try', 'switch', 'for', 'while')
    decreAndIncrStr = ('else', 'elseif', 'otherwise', 'catch')

    keyWordStr = inputStr.split(' ')[0]

    if keyWordStr in incrAfterStr:
        tabStrs = '\t' * cIndents

        print(f"{tabStrs}{inputStr}".format(*argins), file=f)
        # print(f"\n{tabStrs}{inputStr}".format(*argins), file=f)

        cIndents += 1

    elif keyWordStr in decreAndIncrStr:
        cIndents -= 1
        tabStrs = '\t' * cIndents

        print(f"{tabStrs}{inputStr}".format(*argins), file=f)

        cIndents += 1

    elif 'end' == keyWordStr:
        cIndents -= 1
        tabStrs = '\t' * cIndents

        print(f"{tabStrs}{inputStr}".format(*argins), file=f)
        # print(f"{tabStrs}{inputStr}\n".format(*argins), file=f)

    elif 'end%switch' == keyWordStr:
        cIndents -= 2
        tabStrs = '\t' * cIndents

        print(f"{tabStrs}{inputStr}".format(*argins), file=f)
        # print(f"{tabStrs}{inputStr}\n".format(*argins), file=f)

    elif 'case' == keyWordStr:

        if 0 == isPreLineSwitch:
            cIndents -= 1

        tabStrs = '\t' * cIndents

        print(f"{tabStrs}{inputStr}".format(*argins), file=f)

        cIndents += 1

    else:

        tabStrs = '\t' * cIndents

        # print(f"{tabStrs}{inputStr}".format(*argins))
        print(f"{tabStrs}{inputStr}".format(*argins), file=f)

    if 'switch' == keyWordStr:
        isPreLineSwitch = 1
    else:
        isPreLineSwitch = 0

    if cIndents < 0:
        cIndents = 0

    return

def haveTrackerType(trackerType: str = 'EyeLink') -> bool:
    eyetracker_devices = Info.TRACKER_DEVICE_INFO

    haveTrackerType = False

    for cEyeTracker, cEyeTrackerProperty in eyetracker_devices.items():
        if cEyeTrackerProperty.get('Select Tracker Type') == trackerType:
            haveTrackerType = True

    return haveTrackerType

def getAllEventWidgetsList(includedType: int = 1) -> list:
    """
    :param includedType: 1 none LOOP, 2 LOOP, 3 all eventTypes
    :return: a list for event widget
    """
    allEventWidgets = []

    if includedType == 3:
        allEventWidgetTypes = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH,
                               Info.LOOP]
    elif includedType == 2:
        allEventWidgetTypes = [Info.LOOP]
    else:
        allEventWidgetTypes = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH]

    for cWidgetId, cWidget in Info.WID_WIDGET.items():
        if not isSubWidgetOfIfOrSwitch(cWidgetId) and getWidgetType(cWidgetId) in allEventWidgetTypes:
            allEventWidgets.append(cWidget)
    return allEventWidgets


def getAllEventWidgetNamesList(includedType: int = 1) -> list:
    """
    :param includedType: 1 not include LOOP, 2 include LOOP
    :return: a list for event widget names
    """
    cAllEventWidgetNameList = []

    if includedType == 3:
        allEventWidgetTypes = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH,
                               Info.LOOP]
    elif includedType == 2:
        allEventWidgetTypes = [Info.LOOP]
    else:
        allEventWidgetTypes = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH]

    for cWidgetId, cWidget in Info.WID_NODE.items():
        # print(f"line 928: {cWidgetId}")
        if not isSubWidgetOfIfOrSwitch(cWidgetId) and getWidgetType(cWidgetId) in allEventWidgetTypes:
            cAllEventWidgetNameList.append(getWidgetName(cWidgetId))

    return cAllEventWidgetNameList


def getHaveOutputDevs(cWidget) -> bool:
    haveOPDev = False
    cWidgetType = getWidgetType(cWidget)

    if cWidgetType in stimWidgetTypesList:
        if cWidgetType == Info.SWITCH:
            for cCaseDict in cWidget.getCases():
                # {'Case Value': '',
                #  'Id Pool': {'Image': 'Image.0', 'Video': '', 'Text': '', 'Sound': '', 'Slider': ''},
                #  'Sub Wid': 'Image.0', 'Stim Type': 'Image', 'Event Name': 'U_Image_6574'}
                if cCaseDict['Sub Wid']:
                    if Info.WID_WIDGET.get(cCaseDict['Sub Wid']).getOutputDevice():
                        haveOPDev = True
                        break

        elif cWidgetType == Info.IF:
            cTrueWidget = cWidget.getTrueWidget()
            cFalseWidget = cWidget.getFalseWidget()

            nTrueOutputDev = 0
            nFalseOutputDev = 0

            if cTrueWidget is not None:
                nTrueOutputDev = len(cTrueWidget.getOutputDevice())
            if cFalseWidget is not None:
                nFalseOutputDev = len(cFalseWidget.getOutputDevice())

            haveOPDev = (nTrueOutputDev + nFalseOutputDev) > 0
        else:
            haveOPDev = len(cWidget.getOutputDevice()) > 0

    return haveOPDev


def getWidLevel(cWid: str) -> int:
    if isSubWidgetOfIfOrSwitch(cWid):
        cWid = Func.getParentWid(cWid)

    return Func.getWidLevel(cWid)


def getWidgetName(widgetOrId, isNameInTL=True) -> str:
    """
    :param widgetOrId: widget or widget_id
    :param isNameInTL: Is it looking for parent name if the current widget is a sub widget of IF or SWITCH?
    :return:
    """
    if isinstance(widgetOrId, str):
        cWid = widgetOrId
    else:
        cWid = widgetOrId.widget_id

    if isNameInTL and isSubWidgetOfIfOrSwitch(cWid):
        cWid = Func.getParentWid(cWid)

    return Func.getWidgetName(cWid)


def getWidgetPos(widgetOrId) -> None or int:
    if isinstance(widgetOrId, str):
        cWidgetId = widgetOrId
    else:
        cWidgetId = widgetOrId.widget_id

    if isSubWidgetOfIfOrSwitch(cWidgetId):
        cWidgetId = Func.getParentWid(cWidgetId)

    return Func.getWidgetPosition(cWidgetId)


# noinspection PyBroadException
def getWidgetEventPos(widget_id: str):
    # def getWidgetEventPos(widget_id: str) -> int or None:
    allEventWidgetTypes = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH]
    # 如果是widget是timeline，不存在位置信息
    if widget_id.startswith(Info.TIMELINE):
        return None
    #
    try:
        node = Info.WID_NODE[widget_id]
        parent_node = node.parent()

        # for subWidgets under IF or SWITCH, try to extract pos based on IF or SWITCH widget
        if isSubWidgetOfIfOrSwitch(widget_id):
            widget_id = parent_node.widget_id
            parent_node = parent_node.parent()

        allIdList = []
        for iWidget in range(parent_node.childCount()):
            if getWidgetType(parent_node.child(iWidget)) in allEventWidgetTypes:
                allIdList.append(parent_node.child(iWidget).widget_id)

        try:
            return allIdList.index(widget_id)
        except:
            return None
    except:
        print(f"error: widget not founded.")
        return None


def getNextStimWID(WID: str) -> None or str:
    nextStimWID = getNextWID(WID)

    while nextStimWID and getNextWID(WID) not in stimWidgetTypesList:
        nextStimWID = getNextWID(WID)

    return nextStimWID


def getNextWID(WID: str) -> None or str:
    if isSubWidgetOfIfOrSwitch(WID):
        return Func.getNextWidgetId(Func.getParentWid(WID))
    else:
        return Func.getNextWidgetId(WID)


def getPreStimWID(WID: str) -> None or str:
    preWID = getPreWID(WID)

    while preWID and getWidgetType(preWID) not in stimWidgetTypesList:
        preWID = getPreWID(preWID)

    return preWID


def getPreWID(WID: str) -> None or str:
    if isSubWidgetOfIfOrSwitch(WID):
        return Func.getPreviousWidgetId(Func.getParentWid(WID))
    else:
        return Func.getPreviousWidgetId(WID)


def getAllNestedVars(inputStr, opVars=None) -> set:
    if opVars is None:
        opVars = []

    if isRefStr(inputStr):
        inputStr = inputStr[1:-1]

    if len(inputStr.split('.')) == 3:
        opVars.append(inputStr)
        cCycleName, ign, attName = inputStr.split('.')

        cWidget = Info.WID_WIDGET[Info.NAME_WID[cCycleName][0]]

        for iRow in range(cWidget.rowCount()):
            cRowDict = cWidget.getAttributes(iRow)
            getAllNestedVars(cRowDict[attName], opVars)

    return set(opVars)


def getCycleRealRows(widgetId: str) -> int:
    cCycle = Info.WID_WIDGET[widgetId]
    repetitionsList = cCycle.getAttributeValues(0)

    sumValue = 0
    for cWeightStr in repetitionsList:
        sumValue = sumValue + dataStrConvert(cWeightStr)

    return sumValue


def getCycleAttVarNamesList(cWidget) -> list:
    # allAttVarNameList = []

    cRowDict = cWidget.getAttributes(0)
    #
    allAttVarNameList = [f"{Func.getWidgetName(cWidget.widget_id)}_{cVar}" for cVar in cRowDict.keys()]

    return allAttVarNameList


def getAllCycleAttVarNameList() -> list:
    allAttrVarNameList = []
    # 2 for cycle widget only
    allEventWidgets = getAllEventWidgetsList(2)

    for cWidget in allEventWidgets:
        cCycleAttVarNameList = getCycleAttVarNamesList(cWidget)

        allAttrVarNameList.extend(cCycleAttVarNameList)

    return allAttrVarNameList


# def getDevPropertyValue(devList: dict, devName: str, searchedKey: str) -> str or float or int or None:
def getDevPropertyValue(devList: dict, devName: str, searchedKey: str):
    keyValue = None
    for cDevId, cDevPro in devList.items():
        if devName == cDevPro['Device Name']:
            keyValue = cDevPro[searchedKey]
            break

    return keyValue


def getMaxLoopLevel() -> int:
    maxLoopLevel = -1

    for cWidgetId in Info.WID_NODE.keys():
        maxLoopLevel = max(maxLoopLevel, getWidLoopLevel(cWidgetId))
    return maxLoopLevel



def getValueInContainRefExp(cWidget, inputStr, attributesSetDict, isOutStr=False, transformStrDict=None):
    if transformStrDict is None:
        transformStrDict = {'=': '==','≠': '~=', '≥': '>=', '≤': '<='}

    refWithBracketPat = r'(\(\[[A-Za-z]+[a-zA-Z._0-9]*?\]\))'
    refPat = r'(\[[A-Za-z]+[a-zA-Z._0-9]*?\])'
    meanPat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@mean'
    medianPat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@median'
    modePat = r'\[([A-Za-z]+[a-zA-Z._0-9]*?)\]@mode'

    leftPat = r'--impossibleValeForLeftBracket--'
    rightPat = r'--impossibleValeForLeftBracket--'

    inputStr = inputStr.replace('(', leftPat)
    inputStr = inputStr.replace(')', rightPat)



    refedObNameList = list()
    isContainRef = 0

    for key, value in transformStrDict.items():
        inputStr = inputStr.replace(key, value)

    isMatlabStr = inputStr.startswith("'") and inputStr.endswith("'")

    if isOutStr and isMatlabStr is False:
        inputStr = addSingleQuotes(inputStr)

    rawInputStr = inputStr
    # stage 1: parse @mean @median or @mode
    if isMatlabStr or isOutStr:

        inputStr = re.sub(meanPat, r"',num2str(mean([\1])),'", inputStr)
        inputStr = re.sub(medianPat, r"',num2str(median([\1])),'", inputStr)
        inputStr = re.sub(modePat, r"',num2str(mode([\1])),'", inputStr)

        # in case the citation located in the begin or the end of inputStr
        # if rawInputStr != inputStr:
        #     if inputStr.startswith("'',num2str(m"):
        #         inputStr = "'" + inputStr[3:]
        #     if inputStr.endswith(")),''"):
        #         inputStr = inputStr[0:-3] + "'"
    else:
        inputStr = re.sub(meanPat, r'mean([\1])', inputStr)
        inputStr = re.sub(medianPat, r'median([\1])', inputStr)
        inputStr = re.sub(modePat, r'mode([\1])', inputStr)

    # stage 2: parse refs in @ mean, mode, or median
    allRefs = re.findall(refWithBracketPat, inputStr)
    if len(allRefs) > 0:
        for cRefs in allRefs:
            cRefsWithoutBracket = cRefs[1:-1]
            cRefsValue, isRefValue = getRefValue(cWidget, cRefsWithoutBracket, attributesSetDict, True)

            if not isRefStr(cRefsValue):
                refedObNameList.append("".join(cItem + '.' for cItem in re.sub(r'[\[\]]', '', cRefsWithoutBracket).split('.')[0:-1])[0:-1])

                inputStr = inputStr.replace(cRefs, cRefsValue)

                isContainRef = isContainRef + isRefValue

    # stage 3: parse all other refs
    rawInputStr = inputStr
    allRefs = re.findall(refPat, inputStr)

    if len(allRefs) > 0:
        for cRefs in allRefs:
            cRefsValue, isRefValue = getRefValue(cWidget, cRefs, attributesSetDict, True)


            if not isRefStr(cRefsValue):

                refedObNameList.append("".join(cItem + '.' for cItem in re.sub(r'[\[\]]', '', cRefs).split('.')[0:-1])[0:-1])

                if isMatlabStr or isOutStr:
                    # inputStr = re.sub(meanPat, r"',num2str(mean([\1])),'", inputStr)
                    inputStr = inputStr.replace(cRefs, f"',num2str({cRefsValue}),'")
                else:
                    inputStr = inputStr.replace(cRefs, cRefsValue)

                isContainRef = isContainRef + isRefValue



    if isMatlabStr or isOutStr:
        # in case the citation located in the begin or the end of inputStr
        if rawInputStr != inputStr:
            if inputStr.startswith("'',"):
                inputStr = inputStr[3:]
            if inputStr.endswith(",''"):
                inputStr = inputStr[0:-3]

        # for whole citation, there no need to add square brackets
        if isContainRef>1:
            inputStr = addSquBrackets(inputStr)

    isContainRef = isContainRef != 0


    inputStr = inputStr.replace(leftPat, '(')
    inputStr = inputStr.replace(rightPat, ')')


    return repr(inputStr)[1:-1], isContainRef, refedObNameList


def getWidgetIDInTimeline(widget_id: str) -> list:
    wid_name_list = Func.getWidgetIDInTimeline(widget_id)

    return list(wId for wId, wName in wid_name_list)


# def getRefValue2(cWidget, inputStr, attributesSetDict, allowUnlistedAttr=False) -> list:
#     isUnlistedRef = False
#
#     inputStr, isRefValue = getRefValue(cWidget, inputStr, attributesSetDict, allowUnlistedAttr)
#
#     if isRefValue(inputStr):
#         isUnlistedRef = True
#
#     return [inputStr, isRefValue, isUnlistedRef]


def getRefValue(cWidget, inputStr, attributesSetDict, allowUnlistedAttr=False) -> list:
    isRefValue = False

    if isinstance(inputStr, str):

        isRefValue = isRefStr(inputStr)

        if isRefValue:
            # remove the brackets for refValue : a possible bug here
            inputStr = re.sub(r'[\[\]]', '', inputStr)

            if inputStr in attributesSetDict:
                inputStr = attributesSetDict[inputStr][1]
            else:
                if allowUnlistedAttr:
                    inputStr = addSquBrackets(inputStr)
                else:
                    throwCompileErrorInfo(
                        f"The cited attribute '{inputStr}' \nis not available for {getWidgetName(cWidget.widget_id)}")

    return [inputStr, isRefValue]


def getRefValueSet(cWidget, inputStr, attributesSetDict):
    isRefValue = False
    valueSet = set()

    if isinstance(inputStr, str):

        isRefValue = isRefStr(inputStr)

        if isRefValue:
            inputStr = re.sub(r"[\[\]]", '', inputStr)

            if inputStr in attributesSetDict:
                valueSet = attributesSetDict[inputStr][2]
                inputStr = attributesSetDict[inputStr][1]
            else:
                throwCompileErrorInfo(
                    f"The cited attribute '{inputStr}' \nis not available for {getWidgetName(cWidget.widget_id)}")

    return [inputStr, isRefValue, valueSet]


def getSpecialRespsFormatAtts(cInputDevices, cSpecialFormatVarDict):
    for cRespProperties in cInputDevices.values():
        if cRespProperties['Device Id'].split('.')[1] == Info.DEV_KEYBOARD:
            updateSpFormatVarDict(cRespProperties['Correct'], 'kbCorrectResp', cSpecialFormatVarDict)
            updateSpFormatVarDict(cRespProperties['Allowable'], 'kbAllowKeys', cSpecialFormatVarDict)
        else:
            updateSpFormatVarDict(cRespProperties['Correct'], 'noKbDevCorrectResp', cSpecialFormatVarDict)
            updateSpFormatVarDict(cRespProperties['Allowable'], 'noKbAllowKeys', cSpecialFormatVarDict)

        updateSpFormatVarDict(cRespProperties['Start'], 'startRect', cSpecialFormatVarDict)
        updateSpFormatVarDict(cRespProperties['End'], 'endRect', cSpecialFormatVarDict)
        updateSpFormatVarDict(cRespProperties['Mean'], 'meanRect', cSpecialFormatVarDict)


def getSpecialFormatAtts(cSpecialFormatVarDict: dict = None, wIdAndWidgetDict: dict = None) -> dict:
    """
    : special varType:
    : percentage
    """
    if wIdAndWidgetDict is None:
        wIdAndWidgetDict = {}
    if cSpecialFormatVarDict is None:
        cSpecialFormatVarDict = {}

    if len(wIdAndWidgetDict) == 0:
        wIdAndWidgetItems = Info.WID_WIDGET.items()
    else:
        wIdAndWidgetItems = wIdAndWidgetDict.items()

    for widgetId, cWidget in wIdAndWidgetItems:

        cProperties = Func.getWidgetProperties(widgetId)

        if Func.isWidgetType(widgetId, Info.LOOP):
            pass
        elif Func.isWidgetType(widgetId, Info.SWITCH):
            # we do not need to do this here because all sub widgets are contained in Info.Wid_WIDGET
            # cSwitchList = cWidget.getCases()
            #
            # for cCaseList in cSwitchList:
            #     cCaseWidget = cCaseList['Widget']
            #     # skip None type
            #     if cCaseWidget:
            #         cSpecialFormatVarDict = getSpecialFormatAtts(cSpecialFormatVarDict, {cCaseWidget.widget_id: cCaseWidget})
            pass

        elif Func.isWidgetType(widgetId, Info.IF):
            # cTrueWidget = cWidget.getTrueWidget()
            # cSpecialFormatVarDict = getSpecialFormatAtts(cSpecialFormatVarDict, {cTrueWidget.widget_id: cTrueWidget})
            #
            # cFalseWidget = cWidget.getFalseWidget()
            # cSpecialFormatVarDict = getSpecialFormatAtts(cSpecialFormatVarDict, {cFalseWidget.widget_id: cFalseWidget})
            pass

        elif Func.isWidgetType(widgetId, Info.TEXT):
            updateSpFormatVarDict(cWidget.getTransparent(), 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cWidget.getFrameTransparent(), 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Width'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Height'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Center X'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Center Y'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Style'], 'fontStyle', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Clear After'], 'clearAfter', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Flip Horizontal'], 'flipHorizontal', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Flip Vertical'], 'flipVertical', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Right To Left'], 'rightToLeft', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Enable'], 'enableFrame', cSpecialFormatVarDict)
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Text'], 'textContent', cSpecialFormatVarDict)

            getSpecialRespsFormatAtts(cWidget.getInputDevice(), cSpecialFormatVarDict)

        elif Func.isWidgetType(widgetId, Info.VIDEO):
            # updateSpFormatVarDict(cWidget.getTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getFrameTransparent(), 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Width'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Height'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Center X'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Center Y'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Clear After'], 'clearAfter', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Aspect Ratio'], 'aspectRatio', cSpecialFormatVarDict)
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', cSpecialFormatVarDict)

            getSpecialRespsFormatAtts(cWidget.getInputDevice(), cSpecialFormatVarDict)

        elif Func.isWidgetType(widgetId, Info.SOUND):
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Wait For Start'], 'waitForStart', cSpecialFormatVarDict)

            getSpecialRespsFormatAtts(cWidget.getInputDevice(), cSpecialFormatVarDict)

        elif Func.isWidgetType(widgetId, Info.IMAGE):
            updateSpFormatVarDict(cWidget.getTransparent(), 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cWidget.getFrameTransparent(), 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Width'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Height'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Center X'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Center Y'], 'percent', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Clear After'], 'clearAfter', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Enable'], 'enableFrame', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Stretch Mode'], 'stretchMode', cSpecialFormatVarDict)
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', cSpecialFormatVarDict)

            getSpecialRespsFormatAtts(cWidget.getInputDevice(), cSpecialFormatVarDict)

        elif Func.isWidgetType(widgetId, Info.COMBO):
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', cSpecialFormatVarDict)
            updateSpFormatVarDict(cProperties['Properties']['Clear After'], 'clearAfter', cSpecialFormatVarDict)

            cItems = cProperties['Items']
            itemIds = getSliderItemIds(cWidget)
            itemIds.reverse()  # reverse the key id order

            for cItemId in itemIds:
                cItemType = getItemType(cItemId)
                cItemProperties = cItems[cItemId]

                if cItemType == Info.ITEM_IMAGE:
                    updateSpFormatVarDict(cItemProperties['Transparent'], 'percent', cSpecialFormatVarDict)
                    updateSpFormatVarDict(cItemProperties['Width'], 'percent', cSpecialFormatVarDict)
                    updateSpFormatVarDict(cItemProperties['Height'], 'percent', cSpecialFormatVarDict)
                    updateSpFormatVarDict(cItemProperties['Center X'], 'percent', cSpecialFormatVarDict)
                    updateSpFormatVarDict(cItemProperties['Center Y'], 'percent', cSpecialFormatVarDict)
                    updateSpFormatVarDict(cItemProperties['Stretch Mode'], 'stretchMode', cSpecialFormatVarDict)
                elif cItemType == Info.ITEM_SOUND:
                    updateSpFormatVarDict(cItemProperties['Wait For Start'], 'waitForStart', cSpecialFormatVarDict)
                elif cItemType == Info.ITEM_VIDEO:
                    updateSpFormatVarDict(cItemProperties['Transparent'], 'percent', cSpecialFormatVarDict)
                    updateSpFormatVarDict(cItemProperties['Width'], 'percent', cSpecialFormatVarDict)
                    updateSpFormatVarDict(cItemProperties['Height'], 'percent', cSpecialFormatVarDict)
                    updateSpFormatVarDict(cItemProperties['Center X'], 'percent', cSpecialFormatVarDict)
                    updateSpFormatVarDict(cItemProperties['Center Y'], 'percent', cSpecialFormatVarDict)
                    updateSpFormatVarDict(cItemProperties['Aspect Ratio'], 'aspectRatio', cSpecialFormatVarDict)

            getSpecialRespsFormatAtts(cWidget.getInputDevice(), cSpecialFormatVarDict)

    return cSpecialFormatVarDict


def getOutputDevCountsDict() -> dict:
    output_devices = Info.OUTPUT_DEVICE_INFO

    iMonitor = 0
    iParal = 0
    iNetPort = 0
    iSerial = 0
    iSound = 0

    for outDev_Id, cDevice in output_devices.items():

        if cDevice['Device Type'] == Info.DEV_SCREEN:
            iMonitor += 1
        elif cDevice['Device Type'] == Info.DEV_NETWORK_PORT:
            iNetPort += 1
        elif cDevice['Device Type'] == Info.DEV_PARALLEL_PORT:
            iParal += 1
        elif cDevice['Device Type'] == Info.DEV_SERIAL_PORT:
            iSerial += 1
        elif cDevice['Device Type'] == Info.DEV_SOUND:
            iSound += 1

    return {Info.DEV_SCREEN: iMonitor, Info.DEV_NETWORK_PORT: iNetPort, Info.DEV_PARALLEL_PORT: iParal,
            Info.DEV_SERIAL_PORT: iSerial, Info.DEV_SOUND: iSound}


# def getWidgetPosType(cWidget) -> int or None:
def getWidgetPosType(cWidget):
    global stimWidgetTypesList
    cWidgetPosType = None  # 0 -1 None for start, end, and others in event position respectively

    # if is the sub widget of a IF or SWITCH widget, get the pos via inquiring the parent widget
    if isSubWidgetOfIfOrSwitch(cWidget.parent()):
        return getWidgetPosType(cWidget.parent())

    cWidgetId = cWidget.widget_id

    while getWidgetType(cWidgetId) in stimWidgetTypesList:

        if getWidgetType(cWidgetId) in stimWidgetTypesList:
            while isFirstStimWidgetInTL(cWidgetId) or isLastStimWidgetInTL(cWidgetId):
                # Loop till we get a none timeline parentId
                while getWidgetType(cWidgetId) != Info.TIMELINE:
                    cWidgetId = Func.getParentWid(cWidgetId)

            if isFirstStimWidgetInTL(cWidgetId):
                cWidgetPosType = 0
                break
            elif isLastStimWidgetInTL(cWidgetId):
                cWidgetPosType = -1
                break
        else:
            break

    return cWidgetPosType


# noinspection PyBroadException
def getWidLoopLevel(wid: str) -> int:
    """
    :only cycle can increase the loop level
    :param wid: 输入的wid
    :return: 如果wid不存在，返回-1
    """
    try:
        node = Info.WID_NODE[wid]
    except:
        return -1
    # 不断迭代，直至父结点为空
    loopLevel = 1

    node = node.parent()

    while node:
        node = node.parent()
        if Func.isWidgetType(node.widget_id, Info.LOOP):
            loopLevel += 1
    return loopLevel


def getItemType(itemId: str) -> str:
    return itemId.split('_')[0]


def getClearAfterInfo(cWidget, attributesSetDict) -> str:
    """
    :param cWidget:
    :param attributesSetDict:
    :return:
    : "clear_0"     -> "0"
    : "notClear_1"  -> "1"
    : "doNothing_2" -> "2"
    : "0" -> "0"
    : "1" -> "1"
    : "2" -> "2"
    """

    if Info.COMBO == getWidgetType(cWidget):
        cProperties = Func.getWidgetProperties(cWidget.widget_id)['Properties']
    else:
        cProperties = Func.getWidgetProperties(cWidget.widget_id)

    clearAfter = dataStrConvert(*getRefValue(cWidget, cProperties['Clear After'], attributesSetDict))
    clearAfter = parseDontClearAfterStr(clearAfter)

    return clearAfter


def getScreenInfo(cWidget, attributesSetDict):
    """
    :param cWidget:
    :param attributesSetDict:
    :return:
    :cScreenName:
    :cWinIdx: index of the current screen
    :cWinStr: winIdx(index) in matlab
    """
    global outputDevNameIdxDict
    shouldNotBeCitationCheck('Screen Name', cWidget.getScreenName())

    cScreenName, ign = getRefValue(cWidget, cWidget.getScreenName(), attributesSetDict)

    # currently we just used the nearest previous flipped screen info
    cWinIdx = outputDevNameIdxDict.get(cScreenName)
    cWinStr = f"winIds({cWinIdx})"

    return cScreenName, cWinIdx, cWinStr


def getSliderItemIds(cWidget, itemType='') -> list:
    itemIds = []
    if Func.isWidgetType(cWidget.widget_id, Info.COMBO):
        properties = Func.getWidgetProperties(cWidget.widget_id)

        if len(itemType) == 0:
            itemIds = [key for key in properties['Items'].keys()]
        else:
            itemIds = [key for key in properties['Items'].keys() if getItemType(key) == itemType]

    return itemIds


def getSliderItemTypeNums(cWidget, itemType: str) -> int:
    itemNums = 0

    if Func.isWidgetType(cWidget.widget_id, Info.COMBO):
        itemIds = getSliderItemIds(cWidget)

        for cItemId in itemIds:
            if getItemType(cItemId) == itemType:
                itemNums += 1

    return itemNums


def getContainItemTypeNums(itemIds: list, itemType: str) -> int:
    itemNums = 0
    for cItemId in itemIds:
        if getItemType(cItemId) == itemType:
            itemNums += 1

    return itemNums


def getMaximumOpDataRows() -> int:
    MaxOpDataRows = updateTLOpDataRow(Info.WID_WIDGET[f"{Info.TIMELINE}.0"], 0)

    return MaxOpDataRows


def getMaxSlaveSoundDevs() -> dict:
    # dictionary: sound dev ID:maximum slave devs
    maxSlaveSoundDevs = dict()

    for cWidgetId in Info.WID_WIDGET.keys():
        cWidget = Info.WID_WIDGET[cWidgetId]

        if Func.isWidgetType(cWidgetId, Info.COMBO):
            itemIds = getSliderItemIds(cWidget)

            cProperties = Func.getWidgetProperties(cWidget.widget_id)

            if isContainItemType(itemIds, Info.ITEM_SOUND):
                cSoundNumList = dict()

                for cItemId in itemIds:
                    if getItemType(cItemId) == Info.ITEM_SOUND:
                        cItemPro = cProperties['Items'][cItemId]
                        cSoundDevName = cItemPro['Sound Device']
                        cSoundDevNum = cSoundNumList.get(cSoundDevName, 0)
                        cSoundNumList.update({cSoundDevName: cSoundDevNum + 1})

                        nSounds = max(maxSlaveSoundDevs.get(cSoundDevName, 0), cSoundNumList[cSoundDevName])
                        maxSlaveSoundDevs.update({cSoundDevName: nSounds})

        elif Func.isWidgetType(cWidgetId, Info.SOUND):
            cProperties = Func.getWidgetProperties(cWidget.widget_id)
            nSounds = max(maxSlaveSoundDevs.get(cProperties['Sound Device'], 0), 1)
            maxSlaveSoundDevs.update({cProperties['Sound Device']: nSounds})

    return maxSlaveSoundDevs


def getWidgetType(cWidgetOrId) -> str:
    if isinstance(cWidgetOrId, str):
        return cWidgetOrId.split('.')[0]
    else:
        return cWidgetOrId.widget_id.split('.')[0]


def getWidgetIdType(widget_id: str) -> str:
    return widget_id.split('.')[0]


def updateTLOpDataRow(cTLWidget, opDataRowsInPy: int) -> int:
    noSubCycleTL = True

    cTimelineWidgetIds = getWidgetIDInTimeline(cTLWidget.widget_id)

    for cWidgetId in cTimelineWidgetIds:
        cWidget = Info.WID_WIDGET[cWidgetId]

        if Func.isWidgetType(cWidgetId, Info.LOOP):
            noSubCycleTL = False
            opDataRowsInPy = updateCycleOpDataRows(cWidget, opDataRowsInPy)

    if noSubCycleTL:
        opDataRowsInPy += 1

    return opDataRowsInPy


def updateCycleOpDataRows(cCyleWdiget, opDataRowsInPy: int) -> int:
    cTimeLineids = cCyleWdiget.getTimelines()

    for iRow in range(cCyleWdiget.rowCount()):
        cRowDict = cCyleWdiget.getAttributes(iRow)
        cTLid = cTimeLineids[iRow]
        # print(f"{cTLid}")
        cTLWidget = Info.WID_WIDGET[cTLid[1]]

        if '' == cRowDict['Repetitions']:
            cRepeat = 1
        else:
            cRepeat = dataStrConvert(cRowDict['Repetitions'])

        for iRep in range(cRepeat):
            opDataRowsInPy = updateTLOpDataRow(cTLWidget, opDataRowsInPy)
    return opDataRowsInPy


def printCycleWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    global spFormatVarDict, cInfoDict
    # start from 1 to compatible with MATLAB
    cLoopLevel += 1
    # cOpDataRowNum = cInfoDict.get('maximumRows')
    # maybe we need to change copy to deepcopy
    attributesSetDict = copy.deepcopy(attributesSetDict)
    # attributesSetDict = attributesSetDict.copy()
    cWidgetName = getWidgetName(cWidget.widget_id)

    attributesSetDict.setdefault(f"{cWidgetName}.cLoop", [cLoopLevel, f"iLoop_{cLoopLevel}", {f"iLoop_{cLoopLevel}"}])
    attributesSetDict.setdefault(f"{cWidgetName}.rowNums",
                                 [cLoopLevel, f"size({cWidgetName}.var,1)", {f"size({cWidgetName}.var,1)"}])

    cLoopIterStr = attributesSetDict[f"{cWidgetName}.cLoop"][1]

    # create the design matrix  (table) for the current cycle
    startExpStr = cWidgetName + '.var = cell2table({...'
    printAutoInd(f, '% create the designMatrix for the current loop')
    printAutoInd(f, '{0}', startExpStr)

    endExpStr = "},'VariableNames',{"

    for iRow in range(cWidget.rowCount()):
        cRowDict = cWidget.getAttributes(iRow)
        if 0 == iRow:
            endExpStr = endExpStr + ''.join("'" + key + "' " for key in cRowDict.keys()) + "});"

        for key, value in cRowDict.items():
            # get the referenced var value
            cValue, isRefValue, cRefValueSet = getRefValueSet(cWidget, value, attributesSetDict)

            cKeyAttrName = f"{getWidgetName(cWidget.widget_id)}.var.{key}"

            # handle the references and the values in special format (e.g., percent, duration)
            # --- replaced the percentageStr--------/
            if cKeyAttrName in spFormatVarDict:
                if 'percent' == spFormatVarDict[cKeyAttrName]:
                    cValue = parsePercentStr(cValue)
                    cRowDict[key] = cValue

                elif 'dur' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseDurationStr(cValue)
                    cRowDict[key] = cValue

                elif 'fontStyle' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseFontStyleStr(cValue)
                    cRowDict[key] = cValue

                elif 'clearAfter' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseDontClearAfterStr(cValue)
                    cRowDict[key] = cValue

                elif 'flipHorizontal' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif 'flipVertical' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif 'rightToLeft' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif 'enableFrame' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif 'waitForStart' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif 'kbCorrectResp' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseKbCorRespStr(cValue, isRefValue, Info.DEV_KEYBOARD)
                    cRowDict[key] = cValue

                elif 'noKbDevCorrectResp' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseKbCorRespStr(cValue, isRefValue, 'noneKbDevs')
                    cRowDict[key] = cValue

                elif 'kbAllowKeys' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseKbCorRespStr(cValue, isRefValue, Info.DEV_KEYBOARD)
                    cRowDict[key] = cValue

                elif 'noKbAllowKeys' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseKbCorRespStr(cValue, isRefValue, 'noneKbDevs')
                    cRowDict[key] = cValue

                elif 'textContent' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseTextContentStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif 'aspectRation' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseAspectRationStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif 'stretchMode' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseAspectRationStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif 'startRect' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseRectStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif 'endRect' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseRectStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif 'meanRect' == spFormatVarDict[cKeyAttrName]:
                    cValue = parseRectStr(cValue, isRefValue)
                    cRowDict[key] = cValue

            #     TO BE CONTINUING... FOR ALL OTHER Special Types
            # --------------------------------------\

            cAttributeName = f"{cWidgetName}.var.{key}"

            if not isRefValue:
                cRefValueSet = {cValue}

            if cAttributeName in attributesSetDict:
                preValueSet = attributesSetDict[cAttributeName][2]
            else:
                preValueSet = set()

            attributesSetDict.update(
                {cAttributeName: [cLoopLevel, f"{cAttributeName}{{{cLoopIterStr}}}", cRefValueSet.union(preValueSet)]})

        # print out the design matrix of the current Cycle
        if '' == cRowDict['Repetitions']:
            cRepeat = 1
        else:
            cRepeat = dataStrConvert(cRowDict['Repetitions'])

        for iRep in range(cRepeat):
            printAutoInd(f, '{0}', "".join(
                addCurlyBrackets(dataStrConvert(*getRefValue(cWidget, value, attributesSetDict), False, False)) + " "
                for key, value in cRowDict.items()) + ";...")

    printAutoInd(f, '{0}\n', endExpStr)
    # Shuffle the designMatrix:
    cycleOrderStr = dataStrConvert(*getRefValue(cWidget, cWidget.getOrder(), attributesSetDict))
    cycleOrderByStr = dataStrConvert(*getRefValue(cWidget, cWidget.getOrderBy(), attributesSetDict))

    #  to make sure the repetitions is one for counterbalance selection of order ----/
    if cycleOrderStr == "'Counter Balance'":
        cCycleWeightList = cWidget.getAttributeValues(0)
        for cLineWeight in cCycleWeightList:
            if dataStrConvert(cLineWeight) != 1:
                throwCompileErrorInfo(
                    f"Found an incompatible error in Cycle {getWidgetName(cWidget.widget_id)}:\nFor Counter Balance selection, the timeline repetitions should be 1")
    # ------------------------------------------------------------------------\

    printAutoInd(f, "% Shuffle the DesignMatrix")
    printAutoInd(f, 'cShuffledIdx = ShuffleCycleOrder({0},{1},{2},subInfo);',
                 attributesSetDict[f"{cWidgetName}.rowNums"][1], cycleOrderStr, cycleOrderByStr)
    printAutoInd(f, '{0}.var = {0}.var(cShuffledIdx,:);', cWidgetName)
    printAutoInd(f, "\n")

    # cycling
    printAutoInd(f, '% looping across each row of the {0}.var:{1}', cWidgetName, cLoopIterStr)
    printAutoInd(f, 'for {0} =1:size({1},1)', cLoopIterStr, f"{cWidgetName}.var")

    cLoopOpIdxStr = cLoopIterStr + "_cOpR"

    printAutoInd(f, "{0} = opRowIdx; % output var row num for loop level {1}\n", cLoopOpIdxStr, cLoopLevel)

    printAutoInd(f, "% copy attr var values into output vars for row {0}", cLoopOpIdxStr)

    cRowDict = cWidget.getAttributes(0)
    otVarStr = ''.join(cWidgetName + '_' + key + f"{{{cLoopOpIdxStr}}}," for key in cRowDict.keys())
    otVarStr = f"[{otVarStr[0:-1]}] = deal({cWidgetName}.var{{{cLoopIterStr},:}}{{:}});"

    printAutoInd(f, "{0}\n", otVarStr)

    # handle each timeline
    cTimeLineList = cWidget.getTimelines()
    # squeeze the timelines
    cTimelineSet = set()

    for iTimeline in cTimeLineList:
        cTimelineSet.add(iTimeline[1])

    printAutoInd(f, '% switch across timeline types')
    printAutoInd(f, 'switch {0}', f"{cWidgetName}.var.Timeline{{{cLoopIterStr}}}")

    for iTimeline_id in cTimelineSet:
        if '' == iTimeline_id:
            throwCompileErrorInfo(f"In {cWidgetName}: Timeline should not be empty!")
        else:
            printAutoInd(f, 'case {0}', f"{addSingleQuotes(getWidgetName(iTimeline_id))}")

            allWidgetCodes = printTimelineWidget(Info.WID_WIDGET[iTimeline_id], f, attributesSetDict, cLoopLevel,
                                                 allWidgetCodes)

    printAutoInd(f, 'otherwise ')
    printAutoInd(f, '% do nothing ')
    printAutoInd(f, 'end%switch {0}', f"{cWidgetName}.var.Timeline{{{cLoopIterStr}}}")

    printAutoInd(f, "opRowIdx = opRowIdx + 1; % increase the row num of outputVars by 1")
    printAutoInd(f, 'end % {0}', cLoopIterStr)
    # to be continue ...

    # print close possible textures and maybe audio buffers
    # close possible visual textures
    beClosedTxList = allWidgetCodes.get(f"beClosedTextures_{cLoopLevel}", [])
    if len(beClosedTxList) > 0:
        bePrintStr = "".join(f"{cTx}," for cTx in beClosedTxList)
        if len(beClosedTxList) == 1:
            bePrintStr = "Screen('Close'," + bePrintStr[0:-1] + ");\n"
        else:
            bePrintStr = "Screen('Close',[" + bePrintStr[0:-1] + "]);\n"

        printAutoInd(f, ' ')
        printAutoInd(f, '% close visual textures')
        printAutoInd(f, bePrintStr)
    # after print clean up the list
    allWidgetCodes.update({f"beClosedTextures_{cLoopLevel}": []})

    # close possible audio buffers

    return allWidgetCodes


# noinspection PyStringFormat
def printToDelayedCodes(allWidgetCodes, keyName, inputStr, *argins):
    global isDummyPrint

    if not isDummyPrint:
        allWidgetCodes[keyName].append = f"{inputStr}".format(*argins)


def printInAllWidgetCodesByKey(f, bePrintedCodes: dict, key='respCodes') -> dict:
    cKeyValueList = bePrintedCodes.get(key, [])

    for cRowStr in cKeyValueList:
        cRowStr = "{{".join(cRowStr.split('{'))
        cRowStr = "}}".join(cRowStr.split('}'))
        printAutoInd(f, cRowStr)

    bePrintedCodes.update({key: []})  # clean the key value

    return bePrintedCodes


# def printBeforeFlipCodes(f, bePrintedCodes: dict or list) -> dict or list:
def printBeforeFlipCodes(f, bePrintedCodes):
    if isinstance(bePrintedCodes, dict):
        cCodesBeFip = bePrintedCodes.get('codesBeFip', [])
        for cRowStr in cCodesBeFip:
            cRowStr = "{{".join(cRowStr.split('{'))
            cRowStr = "}}".join(cRowStr.split('}'))
            printAutoInd(f, cRowStr)
        # clear out the print buffer
        bePrintedCodes.update({'codesBeFip': []})
    elif isinstance(bePrintedCodes, list):
        for cRowStr in bePrintedCodes:
            cRowStr = "{{".join(cRowStr.split('{'))
            cRowStr = "}}".join(cRowStr.split('}'))
            printAutoInd(f, cRowStr)
        bePrintedCodes = []

    return bePrintedCodes


def flipScreen(cWidget, f, cLoopLevel, attributesSetDict, allWidgetCodes):
    global historyPropDict, isDummyPrint
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num

    # get screen index and cWinStr :winIdx(index)
    _, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    clearAfter = getClearAfterInfo(cWidget, attributesSetDict)

    cWidgetName = getWidgetName(cWidget.widget_id)
    cWidgetPos = getWidgetEventPos(cWidget.widget_id)

    cRespCodes = allWidgetCodes.get(f"{cWidget.widget_id}_cRespCodes", [])

    # if getWidgetPos(cWidget.widget_id) > 0 and not(isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
    #     # Step 2: print out help info for the current widget
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, cWidgetPos + 1,
    #                  getWidgetName(cWidget.widget_id))
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    if isVideoRelatedWidget(cWidget):
        # printAutoInd(f, "% for first event, flip immediately.. ")

        allWidgetCodes = printBeforeFlipCodes(f, allWidgetCodes)

        # printAutoInd(f, " ")
        allWidgetCodes = genCheckResponse(cWidget, f, cLoopLevel, attributesSetDict, allWidgetCodes)
        printAutoInd(f, "%initialise video flip ")
        printAutoInd(f, "isFirstVideoFrame = true;")
        printAutoInd(f, "secs              = GetSecs;")
        printAutoInd(f, "afVideoFipReqTime = GetSecs; % temp value but ensure larger than secs\n")

        cVideoItemNums = getSliderItemTypeNums(cWidget, Info.ITEM_VIDEO)
        if cVideoItemNums <= 1:
            printAutoInd(f, "{0}_tPtr = 1;", cWidgetName)
            printAutoInd(f, "{0}_CPt  =-1;\n", cWidgetName)

            # printAutoInd(f, "while {0}_tPtr > 0 && {0}_CPt < {0}_eMTime", cWidgetName)
            printAutoInd(f, "while secs < afVideoFipReqTime", cWidgetName)
        else:
            printAutoInd(f, "{0}_tPtrs = repmat(1,1,{1});", cWidgetName, cVideoItemNums)
            printAutoInd(f, "{0}_CPts = repmat(-1,1,{1});", cWidgetName, cVideoItemNums)

            printAutoInd(f, "while any( {0}_tPtrs > 0 && ({0}_CPts./{0}_eMTimes) < 1 )", cWidgetName)

            # printAutoInd(f, "if ~isFirstVideoFrame")
            # if cVideoItemNums <= 1:
            #     printAutoInd(f, "Screen('Close',{0}_tPtr);", cWidgetName)
            # else:
            #     printAutoInd(f, "Screen('Close',{0}_tPtrs);", cWidgetName)
            # printAutoInd(f, "end")

        '''
        draw all visual stim looply over here: print cVSLCodes
        '''

        allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, 'forVideoSliderLoopCodes')

        # printAutoInd(f, "% check the 'esc' key to abort the exp")
        # printAutoInd(f, "detectAbortKey(abortKeyCode);\n")

        printAutoInd(f,f"[isTerminateStimEvent, secs]= checkRespAndSendTriggers({cWinIdx}, afVideoFipReqTime, true); ")

        printAutoInd(f, "if isFirstVideoFrame ")

        if cWidgetPos == 0:
            printAutoInd(f, "{0}.onsettime({1})= Screen('Flip',{2},nextEvFlipReqTime,{3});", cWidgetName, cOpRowIdxStr,
                         cWinStr, clearAfter)
        else:
            printAutoInd(f, "{0}.onsettime({1})= Screen('Flip',{2},nextEvFlipReqTime,{3});", cWidgetName, cOpRowIdxStr,
                         cWinStr, clearAfter)
        allWidgetCodes = genStimTriggers(cWidget, f, cLoopLevel, attributesSetDict, allWidgetCodes)
        allWidgetCodes = genUpdateWidgetDur(cWidget, f, attributesSetDict, allWidgetCodes, 'afVideoFipReqTime')

        printAutoInd(f, "nextEvFlipReqTime = afVideoFipReqTime; % after the first flip, update nextEvFlipReqTime")
        printAutoInd(f, "isFirstVideoFrame = false; ")
        printAutoInd(f, "else ")
        printAutoInd(f, "Screen('Flip', {0}, 0, {1}); %", cWinStr, clearAfter)
        printAutoInd(f, "end \n")

        if cVideoItemNums <= 1:
            printAutoInd(f, "Screen('Close',{0}_tPtr);\n", cWidgetName)
        else:
            printAutoInd(f, "Screen('Close',{0}_tPtrs);\n", cWidgetName)

        printAutoInd(f, "if isTerminateStimEvent")
        printAutoInd(f, "nextEvFlipReqTime = 0;")
        printAutoInd(f, "break;")
        printAutoInd(f, "end")
        # print response check section
        printAutoInd(f, "end % while\n")

        printAutoInd(cRespCodes, "% close opened movie prts and visual textures")
        if cVideoItemNums <= 1:
            printAutoInd(cRespCodes, "Screen('CloseMovie', {0}_mPtr);", cWidgetName)
            printAutoInd(cRespCodes, "Screen('Close',{0}_tPtr); % close the last video frame", cWidgetName)
        else:
            printAutoInd(cRespCodes, "Screen('CloseMovie', {0}_mPtrs);", cWidgetName)
            printAutoInd(cRespCodes, "Screen('Close',TPtrs); % close the last video frame")

        cAfEndVideoFlipCodes = allWidgetCodes.get('codesAfEndVideoFip', [])

        cRespCodes.extend(cAfEndVideoFlipCodes)

        allWidgetCodes.update({'codesAfEndVideoFip': []})

        allWidgetCodes.update({f"{cWidget.widget_id}_cRespCodes": cRespCodes})

    else:
        # Flip the Screen
        if cWidgetPos == 0:
            # printAutoInd(f, "% for first event, flip immediately.. ")
            # f"{getWidgetName(cWidget.widget_id)}_onsettime({cOpRowIdxStr})"
            printAutoInd(f, "{0}.onsettime({1}) = Screen('Flip',{2},nextEvFlipReqTime,{3}); %#ok<*STRNU>\n",
                         cWidgetName,
                         cOpRowIdxStr, cWinStr, clearAfter)
        else:
            printAutoInd(f, "{0}.onsettime({1}) = Screen('Flip',{2},nextEvFlipReqTime,{3}); %#ok<*STRNU>\n",
                         cWidgetName,
                         cOpRowIdxStr, cWinStr, clearAfter)

    return allWidgetCodes


def flipAudio(cWidget, f, cLoopLevel, attributesSetDict, iSlave=1):
    # for sound widget only, not for slider that contains sound item
    global historyPropDict, isDummyPrint
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num

    # get screen cWinIdx and cWinStr: winIdx(index)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    clearAfter = getClearAfterInfo(cWidget, attributesSetDict)

    # isSyncToVbl = True
    # haveSound = isContainSound(cWidget)
    # isSlider = Func.isWidgetType(cWidget.widget_id, Info.COMBO)

    # 1) check the sound dev parameter:
    cSoundDevName, isRef = getRefValue(cWidget, cWidget.getSoundDeviceName(), attributesSetDict)
    cSoundIdxStr = f"{outputDevNameIdxDict.get(cSoundDevName)}({iSlave})"

    # 2) check the repetitions parameter:
    repetitionsStr, isRef = getRefValue(cWidget, cWidget.getRepetitions(), attributesSetDict)

    # 3) get the isSyncToVbl parameter for sound widget only:
    #    sound in the slider will force tobe sync to the VBL
    # if Func.isWidgetType(cWidget.widget_id, Info.SOUND):
    isSyncToVbl = cWidget.getSyncToVbl()

    # if getWidgetPos(cWidget.widget_id) > 0 and not(isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
    #     # Step 2: print out help info for the current widget
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
    #                  getWidgetName(cWidget.widget_id))
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    if isSyncToVbl:
        # Flip the Screen
        printAutoInd(f, "% sync to the vertical blank of screen:{0}", cWidget.getScreenName())
        if getWidgetPos(cWidget.widget_id) == 0:
            printAutoInd(f, "% for first event, play the audio at the immediately VBL .. ")
            printAutoInd(f, "predictedVisOnset = PredictVisualOnsetForTime({0}, 0);", cWinStr)

            printAutoInd(f, "PsychPortAudio('Start', {0}, {1}, predictedVisOnset, 0); %\n", cSoundIdxStr,
                         repetitionsStr)
            printAutoInd(f, "{0}.onsettime({1}) = Screen('Flip', {2}, {3}); %\n", getWidgetName(cWidget.widget_id),
                         cOpRowIdxStr, cWinStr, clearAfter)
        else:
            printAutoInd(f, "predictedVisOnset = PredictVisualOnsetForTime({0}, nextEvFlipReqTime);", cWinStr)
            printAutoInd(f, "% schedule start of audio at exactly the predicted time caused by the next flip")
            printAutoInd(f, "PsychPortAudio('Start', {0}, {1}, predictedVisOnset, 0); %\n",
                         cSoundIdxStr, repetitionsStr)
            printAutoInd(f, "{0}.onsettime({1}) = Screen('Flip',{2},nextEvFlipReqTime, {3}); %#ok<*STRNU>\n",
                         getWidgetName(cWidget.widget_id), cOpRowIdxStr, cWinStr, clearAfter)
    else:
        if getWidgetPos(cWidget.widget_id) == 0:
            printAutoInd(f, "% for first event, play the audio immediately.. ")
            printAutoInd(f,
                         "{0}.onsettime({1}) = PsychPortAudio('Start', {2}, {3}, 0, 1); % wait for start and get the real start time\n",
                         getWidgetName(cWidget.widget_id), cOpRowIdxStr, cSoundIdxStr, repetitionsStr)
        else:
            printAutoInd(f, "% for multiple screens, use the maximum of the predicted onsettime")
            printAutoInd(f,
                         "{0}.onsettime({1}) = PsychPortAudio('Start', {2}, {3}, max(cDurs + lastScrOnsettime), 1); % % wait for start and get the real start time\n",
                         getWidgetName(cWidget.widget_id), cOpRowIdxStr, cSoundIdxStr, repetitionsStr)


def genCheckResponse(cWidget, f, cLoopLevel, attributesSetDict, allWidgetCodes):
    global outputDevNameIdxDict, historyPropDict, isDummyPrint, queueDevIdxValueStr

    # for video related widget, will do this during the flip loop
    # if isVideoRelatedWidget(cWidget):
    #     return allWidgetCodes

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"
    cWidgetName = getWidgetName(cWidget.widget_id)

    cOutDeviceDict = historyPropDict.get('cOutDevices', {})
    historyPropDict.update({'cOutDevices': {}})

    outDevCountsDict = getOutputDevCountsDict()

    # get screen cWinIdx and cWinStr: winIds(idx)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    cInputDevices = cWidget.getInputDevice()

    # -------------------------------------------------------------------------------
    # Step 1: check parameters that should not be a citation value
    # -------------------------------------------------------------------------------
    nKbs = 0
    nMouses = 0

    for key, value in cInputDevices.items():
        shouldNotBeCitationCheck('RT Window', value['RT Window'])
        shouldNotBeCitationCheck('End Action', value['End Action'])

        shouldNotBeEmptyCheck(f"the allow able keys in {cWidgetName}:{value['Device Name']}", value['Allowable'])

        # check if the end action and rt window parameters are compatible
        if value.get('End Action').startswith('Terminate'):
            if value.get('RT Window') != '(Same as duration)':
                throwCompileErrorInfo(
                    f"{cWidgetName}:{value.get('Device Name')} when 'End Action' is {value.get('End Action')}, 'RT Window' should be '(Same as duration)'")

        if value['Device Type'] == Info.DEV_KEYBOARD:
            nKbs += 1

        if value['Device Type'] == Info.DEV_MOUSE:
            nMouses += 1

        value.update({'Widget Name': cWidgetName})
        cInputDevices.update({key: value})

    # under windows: all keyboards and mouses will be treated as a single device
    if Info.PLATFORM == 'windows':
        if nKbs > 1 or nMouses > 1:
            tobeShowStr = 'Input devices: \n For windows, specify multiple kbs or mice separately are not allowed!\n you can specify only one keyboard and/or one mouse here!'
            throwCompileErrorInfo(f"{cWidgetName}: {tobeShowStr}")
    #
    if len(cInputDevices) > 0:

        iRespDev = 1
        printAutoInd(f, "% make respDev struct")
        for cInputDev, cProperties in cInputDevices.items():
            # get allowable keys
            allowableKeysStr, isRefValue, cRefValueSet = getRefValueSet(cWidget, cProperties.get('Allowable'),
                                                                        attributesSetDict)
            allowableKeysStr = parseKbCorRespStr(allowableKeysStr, isRefValue, cProperties['Device Type'])

            # update the allowableKeysList
            if cProperties['Device Type'] != Info.DEV_RESPONSE_BOX:

                if isRefValue:
                    for allowableKey in cRefValueSet:
                        updateEnableKbKeysList(allowableKey)
                else:
                    updateEnableKbKeysList(allowableKeysStr)

            # get corRespCode
            corRespStr, isRefValue = getRefValue(cWidget, cProperties['Correct'], attributesSetDict)
            corRespStr = parseKbCorRespStr(corRespStr, isRefValue, cProperties['Device Type'])

            if corRespStr.find(',') == -1:
                corRespStr = removeSquBrackets(corRespStr)

            # get response time window
            rtWindowStr = parseRTWindowStr(cProperties['RT Window'])

            # get end action
            endActionStr = parseEndActionStr(cProperties['End Action'])

            # get Right
            rightStr = dataStrConvert(*getRefValue(cWidget, cProperties['Right'], attributesSetDict), True)

            # get Wrong
            wrongStr = dataStrConvert(*getRefValue(cWidget, cProperties['Wrong'], attributesSetDict), True)

            # get No Resp
            noRespStr = dataStrConvert(*getRefValue(cWidget, cProperties['No Resp'], attributesSetDict), True)

            # get start rect
            startRectStr = parseRectStr(*getRefValue(cWidget, cProperties['Start'], attributesSetDict))

            # get end rect
            endRectStr = parseRectStr(*getRefValue(cWidget, cProperties['End'], attributesSetDict))

            # get mean rect
            meanRectStr = parseRectStr(*getRefValue(cWidget, cProperties['Mean'], attributesSetDict))

            # get os oval
            isOvalStr = parseBooleanStr(cProperties['Is Oval'])

            # get resp output dev name
            respOutDevNameStr, isRefValue = getRefValue(cWidget, cProperties['Output Device'], attributesSetDict)

            # devIndexesVarName = None
            # get dev type and devIndexesVarName
            cInputDevIndexValueStr, cIsQueue, cDevType = inputDevNameIdxDict[cProperties['Device Name']]

            # if the response code send port is a parallel
            if respOutDevNameStr == '' or respOutDevNameStr == 'none':
                needTobeRetStr = 'false'
                respCodeDevIdxStr = '0'
                respCodeDevTypeStr = '[]'
            else:
                # cOutDeviceDict[cDevName] = [devType, pulseDur, devPort]
                respCodeDevIdxStr = cOutDeviceDict[respOutDevNameStr][2]

                respCodeDevTypeStr = cOutDeviceDict[respOutDevNameStr][0]

                if cOutDeviceDict[respOutDevNameStr][0] == '1':
                    needTobeRetStr = 'true'
                else:
                    needTobeRetStr = 'false'

            beUpdatedVarStr = f"sprintf('{cWidgetName}(%d)',{cOpRowIdxStr})"
            startTimeStr = f"lastScrOnsettime({cWinIdx})"

            # eye action 82 should not be "Terminate till release"
            if cDevType == 82 and endActionStr == "2":
                endActionStr = "1"

            printAutoInd(f,
                         "makeRespStruct({0},{1},{2},{3},{4},{5},{6},{7},{8},{9},{10},{11},{12},{13},{14},{15},{16},{17},{18},{19});",
                         beUpdatedVarStr,  # 0 beUpdatedVar
                         allowableKeysStr,  # 1 allowAble
                         corRespStr,  # 2 corResp
                         rtWindowStr,  # 3 rtWindow
                         endActionStr,  # 4 endAction
                         cDevType,  # 5 type
                         cInputDevIndexValueStr,  # 6 index
                         cIsQueue,  # 7 isQueue
                         startTimeStr,  # 8 startTime
                         '1',  # 9 checkStatus
                         needTobeRetStr,  # 10 needTobeReset
                         rightStr,  # 11 right
                         wrongStr,  # 12 wrong
                         noRespStr,  # 13 noResp
                         respCodeDevTypeStr,  # 14 respCodeDevType
                         respCodeDevIdxStr,  # 15 respCodeDevIdx
                         startRectStr,  # 16 start
                         endRectStr,  # 17 end
                         meanRectStr,  # 18 mean
                         isOvalStr,  # 19 isOval
                         )

            iRespDev += 1

        if len(queueDevIdxValueStr) > 0:
            printAutoInd(f, "isQueueStart = switchQueue_bcl({0}, isQueueStart);", queueDevIdxValueStr)

        printAutoInd(f, "\n")
    else:
        if len(queueDevIdxValueStr) > 0:
            printAutoInd(f, "isQueueStart = switchQueue_bcl({0}, isQueueStart);", queueDevIdxValueStr)

    if not isVideoRelatedWidget(cWidget):
        printAutoInd(f, "[~,~,nextEvFlipReqTime] = checkRespAndSendTriggers({0}, nextEvFlipReqTime, false);\n", cWinIdx)
        # printAutoInd(f, "if isTerminateStimEvent")
        # printAutoInd(f, "nextEvFlipReqTime = 0;")
        # printAutoInd(f, "end ")
    # printAutoInd(f, "%=================================================\\\n")

    shortPulseDurParallelsDict = outPutTriggerCheck(cWidget)

    return allWidgetCodes


def genStimWidgetAllCodes(cWidget, attributesSetDict, cLoopLevel, allWidgetCodes):
    cStimCodes = list()
    cFlipCodes = list()
    cStimTriggerCodes = list()
    cUpdateDurCodes = list()
    cRespCodes = list()

    if cWidget is None:
        return allWidgetCodes
    # print comments to indicate the current frame order
    cWidgetName = getWidgetName(cWidget.widget_id)
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    cWidgetType = getWidgetType(cWidget)

    if isSubWidgetOfIfOrSwitch(cWidget) is False:
        #  update the attributesSetDict only for the main widgets
        cWidgetAddedAttrsList = ['rt', 'resp', 'acc', 'onsettime', 'respOnsettime']
        for cAddedAttr in cWidgetAddedAttrsList:
            attributesSetDict.update({
                f"{cWidgetName}.{cAddedAttr}":
                    [cLoopLevel, f"{cWidgetName}({cOpRowIdxStr}).{cAddedAttr}",
                     {f"{cWidgetName}({cOpRowIdxStr}).{cAddedAttr}"}]
            })

    # Step 1: generate codes to draw stim
    if Info.TEXT == cWidgetType:
        drawTextWidget(cWidget, cStimCodes, attributesSetDict, cLoopLevel)
    elif Info.IMAGE == cWidgetType:
        allWidgetCodes, *_ = drawImageWidget(cWidget, cStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes)
    elif Info.SOUND == cWidgetType:
        allWidgetCodes = drawSoundWidget(cWidget, cStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes)
    elif Info.COMBO == cWidgetType:
        allWidgetCodes = drawSliderWidget(cWidget, cStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes)
    elif Info.VIDEO == cWidgetType:
        allWidgetCodes, _ = drawVideoWidget(cWidget, cStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes)

    elif Info.IF == cWidgetType:
        falseWidget = cWidget.getFalseWidget()
        allWidgetCodes = genStimWidgetAllCodes(falseWidget, attributesSetDict, cLoopLevel, allWidgetCodes)

        trueWidget = cWidget.getTrueWidget()
        allWidgetCodes = genStimWidgetAllCodes(trueWidget, attributesSetDict, cLoopLevel, allWidgetCodes)

        # concatenate codes for IF widget
        allWidgetCodes = makeCodes4IfWidget(cWidget, attributesSetDict,cLoopLevel, allWidgetCodes)

        return allWidgetCodes

    elif Info.SWITCH == cWidgetType:
        caseWidgets = cWidget.getCases()

        for cCase in caseWidgets:
            cSubWid = cCase['Sub Wid']

            if cSubWid:
                allWidgetCodes = genStimWidgetAllCodes(Info.WID_WIDGET[cSubWid], attributesSetDict, cLoopLevel,
                                                       allWidgetCodes)

        # concatenate codes for switch widget
        allWidgetCodes = makeCodes4SwitchWidget(cWidget, attributesSetDict, cLoopLevel, allWidgetCodes)

        return allWidgetCodes

    # STEP 2: generate flip code
    if Info.SOUND == cWidgetType:
        flipAudio(cWidget, cFlipCodes, cLoopLevel, attributesSetDict)
    else:
        flipScreen(cWidget, cFlipCodes, cLoopLevel, attributesSetDict, allWidgetCodes)


    # for video related widget, will run step 4-6 (do nothing) in dummy as we already did this in Step3:
    # if is a video related widget, will do this within flip loop
    if not isVideoRelatedWidget(cWidget):
        # step 3: generate sending trigger codes
        allWidgetCodes = genStimTriggers(cWidget, cStimTriggerCodes, cLoopLevel, attributesSetDict, allWidgetCodes)

        # step 4: generate updating cDurs codes
        allWidgetCodes = genUpdateWidgetDur(cWidget, cUpdateDurCodes, attributesSetDict, allWidgetCodes)

        # step 5: generate response checking codes
        allWidgetCodes = genCheckResponse(cWidget, cRespCodes, cLoopLevel, attributesSetDict, allWidgetCodes)

    # save all codes for the current widget
    cStimExistCodes: list = allWidgetCodes.get(f"{cWidget.widget_id}_cStimCodes", [])
    cStimExistCodes.extend(cStimCodes)
    allWidgetCodes.update({f"{cWidget.widget_id}_cStimCodes": cStimExistCodes})

    cFlipExistCodes: list = allWidgetCodes.get(f"{cWidget.widget_id}_cFlipCodes", [])
    cFlipExistCodes.extend(cFlipCodes)
    allWidgetCodes.update({f"{cWidget.widget_id}_cFlipCodes": cFlipExistCodes})

    cStimTriggerExistCodes: list = allWidgetCodes.get(f"{cWidget.widget_id}_cStimTriggerCodes", [])
    cStimTriggerExistCodes.extend(cStimTriggerCodes)
    allWidgetCodes.update({f"{cWidget.widget_id}_cStimTriggerCodes": cStimTriggerExistCodes})

    cUpdateDurExistCodes: list = allWidgetCodes.get(f"{cWidget.widget_id}_cUpdateDurCodes", [])
    cUpdateDurExistCodes.extend(cUpdateDurCodes)
    allWidgetCodes.update({f"{cWidget.widget_id}_cUpdateDurCodes": cUpdateDurExistCodes})

    cRespExistCodes: list = allWidgetCodes.get(f"{cWidget.widget_id}_cRespCodes", [])
    cRespExistCodes.extend(cRespCodes)
    allWidgetCodes.update({f"{cWidget.widget_id}_cRespCodes": cRespExistCodes})

    return allWidgetCodes


def makeCodes4SwitchWidget(cWidget, attributesSetDict, cLoopLevel, allWidgetCodes):
    if getWidgetType(cWidget) == Info.SWITCH:
        codeTypesList = ['_cStimCodes', '_cFlipCodes', '_cStimTriggerCodes', '_cUpdateDurCodes', '_cRespCodes']

        switchExp = cWidget.getSwitch()
        switchExp, *_ = getValueInContainRefExp(cWidget, switchExp, attributesSetDict)

        # cHeaderList = list()
        # printAutoInd(cHeaderList, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        # printAutoInd(cHeaderList, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
        #              getWidgetName(cWidget.widget_id))
        # printAutoInd(cHeaderList, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

        # cases: list = [{'Case Value': '',
        #  'Id Pool': {'Image': 'Image.0', 'Video': '', 'Text': '', 'Sound': '', 'Slider': ''},
        #  'Sub Wid': 'Image.0', 'Stim Type': 'Image', 'Event Name': 'U_Image_6574'},]
        cases = cWidget.getCases()
        otherwiseExp = cases[-1]

        cases = cases[0:-1]

        for cCase in cases:
            if cCase['Case Value']:
                cCaseValueExp, *_ = getValueInContainRefExp(cWidget, cCase['Case Value'], attributesSetDict)
                cCase.update({'Case Value': cCaseValueExp})

        for cCodeType in codeTypesList:
            cTypeCodes = list()
            # print out the frame header
            # if getWidgetPos(cWidget.widget_id) == 0 and cCodeType == '_cStimCodes':
                # cTypeCodes.extend(cHeaderList)

            # if getWidgetPos(cWidget.widget_id) > 0 and cCodeType == '_cFlipCodes':
                # cTypeCodes.extend(cHeaderList)

            printAutoInd(cTypeCodes, "switch {0}", switchExp)

            for cCase in cases:
                printAutoInd(cTypeCodes, "case {0}", cCase['Case Value'])

                if cCase['Sub Wid']:
                    cTypeCodes.extend(allWidgetCodes[f"{cCase['Sub Wid']}{cCodeType}"])
                else:
                    printAutoInd(cTypeCodes, "% do nothing")

            if otherwiseExp['Sub Wid']:
                printAutoInd(cTypeCodes, "otherwise")
                cTypeCodes.extend(allWidgetCodes[f"{otherwiseExp['Sub Wid']}{cCodeType}"])

            printAutoInd(cTypeCodes, "end%switch ")

            allWidgetCodes.update({f"{cWidget.widget_id}{cCodeType}": cTypeCodes})

    return allWidgetCodes


def makeCodes4IfWidget(cWidget, attributesSetDict,cLoopLevel ,allWidgetCodes):
    if getWidgetType(cWidget) == Info.IF:
        condStr = cWidget.getCondition()
        condStr, *_ = getValueInContainRefExp(cWidget, condStr, attributesSetDict)

        codeTypesList = ['_cStimCodes', '_cFlipCodes', '_cStimTriggerCodes', '_cUpdateDurCodes', '_cRespCodes']

        trueWidget = cWidget.getTrueWidget()
        falseWidget = cWidget.getFalseWidget()

        # if getWidgetPos(cWidget.widget_id) > 0 and not (isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
        # generate Event Header

        # cHeaderList = list()
        # printAutoInd(cHeaderList, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        # printAutoInd(cHeaderList, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
        #              getWidgetName(cWidget.widget_id))
        # printAutoInd(cHeaderList, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')


        for cCodeType in codeTypesList:
            cTypeCodes = list()

            # if getWidgetPos(cWidget.widget_id) == 0 and cCodeType == '_cStimCodes':
                # cTypeCodes.extend(cHeaderList)

            # if getWidgetPos(cWidget.widget_id) > 0 and cCodeType == '_cFlipCodes':
                # cTypeCodes.extend(cHeaderList)

            cTypeCodes.extend([f"% {Func.getWidgetName(cWidget.widget_id)}{cCodeType}"])

            trueWidgetCodesList = list()
            falseWidgetCodesList = list()

            if trueWidget:
                trueWidgetCodesList = allWidgetCodes[f"{trueWidget.widget_id}{cCodeType}"]

            if falseWidget:
                falseWidgetCodesList = allWidgetCodes[f"{falseWidget.widget_id}{cCodeType}"]


            if len(trueWidgetCodesList)>0:
                printAutoInd(cTypeCodes, "if {0}", condStr)
                cTypeCodes.extend(trueWidgetCodesList)

                if len(falseWidgetCodesList) > 0:
                    printAutoInd(cTypeCodes, "else")
            else:
                if len(falseWidgetCodesList) > 0:
                    printAutoInd(cTypeCodes, "if ~{0}", condStr)


            if len(falseWidgetCodesList) > 0:
                cTypeCodes.extend(falseWidgetCodesList)

            if len(trueWidgetCodesList) + len(falseWidgetCodesList)> 0:
                printAutoInd(cTypeCodes, "end ")


            allWidgetCodes.update({f"{cWidget.widget_id}{cCodeType}": cTypeCodes})

    return allWidgetCodes


def printGeneratedCodes(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    # print comments to indicate the current frame order
    cHeaderList = list()
    printAutoInd(cHeaderList, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    printAutoInd(cHeaderList, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
                 getWidgetName(cWidget.widget_id))
    printAutoInd(cHeaderList, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # ====================
    # PRINT ALL CODES
    # ===================
    preStimWId = getPreStimWID(cWidget.widget_id)

    printPreRespCodesFirst = False

    if getWidgetType(cWidget) == Info.SWITCH:
        # switch expression
        _, _, referObNameList = getValueInContainRefExp(cWidget, cWidget.getSwitch(), attributesSetDict)

        # case values
        for cCaseDict in cWidget.getCases():
            cCaseValueStr = cCaseDict['Case Value']
            if len(cCaseValueStr) > 0:
                _, _, cValueReferObNameList = getValueInContainRefExp(cWidget, cCaseValueStr, attributesSetDict)
                referObNameList.extend(cValueReferObNameList)

        if preStimWId and Func.getWidgetName(preStimWId) in referObNameList:
            printPreRespCodesFirst = True

    elif getWidgetType(cWidget) == Info.IF:
        condStr = cWidget.getCondition()

        condStr, haveRef, referObNameList = getValueInContainRefExp(cWidget, condStr, attributesSetDict)

        # trueWidget = cWidget.getTrueWidget()
        # falseWidget = cWidget.getFalseWidget()

        if preStimWId and Func.getWidgetName(preStimWId) in referObNameList:
            printPreRespCodesFirst = True

    # todo to be continued ...

    if getWidgetPos(cWidget.widget_id) == 0:
        printPreRespCodesFirst = True


    if printPreRespCodesFirst or len(allWidgetCodes.get(f"{preStimWId}_cRespCodes",[])) == 0:
        # draw previous widget's resp code first
        # step 2: print response codes of the previous widget if possible
        printInAllWidgetCodesByKey(f, allWidgetCodes, f"{preStimWId}_cRespCodes")

        printOutList(f,cHeaderList)
        # step 1: print stim codes of the current widget
        printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cStimCodes")
    else:
        # step 1: print stim codes of the current widget
        printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cStimCodes")

        if preStimWId:
            # step 2: print response codes of the previous widget if possible
            printInAllWidgetCodesByKey(f, allWidgetCodes, f"{preStimWId}_cRespCodes")

        printOutList(f, cHeaderList)

    # step 3: print flip codes of the current widget
    printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cFlipCodes")
    # step 4: print stim trigger codes of the current widget if possible
    printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cStimTriggerCodes")
    # step 5: print stim update duration codes of the current widget if possible
    printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cUpdateDurCodes")

    #  if the last stim widget print the resp codes here
    if isLastStimWidgetInTL(cWidget.widget_id):
        printInAllWidgetCodesByKey(f, allWidgetCodes, f"{cWidget.widget_id}_cRespCodes")

    return allWidgetCodes


def printStimWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    # step 1: generate all codes (stim, flip ,send stim trigger, update cDurs, response check)
    allWidgetCodes = genStimWidgetAllCodes(cWidget, attributesSetDict, cLoopLevel, allWidgetCodes)

    # step 2: print out the generated codes
    allWidgetCodes = printGeneratedCodes(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)

    return allWidgetCodes


def genUpdateWidgetDur(cWidget, f, attributesSetDict, allWidgetCodes, nextEventFlipReqTimeStr='nextEvFlipReqTime'):
    global outputDevNameIdxDict, historyPropDict

    # get screen index
    _, cWinIdx, _ = getScreenInfo(cWidget, attributesSetDict)

    # Step 1: get the current screen duration that determined by the next flip
    # after drawing the next widget's stimuli, get the duration first
    durStr, isRefValue, cRefValueSet = getRefValueSet(cWidget, cWidget.getDuration(), attributesSetDict)
    durStr = parseDurationStr(durStr)

    # updated the screen flip times in matlab
    # printAutoInd(f, "%%%")
    printAutoInd(f, "% get cDur and the next event flip time")
    # printAutoInd(f, "%%%")
    if Func.isWidgetType(cWidget.widget_id, Info.SOUND):
        if re.fullmatch(r"\d+,\d+", durStr):
            printAutoInd(f, "cDurs(:)          = getDurValue([{0}],winIFIs({1}), true);", durStr, cWinIdx)
        else:
            printAutoInd(f, "cDurs(:)          = getDurValue({0},winIFIs({1}), true);", durStr, cWinIdx)
    else:
        if re.fullmatch(r"\d+,\d+", durStr):
            printAutoInd(f, "cDurs({0})          = getDurValue([{1}],winIFIs({0}));", cWinIdx, durStr)
        else:
            printAutoInd(f, "cDurs({0})          = getDurValue({1},winIFIs({0}));", cWinIdx, durStr)

    # printAutoInd(f, "(not the real flip time) ")
    printAutoInd(f, "{0} = cDurs({1}) + lastScrOnsettime({1}) - flipComShiftDur({1}); "
                    "% get the required time of the  Flip for the next event \n",
                 nextEventFlipReqTimeStr, cWinIdx)

    return allWidgetCodes  # O for successful


def genStimTriggers(cWidget, f, cLoopLevel, attributesSetDict, allWidgetCodes):
    global outputDevNameIdxDict, historyPropDict

    # if is a video related widget, will do this within flip loop
    # if isVideoRelatedWidget(cWidget):
    #     return allWidgetCodes

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"
    cWidgetName = getWidgetName(cWidget.widget_id)
    cWidgetType = getWidgetType(cWidget)

    # get screen index
    _, cWinIdx, _ = getScreenInfo(cWidget, attributesSetDict)

    # ---------------------------------------------------------------------------------------
    # Step 1: print out previous widget's codes that suppose to be print just after the Flip
    # ----------------------------------------------------------------------------------------
    for cRowStr in allWidgetCodes['codesAfFip']:
        printAutoInd(f, cRowStr)
    # clear out the print buffer
    allWidgetCodes.update({'codesAfFip': []})

    # ------------------------------------------------------------
    # Step 2: send output triggers and messages
    # ------------------------------------------------------------

    output_device = cWidget.getOutputDevice()
    if len(output_device) > 0:
        printAutoInd(f, "% -- send output trigger and msg: --/")

    # initializing the outDevices that could be used to store the outDev info
    cOutDeviceDict = dict()

    for device, properties in output_device.items():
        msgValue = dataStrConvert(*getRefValue(cWidget, properties['Value Or Msg'], attributesSetDict), True)
        pulseDur = dataStrConvert(*getRefValue(cWidget, properties['Pulse Duration'], attributesSetDict), False)

        cDevName = properties.get("Device Name", "")
        devType = properties.get("Device Type", "")

        if devType == Info.DEV_PARALLEL_PORT:
            # currently only ppl need to be reset to zero
            # cOutDeviceDict[cDevName] = ['1', pulseDur, re.split('(\(\d*\))', outputDevNameIdxDict.get(cDevName))[1][1:-1]]
            cOutDeviceDict[cDevName] = ['1', pulseDur, outputDevNameIdxDict.get(cDevName)]
            # cOutDeviceDict[cDevName] = [devType,pulseDur, parallelPortNumInMatlab]
            if Info.PLATFORM == 'linux':
                printAutoInd(f, "lptoutMex({0},{1});", outputDevNameIdxDict.get(cDevName), msgValue)
            elif Info.PLATFORM == 'windows':
                printAutoInd(f, "io64(io64Obj,{0},{1});", outputDevNameIdxDict.get(cDevName), msgValue)
            elif Info.PLATFORM == 'mac':
                printAutoInd(f, "% currently, under Mac OX we just do nothing for parallel ports")

            # printAutoInd(f, "isParallelOn = true; ")
        # outputDevNameIdxDict.update({cDevice['Device Name']: f"tcpipCons({iNetPort})"})
        elif devType == Info.DEV_NETWORK_PORT:
            printAutoInd(f, "pnet({0},'write',{1});", outputDevNameIdxDict.get(cDevName), msgValue)
            # cOutDeviceDict[cDevName] = ['2', pulseDur, re.split('(\(\d*\))', outputDevNameIdxDict.get(cDevName))[1][1:-1]]
            cOutDeviceDict[cDevName] = ['2', pulseDur, outputDevNameIdxDict.get(cDevName)]

        elif devType == Info.DEV_SERIAL_PORT:
            printAutoInd(f, "[ign, when] = IOPort('Write', {0}, {1});", outputDevNameIdxDict.get(cDevName), msgValue)
            # cOutDeviceDict[cDevName] = ['3', pulseDur, re.split('(\(\d*\))', outputDevNameIdxDict.get(cDevName))[1][1:-1]]
            cOutDeviceDict[cDevName] = ['3', pulseDur, outputDevNameIdxDict.get(cDevName)]

        # printAutoInd(f, "sendTriggerOrMsg({0},{1},{2});", cOutDeviceDict[cDevName][0], cOutDeviceDict[cDevName][2],
        #              msgValue)

    historyPropDict.update({'cOutDevices': cOutDeviceDict})

    if len(output_device) > 0:
        printAutoInd(f, "{0}.msgEndTime({1}) = GetSecs;", cWidgetName, cOpRowIdxStr)
        printAutoInd(f, "% ----------------------------------\\\n")

    # print out event onset marker for eyelink
    if allWidgetCodes.get('isEyeLinkStartRecord'):
        printAutoInd(f, "Eyelink('Message', '{0}_onsettime');", cWidgetName)

    # updated the screen flip times in matlab
    if Info.SOUND == cWidgetType:
        printAutoInd(f, "% for event type of sound, make it to all lastScrOnsetime")
        printAutoInd(f, "lastScrOnsettime(:) = {0}.onsettime({1}); % temp save the last screen onsettimes\n",
                     getWidgetName(cWidget.widget_id),
                     cOpRowIdxStr)
    else:
        printAutoInd(f, "lastScrOnsettime({0}) = {1}.onsettime({2}); %temp save the last screen onsettimes\n",
                     cWinIdx,
                     getWidgetName(cWidget.widget_id),
                     cOpRowIdxStr)

    return allWidgetCodes


def printTimelineWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes) -> dict:
    global cInfoDict, isDummyPrint

    cTimelineWidgetIds = getWidgetIDInTimeline(cWidget.widget_id)

    for cWidgetId in cTimelineWidgetIds:
        cWidget = Info.WID_WIDGET[cWidgetId]

        # for dummyPrint get the last widget id and loopNum
        if isDummyPrint:
            cInfoDict.update({'lastWidgetId': cWidgetId})

        cWidgetType = getWidgetType(cWidget)

        if Info.LOOP == cWidgetType:
            allWidgetCodes = printCycleWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)
        elif cWidgetType in [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO, Info.IF, Info.SWITCH]:
            allWidgetCodes = printStimWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)
        elif Info.DC == cWidgetType:
            allWidgetCodes = printETDcCorrectWidget(cWidget, f, allWidgetCodes)
        elif Info.CALIBRATION == cWidgetType:
            allWidgetCodes = printETCalibWidget(cWidget, f, allWidgetCodes)
        elif Info.STARTR == cWidgetType:
            allWidgetCodes = printETStartRWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)
        elif Info.ENDR == cWidgetType:
            allWidgetCodes = printETEndRWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)
        elif Info.LOG == cWidgetType:
            allWidgetCodes = printETLogWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes)
        elif Info.QUEST_UPDATE == cWidgetType:
            allWidgetCodes = printQuestUpdateWidget(cWidget, f, attributesSetDict, allWidgetCodes, cLoopLevel)
    return allWidgetCodes


def printETLogWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    cProperties = Func.getWidgetProperties(cWidget.widget_id)

    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    printAutoInd(f, '%eyetracker: logging variables')

    shouldNotBeCitationCheck('Pause between messages', cWidget.getPauseBetweenMessages())

    usedAttributesList = cProperties.get('Used Variables', [])

    printAutoInd(f, "Eyelink('Message', '!V TRIAL_VAR index %s', {0});", cOpRowIdxStr)

    if len(usedAttributesList) > 0:

        varValueStrList = []

        for varName in usedAttributesList:
            varValueStr, _ = getRefValue(cWidget, addSquBrackets(varName), attributesSetDict)
            varValueStrList.append(varValueStr)

        bePrintLogVarStr = "{" + "".join(f"'{varName}'," for varName in usedAttributesList)[0:-1] + "}"
        bePrintLogVarValueStr = "{" + "".join(f"{varName}," for varName in varValueStrList)[0:-1] + "}"

        printAutoInd(f, "logVarNames  = {0};", bePrintLogVarStr)
        printAutoInd(f, "logVarValues = {0};", bePrintLogVarValueStr)
        printAutoInd(f, "eyelinkLog(logVarNames, logVarValues, {0});", float(cWidget.getPauseBetweenMessages()) / 1000)
    '''
        to be continue ...
    '''
    printAutoInd(f, "Eyelink('Message', 'TRIAL_RESULT 0');\n\n")

    return allWidgetCodes


def printQuestUpdateWidget(cWidget, f, attributesSetDict, allWidgetCodes, cLoopLevel):
    global outputDevNameIdxDict
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    cProperties = Func.getWidgetProperties(cWidget.widget_id)

    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    shouldNotBeCitationCheck('Quest Name', cProperties['Quest Name'])

    cQuestName, isRef = getRefValue(cWidget, cProperties['Quest Name'], attributesSetDict)

    respVarStr, isRef = getRefValue(cWidget, cProperties['Is Correct'], attributesSetDict)

    respVarStr = parseBooleanStr(respVarStr, isRef)

    cQuestIdx = outputDevNameIdxDict.get('quest-' + cQuestName)

    printAutoInd(f, "% update {0}: quest({1})", cQuestName, cQuestIdx)

    if cQuestName == "quest_rand":
        printAutoInd(f, "quest({0}) = updateQuestValue(quest({0}),quest({0}).cValue,response);",
                     f"randQuestIds({cOpRowIdxStr})", respVarStr)
        printAutoInd(f, "quest({0}) = getQuestValue(quest({0})); % get the new cValue", f"randQuestIds({cOpRowIdxStr})")

    else:
        printAutoInd(f, "quest({0}) = updateQuestValue(quest({0}),quest({0}).cValue,response);", cQuestIdx, respVarStr)
        printAutoInd(f, "quest({0}) = getQuestValue(quest({0})); % get the new cValue", cQuestIdx)

    printAutoInd(f, "\n")

    return allWidgetCodes


def printETDcCorrectWidget(cWidget, f, allWidgetCodes):
    # cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    # cProperties = Func.getWidgetProperties(cWidget.widget_id)
    allWidgetCodes.update({"isEyeLinkStartRecord": True})
    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    nextWidgetId = getNextWID(cWidget.widget_id)

    printAutoInd(f, "EyelinkDoDriftCorrection(el);% do drift correction")

    if nextWidgetId and Func.isWidgetType(nextWidgetId, Info.STARTR):
        printAutoInd(f, "% start recording eye position (preceded by a short pause so that")
        printAutoInd(f, "% the tracker can finish the mode transition)")
        printAutoInd(f, "WaitSecs(0.05);")
    # printAutoInd(f, "Eyelink('Command', 'set_idle_mode');")
    printAutoInd(f, " ")

    return allWidgetCodes


def printETCalibWidget(cWidget, f, allWidgetCodes):
    # cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    # cProperties = Func.getWidgetProperties(cWidget.widget_id)

    allWidgetCodes.update({"isEyeLinkStartRecord": True})
    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    # if preStimWid:
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    printAutoInd(f, "EyelinkDoTrackerSetup(el); % eyelink setup: adjust the camera,calibration and validation")

    return allWidgetCodes


def printETStartRWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    # cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    # cProperties = Func.getWidgetProperties(cWidget.widget_id)

    allWidgetCodes.update({"isEyeLinkStartRecord": True})
    cCodesForResp = allWidgetCodes.get('respCodes', [])

    if len(cCodesForResp) > 0:
        haveRespCodes = True
    else:
        haveRespCodes = False

    cLoopStr = f"iLoop_{cLoopLevel}"

    cMessageStr = cWidget.getStatusMessage()

    if len(cMessageStr) == 0:
        cMessageStr = "''"

    printAutoInd(f, '%--- Eye tracker: start to record ---/')
    printAutoInd(f, "% Sending a 'TRIALID' message to mark the start of a trial in Data Viewer")
    if haveRespCodes:
        printAutoInd(f, "sendStartRecordComTime = GetSecs;")
    printAutoInd(f, "Eyelink('Message','TRIALID %d',{0});", cLoopStr)

    printAutoInd(f, "% This status message will be displayed at the bottom of the eyetracker display")
    printAutoInd(f, "Eyelink('Command','record_status_message \"TRIAL\" %d: %s',{0},{1});", cLoopStr,cMessageStr)
    printAutoInd(f, "Eyelink('StartRecording');")
    printAutoInd(f, '%-----------------------------------\\\n')

    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    printAutoInd(f, "% record a few samples before we actually start displaying")
    printAutoInd(f, "% otherwise you may lose a few msec of data")

    if haveRespCodes:
        printAutoInd(f, "if GetSecs < sendStartRecordComTime + 0.1")
        printAutoInd(f, "WaitSecs('UntilTime', sendStartRecordComTime + 0.1);")
        printAutoInd(f, "end")
    else:
        printAutoInd(f, "WaitSecs(0.1);")

    printAutoInd(f, "% mark zero-plot time in data file")
    printAutoInd(f, "Eyelink('message', 'SYNCTIME');\n")

    return allWidgetCodes


def printETEndRWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes):
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    cProperties = Func.getWidgetProperties(cWidget.widget_id)

    allWidgetCodes.update({"isEyeLinkStartRecord": False})

    # print previous widget's response code
    preStimWid = getPreStimWID(cWidget.widget_id)
    allWidgetCodes = printInAllWidgetCodesByKey(f, allWidgetCodes, f'{preStimWid}_respCodes')

    printAutoInd(f, '%- eyetracker: stoprecord ---/')
    printAutoInd(f, "Eyelink('StopRecording');")
    printAutoInd(f, '%----------------------------\\\n')

    return allWidgetCodes


def drawSliderWidget(cWidget, sliderStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes):
    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint, haveGaborStim, haveSnowStim

    cVSLCodes = allWidgetCodes.get('forVideoSliderLoopCodes', [])
    beClosedTxAFCycleList = allWidgetCodes.get(f"beClosedTextures_{cLoopLevel}", [])

    iVideoNum = 1
    # print(os.path.abspath(__file__))

    # if getWidgetPos(cWidget.widget_id) == 0  and not(isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
    #     # Step 2: print out help info for the current widget
    #     printAutoInd(sliderStimCodes, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     printAutoInd(sliderStimCodes, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
    #                  getWidgetName(cWidget.widget_id))
    #     printAutoInd(sliderStimCodes, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    cSliderProperties = Func.getWidgetProperties(cWidget.widget_id)
    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)
    # ------------------------------------------------
    # Step 2: draw eachItem
    # -------------------------------------------------
    cItems = cSliderProperties['Items']

    cCloseIdxesStr = ""
    # zVlaues = [value['z'] for value in cItems.values()]
    # the items were already sorted in descend order
    itemIds = getSliderItemIds(cWidget)
    itemIds.reverse()  # reverse the key id order
    # itemIds = itemIds[-1::-1] # reverse the key id order in ascend
    printAutoInd(sliderStimCodes, "% prepare audio materials for widget {0}", getWidgetName(cWidget.widget_id))
    if isContainItemType(itemIds, Info.ITEM_SOUND):
        printAutoInd(sliderStimCodes,
                     "predictedVisOnset = PredictVisualOnsetForTime({0}, cDurs({1}) + lastScrOnsettime({1}) - flipComShiftDur({1}));",
                     cWinStr, cWinIdx)
    # loop twice, once for audio and once for all visual stimuli
    iSoundSlave = 1

    for cItemId in itemIds:
        cItemProperties = cItems[cItemId]

        if getItemType(cItemId) == Info.ITEM_SOUND:
            printAutoInd(sliderStimCodes, "% create item: {0} in {1}", cItemId, getWidgetName(cWidget.widget_id))
            if iSoundSlave == 1:
                printAutoInd(sliderStimCodes,
                             "% schedule start of audio at exactly the predicted time of the next flip")

            allWidgetCodes = drawSoundWidget(cWidget, sliderStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes,
                                             cItemProperties, iSoundSlave)
            iSoundSlave += 1
        else:
            pass
    # remove sound items
    itemIds = [cItemId for cItemId in itemIds if getItemType(cItemId) != Info.ITEM_SOUND]
    '''
    loop to handle all visual stimuli
    '''
    cWidgetName = getWidgetName(cWidget.widget_id)

    printAutoInd(cVSLCodes, "% draw item {0} in {1}", itemIds, cWidgetName)

    for cItemId in itemIds:
        cItems = cSliderProperties['Items']
        cItemType = getItemType(cItemId)
        cItemProperties = cItems[cItemId]
        isItemRef = False

        if cItemType in [Info.ITEM_GABOR, Info.ITEM_IMAGE, Info.ITEM_SNOW, Info.ITEM_TEXT, Info.ITEM_VIDEO]:
            printAutoInd(sliderStimCodes, "% prepare materials for item {0} in {1}", cItemId, cWidgetName)

        # printAutoInd(cVSLCodes, "% draw item {0} in {1}", cItemId, cWidgetName)

        cItemId = cWidgetName + '_' + cItemId

        if cItemType == Info.ITEM_LINE:
            borderColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Color'], attributesSetDict))
            lineWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Width'], attributesSetDict))
            cX1 = dataStrConvert(*getRefValue(cWidget, cItemProperties['X1'], attributesSetDict))
            cY1 = dataStrConvert(*getRefValue(cWidget, cItemProperties['Y1'], attributesSetDict))
            cX2 = dataStrConvert(*getRefValue(cWidget, cItemProperties['X2'], attributesSetDict))
            cY2 = dataStrConvert(*getRefValue(cWidget, cItemProperties['Y2'], attributesSetDict))

            printAutoInd(cVSLCodes, "Screen('DrawLine', {0}, {1}, {2}, {3}, {4}, {5}, {6});", cWinStr, borderColor, cX1,
                         cY1, cX2, cY2, lineWidth)

        if cItemType == Info.ITEM_RECT:

            centerX = dataStrConvert(*getRefValue(cWidget, cItemProperties['Center X'], attributesSetDict))
            centerY = dataStrConvert(*getRefValue(cWidget, cItemProperties['Center Y'], attributesSetDict))
            cWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Width'], attributesSetDict))
            cHeight = dataStrConvert(*getRefValue(cWidget, cItemProperties['Height'], attributesSetDict))
            lineWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Width'], attributesSetDict))

            fillColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Fill Color'], attributesSetDict))
            borderColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Color'], attributesSetDict))

            if fillColor == "[0,0,0,0]":
                printAutoInd(cVSLCodes,
                             "Screen('FrameRect' ,{0} ,{1} ,CenterRectOnPoint([0,0,{2},{3}], {4}, {5}) ,{6});", cWinStr,
                             borderColor, cWidth, cHeight, centerX, centerY, lineWidth)
            elif lineWidth == '0' or fillColor == borderColor:
                printAutoInd(cVSLCodes, "Screen('FillRect',{0} ,{1}, CenterRectOnPoint([0,0,{2},{3}], {4}, {5}));",
                             cWinStr, fillColor, cWidth, cHeight, centerX, centerY)
            else:
                printAutoInd(sliderStimCodes, "{0}cRect = CenterRectOnPoint([0, 0, {1}, {2}], {3}, {4});", cItemId,
                             cWidth, cHeight,
                             centerX, centerY)
                printAutoInd(cVSLCodes, "Screen('FillRect' ,{0} ,{1} ,{2}cRect);", cWinStr, fillColor, cItemId)
                printAutoInd(cVSLCodes, "Screen('FrameRect' ,{0} ,{1} ,{2}cRect ,{3});", cWinStr, borderColor, cItemId,
                             lineWidth)

        elif cItemType == Info.ITEM_CIRCLE:
            centerX = dataStrConvert(*getRefValue(cWidget, cItemProperties['Center X'], attributesSetDict))
            centerY = dataStrConvert(*getRefValue(cWidget, cItemProperties['Center Y'], attributesSetDict))
            cWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Width'], attributesSetDict))
            cHeight = dataStrConvert(*getRefValue(cWidget, cItemProperties['Height'], attributesSetDict))
            lineWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Width'], attributesSetDict))

            fillColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Fill Color'], attributesSetDict))
            borderColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Color'], attributesSetDict))

            if fillColor == "[0,0,0,0]":
                printAutoInd(cVSLCodes,
                             "Screen('FrameOval', {0}, {1}, CenterRectOnPoint([0, 0, {2}, {3}], {4}, {5}) ,{6}, {6});",
                             cWinStr, borderColor, cWidth, cHeight, centerX, centerY, lineWidth)
            elif lineWidth == '0' or fillColor == borderColor:
                printAutoInd(cVSLCodes, "Screen('FillOval', {0}, {1}, CenterRectOnPoint([0, 0, {2}, {3}], {4}, {5}));",
                             cWinStr, fillColor, cWidth, cHeight, centerX, centerY)
            else:
                printAutoInd(sliderStimCodes, "{0}cRect = CenterRectOnPoint([0, 0, {1}, {2}], {3}, {4});", cItemId,
                             cWidth, cHeight,
                             centerX, centerY)
                printAutoInd(cVSLCodes, "Screen('FillOval',{0}, {1}, {2}cRect);", cWinStr, fillColor, cItemId)
                printAutoInd(cVSLCodes, "Screen('FrameOval',{0}, {1}, {2}cRect, {3}, {3});", cWinStr, borderColor,
                             cItemId, lineWidth)

        elif cItemType == Info.ITEM_POLYGON:
            lineWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Width'], attributesSetDict))

            fillColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Fill Color'], attributesSetDict))
            borderColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Color'], attributesSetDict))

            points = cItemProperties['Points']
            parsedPoints = []
            for cXY in points:
                cX = getRefValue(cWidget, cXY[0], attributesSetDict)
                cY = getRefValue(cWidget, cXY[1], attributesSetDict)

                parsedPoints.append([cX[0], cY[0]])

            pointListStr = "".join(cXY[0] + "," + cXY[1] + ";" for cXY in parsedPoints)
            pointListStr = addSquBrackets(pointListStr[0:-1])

            if fillColor == "[0,0,0,0]":
                printAutoInd(cVSLCodes, "Screen('FramePoly', {0}, {1}, {2}, {3});", cWinStr, borderColor, pointListStr,
                             lineWidth)
            elif lineWidth == '0' or fillColor == borderColor:
                printAutoInd(cVSLCodes, "Screen('FillPoly', {0}, {1}, {2});", cWinStr, fillColor, pointListStr)
            else:
                printAutoInd(sliderStimCodes, "{0}cPointList = {1};", cItemId, pointListStr)
                printAutoInd(cVSLCodes, "Screen('FillPoly', {0}, {1}, {2}cPointList);", cWinStr, fillColor, cItemId)
                printAutoInd(cVSLCodes, "Screen('FramePoly', {0}, {1}, {2}cPointList, {3}, {3});", cWinStr, borderColor,
                             cItemId, lineWidth)

        elif cItemType == Info.ITEM_ARC:
            centerX = dataStrConvert(*getRefValue(cWidget, cItemProperties['Center X'], attributesSetDict))
            centerY = dataStrConvert(*getRefValue(cWidget, cItemProperties['Center Y'], attributesSetDict))
            cWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Width'], attributesSetDict))
            cHeight = dataStrConvert(*getRefValue(cWidget, cItemProperties['Height'], attributesSetDict))
            lineWidth = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Width'], attributesSetDict))

            fillColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Fill Color'], attributesSetDict))
            borderColor = dataStrConvert(*getRefValue(cWidget, cItemProperties['Border Color'], attributesSetDict))

            angleStart = dataStrConvert(*getRefValue(cWidget, cItemProperties['Angle Start'], attributesSetDict))
            angleLength = dataStrConvert(*getRefValue(cWidget, cItemProperties['Angle Length'], attributesSetDict))

            if fillColor == "[0,0,0,0]":
                printAutoInd(cVSLCodes,
                             "Screen('FrameArc', {0}, {1}, CenterRectOnPoint([0, 0, {2}, {3}], {4}, {5}), {6}, {7} ,{8}, {8});",
                             cWinStr, borderColor, cWidth, cHeight, centerX, centerY, angleStart, angleLength,
                             lineWidth)
            elif lineWidth == '0' or fillColor == borderColor:
                printAutoInd(cVSLCodes,
                             "Screen('FillArc', {0}, {1}, CenterRectOnPoint([0, 0, {2}, {3}], {4}, {5}), {6}, {7});",
                             cWinStr,
                             fillColor, cWidth, cHeight, centerX, centerY, angleStart, angleLength)
            else:
                printAutoInd(sliderStimCodes, "{0}cRect = CenterRectOnPoint([0, 0, {1}, {2}], {3}, {4});", cItemId,
                             cWidth, cHeight,
                             centerX, centerY)
                printAutoInd(cVSLCodes, "Screen('FillArc', {0}, {1}, {2}cRect, {3}, {4});", cWinStr, fillColor, cItemId,
                             angleStart, angleLength)
                printAutoInd(cVSLCodes, "Screen('FrameArc', {0}, {1}, {2}cRect, {3}, {4}, {5}, {5});", cWinStr,
                             borderColor, cItemId, angleStart, angleLength, lineWidth)

        elif cItemType == 'gabor':
            centerX, isCenterXRef = getRefValue(cWidget, cItemProperties['Center X'], attributesSetDict)
            centerX = dataStrConvert(centerX, isCenterXRef)

            centerY, isCenterYRef = getRefValue(cWidget, cItemProperties['Center Y'], attributesSetDict)
            centerY = dataStrConvert(centerY, isCenterYRef)

            cWidth, isWidthRef = getRefValue(cWidget, cItemProperties['Width'], attributesSetDict)
            cWidth = dataStrConvert(cWidth, isWidthRef)

            cHeight, isHeightRef = getRefValue(cWidget, cItemProperties['Height'], attributesSetDict)
            cHeight = dataStrConvert(cHeight, isHeightRef)

            cSpatialFreq, isSpatialFreqRef = getRefValue(cWidget, cItemProperties['Spatial'], attributesSetDict)
            cSpatialFreq = dataStrConvert(cSpatialFreq, isSpatialFreqRef)

            cContrast, isContrastRef = getRefValue(cWidget, cItemProperties['Contrast'], attributesSetDict)
            cContrast = dataStrConvert(cContrast, isContrastRef)

            cPhase, isPhaseRef = getRefValue(cWidget, cItemProperties['Phase'], attributesSetDict)
            cPhase = dataStrConvert(cPhase, isPhaseRef)

            cOrientation, isOrientationRef = getRefValue(cWidget, cItemProperties['Orientation'], attributesSetDict)
            cOrientation = dataStrConvert(cOrientation, isOrientationRef)

            cRotation, isRotationRef = getRefValue(cWidget, cItemProperties['Rotation'], attributesSetDict)
            cRotation = dataStrConvert(cRotation, isRotationRef)

            cSDx, isSDxRef = getRefValue(cWidget, cItemProperties['SDx'], attributesSetDict)
            cSDx = dataStrConvert(cSDx, isSDxRef)

            cSDy, isSDyRef = getRefValue(cWidget, cItemProperties['SDy'], attributesSetDict)
            cSDy = dataStrConvert(cSDy, isSDyRef)

            cBackColor, isBkColorRef = getRefValue(cWidget, cItemProperties['Back Color'], attributesSetDict)
            cBackColor = dataStrConvert(cBackColor, isBkColorRef)

            cTransparency = dataStrConvert(*getRefValue(cWidget, cItemProperties['Transparency'], attributesSetDict))

            isItemRef = isCenterYRef + isCenterXRef + isWidthRef + isHeightRef + isSpatialFreqRef + isContrastRef + isPhaseRef + isOrientationRef + isRotationRef + isSDxRef + isSDyRef + isBkColorRef

            if isItemRef == 0 and cLoopLevel > 0:
                # if its not ref and should be under cycling
                printAutoInd(sliderStimCodes, "if ~exist('{0}_Mx','var')", cItemId)
                printAutoInd(sliderStimCodes, "{0}_Mx  = makeGabor_bcl({1}, {2}, {3}, {4}, {5}, [{6},{7}], {8}, {9});",
                             cItemId,
                             cSpatialFreq,
                             cContrast, cPhase, cOrientation, cBackColor, cWidth, cHeight, cSDx, cSDy)
                printAutoInd(sliderStimCodes, "{0}_idx = Screen('MakeTexture', {1}, {0}_Mx);", cItemId, cWinStr)
                printAutoInd(sliderStimCodes, "end ")

                beClosedTxAFCycleList.append(f"{cItemId}_idx")
            else:
                printAutoInd(sliderStimCodes, "{0}_Mx  = makeGabor_bcl({1}, {2}, {3}, {4}, {5}, [{6},{7}], {8}, {9});",
                             cItemId,
                             cSpatialFreq,
                             cContrast, cPhase, cOrientation, cBackColor, cWidth, cHeight, cSDx, cSDy)
                printAutoInd(sliderStimCodes, "{0}_idx = Screen('MakeTexture', {1}, {0}_Mx);", cItemId, cWinStr)

                cCloseIdxesStr += f"{cItemId}_idx, "

            printAutoInd(cVSLCodes,
                         "Screen('DrawTexture', {0}, {1}_idx, [], CenterRectOnPointd([0,0,size({1}_Mx,2),size({1}_Mx,1)], {2}, {3}), {4}, [], abs({5}) );",
                         cWinStr, cItemId, centerX, centerY,
                         cRotation,
                         cTransparency)

        elif cItemType == Info.ITEM_SNOW:
            centerX, isCenterXRef = getRefValue(cWidget, cItemProperties['Center X'], attributesSetDict)
            centerX = dataStrConvert(centerX, isCenterXRef)

            centerY, isCenterYRef = getRefValue(cWidget, cItemProperties['Center Y'], attributesSetDict)
            centerY = dataStrConvert(centerY, isCenterYRef)

            cWidth, isWidthRef = getRefValue(cWidget, cItemProperties['Width'], attributesSetDict)
            cWidth = dataStrConvert(cWidth, isWidthRef)

            cHeight, isHeightRef = getRefValue(cWidget, cItemProperties['Height'], attributesSetDict)
            cHeight = dataStrConvert(cHeight, isHeightRef)

            cScale, isScaleRef = getRefValue(cWidget, cItemProperties['Scale'], attributesSetDict)
            cScale = dataStrConvert(cScale, isScaleRef)

            isItemRef = isCenterXRef + isCenterYRef + isWidthRef + isHeightRef + isScaleRef

            cRotation = dataStrConvert(*getRefValue(cWidget, cItemProperties['Rotation'], attributesSetDict))

            cTransparency = dataStrConvert(*getRefValue(cWidget, cItemProperties['Transparency'], attributesSetDict))

            if isItemRef == 0 and cLoopLevel > 0:
                printAutoInd(sliderStimCodes, "if ~exist('{0}_Mx','var')", cItemId)
                printAutoInd(sliderStimCodes, "{0}_Mx  = makeSnow_bcl({1}, {2}, {3});", cItemId, cWidth, cHeight,
                             cScale)
                # printAutoInd(f, " stim = rand(round([stimHeigh, stimWidth]/scale)) * 255;")
                printAutoInd(sliderStimCodes, "{0}_idx = Screen('MakeTexture', {1}, {0}_Mx);", cItemId, cWinStr)
                printAutoInd(sliderStimCodes, "end")

                beClosedTxAFCycleList.append(f"{cItemId}_idx")
            else:
                printAutoInd(sliderStimCodes, "{0}_Mx  = makeSnow_bcl({1}, {2}, {3});", cItemId, cWidth, cHeight,
                             cScale)
                printAutoInd(sliderStimCodes, "{0}_idx = Screen('MakeTexture', {1}, {0}_Mx);", cItemId, cWinStr)
                # for possible to be closed textures
                cCloseIdxesStr += f"{cItemId}_idx, "

            printAutoInd(cVSLCodes,
                         "Screen('DrawTexture', {0}, {1}_idx, [], CenterRectOnPointd([0,0,{2},{3}], {4}, {5}), {6}, [], abs({7}));",
                         cWinStr, cItemId, cWidth, cHeight, centerX, centerY,
                         cRotation,
                         cTransparency)

        elif Info.ITEM_TEXT == cItemType:
            cVSLCodes = drawTextForSlider(cWidget, sliderStimCodes, attributesSetDict, cLoopLevel, cItemProperties,
                                          cVSLCodes)
        elif cItemType == Info.ITEM_VIDEO:
            allWidgetCodes, cVSLCodes = drawVideoWidget(cWidget, sliderStimCodes, attributesSetDict, cLoopLevel,
                                                        allWidgetCodes,
                                                        cItemProperties, cVSLCodes, iVideoNum)
            iVideoNum += 1

        elif cItemType == Info.ITEM_IMAGE:
            allWidgetCodes, cVSLCodes, isImFileNameRef = drawImageWidget(cWidget, sliderStimCodes, attributesSetDict,
                                                                         cLoopLevel,
                                                                         allWidgetCodes, cItemProperties,
                                                                         cVSLCodes)

            if isImFileNameRef or cLoopLevel == 0:
                cCloseIdxesStr += f"{cItemId}_idx, "

    # sortedZIdx = sorted(range(len(zVlaues)), key=zVlaues.__getitem__)

    if isVideoRelatedWidget(cWidget) is not True:
        clearAfter = getClearAfterInfo(cWidget, attributesSetDict)

        printAutoInd(sliderStimCodes, "Screen('DrawingFinished',{0},{1});", cWinStr, clearAfter)
        # printAutoInd(sliderStimCodes, "% check the 'esc' key to abort the exp")
        # printAutoInd(sliderStimCodes, "detectAbortKey(abortKeyCode);\n")

    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------

    if len(cCloseIdxesStr) > 0:
        cAfEndVideoFlipCodes = allWidgetCodes.get('codesAfEndVideoFip', [])
        cAfEndVideoFlipCodes.append(f"Screen('Close', [{cCloseIdxesStr[0:-2]}]);\n")
        allWidgetCodes.update({'codesAfEndVideoFip': cAfEndVideoFlipCodes})

    allWidgetCodes.update({'forVideoSliderLoopCodes': cVSLCodes})

    allWidgetCodes.update({'f"beClosedTextures_{cLoopLevel}"': beClosedTxAFCycleList})

    return allWidgetCodes


def drawSoundWidget(cWidget, soundStimCodes, attributesSetDict, cLoopLevel, allWidgetCodes, cProperties=None, iSlave=1):
    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint

    if cProperties is None:
        cProperties = []

    # cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num

    if len(cProperties) == 0:
        isNotInSlide = True
        cProperties = Func.getWidgetProperties(cWidget.widget_id)
    else:
        isNotInSlide = False

    # data and buffer prefixStr e.g., slider_1_sound_1_Dat
    if isNotInSlide:
        cPrefixStr = getWidgetName(cWidget.widget_id)
    else:
        cPrefixStr = getWidgetName(cWidget.widget_id) + '_' + cProperties['Name']

    # if getWidgetPos(cWidget.widget_id) == 0 and isNotInSlide and not(isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
    #     # Step 2: print out help info for the current widget
    #     printAutoInd(soundStimCodes, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     printAutoInd(soundStimCodes, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
    #                  getWidgetName(cWidget.widget_id))
    #     printAutoInd(soundStimCodes, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    # 2) handle file name:
    # cFilenameStr, isFileNameRef = getRefValue(cWidget, cProperties['File Name'], attributesSetDict)
    cFileNameStr = trans2relativePath(cProperties['File Name'])
    cFilenameStr, isFileNameRef, _ = getValueInContainRefExp(cWidget, cFileNameStr, attributesSetDict)

    cFilenameStr = genAppropriatePathSplitter(cFilenameStr, Info.PLATFORM == 'windows')


    # # 3) check the Buffer Size parameter:
    # bufferSizeStr, isRef = getRefValue(cWidget, cWidget.getBufferSize(), attributesSetDict)

    # 3) check the Stream Refill parameter:
    streamRefillStr, isRef = getRefValue(cWidget, cProperties['Stream Refill'], attributesSetDict)

    # 4) check the start offset in ms parameter:
    startOffsetStr, isRef = getRefValue(cWidget, cProperties['Start Offset'], attributesSetDict)

    # 5) check the stop offset in ms parameter:
    StopOffsetStr, isRef = getRefValue(cWidget, cProperties['Stop Offset'], attributesSetDict)

    # # 6) check the repetitions parameter:
    # repetitionsStr, isRef = getRefValue(cWidget, cWidget.getRepetitions(), attributesSetDict)

    # 7) check the volume control parameter:
    isVolumeControl, isRef = getRefValue(cWidget, cProperties['Volume Control'], attributesSetDict)

    # 8) check the volume parameter:
    volumeStr, isRef = getRefValue(cWidget, cProperties['Volume'], attributesSetDict)

    # 9) check the latencyBias control parameter:
    isLatencyBiasControl, isRef = getRefValue(cWidget, cProperties['Latency Bias'], attributesSetDict)

    # 10) check the volume parameter:
    latencyBiasStr, isRef = getRefValue(cWidget, cProperties['Bias Time'], attributesSetDict)

    # 11) check the sound device name parameter:
    shouldNotBeCitationCheck('Sound Device', cProperties['Sound Device'])
    cSoundDevName, isRef = getRefValue(cWidget, cProperties['Sound Device'], attributesSetDict)

    cSoundIdxStr = f"{outputDevNameIdxDict.get(cSoundDevName)}({iSlave})"

    # 12) check the volume parameter:
    waitForStartStr = parseBooleanStr(*getRefValue(cWidget, cProperties['Wait For Start'], attributesSetDict))

    # read audio file
    if isFileNameRef is False and cLoopLevel > 0:
        printAutoInd(soundStimCodes, "if ~exist({0}_Dat,'var')", cPrefixStr)
        printAutoInd(soundStimCodes, "{0}_Dat = audioread(fullfile(cFolder,{1}) );", cPrefixStr,
                     addSingleQuotes(cFilenameStr))
        # make audio buffer
        # printAutoInd(f, "{0}_idx = PsychPortAudio('CreateBuffer', {1}, cAudioData);",cPrefixStr,cSoundIdxStr)
        printAutoInd(soundStimCodes, "end")
    else:
        printAutoInd(soundStimCodes, "{0}_Dat = audioread(fullfile(cFolder,{1}) );", cPrefixStr,
                     addSingleQuotes(cFilenameStr))
        # make audio buffer
        # printAutoInd(f, "{0}_idx = PsychPortAudio('CreateBuffer', {1}, cAudioData);",cPrefixStr,cSoundIdxStr)

    #  draw buffer to  hw
    # printAutoInd(f, "PsychPortAudio('FillBuffer', {0}, {1}_idx, {2});",cSoundIdxStr,cPrefixStr, streamRefillStr)

    printAutoInd(soundStimCodes, "PsychPortAudio('FillBuffer', {0}, {1}_Dat, {2});", cSoundIdxStr, cPrefixStr,
                 streamRefillStr)

    if isVolumeControl:
        printAutoInd(soundStimCodes, "PsychPortAudio('Volume', {0}, {1});\n", cSoundIdxStr, volumeStr)

    if isLatencyBiasControl:
        printAutoInd(soundStimCodes, "PsychPortAudio('LatencyBias', {0}, {1}/1000);\n", cSoundIdxStr, latencyBiasStr)

    if isNotInSlide:
        pass
        # printAutoInd(soundStimCodes, "% check the 'esc' key to abort the exp")
        # printAutoInd(soundStimCodes, "detectAbortKey(abortKeyCode);\n")
    else:
        # check the repetitions parameter:
        repetitionsStr, isRef = getRefValue(cWidget, cProperties['Repetitions'], attributesSetDict)
        printAutoInd(soundStimCodes, "PsychPortAudio('Start', {0}, {1}, predictedVisOnset, 0); %\n", cSoundIdxStr,
                     repetitionsStr)

    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------

    return allWidgetCodes


def drawImageWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes, cProperties=None, cVSLCodes=None):
    if cVSLCodes is None:
        cVSLCodes = []
    if cProperties is None:
        cProperties = []

    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint
    isNotInSlide = True

    if len(cProperties) == 0:
        cProperties = Func.getWidgetProperties(cWidget.widget_id)
    else:
        isNotInSlide = False

    if isNotInSlide:
        cPrefixStr = getWidgetName(cWidget.widget_id)
    else:
        cPrefixStr = getWidgetName(cWidget.widget_id) + '_' + cProperties['Name']

    cRespCodes = allWidgetCodes.get(f"{cWidget.widget_id}_respCodes", [])
    beClosedTxAFCycleList = allWidgetCodes.get(f"beClosedTextures_{cLoopLevel}", [])

    # if getWidgetPos(cWidget.widget_id) == 0 and isNotInSlide and not(isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
    #     # Step 2: print out help info for the current widget
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
    #                  getWidgetName(cWidget.widget_id))
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    # 2) handle file name:
    cFileNameStr = trans2relativePath(cProperties['File Name'])
    cFilenameStr, isFileNameRef, _ = getValueInContainRefExp(cWidget, cFileNameStr, attributesSetDict)

    # cFilenameStr, isFileNameRef = getRefValue(cWidget, cProperties['File Name'], attributesSetDict)
    cFilenameStr = genAppropriatePathSplitter(cFilenameStr, Info.PLATFORM == 'windows')

    # 3) check the mirror up/down parameter:
    isMirrorUpDownStr = parseBooleanStr(cProperties['Mirror Up/Down'])

    # 3) check the mirror left/right parameter:
    isMirrorLeftRightStr = parseBooleanStr(cProperties['Mirror Left/Right'])

    # 4) check the rotate parameter:
    rotateStr, isRef = getRefValue(cWidget, cProperties['Rotate'], attributesSetDict)

    # 5) check the stretch mode parameter:
    if cProperties['Stretch']:
        # ""、Both、Horizontal、UpDown、[attr]
        stretchModeStr = parseStretchModeStr(*getRefValue(cWidget, cProperties['Stretch Mode'], attributesSetDict))
    else:
        stretchModeStr = "0"

    # 6) check the Transparent parameter:
    imageTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Transparent'], attributesSetDict))

    # 7) check the parameter winRect
    sx = dataStrConvert(*getRefValue(cWidget, cProperties['Center X'], attributesSetDict))
    sy = dataStrConvert(*getRefValue(cWidget, cProperties['Center Y'], attributesSetDict))

    cWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Width'], attributesSetDict))
    cHeight = dataStrConvert(*getRefValue(cWidget, cProperties['Height'], attributesSetDict))

    printAutoInd(f, "{0}_fRect = makeFrameRect({1}, {2}, {3}, {4}, fullRects({5},:));", cPrefixStr, sx, sy, cWidth,
                 cHeight, cWinIdx)

    if isNotInSlide:
        # before we draw the image， we draw the frame rect first:
        borderColor = dataStrConvert(*getRefValue(cWidget, cProperties['Border Color'], attributesSetDict))
        borderWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Border Width'], attributesSetDict))
        frameFillColor = dataStrConvert(*getRefValue(cWidget, cProperties['Frame Fill Color'], attributesSetDict))
        frameTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Frame Transparent'], attributesSetDict))

        # get enable parameter
        cRefedValue, isRef = getRefValue(cWidget, cProperties['Enable'], attributesSetDict)
        isBkFrameEnable = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

        if isBkFrameEnable == '1':
            if isNotInSlide:
                # if (frameFillColor == historyPropDict[cScreenName]) and (frameTransparent in [1,255]):
                if frameFillColor != historyPropDict[f"{cScreenName}_bkColor"]:
                    printAutoInd(f, "Screen('FillRect',{0},{1}, {2}_fRect);", cWinStr,
                                 addedTransparentToRGBStr(frameFillColor, frameTransparent), cPrefixStr)

                # draw the frame only when the frame color is different from the frame fill color
                if borderColor != frameFillColor:
                    printAutoInd(f, "Screen('FrameRect',{0},{1},{2}_fRect,{3});", cWinStr,
                                 addedTransparentToRGBStr(frameFillColor, frameTransparent), cPrefixStr, borderWidth)

            else:
                # if (frameFillColor == historyPropDict[cScreenName]) and (frameTransparent in [1,255]):
                if frameFillColor != historyPropDict[f"{cScreenName}_bkColor"]:
                    printAutoInd(cVSLCodes, "Screen('FillRect',{0},{1}, {2}_fRect);", cWinStr,
                                 addedTransparentToRGBStr(frameFillColor, frameTransparent), cPrefixStr)

                # draw the frame only when the frame color is different from the frame fill color
                if borderColor != frameFillColor:
                    printAutoInd(cVSLCodes, "Screen('FrameRect',{0},{1},{2}_fRect,{3});", cWinStr,
                                 addedTransparentToRGBStr(frameFillColor, frameTransparent), cPrefixStr,
                                 borderWidth)

    # make texture
    if isFileNameRef is False and cLoopLevel > 0:
        printAutoInd(f, "if ~exist('{0}_dat','var')", cPrefixStr)
        printAutoInd(f, "{0}_dat   = imread(fullfile(cFolder,{1}) );", cPrefixStr, addSingleQuotes(cFilenameStr))
        printAutoInd(f, "{0}_idx   = Screen('MakeTexture',{1}, {0}_dat);", cPrefixStr, cWinStr)
        printAutoInd(f, "end")

        beClosedTxAFCycleList.append(f"{cPrefixStr}_idx")
    else:
        # should be updated for each loop
        printAutoInd(f, "{0}_dat  = imread(fullfile(cFolder,{1}) );", cPrefixStr, addSingleQuotes(cFilenameStr))
        printAutoInd(f, "{0}_idx  = Screen('MakeTexture',{1}, {0}_dat);", cPrefixStr, cWinStr)

    printAutoInd(f, "[{0}_dRect, {0}_sRect] = makeImDestRect({0}_fRect, size({0}_dat), {1});", cPrefixStr,
                 stretchModeStr)

    if isNotInSlide:
        '''
        for no-slider image that means the image widget
        '''
        if isMirrorUpDownStr == '1' or isMirrorLeftRightStr == '1':
            printAutoInd(f, "[{0}xc, {0}yc] = RectCenter({0}_dRect);        % get the center of the {0}_dRect",
                         cPrefixStr)
            printAutoInd(f, "Screen('glPushMatrix', {0});             % enter into mirror mode", cWinStr)
            printAutoInd(f,
                         "Screen('glTranslate', {0}, {1}xc, {1}yc, 0);   % translate origin into the center of {1}_dRect",
                         cWinStr, cPrefixStr)
            if isMirrorLeftRightStr == '1':
                leftRightStr = '-1'
            else:
                leftRightStr = '1'

            if isMirrorUpDownStr == '1':
                upDownStr = '-1'
            else:
                upDownStr = '1'

            printAutoInd(f, "Screen('glScale', {0}, {1}, {2}, 1);     % mirror the drawn image", cWinStr, leftRightStr,
                         upDownStr)
            printAutoInd(f, "Screen('glTranslate', {0}, -{1}xc, -{1}yc, 0); % undo the translations", cWinStr,
                         cPrefixStr)

        printAutoInd(f, "Screen('DrawTexture', {0}, {1}_idx, {1}_sRect, {1}_dRect, {2}, [], abs({3}));",
                     cWinStr,
                     cPrefixStr,
                     rotateStr,
                     imageTransparent)

        if isMirrorUpDownStr == '1' or isMirrorLeftRightStr == '1':
            printAutoInd(f, "Screen('glPopMatrix', {0}); % restore to non mirror mode", cWinStr)
    else:
        '''
        for image item in slider
        '''
        if isMirrorUpDownStr == '1' or isMirrorLeftRightStr == '1':
            printAutoInd(f, "[{0}xc, {0}yc] = RectCenter({0}_dRect);        % get the center of the {0}_dRect",
                         cPrefixStr)

            printAutoInd(cVSLCodes, "Screen('glPushMatrix', {0});             % enter into mirror mode", cWinStr)
            printAutoInd(cVSLCodes,
                         "Screen('glTranslate', {0}, {1}xc, {1}yc, 0);   % translate origin into the center of {1}_dRect",
                         cWinStr, cPrefixStr)
            if isMirrorLeftRightStr == '1':
                leftRightStr = '-1'
            else:
                leftRightStr = '1'

            if isMirrorUpDownStr == '1':
                upDownStr = '-1'
            else:
                upDownStr = '1'

            printAutoInd(cVSLCodes, "Screen('glScale', {0}, {1}, {2}, 1);     % mirror the drawn image", cWinStr,
                         leftRightStr,
                         upDownStr)
            printAutoInd(cVSLCodes, "Screen('glTranslate', {0}, -{1}xc, -{1}yc, 0); % undo the translations", cWinStr,
                         cPrefixStr)

        printAutoInd(cVSLCodes, "Screen('DrawTexture', {0}, {1}_idx, {1}_sRect, {1}_dRect, {2}, [], abs({3}));",
                     cWinStr,
                     cPrefixStr,
                     rotateStr,
                     imageTransparent)

        if isMirrorUpDownStr == '1' or isMirrorLeftRightStr == '1':
            printAutoInd(cVSLCodes, "Screen('glPopMatrix', {0}); % restore to non mirror mode", cWinStr)

    if isNotInSlide:
        clearAfter = getClearAfterInfo(cWidget, attributesSetDict)

        printAutoInd(f, "Screen('DrawingFinished',{0},{1});", cWinStr, clearAfter)
        # printAutoInd(f, "% check the 'esc' key to abort the exp")
        # printAutoInd(f, "detectAbortKey(abortKeyCode);\n")

        '''
        # in slider, will do the close texture job within slider widget instead of here
        '''
        if isFileNameRef or cLoopLevel == 0:
            printAutoInd(cRespCodes, "% close the texture corresponding to {0}", cFilenameStr)
            printAutoInd(cRespCodes, "Screen('Close', {0}_idx);\n", cPrefixStr)

    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------
    allWidgetCodes.update({f"{cWidget.widget_id}_respCodes": cRespCodes})

    allWidgetCodes.update({f"beClosedTextures_{cLoopLevel}": beClosedTxAFCycleList})

    return allWidgetCodes, cVSLCodes, isFileNameRef


def drawVideoWidget(cWidget, f, attributesSetDict, cLoopLevel, allWidgetCodes, cProperties=None, cVSLCodes=None,
                    iVideoNum=0):
    # cVSLCode: codes for current video slider loop
    if cVSLCodes is None:
        cVSLCodes = []
    if cProperties is None:
        cProperties = []

    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint
    isNotInSlide = True

    if len(cProperties) == 0:
        cProperties = Func.getWidgetProperties(cWidget.widget_id)
    else:
        isNotInSlide = False

    cWidgetName = getWidgetName(cWidget.widget_id)
    if isNotInSlide:
        cItemOrWidgetNameStr = cWidgetName
    else:
        cItemOrWidgetNameStr = cProperties['Name']

    cVideoItemNums = getSliderItemTypeNums(cWidget, Info.ITEM_VIDEO)

    cBeFlipCodes = allWidgetCodes.get('codesBeFlip', [])

    # if getWidgetPos(cWidget.widget_id) == 0 and isNotInSlide and not(isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
    #     # Step 2: print out help info for the current widget
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
    #                  cWidgetName)
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    # 2) handle file name:
    cFileNameStr = trans2relativePath(cProperties['File Name'])
    cFilenameStr, isFileNameRef, _ = getValueInContainRefExp(cWidget, cFileNameStr, attributesSetDict)

    # cFilenameStr, isFileNameRef = getRefValue(cWidget, cProperties['File Name'], attributesSetDict)
    cFilenameStr = genAppropriatePathSplitter(cFilenameStr, Info.PLATFORM == 'windows')

    # 2) handle aspect ration name:
    stretchModeStr, isRef = getRefValue(cWidget, cProperties['Aspect Ratio'], attributesSetDict)
    stretchModeStr = parseAspectRationStr(stretchModeStr, isRef)

    # 3) check the playback rate parameter:
    playbackRateStr = dataStrConvert(*getRefValue(cWidget, cProperties['Playback Rate'], attributesSetDict))
    # 4) check the Start position parameter:

    startPositionStr, isRef = getRefValue(cWidget, cProperties['Start Position'], attributesSetDict)
    startPositionStr = parseStartEndTimeStr(startPositionStr, isRef)

    endPositionStr, isRef = getRefValue(cWidget, cProperties['End Position'], attributesSetDict)
    endPositionStr = parseStartEndTimeStr(endPositionStr, isRef)

    # 4) check the parameter winRect
    sx = dataStrConvert(*getRefValue(cWidget, cProperties['Center X'], attributesSetDict))
    sy = dataStrConvert(*getRefValue(cWidget, cProperties['Center Y'], attributesSetDict))

    cWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Width'], attributesSetDict))
    cHeight = dataStrConvert(*getRefValue(cWidget, cProperties['Height'], attributesSetDict))

    printAutoInd(f, "{0}_fRect = makeFrameRect({1}, {2}, {3}, {4}, fullRects({5},:));", cItemOrWidgetNameStr, sx, sy,
                 cWidth, cHeight, cWinIdx)

    if isNotInSlide:
        # before we draw the image， we draw the frame rect first:
        borderColor = dataStrConvert(*getRefValue(cWidget, cProperties['Border Color'], attributesSetDict))
        borderWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Border Width'], attributesSetDict))
        frameFillColor = dataStrConvert(*getRefValue(cWidget, cProperties['Frame Fill Color'], attributesSetDict))
        frameTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Frame Transparent'], attributesSetDict))

        # get enable parameter
        cRefedValue, isRef = getRefValue(cWidget, cProperties['Enable'], attributesSetDict)
        isBkFrameEnable = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

        if isBkFrameEnable == '1':
            # if (frameFillColor == historyPropDict[cScreenName]) and (frameTransparent in [1,255]):
            if frameFillColor != historyPropDict[f"{cScreenName}_bkColor"]:
                printAutoInd(f, "Screen('FillRect',{0},{1}, {2}_fRect);", cWinStr,
                             addedTransparentToRGBStr(frameFillColor, frameTransparent), cItemOrWidgetNameStr)

            # draw the frame only when the frame color is different from the frame fill color
            if borderColor != frameFillColor:
                printAutoInd(f, "Screen('FrameRect',{0},{1},{2}_fRect,{3});", cWinStr,
                             addedTransparentToRGBStr(frameFillColor, frameTransparent), cItemOrWidgetNameStr,
                             borderWidth)

    # make texture
    if isNotInSlide:
        printAutoInd(f, "% preload movie for widget: {0}", cItemOrWidgetNameStr)

    if Info.PLATFORM == 'linux':
        printAutoInd(f,
                     "% For linux, to use movie playback and PsychPortAudio at the same time, set specialFlags1 to 2")
        printAutoInd(f,
                     "Screen('OpenMovie', {0}, fullfile(cFolder,{1}), 1, [], 2); % Preloading the movie in background...\n",
                     cWinStr, addSingleQuotes(cFilenameStr))
    else:
        printAutoInd(f, "Screen('OpenMovie', {0}, fullfile(cFolder,{1}), 1); % Preloading the movie in background...\n",
                     cWinStr, addSingleQuotes(cFilenameStr))

    '''
    get the durStr to calculate the end movie times
    '''
    durStr, isRefValue, cRefValueSet = getRefValueSet(cWidget, cWidget.getDuration(), attributesSetDict)
    durStr = parseDurationStr(durStr)

    if isNotInSlide is True:
        cBeFlipCodes.append(f"% Really start to handle movie file in widget {cWidgetName}")
    else:
        cBeFlipCodes.append(f"% Really start to handle movie item: {cItemOrWidgetNameStr} in slider {cWidgetName}")

    printAutoInd(cVSLCodes, "% get and draw each video frame of ", cItemOrWidgetNameStr)

    if cVideoItemNums <= 1:
        '''
        for video widget or slider containing only one video item
        '''
        cBeFlipCodes.append(f"{cWidgetName}_sMTime = {startPositionStr}/1000; ")
        cBeFlipCodes.append(f"{cWidgetName}_eMTime = {endPositionStr}/1000; ")

        if Info.PLATFORM == 'linux':
            cBeFlipCodes.append(
                "% For linux, to use movie playback and PsychPortAudio at the same time, set specialFlags1 to 2")
            cBeFlipCodes.append(
                f"[{cWidgetName}_mPtr,{cWidgetName}_mDur, ~,{cItemOrWidgetNameStr}_ImgW, {cItemOrWidgetNameStr}_ImgH] = Screen('OpenMovie',{cWinStr}, fullfile(cFolder,{addSingleQuotes(cFilenameStr)}),[],[],2 );")
        else:
            cBeFlipCodes.append(
                f"[{cWidgetName}_mPtr,{cWidgetName}_mDur, ~,{cItemOrWidgetNameStr}_ImgW, {cItemOrWidgetNameStr}_ImgH] = Screen('OpenMovie',{cWinStr}, fullfile(cFolder,{addSingleQuotes(cFilenameStr)}) );")

        cBeFlipCodes.append(
            f"Screen('SetMovieTimeIndex', {cWidgetName}_mPtr, {cWidgetName}_sMTime); % skip the first n seconds")
        cBeFlipCodes.append(f"Screen('PlayMovie', {cWidgetName}Ptr, {playbackRateStr});")
        cBeFlipCodes.append(
            f"{cItemOrWidgetNameStr}_dRect = makeImDestRect({cItemOrWidgetNameStr}_fRect, [{cItemOrWidgetNameStr}_ImgW, {cItemOrWidgetNameStr}_ImgH], {stretchModeStr});\n")

        if re.fullmatch("\d+,\d+", durStr):
            cBeFlipCodes.append(
                f"{cWidgetName}_eMTime = min([{cWidgetName}_eMTime, {cWidgetName}_mDur, cDurs({cWinIdx}) - {cWidgetName}_sMTime]);")
        else:
            cBeFlipCodes.append(
                f"{cWidgetName}_eMTime = min([{cWidgetName}_eMTime, {cWidgetName}_mDur, cDurs({cWinIdx}) - {cWidgetName}_sMTime]);")

        printAutoInd(cVSLCodes, "if {0}_tPtr > 0 && {0}_CPt < {0}_eMTime", cWidgetName)
        printAutoInd(cVSLCodes, "[{0}_tPtr,{0}_CPt] = Screen('GetMovieImage', {1}, {0}_mPtr, 1); %", cWidgetName,
                     cWinStr)
        printAutoInd(cVSLCodes, "Screen('DrawTexture', {0}, {1}_tPtr, [], {2}_dRect);", cWinStr, cWidgetName,
                     cItemOrWidgetNameStr)
        printAutoInd(cVSLCodes, "end ")

    else:
        '''
        for slider containing more than one video items
        '''
        if Info.PLATFORM == 'linux':
            cBeFlipCodes.append(
                "% For linux, to use movie playback and PsychPortAudio at the same time, set specialFlags1 to 2")
            cBeFlipCodes.append(f"[{cWidgetName}Ptrs{iVideoNum},{cWidgetName}_mDurs{iVideoNum}, ~,"
                                f"{cWidgetName}_ImgWs{iVideoNum}, {cWidgetName}_ImgHs{iVideoNum}] = Screen('OpenMovie',"
                                f"{cWinStr}, fullfile(cFolder,{addSingleQuotes(cFilenameStr)}),[],[],2 );")
        else:
            cBeFlipCodes.append(
                f"[{cWidgetName}Ptrs{iVideoNum},{cWidgetName}_mDurs{iVideoNum}, ~,{cWidgetName}_ImgWs{iVideoNum}, {cWidgetName}_ImgHs{iVideoNum}] = Screen('OpenMovie',{cWinStr}, fullfile(cFolder,{addSingleQuotes(cFilenameStr)}) );")

        cBeFlipCodes.append(f"{cWidgetName}_sMTimes{iVideoNum} = {endPositionStr}/1000; ")
        cBeFlipCodes.append(
            f"Screen('SetMovieTimeIndex', {cWidgetName}Ptrs{iVideoNum}, {cWidgetName}_sMTimes{iVideoNum}); % skip the first n seconds")
        cBeFlipCodes.append(f"{cWidgetName}_eMTimes{iVideoNum} = {endPositionStr}/1000; ")
        cBeFlipCodes.append(f"Screen('PlayMovie', {cWidgetName}Ptrs{iVideoNum}, {playbackRateStr});")
        cBeFlipCodes.append(
            f"{cItemOrWidgetNameStr}_dRect = makeImDestRect({cItemOrWidgetNameStr}_fRect, [{cWidgetName}_ImgWs{iVideoNum}, {cWidgetName}_ImgHs{iVideoNum}], {stretchModeStr});\n")

        if re.fullmatch(r"\d+,\d+", durStr):
            cBeFlipCodes.append(
                f"{cWidgetName}_eMTimes{iVideoNum} = min([{cWidgetName}_eMTimes{iVideoNum}, {cWidgetName}_mDurs{iVideoNum}, getDurValue([{durStr}],winIFIs({cWinIdx})) - {cWidgetName}_sMTimes{iVideoNum}]);")
        else:
            cBeFlipCodes.append(
                f"{cWidgetName}_eMTimes{iVideoNum} = min([{cWidgetName}_eMTimes{iVideoNum}, {cWidgetName}_mDurs{iVideoNum}, getDurValue({durStr},winIFIs({cWinIdx})) - {cWidgetName}_sMTimes{iVideoNum}]);")

        printAutoInd(cVSLCodes, "if {0}_tPtrs({1}) > 0 && {0}_CPts({1}) < {0}_eMTimes({1})", cWidgetName, iVideoNum)
        printAutoInd(cVSLCodes, "[{0}_tPtrs({1}),{0}_CPts({1})] = Screen('GetMovieImage',{2} , {0}Ptrs({1}), 1); %",
                     cWidgetName, iVideoNum, cWinStr)
        printAutoInd(cVSLCodes, "Screen('DrawTexture', {0}, {1}_tPtrs({1}), [], {2}_dRect);", cWinStr, iVideoNum,
                     cItemOrWidgetNameStr)
        printAutoInd(cVSLCodes, "end ")

    if isNotInSlide:
        # for video widget , upload the cVSLCodes into allWidgetCodes
        allWidgetCodes.update({'forVideoSliderLoopCodes': cVSLCodes})

    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------

    allWidgetCodes.update({'codesBeFip': cBeFlipCodes})

    return allWidgetCodes, cVSLCodes


def drawTextForSlider(cWidget, f, attributesSetDict, cLoopLevel, cProperties, cVSLCodes):
    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num

    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    # 2) handle the current_text content
    inputStr, isContainRef, _ = getValueInContainRefExp(cWidget, cProperties['Text'], attributesSetDict, True, dict())
    cTextContentStr = parseTextContentStrNew(inputStr)
    # cTextContentStr = parseTextContentStr(*getRefValue(cWidget, cProperties['Text'], attributesSetDict))

    # 3) check the alignment X parameter:
    leftX = dataStrConvert(*getRefValue(cWidget, cProperties['Left X'], attributesSetDict))

    # 4) check the alignment X parameter:
    topY = dataStrConvert(*getRefValue(cWidget, cProperties['Top Y'], attributesSetDict))

    # 5) check the color parameter:
    fontColorStr = dataStrConvert(*getRefValue(cWidget, cProperties['Fore Color'], attributesSetDict))
    fontTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Transparent'], attributesSetDict))

    # 6) check the right to left parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Right To Left'], attributesSetDict)
    rightToLeft = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 7) set the font name size color style:
    fontName = dataStrConvert(*getRefValue(cWidget, cProperties['Font Family'], attributesSetDict))
    fontSize = dataStrConvert(*getRefValue(cWidget, cProperties['Font Size'], attributesSetDict))
    fontStyle = dataStrConvert(*getRefValue(cWidget, cProperties['Style'], attributesSetDict))
    fontStyle = parseFontStyleStr(fontStyle)

    fontBkColor = dataStrConvert(*getRefValue(cWidget, cProperties['Back Color'], attributesSetDict))

    isChangeFontPars = False
    #  font name
    if historyPropDict['fontName'] != fontName:
        printAutoInd(f, "Screen('TextFont',{0},{1});", cWinStr, fontName)
        historyPropDict.update({'fontName': fontName})
        isChangeFontPars = True

    # font size
    if historyPropDict['fontSize'] != fontSize:
        printAutoInd(f, "Screen('TextSize',{0},{1});", cWinStr, fontSize)
        historyPropDict.update({'fontSize': fontSize})
        isChangeFontPars = True

    # font style
    if historyPropDict['fontStyle'] != fontStyle:
        printAutoInd(f, "Screen('TextStyle',{0},{1});", cWinStr, fontStyle)
        historyPropDict.update({'fontStyle': fontStyle})
        isChangeFontPars = True

    printAutoInd(cVSLCodes, "Screen('DrawText',{0},{1},{2},{3},{4},{5},{6},{7});",
                 cWinStr,
                 cTextContentStr,
                 leftX,
                 topY,
                 addedTransparentToRGBStr(fontColorStr, fontTransparent),
                 fontBkColor,
                 0,
                 rightToLeft)

    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------

    return cVSLCodes


def drawTextWidget(cWidget, f, attributesSetDict, cLoopLevel):
    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num

    # if getWidgetPos(cWidget.widget_id) == 0 and not(isSubWidgetOfIfOrSwitch(cWidget.widget_id)):
    #     # Step 2: print out help info for the current widget
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    #     printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, getWidgetEventPos(cWidget.widget_id) + 1,
    #                  getWidgetName(cWidget.widget_id))
    #     printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    cProperties = Func.getWidgetProperties(cWidget.widget_id)
    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, cWinIdx, cWinStr = getScreenInfo(cWidget, attributesSetDict)

    # 2) handle the current_text content
    inputStr, isContainRef, _ = getValueInContainRefExp(cWidget, cProperties['Text'], attributesSetDict, True, dict())
    cTextContentStr = parseTextContentStrNew(inputStr)
    # cTextContentStr = parseTextContentStr(*getRefValue(cWidget, cProperties['Text'], attributesSetDict))

    # 3) check the alignment X parameter:
    alignmentX = dataStrConvert(*getRefValue(cWidget, cProperties['Alignment X'], attributesSetDict))

    # 4) check the alignment X parameter:
    alignmentY = dataStrConvert(*getRefValue(cWidget, cProperties['Alignment Y'], attributesSetDict))

    # 5) check the color parameter:
    fontColorStr = dataStrConvert(*getRefValue(cWidget, cProperties['Fore Color'], attributesSetDict))
    fontTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Transparent'], attributesSetDict))

    # 7) check the flip hor parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Flip Horizontal'], attributesSetDict)
    flipHorStr = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 8) check the flip ver parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Flip Vertical'], attributesSetDict)
    flipVerStr = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 10) check the right to left parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Right To Left'], attributesSetDict)
    rightToLeft = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 11) check the parameter winRect
    sx = dataStrConvert(*getRefValue(cWidget, cProperties['Center X'], attributesSetDict))
    sy = dataStrConvert(*getRefValue(cWidget, cProperties['Center Y'], attributesSetDict))
    cWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Width'], attributesSetDict))
    cHeight = dataStrConvert(*getRefValue(cWidget, cProperties['Height'], attributesSetDict))

    frameRectStr = f"makeFrameRect({sx}, {sy}, {cWidth}, {cHeight}, fullRects({cWinIdx},:))"

    # set the font name size color style:
    fontName = dataStrConvert(*getRefValue(cWidget, cProperties['Font Family'], attributesSetDict))
    fontSize = dataStrConvert(*getRefValue(cWidget, cProperties['Font Size'], attributesSetDict))
    fontStyle = dataStrConvert(*getRefValue(cWidget, cProperties['Style'], attributesSetDict))
    fontStyle = parseFontStyleStr(fontStyle)

    fontBkColor = dataStrConvert(*getRefValue(cWidget, cProperties['Back Color'], attributesSetDict))

    isChangeFontPars = False
    #  font name
    if historyPropDict['fontName'] != fontName:
        printAutoInd(f, "Screen('TextFont',{0},{1});", cWinStr, fontName)
        historyPropDict.update({'fontName': fontName})
        isChangeFontPars = True

    # font size
    if historyPropDict['fontSize'] != fontSize:
        printAutoInd(f, "Screen('TextSize',{0},{1});", cWinStr, fontSize)
        historyPropDict.update({'fontSize': fontSize})
        isChangeFontPars = True

    # font style
    if historyPropDict['fontStyle'] != fontStyle:
        printAutoInd(f, "Screen('TextStyle',{0},{1});", cWinStr, fontStyle)
        historyPropDict.update({'fontStyle': fontStyle})
        isChangeFontPars = True

    # font background color
    if historyPropDict['fontBkColor'] != fontBkColor:
        printAutoInd(f, "Screen('TextBackgroundColor',{0},{1});", cWinStr, fontBkColor)
        historyPropDict.update({'fontBkColor': fontBkColor})
        isChangeFontPars = True

    if isChangeFontPars:
        printAutoInd(f, "")

    # before we draw the formattedtext， we draw the frame rect first:
    borderColor = dataStrConvert(*getRefValue(cWidget, cProperties['Border Color'], attributesSetDict))
    borderWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Border Width'], attributesSetDict))
    frameFillColor = dataStrConvert(*getRefValue(cWidget, cProperties['Frame Fill Color'], attributesSetDict))
    # if f"preFrameFillColor" not in historyPropDict:
    frameTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Frame Transparent'], attributesSetDict))

    cRefedValue, isRef = getRefValue(cWidget, cProperties['Enable'], attributesSetDict)
    isBkFrameEnable = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    if isBkFrameEnable == '1':
        # if (frameFillColor == historyPropDict[cScreenName]) and (frameTransparent in [1,255]):
        if frameFillColor != historyPropDict[f"{cScreenName}_bkColor"]:
            printAutoInd(f, "Screen('FillRect',{0},{1},{2});", cWinStr,
                         addedTransparentToRGBStr(frameFillColor, frameTransparent), frameRectStr)

        # draw the frame only when the frame color is different from the frame fill color
        if borderColor != frameFillColor:
            printAutoInd(f, "Screen('FrameRect',{0},{1},{2},{3});", cWinStr,
                         addedTransparentToRGBStr(frameFillColor, frameTransparent), frameRectStr, borderWidth)

    #  print out the current_text
    printAutoInd(f, "DrawFormattedText({0},{1},{2},{3},{4},{5},{6},{7},[],{8},{9});",
                 cWinStr,
                 cTextContentStr,
                 alignmentX,
                 alignmentY,
                 addedTransparentToRGBStr(fontColorStr, fontTransparent),
                 dataStrConvert(*getRefValue(cWidget, cProperties['Wrapat Chars'], attributesSetDict)),
                 flipHorStr,
                 flipVerStr,
                 rightToLeft,
                 frameRectStr)

    clearAfter = getClearAfterInfo(cWidget, attributesSetDict)

    printAutoInd(f, "Screen('DrawingFinished',{0},{1});", cWinStr, clearAfter)
    # printAutoInd(f, "% check the 'esc' key to abort the exp")
    # printAutoInd(f, "detectAbortKey(abortKeyCode);\n")

    return 0


def compilePTB():
    global cInfoDict
    cInfoDict.clear()

    compileCode(False)

    cInfoDict.clear()


def compileCode(isDummyCompile):
    global enabledKBKeysSet, inputDevNameIdxDict, outputDevNameIdxDict, cIndents, historyPropDict, isDummyPrint, spFormatVarDict, cInfoDict, queueDevIdxValueStr

    # -----------initialize global variables ------/
    isDummyPrint = isDummyCompile

    cInfoDict.update({'maximumRows': 1})

    allWidgetCodes = {'codesAfFip': [], 'respCodes': []}

    historyPropDict = dict()

    historyPropDict.update({'clearAfter': "0"})
    historyPropDict.update({'fontName': "simSun"})
    historyPropDict.update({'fontSize': "12"})
    historyPropDict.update({'fontStyle': "0"})
    historyPropDict.update({'fontBkColor': "[259,0,0]"})  # we give the bkcolor an impossible initial value

    cIndents = 0
    cLoopLevel = 0
    isGampadWorksInWIn = True

    inputDevNameIdxDict = dict()
    outputDevNameIdxDict = dict()

    enabledKBKeysSet.clear()

    # eventWidgetList = [Info.TEXT, Info.IMAGE, Info.SOUND, Info.COMBO, Info.VIDEO,Info.IF, Info.SWITCH]

    enabledKBKeysSet.add(parseKbCorRespStr('{escape}', False, Info.DEV_KEYBOARD)[1:-1])

    # attributesSetDict 0,1,2 for looplevel, becitedStr,all possible values
    attributesSetDict = {'sessionNum': [0, 'subInfo.session', {'subInfo.session'}],
                         'subAge': [0, 'subInfo.age', {'subInfo.age'}],
                         'subName': [0, 'subInfo.name', {'subInfo.name'}],
                         'subSex': [0, 'subInfo.sex', {'subInfo.sex'}], 'subNum': [0, 'subInfo.num', {'subInfo.num'}],
                         'subHandness': [0, 'subInfo.hand', {'subInfo.hand'}]}
    spFormatVarDict = dict()
    # -------------------------------------------\

    # only replaced percent vars that will be reffed by % with - value /100
    spFormatVarDict = getSpecialFormatAtts()

    wid_widgetList = list(Info.WID_WIDGET.keys())
    wid_node_list = list(Info.WID_NODE.keys())
    # print(f"Name:WID_WIDGET: {list(Func.getWidgetName(cId) for cId in wid_widgetList)}")
    # print(f"Name:WID_NODE: {list(Func.getWidgetName(cId) for cId in wid_node_list)}")
    #
    # print(f"WID_WIDGET: {wid_widgetList}")
    # print(f"WID_NODE: {wid_node_list}")
    # print(f"=====================================\n")

    # get save path
    compile_file_name = ".".join(Info.FILE_NAME.split('.')[:-1]) + ".m"
    # open file
    with open(compile_file_name, "w", encoding="GBK") as f:
        #  print function start info
        cFilenameOnly = os.path.split(compile_file_name)[1].split('.')[0]
        # the help info

        printAutoInd(f, "function {0}()", cFilenameOnly)
        printAutoInd(f, "% function generated by PsyBuilder 0.1")
        printAutoInd(f,
                     "% If you use PsyBuilder for your research, then we would appreciate your citing our work in your paper:")
        printAutoInd(f, "% , (2019) PTB builder: a free GUI to generate experimental codes for Psychoolbox. \n%")
        printAutoInd(f, "% To report possible bugs and any suggestions please send us e-mail:")
        printAutoInd(f, "% Yang Zhang")
        printAutoInd(f, "% Ph.D, Prof.")
        printAutoInd(f, "% Department of Psychology, \n% SooChow University")
        printAutoInd(f, "% zhangyang873@gmail.com \n% Or\n% yzhangpsy@suda.edu.cn")
        printAutoInd(f, "% {0}", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # begin of the function
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "%      begin      ")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        if not isDummyCompile:
            globalVarEventStr = ''.join(' ' + cWidgetName for cWidgetName in getAllEventWidgetNamesList(1))
            globalVarAttStr = ''.join(' ' + cAttVarName for cAttVarName in getAllCycleAttVarNameList())

            isEyelink = haveTrackerType('EyeLink')

            if isEyelink:
                printAutoInd(f, "global{0}{1} beChkedRespDevs tracker2PtbTimeCoefs abortKeyCode cFrame %#ok<*NUSED>\n", globalVarEventStr, globalVarAttStr)
            else:
                printAutoInd(f, "global{0}{1} beChkedRespDevs abortKeyCode cFrame %#ok<*NUSED>\n", globalVarEventStr, globalVarAttStr)

            # get subject information
        printAutoInd(f, "% running platform check: ")
        if Info.PLATFORM == 'windows':
            printAutoInd(f, "if ~IsWin")
            printAutoInd(f, "error('Current platform is not Windows (you selected Windows in platform under building menu)!');")
            printAutoInd(f, "end \n")

        elif Info.PLATFORM == 'linux':
            printAutoInd(f, "if ~IsLinux")
            printAutoInd(f, "error('Current platform is not Linux (you selected Linux in platform under building menu)!');")
            printAutoInd(f, "end \n")

        elif Info.PLATFORM == 'mac':
            printAutoInd(f, "if ~IsOSX")
            printAutoInd(f, "error('Current platform is not Mac ox (you selected Mac in platform under building menu)!');")
            printAutoInd(f, "end \n")

        printAutoInd(f, "%===== get subject information =========/", )
        printAutoInd(f, "cFolder = fileparts(mfilename('fullpath'));")
        printAutoInd(f, "subInfo = OpenExp_BCL('{0}', cFolder);", cFilenameOnly)
        printAutoInd(f, "close(gcf);")
        printAutoInd(f, "%=====================================\\\n")

        # the function body try, catch end
        printAutoInd(f, "try")
        printAutoInd(f, "KbName('UnifyKeyNames');")
        printAutoInd(f, "abortKeyCode = KbName('ESCAPE');")

        printAutoInd(f, "expStartTime = datestr(now,'dd-mmm-YYYY:HH:MM:SS'); %#ok<*NASGU> % record start time \n")

        printAutoInd(f, "%======= Reinitialize the global random seed =======/")
        printAutoInd(f, "cRandSeed = RandStream('mt19937ar','Seed','shuffle');")
        printAutoInd(f, "RandStream.setGlobalStream(cRandSeed);")
        printAutoInd(f, "%===================================================\\\n")
        printAutoInd(f, "HideCursor;            % hide mouse cursor")

        if Info.PLATFORM == 'windows':
            printAutoInd(f, "ShowHideWinTaskbar(0); % hide the window taskbar")

        printAutoInd(f, "commandwindow;         % bring the command window into front")

        if Info.PLATFORM == 'mac':
            printAutoInd(f, "Priority(9);           % bring to high priority")
        else:
            printAutoInd(f, "Priority(1);           % bring to high priority")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% define and initialize input/output devices")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        maximumOpDataRows = getMaximumOpDataRows()

        # get output devices, such as global output devices.
        # you can get each widget's device you selected
        output_devices = Info.OUTPUT_DEVICE_INFO
        input_devices = Info.INPUT_DEVICE_INFO
        eyetracker_devices = Info.TRACKER_DEVICE_INFO
        quest_devices = Info.QUEST_DEVICE_INFO

        if len(eyetracker_devices) == 0:
            pass
        elif len(eyetracker_devices) == 1:

            for cEyeTracker in eyetracker_devices.keys():
                cEyeTrackerProperty = eyetracker_devices[cEyeTracker]

                if cEyeTrackerProperty.get('Select Tracker Type') == 'EyeLink':

                    printAutoInd(f, "%====== define edf filename  ========/")
                    printAutoInd(f, "edfFile = [subInfo.num,'_',subInfo.session,'.edf'];% should be less than 8 chars")
                    # printAutoInd(f, "edfFile = [subInfo.num,'_',subInfo.session,'.edf'];% should be less than 8 chars")
                    printAutoInd(f, "if numel(edfFile)>8")
                    printAutoInd(f, "edfFile = input('edf File name(should be less than 8 chars): ','s');")
                    printAutoInd(f, "edfFile = [edfFile '.edf'];")
                    printAutoInd(f, "end")
                    printAutoInd(f, "%===================================\\\n")

                else:
                    throwCompileErrorInfo(
                        f"Currently, only Eyelink action is supported\n because we only have an Eyelink 1000 for debug.")
        else:
            throwCompileErrorInfo(f"Currently number of eye tracker devs should be only one !")

        iQuest = 1
        if len(quest_devices) > 0:
            printAutoInd(f, "%======= initialize Quests ==========/")

            for quest in quest_devices.values():
                outputDevNameIdxDict.update({f"quest-{quest['Device Name']}": f"{iQuest}"})

                printAutoInd(f, "quest({0}) = QuestCreate({1},{2},{3},{4},{5},{6},{7},{8});",
                             iQuest,
                             quest['Guess Threshold'],
                             quest['Std. Dev.'],
                             quest['Desired Proportion'],
                             quest['Steepness'],
                             quest['Proportion'],
                             quest['Chance Level'],
                             quest['Grain'],
                             quest['Range'])

                if quest['Is Log10 Transform'] == 'yes':
                    printAutoInd(f, "quest({0}).isLog10Trans = true;", iQuest)
                else:
                    printAutoInd(f, "quest({0}).isLog10Trans = false;", iQuest)

                printAutoInd(f, "quest({0}).maxValue = {1};", iQuest, quest['Maximum Test Value'])
                printAutoInd(f, "quest({0}).minValue = {1};", iQuest, quest['Minimum Test Value'])

                # printAutoInd(f, "% get the first stimulus intensity")
                if quest['Method'] == 'quantile':
                    printAutoInd(f, "quest({0}).method = 1; % 1,2,3 for quantile, mean, and mode, respectively", iQuest)
                elif quest['Method'] == 'mean':
                    printAutoInd(f, "quest({0}).method = 2; % 1,2,3 for quantile, mean, and mode, respectively", iQuest)
                elif quest['Method'] == 'mode':
                    printAutoInd(f, "quest({0}).method = 3; % 1,2,3 for quantile, mean, and mode, respectively", iQuest)
                else:
                    throwCompileErrorInfo("quest method should be of {'quantile', 'mean', or 'mode'}!!")

                #  intensity transform:
                # printAutoInd(f, "quest({0}) = questValueTrans(quest({0}));\n", iQuest)
                printAutoInd(f, "")

                # attributesSetDict 0,1,2 for looplevel, becitedStr,all possible values
                attributesSetDict.update(
                    {f"{quest['Device Name']}.cValue": [0, f"quest({iQuest}).cValue", {f"quest({iQuest}).cValue"}]})

                iQuest += 1

            if iQuest > 0:
                printAutoInd(f, "nQuests = numel(quest);")
                printAutoInd(f, "% get the first stimulus intensity")
                printAutoInd(f, "for iQuest = 1:nQuests")
                printAutoInd(f, "quest(iQuest) = getQuestValue(quest(iQuest));")
                printAutoInd(f, "end")

            if iQuest > 1:
                printAutoInd(f, "randQuestIds = Randi(nQuests,[{0},1]);", maximumOpDataRows)
                attributesSetDict.update(
                    {f"randQuestValue": [0, f"quest(questRandIdx).cValue", {f"quest(questRandIdx).cValue"}]})

            printAutoInd(f, "%====================================\\\n")

        printAutoInd(f, "%====== define input devices ========/")
        iKeyboard = 1
        iGamepad = 1
        iRespBox = 1
        iMouse = 1
        iEyetracker = 1
        iQueueDev = 1

        for inputDevId, cDevice in input_devices.items():

            cIsQueue = cDevice.get('Is KB Queue', False)

            if cDevice['Device Type'] == Info.DEV_KEYBOARD:
                cInputDevIndexStr = f"{iKeyboard}"
                iKeyboard += 1

            elif cDevice['Device Type'] == Info.DEV_MOUSE:
                cInputDevIndexStr = f"{iMouse}"
                iMouse += 1

            elif cDevice['Device Type'] == Info.DEV_GAMEPAD:
                # looks like current the gamepad can be queued
                if Info.PLATFORM == 'windows' and cIsQueue and not(isGampadWorksInWIn):
                    throwCompileErrorInfo("In windows OS, using Gamepad for Queue is not allowed!\n")
                cInputDevIndexStr = f"{iGamepad}"
                iGamepad += 1

            elif cDevice['Device Type'] == Info.DEV_RESPONSE_BOX:
                printAutoInd(f, "rbIndices({0})   = CedrusResponseBox('Open', '{1}');", iRespBox,
                             cDevice['Device Index'])
                cInputDevIndexStr = f"{iRespBox}"
                iRespBox += 1

            elif cDevice['Device Type'] == Info.DEV_EYE_ACTION:
                # only one eye tracker are allow currently
                cInputDevIndexStr = f"{iEyetracker}"
                cDevice.update({'Device Index':cDevice['Tracker Name']})
                iEyetracker += 1

            if cDevice['Device Type'] in [Info.DEV_MOUSE, Info.DEV_KEYBOARD, Info.DEV_GAMEPAD]:
                if cDevice['Device Index'] != 'auto':
                    cInputDevIndexStr = cDevice['Device Index']

            cInputDevIndexValueStr, cDevTypeNum = makeInputDevIndexValueStr(cDevice['Device Type'], cInputDevIndexStr,
                                                                            cDevice['Device Index'] == 'auto')
            inputDevNameIdxDict.update({cDevice['Device Name']: [cInputDevIndexValueStr, int(cIsQueue), cDevTypeNum]})

            if cIsQueue is True:
                queueDevIdxValueStr = cInputDevIndexValueStr
                iQueueDev += 1

        # check input devs
        if Info.PLATFORM == 'windows':
            if iKeyboard > 2:
                throwCompileErrorInfo("In windows OS, only one keyboard is allowed!\n"
                                      " PTB can not address different keyboard devices!")
            elif iMouse > 2:
                throwCompileErrorInfo("In windows OS, only one mouse is allowed!\n"
                                      " PTB can not address different mice!")

        if iEyetracker > 2:
            throwCompileErrorInfo("Currently, we only support Eyelink(we only have a Eyelink1000 for debugging)!\n"
                                  "For Eyelink only one tracker device is allowed!")
        if iQueueDev > 2:
            throwCompileErrorInfo(f"Only one input device is allowed to be used for the KbQueue\n"
                                  f" (You selected {iQueueDev - 1}) devices!")

        # printAutoInd(f, "% get input device indices")
        printAutoInd(f, "kbIndices      = unique(GetKeyboardIndices);")

        if iGamepad > 1:
            # looks like GetGamepadIndices can work on windows
            if Info.PLATFORM == 'windows':
                if isGampadWorksInWIn:
                    printAutoInd(f, "gamepadIndices = unique(GetGamepadIndices);")
                else:
                    if iGamepad == 2:
                        printAutoInd(f, "gamepadIndices = 0; % joystickMex starts from 0 ")
                    else:
                        printAutoInd(f, "gamepadIndices = 0:{0}; % getGamepadIndices does not work on windows ",
                                     iGamepad - 2)
            else:
                printAutoInd(f, "gamepadIndices = unique(GetGamepadIndices);")

        if Info.PLATFORM == "linux":
            printAutoInd(f, "miceIndices    = unique(GetMouseIndices('slavePointer'));")
        else:
            printAutoInd(f, "miceIndices    = unique(GetMouseIndices);")


        if len(queueDevIdxValueStr)>0:
            printAutoInd(f, "% initialize the to be queued Device")
            printAutoInd(f, "KbQueueCreate({0});",queueDevIdxValueStr)
            printAutoInd(f, "isQueueStart = false;")
        printAutoInd(f, "%====================================\\\n")

        printAutoInd(f, "%===== define output devices ========/")

        iMonitor = 1
        iParal = 1
        iNetPort = 1
        iSerial = 1
        iSound = 1

        for outDev_Id, cDevice in output_devices.items():

            if cDevice['Device Type'] == Info.DEV_SCREEN:
                outputDevNameIdxDict.update({cDevice['Device Name']: f"{iMonitor}"})

                historyPropDict.update({f"{cDevice['Device Name']}_bkColor": addSquBrackets(cDevice['Back Color'])})
                # historyPropDict.update({f"{cDevice['Device Name']}_lastFlipTimeVar": []})

                printAutoInd(f, "monitors({0}).port        =  {1};", iMonitor, cDevice['Device Index'])
                printAutoInd(f, "monitors({0}).name        = '{1}';", iMonitor, cDevice['Device Name'])
                printAutoInd(f, "monitors({0}).bkColor     = [{1}];", iMonitor, cDevice['Back Color'])

                cDevResList = parsePhysicSize(cDevice['Resolution'])
                if len(cDevResList) == 2:
                    printAutoInd(f, "monitors({0}).rect        = [0,0,{2},{3}];", iMonitor, cDevResList[0],
                                 cDevResList[1])
                else:
                    printAutoInd(f, "monitors({0}).rect        = [];", iMonitor)

                printAutoInd(f, "monitors({0}).multiSample =  {1};\n", iMonitor, cDevice['Multi Sample'])
                iMonitor += 1

            elif cDevice['Device Type'] == Info.DEV_NETWORK_PORT:

                outputDevNameIdxDict.update({cDevice['Device Name']: f"tcpipCons({iNetPort})"})
                printAutoInd(f, "TCPIPs({0}).ipAdd    = '{1}';", iNetPort, cDevice['IP Address'])
                printAutoInd(f, "TCPIPs({0}).port     =  {1};", iNetPort, cDevice['IP Port'])
                printAutoInd(f, "TCPIPs({0}).name     = '{1}';", iNetPort, cDevice['Device Name'])
                printAutoInd(f, "TCPIPs({0}).isClient = {1};\n", iNetPort, cDevice['Is Client'])
                iNetPort += 1

            elif cDevice['Device Type'] == Info.DEV_PARALLEL_PORT:
                outputDevNameIdxDict.update({cDevice['Device Name']: f"parPort({iParal}).port"})
                printAutoInd(f, "parPort({0}).port     = hex2dec('{1}');", iParal, cDevice['Device Port'])
                printAutoInd(f, "parPort({0}).name     = '{1}';\n", iParal, cDevice['Device Name'])
                iParal += 1

            elif cDevice['Device Type'] == Info.DEV_SERIAL_PORT:

                outputDevNameIdxDict.update({cDevice['Device Name']: f"serialCons({iSerial})"})
                printAutoInd(f, "serPort({0}).port     = '{1}';", iSerial, cDevice['Device Port'])
                printAutoInd(f, "serPort({0}).name     = '{1}';", iSerial, cDevice['Device Name'])
                printAutoInd(f, "serPort({0}).baudRate = '{1}';", iSerial, cDevice['Baud Rate'])
                printAutoInd(f, "serPort({0}).dataBits = '{1}';\n", iSerial, cDevice['Data Bits'])
                iSerial += 1

            elif cDevice['Device Type'] == Info.DEV_SOUND:

                soundDevSlavesDict = getMaxSlaveSoundDevs()
                cSoundDevNameStr = cDevice['Device Name']

                if soundDevSlavesDict.get(cSoundDevNameStr, 0) > 0:
                    outputDevNameIdxDict.update({cSoundDevNameStr: f"audioDevs({iSound}).slaveIdxes"})
                    printAutoInd(f, "audioDevs({0}).nSlaves = {1};", iSound, soundDevSlavesDict[cSoundDevNameStr])

                    if cDevice['Device Index'] == 'auto':
                        printAutoInd(f, "soundDevs            = getOptimizedSoundDev;")
                        printAutoInd(f, "audioDevs({0}).port    = soundDevs({0}).DeviceIndex;", iSound)
                    else:
                        printAutoInd(f, "audioDevs({0}).port    = {1};", iSound, cDevice['Device Index'])

                    printAutoInd(f, "audioDevs({0}).name    = '{1}';", iSound, cSoundDevNameStr)

                    if 'auto' == cDevice['Sampling Rate']:
                        printAutoInd(f, "audioDevs({0}).fs      = []; % the default value in PTB is 48000 Hz\n",
                                     iSound)
                    else:
                        printAutoInd(f, "audioDevs({0}).fs      = {1};\n", iSound, cDevice['Sampling Rate'])

                    iSound += 1

        printAutoInd(f, "%====================================\\\n")

        printAutoInd(f, "disableSomeKbKeys; % restrictKeysForKbCheck \n")

        printAutoInd(f, "% initialize vars")
        printAutoInd(f, "[winIds,winIFIs,lastScrOnsettime, cDurs] = deal(zeros({0},1));", iMonitor - 1)
        printAutoInd(f, "nextEvFlipReqTime = 0;")

        printAutoInd(f, "fullRects         = zeros({0},4);\n", iMonitor - 1)
        #
        printAutoInd(f, "beChkedRespDevs = struct('beUpdatedVar','','allowAble',[],'corResp',[],'rtWindow',[],"
                        "'endAction',[],'type',[],'index',[],'isQueue',[],'startTime',[],'checkStatus',[],'needTobeReset',[],"
                        "'right',[],'wrong',[],'noResp',[],'respCodeDevType',[],'respCodeDevIdx',[],'start',[],"
                        "'end',[],'mean',[],'isOval',false,'onsettime',[],'resp',[]);")

        # printAutoInd(f, "cRespDevStruct = beChkedRespDevs;")
        printAutoInd(f, "beChkedRespDevs(1) = [];\n")
        printAutoInd(f, "cFrame = struct('rt',[],'acc',[],'resp',[],'onsettime',[],'respOnsettime',[]);")
        printAutoInd(f, "cFrameNoResp = struct('onsettime',[]);\n")
        #
        # print out initialize OP vars
        if not isDummyCompile:
            # maximumOpDataRows = getMaximumOpDataRows()
            # input parameter 2 will include widget type of LOOP
            allEventWidgets = getAllEventWidgetsList(3)

            for cWidget in allEventWidgets:
                cWidgetType = getWidgetType(cWidget)
                cWidgetName = getWidgetName(cWidget.widget_id)
                cWidgetLoopLevel = getWidLevel(cWidget.widget_id)

                if cWidgetType in stimWidgetTypesList:

                    haveRespDev = cWidget.getUsingDeviceCount() > 0

                    if haveRespDev:
                        cFrameVarNameStr = 'cFrame'
                    else:
                        cFrameVarNameStr = 'cFrameNoResp'

                    if cWidgetLoopLevel == 1:
                        printAutoInd(f, "{0} = {1};", cWidgetName, cFrameVarNameStr)
                    else:
                        printAutoInd(f, "{0} = repmat({1},{2},1);", cWidgetName, cFrameVarNameStr, maximumOpDataRows)

                    if getHaveOutputDevs(cWidget):
                        printAutoInd(f, "{0}(end).msgEndTime = [];", cWidgetName)

                elif cWidgetType == Info.LOOP:

                    cAttVarNameList = getCycleAttVarNamesList(cWidget)

                    bePrintStr = ''.join(f"{cVar}," for cVar in cAttVarNameList)

                    bePrintStr = f"[{bePrintStr[0:-1]}] = deal(cell({maximumOpDataRows},1)); % save cycle attrs"
                    printAutoInd(f, bePrintStr)

        # printAutoInd(f, "%-----------------------\\\n")
        printAutoInd(f, " ")

        printAutoInd(f, "% open windows")
        # printAutoInd(f, "%--- open windows ---/")
        printAutoInd(f, "for iWin = 1:numel(monitors)")
        printAutoInd(f,
                     "[winIds(iWin),fullRects(iWin,:)] = Screen('OpenWindow',monitors(iWin).port,monitors(iWin).bkColor,monitors(iWin).rect,[],[],[],monitors(iWin).multiSample);")
        printAutoInd(f,
                     "Screen('BlendFunction', winIds(iWin),'GL_SRC_ALPHA','GL_ONE_MINUS_SRC_ALPHA'); % force to most common alpha-blending factors")
        printAutoInd(f,
                     "winIFIs(iWin) = Screen('GetFlipInterval',winIds(iWin));                        % get inter frame interval (i.e., 1/refresh rate)")
        printAutoInd(f, "end % for iWin ")
        # printAutoInd(f, "%--------------------\\\n")
        printAutoInd(f, " ")
        printAutoInd(f, "flipComShiftDur  = winIFIs*0.5; % 0.5 IFI before flip to ensure flipping at right time")

        isNoneScreenOutPutDevs = (iNetPort + iSerial+ iParal + iSound) > 4

        if isNoneScreenOutPutDevs:
            printAutoInd(f, "%===== initialize output devices ========/")
        # initialize TCPIP connections
        if iNetPort > 1:
            printAutoInd(f, "% open TCPIPs")
            # printAutoInd(f, "%--- open TCPIPs ----/")
            printAutoInd(f, "tcpipCons = zeros({0},1);", iNetPort - 1)

            printAutoInd(f, "for iCount = 1:numel(TCPIPs)")

            printAutoInd(f, "if TCPIPs(iCount).isClient")
            printAutoInd(f, "tcpipCons(iCount) = pnet('tcpconnect',TCPIPs(iCount).ipAdd,TCPIPs(iCount).port);")
            printAutoInd(f, "else")
            printAutoInd(f, "tcpipCons(iCount) = pnet('tcpsocket',TCPIPs(iCount).port);")
            printAutoInd(f, "end")

            printAutoInd(f, "end % iCount")

            printAutoInd(f, " ")
            # printAutoInd(f, "%----------------------\\\n")

        # initialize serial ports
        if iSerial > 1:
            # printAutoInd(f, "%--- open serial ports ----/")
            printAutoInd(f, "% open serial ports")
            printAutoInd(f, "serialCons = zeros({0},1);", iSerial - 1)

            printAutoInd(f, "for iCount = 1:numel(serialCons)")
            printAutoInd(f,
                         "serialCons(iCount) = IOPort('OpenSerialPort',serPort(iCount).port,['BaudRate=',serPort(iCount).baudRate,',DataBits=',serPort(iCount).dataBits]);")
            printAutoInd(f, "end % iCount")
            printAutoInd(f, "")
        # initialize parallel ports
        if iParal > 1:
            printAutoInd(f, "% open parallel ports")
            # printAutoInd(f, "%--- open parallel ports ----/")
            if Info.PLATFORM == 'linux':
                printAutoInd(f, "% for linux we directly use outb under sodo mode ")

            if Info.PLATFORM == 'windows':
                printAutoInd(f, "try")
                printAutoInd(f, "io64Obj = io64;")
                printAutoInd(f, "catch")
                printAutoInd(f,
                             "error('Failed to find io64, please see \"http://apps.usd.edu/coglab/psyc770/IO64.html\" for instruction of installation!');")
                printAutoInd(f, "end % try")

                printAutoInd(f, "if 0 ~= io64(ioObj)")
                printAutoInd(f, "error('in/outPut 64 installation failed!');")
                printAutoInd(f, "end % if 0 ~= ")

            if Info.PLATFORM == 'mac':
                printAutoInd(f, "error('Currently, we did not support output via parallel under Mac OX!');")
            # printAutoInd(f, "%----------------------------\\\n")
            printAutoInd(f, "")

        #  initialize audio output devices
        if iSound > 1:
            printAutoInd(f, "% open output audio devs")
            # printAutoInd(f, "%--open output audio devs----/")
            printAutoInd(f, "InitializePsychSound(1); % Initialize the audio driver, require low-latency preinit\n")

            printAutoInd(f, "for iCount = 1:numel(audioDevs)")
            printAutoInd(f,
                         "audioDevs(iCount).idx = PsychPortAudio('Open',audioDevs(iCount).port,8,[],audioDevs(iCount).fs,2); %#ok<AGROW>")
            printAutoInd(f, "for iSlave = 1:audioDevs(iCount).nSlaves")
            printAutoInd(f,
                         "audioDevs(iCount).slaveIdxes(iSlave) = PsychPortAudio('OpenSlave', audioDevs(iCount).idx, 1);")
            printAutoInd(f, "end % iSlave")
            printAutoInd(f, "end % iCount")

            # printAutoInd(f, "%----------------------------\\\n")
            printAutoInd(f, "")

        if isNoneScreenOutPutDevs:
            printAutoInd(f, "%========================================\\\n")



        if isEyelink:
            # get sound dev for eye tracker feedback:
            # shouldNotBeCitationCheck('Sound Device', cEyeTrackerProperty['Sound Device'])
            # cSoundDevName = cEyeTrackerProperty.get('Sound Device')
            cSoundDevName = cEyeTrackerProperty.get('Sound', '')

            if len(cSoundDevName) == 0:
                throwCompileErrorInfo('should define a sound device for eyetracker')

            cSoundIdxStr = f"{outputDevNameIdxDict.get(cSoundDevName)}(1)"

            printAutoInd(f, "% set a sound dev for eyetracker feedbacks")
            printAutoInd(f, "if exist('audioDevs','var')")
            printAutoInd(f, "Snd('Open', {0})", cSoundIdxStr)
            printAutoInd(f, "end ")
            printAutoInd(f, "% init and send global commands to Eyelink")
            printAutoInd(f, "el = initEyelink;\n")

        printAutoInd(f, "opRowIdx = 1; % set the output variables row num")
        # use iLoop_*_cOpR to record cTL's output var row, so that we can keep this num when there is a subCycle widget
        printAutoInd(f, "iLoop_0_cOpR = opRowIdx; % use iLoop_*_cOpR to record cTL's output var row")

        # start to handle all the widgets
        printTimelineWidget(Info.WID_WIDGET[f"{Info.TIMELINE}.0"], f, attributesSetDict, cLoopLevel, allWidgetCodes)

        printAutoInd(f, "% for the last event in timeline just wait for duration")
        printAutoInd(f, "WaitSecs('UntilTime', nextEvFlipReqTime); \n")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% end of the main exp procedure")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "expEndTime = datestr(now,'dd-mmm-YYYY:HH:MM:SS'); % record the end time \n")
        printAutoInd(f, "sca;                        % Close opened windows")
        printAutoInd(f, "ShowCursor;                 % Show the hided mouse cursor")
        printAutoInd(f, "Priority(0);                % Turn the priority back to normal")
        printAutoInd(f, "RestrictKeysForKbCheck([]); % Re-enable all keys\n")

        if Info.PLATFORM == 'windows':
            printAutoInd(f, "ShowHideWinTaskbar(1);      % show the window taskbar.")

        printAutoInd(f, "fillResultVars(opRowIdx); % update results vars for analysis")
        printAutoInd(f, "save(subInfo.filename); % save the results\n")

        if isEyelink:
            printAutoInd(f, "Eyelink('CloseFile');")
            printAutoInd(f, "Eyelink('ReceiveFile', edfFile, cFolder,1);\n")

        if iNetPort > 1 or iParal > 1 or iSerial > 1 or iRespBox > 1 or iSound > 1:
            #  close opened devices
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% close opened devices")
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # close TCPIP connections
        if iNetPort > 1:
            printAutoInd(f, "%-- close serial ports --/")

            printAutoInd(f, "for iCount = 1:numel(tcpipCons)")
            printAutoInd(f, "pnet(tcpipCons(iCount),'close');")
            printAutoInd(f, "end % iCount")

            printAutoInd(f, "%------------------------\\\n")

        # close serial ports
        if iSerial > 1:
            printAutoInd(f, "%--- close serial ports ---/")
            printAutoInd(f, "for iCount = 1:numel(serialCons)")
            printAutoInd(f, "IOPort('Close',serialCons(iCount));")
            printAutoInd(f, "end % iCount")
            printAutoInd(f, "%--------------------------\\\n")

        # close parallel ports
        if iParal > 1:
            if Info.PLATFORM == 'windows':
                printAutoInd(f, "%--- close parallel ports ---/")
                printAutoInd(f, "clear io64;")
                printAutoInd(f, "%----------------------------\\\n")

        # close Cedrus response box
        if iRespBox > 1:
            printAutoInd(f, "%close Cedrus response boxes:")
            printAutoInd(f, "CedrusResponseBox('CloseAll');\n")

        # close psychPortAudio device
        if iSound > 1:
            # printAutoInd(f, "%--- close outputAudio devs--/")
            printAutoInd(f, "% close outputAudio devs")
            printAutoInd(f, "PsychPortAudio('Close', [audioDevs(:).idx]);\n")
            # printAutoInd(f, "%----------------------------\\\n")

        if len(queueDevIdxValueStr) > 0:
            printAutoInd(f, "% close queue device")
            printAutoInd(f, "KbQueueStop({0});", queueDevIdxValueStr)
            printAutoInd(f, "KbQueueRelease({0});", queueDevIdxValueStr)

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% end of the experiment", )
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

        printAutoInd(f, "catch {0}_error\n", cFilenameOnly)

        printAutoInd(f, "sca;                        % Close opened windows")
        printAutoInd(f, "ShowCursor;                 % Show the hided mouse cursor")
        printAutoInd(f, "Priority(0);                % Turn the priority back to normal")
        printAutoInd(f, "RestrictKeysForKbCheck([]); % Re-enable all keys")

        if isEyelink:
            printAutoInd(f, "try")
            printAutoInd(f, "cleanup;")
            printAutoInd(f, "end")

        if Info.PLATFORM == 'windows':
            printAutoInd(f, "ShowHideWinTaskbar(1);      % show the window taskbar")

        # close TCPIP connections
        if iNetPort > 1:
            printAutoInd(f, "%close net ports:")

            printAutoInd(f, "for iCount = 1:numel(tcpipCons)")
            printAutoInd(f, "pnet(tcpipCons(iCount),'close');")
            printAutoInd(f, "end % iCount")
            #
            # printAutoInd(f,"%------------------------\\\n")

        # close serial ports
        if iSerial > 1:
            printAutoInd(f, "%close serial ports: ")
            printAutoInd(f, "for iCount = 1:numel(serialCons)")
            printAutoInd(f, "IOPort('Close',serialCons(iCount));")
            printAutoInd(f, "end % iCount")
            # printAutoInd(f,"%--------------------------\\\n")

        # close parallel ports
        if iParal > 1:
            if Info.PLATFORM == 'windows':
                printAutoInd(f, "%close parallel ports")
                printAutoInd(f, "clear io64;% Under windows io64 need to be closed")

        # close psychPortAudio device
        if iSound > 1:
            # printAutoInd(f, "%--- close outputAudio devs--/")
            printAutoInd(f, "% close outputAudio devs")
            # printAutoInd(f, "for iCount = 1:numel(audioDevs)")
            printAutoInd(f, "PsychPortAudio('Close', [audioDevs(:).idx]);")
            # printAutoInd(f, "end % iCount")
            # printAutoInd(f, "%----------------------------\\\n")

        # close Cedrus response box
        if iRespBox > 1:
            printAutoInd(f, "%close Cedrus response boxes:")
            printAutoInd(f, "CedrusResponseBox('CloseAll');\n")

        printAutoInd(f, "save([subInfo.filename,'_debug']);")

        if isEyelink:
            printAutoInd(f, "try %#ok<*TRYNC>")
            printAutoInd(f, "Eyelink('CloseFile');")
            printAutoInd(f, "Eyelink('ReceiveFile', edfFile, cFolder,1);")
            printAutoInd(f, "end \n")

        if len(queueDevIdxValueStr) > 0:
            printAutoInd(f, "% close queue device")
            printAutoInd(f, "KbQueueStop({0});", queueDevIdxValueStr)
            printAutoInd(f, "KbQueueRelease({0});", queueDevIdxValueStr)

        printAutoInd(f, "rethrow({0}_error);", cFilenameOnly)

        printAutoInd(f, "end % try")

        printAutoInd(f, "end % main function \n\n\n\n\n\n\n")

        outDevCountsDict = getOutputDevCountsDict()
        nOutPortsNums = outDevCountsDict[Info.DEV_PARALLEL_PORT] + outDevCountsDict[Info.DEV_NETWORK_PORT] + \
                        outDevCountsDict[Info.DEV_SERIAL_PORT]

        iSubFunNum = 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: fillResultVars", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "function fillResultVars(opRowIdx)%#ok<*DEFNU,*INUSD>")
        printAutoInd(f, "global{0}{1}\n", globalVarEventStr, globalVarAttStr)

        resultEventVarsStr4Cell = ''.join("'" + cWidgetName + "'," for cWidgetName in getAllEventWidgetNamesList(1))
        resultAttVarsStr4Cell = ''.join("'" + cAttName + "'," for cAttName in getAllCycleAttVarNameList())
        allStr4Cell = resultEventVarsStr4Cell + resultAttVarsStr4Cell
        allStr4Cell = '{' + allStr4Cell[0:-1] + '}'

        printAutoInd(f, "resultVarNames = {0};", allStr4Cell)
        printAutoInd(f, f"for iVar = 1:numel(resultVarNames)")
        printAutoInd(f, "{0}", "eval([resultVarNames{iVar},' = updateResultVar(',resultVarNames{iVar},'opRowIdx);']);")
        printAutoInd(f, f"end % for iVar")

        printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
        iSubFunNum = 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: updateResultVar", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "function beUpdatedVar = updateResultVar(beUpdatedVar,opRowIdx)")
        printAutoInd(f, 'if numel(beUpdatedVar) > 1')
        printAutoInd(f, 'beUpdatedVar(opRowIdx+1:end) = [];\n')
        printAutoInd(f, 'for iRow = 1:numel(beUpdatedVar)')
        printAutoInd(f, 'if isstruct(beUpdatedVar)')

        printAutoInd(f, '% for event log vars')
        printAutoInd(f, 'if isempty(beUpdatedVar(iRow).onsettime)')
        printAutoInd(f, 'beUpdatedVar(iRow) = beUpdatedVar(iRow - 1);')
        printAutoInd(f, 'end')

        printAutoInd(f, 'else')

        printAutoInd(f, '% for attributes in cycle')
        printAutoInd(f, "if {0}", 'isempty(beUpdatedVar{iRow})')
        printAutoInd(f, 'beUpdatedVar(iRow) = beUpdatedVar(iRow - 1);')
        printAutoInd(f, 'end ')

        printAutoInd(f, 'end %  isstruct(beUpdatedVar)')
        printAutoInd(f, '')
        printAutoInd(f, 'end % for iRow')
        printAutoInd(f, 'end % if numel(beUpdatedVar) > 1')

        printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
        iSubFunNum = 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: checkRespAndSendTriggers", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f,
                     "function [isTerminateStimEvent, secs, nextEvFlipReqTime] = checkRespAndSendTriggers(cWIdx, nextEvFlipReqTime, isOneTimeCheck) %#ok<INUSL>")
        # globalVarEventStr = ''.join(' ' + cWidgetName for cWidgetName in getAllEventWidgetNamesList() )
        printAutoInd(f, "global{0} abortKeyCode beChkedRespDevs cFrame\n", globalVarEventStr)

        # printAutoInd(f, "% to speed up the process, we removed argins check")
        # printAutoInd(f, "%if ~exist('isOneTimeCheck','var')")
        # printAutoInd(f, "%isOneTimeCheck = false;")
        # printAutoInd(f, "%end ")

        printAutoInd(f, "isTerminateStimEvent = false; \n")
        printAutoInd(f, "secs = GetSecs; \n")

        printAutoInd(f, "allTypeIndex = [beChkedRespDevs(:).type;beChkedRespDevs(:).index]';")
        printAutoInd(f, "uniqueDevs   = unique(allTypeIndex,'rows');\n")

        printAutoInd(f, "if ~isempty(beChkedRespDevs) && any([beChkedRespDevs(:).checkStatus])")

        printAutoInd(f, "while secs < nextEvFlipReqTime && any([beChkedRespDevs(:).checkStatus])")
        printAutoInd(f, "% loop across each unique resp dev: ")
        printAutoInd(f, "for iUniDev = 1:size(uniqueDevs,1)")

        printAutoInd(f, "cRespDevs = beChkedRespDevs(ismember(uniqueDevs(iUniDev,:),allTypeIndex,'rows'));\n")

        printAutoInd(f, "if any([cRespDevs(:).checkStatus])")
        printAutoInd(f, "[secs,keyCode,fEventOr1stRelease] = responseCheck(uniqueDevs(iUniDev,1),uniqueDevs(iUniDev,2),cRespDevs(iUniDev).isQueue);\n")

        printAutoInd(f, "% check aborted key")
        printAutoInd(f, "if keyCode(abortKeyCode)")
        printAutoInd(f, "error('The program was aborted ...!');")
        printAutoInd(f, "end \n")

        printAutoInd(f, "for iRespDev = 1:numel(cRespDevs)")

        if outDevCountsDict[Info.DEV_PARALLEL_PORT] > 0:
            printAutoInd(f, "{0}", "% reset parallel port back to 0")
            printAutoInd(f, "if {0}", "cRespDevs(iRespDev).needTobeReset && (secs - cRespDevs(iRespDev).startTime) > 0.01 % currently set to 10 ms")
            printAutoInd(f, "{0}", "sendTriggerOrMsg(cRespDevs(iRespDev).respCodeDevType,cRespDevs(iRespDev).respCodeDevIdx, 0);")
            printAutoInd(f, "{0}", "cRespDevs(iRespDev).needTobeReset = false;")
            printAutoInd(f, "end \n")

        printAutoInd(f, "% if RT window is not negative and cTime is out of RT Window")
        printAutoInd(f, "if cRespDevs(iRespDev).rtWindow > 0 && (secs - cRespDevs(iRespDev).startTime) > cRespDevs(iRespDev).rtWindow")

        if nOutPortsNums > 0:
            printAutoInd(f, "% send no response trigger")
            printAutoInd(f, "sendTriggerOrMsg(cRespDevs(iRespDev).respCodeDevType, cRespDevs(iRespDev).respCodeDevIdx, cRespDevs(iRespDev).noResp);")

        printAutoInd(f, "% 0, 1, 2 for off, press check and release check, respectively")
        printAutoInd(f, "cRespDevs(iRespDev).checkStatus = 0;")
        printAutoInd(f, "end \n")

        printAutoInd(f, "if cRespDevs(iRespDev).checkStatus == 1")
        printAutoInd(f, "if cRespDevs(iRespDev).isQueue")
        printAutoInd(f, "% excluded the key presses before the onsettime of the current event")
        printAutoInd(f, "cValidRespKeys = keyCode(cRespDevs(iRespDev).allowAble)> cRespDevs(iRespDev).startTime;")
        printAutoInd(f, "else")
        printAutoInd(f, "cValidRespKeys = ~~keyCode(cRespDevs(iRespDev).allowAble);")
        printAutoInd(f, "end \n")

        printAutoInd(f, "if any(cValidRespKeys)")
        printAutoInd(f, "cFrame.onsettime = cRespDevs(iRespDev).startTime;\n")

        printAutoInd(f, "if cRespDevs(iRespDev).isQueue")
        printAutoInd(f, "cFrame.respOnsettime = min(keyCodes(cRespDevs(iRespDev).allowAble(cValidRespKeys))); % only the first key are valid ")
        printAutoInd(f, "else")
        printAutoInd(f, "if cRespDevs(iRespDev).respCodeDevType == 82 % Eyelink eye action")
        printAutoInd(f, "cFrame.respOnsettime = fEventOr1stRelease.time;")
        printAutoInd(f, "else")
        printAutoInd(f, "cFrame.respOnsettime = secs;")
        printAutoInd(f, "end ")
        # printAutoInd(f, "cFrame.resp          = find(keyCode);")
        printAutoInd(f, "end \n")
        printAutoInd(f, "cFrame.resp = intersect(find(keyCode),cRespDevs(iRespDev).allowAble(cValidRespKeys));\n")

        printAutoInd(f, "cFrame.rt = cFrame.respOnsettime - cRespDevs(iRespDev).startTime; ")
        printAutoInd(f, "cRespDevs(iRespDev).onsettime = cFrame.respOnsettime;\n")
        printAutoInd(f, "if cRespDevs(iRespDev).respCodeDevType == 82 % 82 is Eyelink eye action")
        printAutoInd(f, "cFrame.acc = all(ismember(cRespDevs(iRespDev).resp, cRespDevs(iRespDev).corResp)) && isEyeActionInROIs(fEventOr1stRelease, cRespDevs(iRespDev));")
        printAutoInd(f, "else ")
        printAutoInd(f, "cFrame.acc = all(ismember(cRespDevs(iRespDev).resp, cRespDevs(iRespDev).corResp));")
        printAutoInd(f, "end \n")

        # print resp codes
        if nOutPortsNums > 0:
            printAutoInd(f, "if cFrame.acc")
            printAutoInd(f, "sendTriggerOrMsg(cRespDevs(iRespDev).respCodeDevType, cRespDevs(iRespDev).respCodeDevIdx, cRespDevs(iRespDev).right);")
            printAutoInd(f, "else ")
            printAutoInd(f, "sendTriggerOrMsg(cRespDevs(iRespDev).respCodeDevType, cRespDevs(iRespDev).respCodeDevIdx, cRespDevs(iRespDev).wrong);")
            printAutoInd(f, "end \n")

        printAutoInd(f, "eval([cRespDevs(iRespDev).beUpdatedVar,' = cFrame;']); \n")

        printAutoInd(f, "switch cRespDevs(iRespDev).endAction")
        printAutoInd(f, "case 2")
        printAutoInd(f, "% end action: terminate till release")
        printAutoInd(f, "cRespDevs(iRespDev).checkStatus = 2;\n")
        printAutoInd(f, "cRespDevs(iRespDev).onsettime = cFrame.respOnsettime;")
        printAutoInd(f, "cRespDevs(iRespDev).resp = cFrame.resp;\n")
        printAutoInd(f, "if cRespDevs(iRespDev).isQueue")
        printAutoInd(f, "if any(fEventOr1stRelease(cRespDevs(iRespDev).resp))")
        printAutoInd(f, "cRespDevs(iRespDev).checkStatus = 0;")
        printAutoInd(f, "isTerminateStimEvent = true; % will break out the while loop soon")
        printAutoInd(f, "end")
        printAutoInd(f, "end")

        printAutoInd(f, "case 1")
        printAutoInd(f, "% end action: terminate")
        printAutoInd(f, "cRespDevs(iRespDev).checkStatus = 0;")
        printAutoInd(f, "isTerminateStimEvent = true; % will break out the while loop soon")
        printAutoInd(f, "case 0")
        printAutoInd(f, "% end action: none")
        printAutoInd(f, "cRespDevs(iRespDev).checkStatus = 0;")
        printAutoInd(f, "otherwise")
        printAutoInd(f, "% do nothing")
        printAutoInd(f, "end%switch ")
        printAutoInd(f, " ")

        printAutoInd(f, "end % if there was a response\n")

        printAutoInd(f, "% check key release ")
        printAutoInd(f, "elseif cRespDevs(iRespDev).checkStatus == 2")

        printAutoInd(f, "if cRespDevs(iRespDev).isQueue")
        printAutoInd(f, "if any(fEventOr1stRelease(cRespDevs(iRespDev).resp))")
        printAutoInd(f, "cRespDevs(iRespDev).checkStatus = 0;")
        printAutoInd(f, "isTerminateStimEvent = true; % will break out the while loop soon")
        printAutoInd(f, "end")
        printAutoInd(f, "else")
        printAutoInd(f, "if any(~keyCode(cRespDevs(iRespDev).resp))")
        printAutoInd(f, "cRespDevs(iRespDev).checkStatus = 0;")
        printAutoInd(f, "isTerminateStimEvent = true; % will break out the while loop soon")
        printAutoInd(f, "end \n")
        printAutoInd(f, "end \n")


        printAutoInd(f, "end % if the check switch is on\n")
        printAutoInd(f, "end % for iRespDev")
        printAutoInd(f, "end % any(cRespDevs(:).checkStatus)")
        printAutoInd(f, "end % iUnique Dev\n")

        printAutoInd(f, "% after checking all respDev, break out the respCheck while loop")
        printAutoInd(f, "if isTerminateStimEvent ")
        printAutoInd(f, "nextEvFlipReqTime = 0;")
        printAutoInd(f, "break; ")
        printAutoInd(f, "end \n")
        printAutoInd(f, "if isOneTimeCheck ")
        printAutoInd(f, "break; ")
        printAutoInd(f, "end \n")

        printAutoInd(f, "% to give the cpu a little bit break")
        printAutoInd(f, "if ~isOneTimeCheck")
        printAutoInd(f, "WaitSecs(0.001);")
        printAutoInd(f, "end \n")

        printAutoInd(f, "end % while\n")

        printAutoInd(f, "% remove unchecked respDevs")
        printAutoInd(f, "if numel(beChkedRespDevs) > 0")
        printAutoInd(f, "beChkedRespDevs(~[beChkedRespDevs(:).checkStatus]) = [];")
        printAutoInd(f, "end \n")

        printAutoInd(f, "% when no resp && cDur is reached")
        printAutoInd(f, "if numel(beChkedRespDevs) > 0 && secs >= nextEvFlipReqTime")
        printAutoInd(f, "% for resp dev that have rtWindow == 'same as duration' (no need to check this respDev)")
        printAutoInd(f, "cEndDevsIdx  = [beChkedRespDevs(:).rtWindow] == -1;\n")
        # print resp codes
        if nOutPortsNums > 0:
            printAutoInd(f, "sentNoRespCodeDevs = beChkedRespDevs(cEndDevsIdx);")
            printAutoInd(f, "for iRespDev = 1:numel(sentNoRespCodeDevs)")
            printAutoInd(f, "sendTriggerOrMsg(sentNoRespCodeDevs(iRespDev).respCodeDevType, sentNoRespCodeDevs(iRespDev).respCodeDevIdx, sentNoRespCodeDevs(iRespDev).noResp);")
            printAutoInd(f, "end % for")

        printAutoInd(f, "% remove no need to be checked Devs")
        printAutoInd(f, "beChkedRespDevs(cEndDevsIdx) = []; ")
        printAutoInd(f, "end % if\n")

        if outDevCountsDict[Info.DEV_PARALLEL_PORT] > 0:
            printAutoInd(f,
                         "% if cDur less than 0.01 s (barely likely), reset parallel port back to 0, as soon as possible")
            printAutoInd(f, "if cDurs(cWIdx) < 0.01")
            printAutoInd(f, "for iRespDev = 1:numel(beChkedRespDevs)")
            printAutoInd(f, "if beChkedRespDevs(iRespDev).needTobeReset")
            printAutoInd(f,
                         "sendTriggerOrMsg(sentNoRespCodeDevs(iRespDev).respCodeDevType, sentNoRespCodeDevs(iRespDev).respCodeDevIdx, 0);")
            printAutoInd(f, "beChkedRespDevs(iRespDev).needTobeReset = false;")
            printAutoInd(f, "end % if needTobeSet")
            printAutoInd(f, "end % for iRespDev")
            printAutoInd(f, "end % if cFrame Dur less than 10 ms\n")

        printAutoInd(f, "else")
        printAutoInd(f, "detectAbortKey(abortKeyCode);")
        printAutoInd(f, "end % if numel(beChkedRespDevs) > 0\n")


        printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
        iSubFunNum += 1

        # printAutoInd(f, "for iRespDev = 1:numel(beChkedRespDevs) ")
        # printAutoInd(f, "if beChkedRespDevs(iRespDev).checkStatus")
        # printAutoInd(f, "[secs,keyCode,fEvent] = responseCheck(beChkedRespDevs(iRespDev).type,beChkedRespDevs(iRespDev).index);\n")
        #
        # if outDevCountsDict[Info.DEV_PARALLEL_PORT] > 0:
        #     printAutoInd(f, "% reset parallel port back to 0 ")
        #     printAutoInd(f, "if beChkedRespDevs(iRespDev).needTobeReset && (secs - beChkedRespDevs(iRespDev).startTime) > 0.01 % currently set to 10 ms")
        #     if Info.PLATFORM == 'linux':
        #         printAutoInd(f, "lptoutMex(parPort(beChkedRespDevs(iRespDev).respCodeDevIdx).port, 0);")
        #     elif Info.PLATFORM == 'windows':
        #         printAutoInd(f, "io64(io64Obj, parPort(beChkedRespDevs(iRespDev).respCodeDevIdx).port, 0);")
        #     elif Info.PLATFORM == 'mac':
        #         printAutoInd(f, "% currently, under Mac OX we just do nothing for parallel ports")
        #     printAutoInd(f, "beChkedRespDevs(iRespDev).needTobeReset = false;")
        #     printAutoInd(f, "end \n")
        #
        # printAutoInd(f, "if beChkedRespDevs(iRespDev).rtWindow > 0 && (secs - beChkedRespDevs(iRespDev).startTime) > beChkedRespDevs(iRespDev).rtWindow")
        # # print resp codes
        # if nOutPortsNums > 0:
        #     printAutoInd(f, "% send no response trigger")
        #     printAutoInd(f, "sendTriggerOrMsg(beChkedRespDevs(iRespDev).respCodeDevType, beChkedRespDevs(iRespDev).respCodeDevIdx, beChkedRespDevs(iRespDev).noResp);")
        #
        # printAutoInd(f, "beChkedRespDevs(iRespDev).checkStatus = false;")
        # printAutoInd(f, "end % if RT window is not negative and cTime is out of RT Window\n")
        #
        # printAutoInd(f, "if any(keyCodes(beChkedRespDevs(iRespDev).allowAble))")
        # printAutoInd(f, "cFrame.respOnsettime = secs;")
        # printAutoInd(f, "cFrame.rt            = secs - beChkedRespDevs(iRespDev).startTime;")
        # printAutoInd(f, "cFrame.resp          = find(keyCode);\n")
        # printAutoInd(f, "if beChkedRespDevs(iRespDev).respCodeDevType == 82 % 82 is Eyelink eye action")
        # printAutoInd(f,"cFrame.acc = all(ismember(beChkedRespDevs(iRespDev).resp, beChkedRespDevs(iRespDev).corResp));")
        # printAutoInd(f, "else ")
        # printAutoInd(f,"cFrame.acc = all(ismember(beChkedRespDevs(iRespDev).resp, beChkedRespDevs(iRespDev).corResp)) && isEyeActionInROIs(fEvent, beChkedRespDevs(iRespDev));")
        # printAutoInd(f, "end \n")
        #
        # # print resp codes
        # if nOutPortsNums > 0:
        #     printAutoInd(f, "if cFrame.acc")
        #     printAutoInd(f, "sendTriggerOrMsg(beChkedRespDevs(iRespDev).respCodeDevType, beChkedRespDevs(iRespDev).respCodeDevIdx, beChkedRespDevs(iRespDev).right);")
        #     printAutoInd(f, "else")
        #     printAutoInd(f,"sendTriggerOrMsg(beChkedRespDevs(iRespDev).respCodeDevType, beChkedRespDevs(iRespDev).respCodeDevIdx, beChkedRespDevs(iRespDev).wrong);")
        #     printAutoInd(f, "end \n")
        #
        # printAutoInd(f, "evalc([beChkedRespDevs(iRespDev).beUpdatedVar,' = cFrame;']);\n")
        # printAutoInd(f, "beChkedRespDevs(iRespDev).checkStatus = false;")
        #
        # printAutoInd(f, "if beChkedRespDevs(iRespDev).endAction")
        # printAutoInd(f, "isTerminateStimEvent = true; % will break out the while loop soon")
        # printAutoInd(f, "end % end action")
        #
        # printAutoInd(f, "end % if there was a response")
        # printAutoInd(f, "end % if the check switch is on")
        # printAutoInd(f, "end % for iRespDev")
        #
        # printAutoInd(f, "if isOneTimeCheck||isTerminateStimEvent")
        # printAutoInd(f, "break; % break out the while loop")
        # printAutoInd(f, "end % ")
        #
        # printAutoInd(f, "WaitSecs(0.001); % to give the cpu a little bit break ")
        # printAutoInd(f, "end % while")
        #
        # # printAutoInd(f, "%------ remove unchecked respDevs ------/")
        # printAutoInd(f, "% remove unchecked respDevs ")
        # printAutoInd(f, "if ~isempty(beChkedRespDevs)")
        # printAutoInd(f, "beChkedRespDevs(~[beChkedRespDevs(:).checkStatus]) = [];")
        # # printAutoInd(f, "beChkedRespDevs([beChkedRespDevs(:).rtWindow] == -1) = []; % excluded '(Same as duration)' ")
        # printAutoInd(f, "end ")
        # # printAutoInd(f, "%---------------------------------------\\\n")
        #
        # printAutoInd(f, "% rtWindow = same as duration and ")
        # printAutoInd(f, "if numel(beChkedRespDevs) > 0 && secs >= nextEvFlipReqTime")
        # printAutoInd(f, "cEndDevsIdx = beChkedRespDevs(:).rtWindow == -1;")
        # if nOutPortsNums > 0:
        #     printAutoInd(f, "sentNoRespCodeDevs = beChkedRespDevs(cEndDevsIdx);")
        #     printAutoInd(f, "for iRespDev = 1:numel(sentNoRespCodeDevs)")
        #     printAutoInd(f, "sendTriggerOrMsg(sentNoRespCodeDevs(iRespDev).respCodeDevType, sentNoRespCodeDevs(iRespDev).respCodeDevIdx, sentNoRespCodeDevs(iRespDev).noResp);")
        #     printAutoInd(f, "end % for")
        #
        # printAutoInd(f, "beChkedRespDevs(cEndDevsIdx) = []; % remove no need to be checked Devs")
        #
        # printAutoInd(f, "end % if\n")
        #
        # if outDevCountsDict[Info.DEV_PARALLEL_PORT] > 0:
        #     printAutoInd(f, "if cDurs(cWIdx) < 0.01 ")
        #     printAutoInd(f, "for iRespDev = 1:numel(beChkedRespDevs) ")
        #     printAutoInd(f, "if beChkedRespDevs(iRespDev).needTobeReset")
        #     if Info.PLATFORM == 'linux':
        #         printAutoInd(f, "lptoutMex(parPort(beChkedRespDevs(iRespDev).respCodeDevIdx).port, 0);")
        #     elif Info.PLATFORM == 'windows':
        #         printAutoInd(f, "io64(io64Obj, parPort(beChkedRespDevs(iRespDev).respCodeDevIdx).port, 0);")
        #     elif Info.PLATFORM == 'mac':
        #         printAutoInd(f, "% currently, under Mac OX we just do nothing for parallel ports")
        #     printAutoInd(f, "beChkedRespDevs(iRespDev).needTobeReset = false;")
        #     printAutoInd(f, "end % if needTobeSet")
        #     printAutoInd(f, "end % for iRespDev")
        #     printAutoInd(f, "end % if cFrame Dur less than 10 ms\n")
        #
        # printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
        # iSubFunNum += 1

        if outDevCountsDict[Info.DEV_PARALLEL_PORT] > 0:
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: sendTriggerOrMsg", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            printAutoInd(f, "function sendTriggerOrMsg(devType, devIdx, tobeSendInfo)")
            printAutoInd(f, "if ~isempty(devType)")
            printAutoInd(f, "switch devType")
            printAutoInd(f, "case 1 % parallel port")

            if Info.PLATFORM == 'linux':
                printAutoInd(f, "lptoutMex(devIdx,tobeSendInfo);")
            elif Info.PLATFORM == 'windows':
                printAutoInd(f, "io64(io64Obj,devIdx,tobeSendInfo);")
            elif Info.PLATFORM == 'mac':
                printAutoInd(f, "% currently, under Mac OX we just do nothing for parallel ports")

            printAutoInd(f, "case 2 % network port")
            printAutoInd(f, "pnet(devIdx,'write',tobeSendInfo);")
            printAutoInd(f, "case 3 % serial port")
            printAutoInd(f, "IOPort('Write', devIdx,tobeSendInfo);")
            # printAutoInd(f, "[ign, when] = IOPort('Write', devIdx,tobeSendInfo);")
            printAutoInd(f, "otherwise")
            printAutoInd(f, "% do nothing")
            printAutoInd(f, "end%switch ")

            printAutoInd(f, "end % if ~isempty(devType)")

            printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)

            iSubFunNum += 1

        if len(queueDevIdxValueStr) > 0:
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: switchQueue_bcl", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            printAutoInd(f, "function isQueueStart = switchQueue_bcl(queueDevIdx,isQueueStart)")
            printAutoInd(f, "global beChkedRespDevs")
            printAutoInd(f, "if isQueueStart")

            printAutoInd(f, "if isempty(beChkedRespDevs)")
            printAutoInd(f, "KbQueueStop(queueDevIdx);")
            printAutoInd(f, "isQueueStart = false;")
            printAutoInd(f, "end ")

            printAutoInd(f, "else")

            printAutoInd(f, "if ~isempty(beChkedRespDevs)")
            printAutoInd(f, "devIsQueue = [beChkedRespDevs(:).isQueue];")
            printAutoInd(f, "if any(devIsQueue)")
            printAutoInd(f, "KbQueueStart(queueDevIdx);")
            printAutoInd(f, "isQueueStart = true;")
            printAutoInd(f, "end %any(devIsQueue)")

            printAutoInd(f, "end ")

            printAutoInd(f, "end %isQueueStart")

            # printAutoInd(f, "if numel(beChkedRespDevs) > 0")
            # printAutoInd(f, "devIsQueue = [beChkedRespDevs(:).isQueue];")
            #
            # printAutoInd(f, "if any(devIsQueue)")
            # printAutoInd(f, "% update the allowed key list")
            # printAutoInd(f, "KbQueueCreate(queueDevIndex,[beChkedRespDevs(devIsQueue).allowAble]);")
            # printAutoInd(f, "end ")
            # printAutoInd(f, "else ")
            # printAutoInd(f, "KbQueueStop(queueDevIndex);")
            # printAutoInd(f, "KbQueueFlush(queueDevIndex);")
            # printAutoInd(f, "end ")

            printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)

            iSubFunNum += 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: detectAbortKey", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f, "function detectAbortKey(abortKeyCode)")
        printAutoInd(f, "[keyIsDown, ~, keyCode] = KbCheck(-1);")
        printAutoInd(f, "if keyIsDown && keyCode(abortKeyCode)")
        printAutoInd(f, "error('The program was aborted ...!');")
        printAutoInd(f, "end ")

        printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)

        iSubFunNum += 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: disableSomeKeys", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f, "function disableSomeKbKeys()")

        enabledKBKeysSet = enabledKBKeysSet.difference({'', '0'})
        # enabledKBKeysSet = set(enabledKBKeysSet)
        # printAutoInd(f, "{0}{1}{2}\n", "RestrictKeysForKbCheck(unique([",
        #              ''.join(cItem + ", " for cItem in enabledKBKeysList)[:-2], "]));")
        if len(enabledKBKeysSet) == 1:
            printAutoInd(f, "RestrictKeysForKbCheck(unique({0}));\n",
                         ''.join(cItem + ", " for cItem in enabledKBKeysSet)[:-2])
        else:
            printAutoInd(f, "RestrictKeysForKbCheck(unique([{0}]));\n",
                         ''.join(cItem + ", " for cItem in enabledKBKeysSet)[:-2])
        printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)

        iSubFunNum += 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: makeFrameRect", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f, "function outRect = makeFrameRect(x, y, frameWidth, frameHeight, fullRect)")
        printAutoInd(f, "if x <= 0")
        printAutoInd(f, "x = -x*fullRect(3);")
        printAutoInd(f, "end % if")

        printAutoInd(f, "if y <= 0")
        printAutoInd(f, "y = -y*fullRect(4);")
        printAutoInd(f, "end % if")

        printAutoInd(f, "if frameWidth <= 0")
        printAutoInd(f, "frameWidth = -frameWidth*fullRect(3);")
        printAutoInd(f, "end % if")

        printAutoInd(f, "if frameHeight <= 0")
        printAutoInd(f, "frameHeight = -frameHeight*fullRect(4);")
        printAutoInd(f, "end % if")

        printAutoInd(f, "outRect = CenterRectOnPointd([0, 0, frameWidth, frameHeight], x, y);")

        printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)

        iSubFunNum += 1

        # only print out this fun when there exist Cycle
        allCycleWidgetList = getAllEventWidgetsList(2)

        if len(allCycleWidgetList) > 0:
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: ShuffleCycleOrder", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

            printAutoInd(f, "function cShuffledIdx = ShuffleCycleOrder(nRows,orderStr,orderByStr,subInfo)")
            printAutoInd(f, "cShuffledIdx = 1:nRows;")
            printAutoInd(f, "switch orderStr")
            printAutoInd(f, "case 'Sequential'")
            printAutoInd(f, "% do nothing")

            printAutoInd(f, "case 'Random without Replacement'")
            printAutoInd(f, "cShuffledIdx = Shuffle(cShuffledIdx);")

            printAutoInd(f, "case 'Random with Replacement'")
            printAutoInd(f, "cShuffledIdx = Randi(nRows,[nRows,1]);")

            printAutoInd(f, "case 'Counter Balance'")
            printAutoInd(f, "switch orderByStr")
            printAutoInd(f, "case 'N/A'")

            printAutoInd(f, "case 'Subject'")
            printAutoInd(f, "cCBRow = rem(str2double(subInfo.num),nRows);")
            printAutoInd(f, "if cCBRow == 0")
            printAutoInd(f, "cCBRow = nRows;")
            printAutoInd(f, "end")
            printAutoInd(f, "cShuffledIdx = cShuffledIdx(cCBRow);")

            printAutoInd(f, "case 'Session'")
            printAutoInd(f, "cCBRow = rem(str2double(subInfo.session),nRows);")
            printAutoInd(f, "if cCBRow == 0")
            printAutoInd(f, "cCBRow = nRows;")
            printAutoInd(f, "end")
            printAutoInd(f, "cShuffledIdx = cShuffledIdx(cCBRow);")

            printAutoInd(f, "case 'Run'")
            printAutoInd(f, "cCBRow = rem(str2double(subInfo.num),nRows);")
            printAutoInd(f, "if cCBRow == 0")
            printAutoInd(f, "cCBRow = nRows;")
            printAutoInd(f, "end")
            printAutoInd(f, "cShuffledIdx = cShuffledIdx(cCBRow);")

            printAutoInd(f, "otherwise")
            printAutoInd(f, "error('Order By should be of {{''Run'',''Subject'',''Session'',''N/A''}}');")
            printAutoInd(f, "end%switch ")

            printAutoInd(f, "otherwise")
            printAutoInd(f,
                         "error('order methods should be of {{''Sequential'',''Random without Replacement'',''Random with Replacement'',''Counter Balance''}}');")
            printAutoInd(f, "end%switch ")

            printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)

            iSubFunNum += 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: getDurValue", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "function cDur = getDurValue(cDur,cIFI, isSound)")
        printAutoInd(f, "if nargin < 3")
        printAutoInd(f, "isSound = false;")
        printAutoInd(f, "end")

        # printAutoInd(f, "if numel(cDur) == 1 && cDur == 0")
        # printAutoInd(f, "return;")
        # printAutoInd(f, "end")

        printAutoInd(f, "if numel(cDur) > 1")
        printAutoInd(f, "cDur = rand*(cDur(2) - cDur(1)) + cDur(1);")
        printAutoInd(f, "end ")
        printAutoInd(f, "cDur = cDur./1000; % transform the unit from ms to sec")

        printAutoInd(f, "if ~isSound")
        printAutoInd(f, "cDur = round(cDur/cIFI)*cIFI;")
        printAutoInd(f, "end ")

        printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)

        iSubFunNum += 1

        if iQuest > 1:
            # printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            # printAutoInd(f, "% subfun {0}: getQuestValue", iSubFunNum)
            # printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            # printAutoInd(f, "function quest = getQuestValue(quest)")
            # printAutoInd(f, "if quest.isLog10Trans")
            # printAutoInd(f, "quest.cValue = 10^quest.cValue;")
            # printAutoInd(f, "end ")
            # printAutoInd(f, "quest.cValue = max(quest.cValue,quest.minValue);")
            # printAutoInd(f, "quest.cValue = min(quest.cValue,quest.maxValue);")
            # printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
            #
            # iSubFunNum += 1

            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: getQuestValue", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "function quest = getQuestValue(quest)")
            printAutoInd(f, "% 1,2,3 for quantile, mean, and mode, respectively")
            printAutoInd(f, "switch quest.method")
            printAutoInd(f, "case 1")
            printAutoInd(f, "quest = QuestQuantile(quest);")
            printAutoInd(f, "case 2")
            printAutoInd(f, "quest = QuestMean(quest);")
            printAutoInd(f, "case 3")
            printAutoInd(f, "quest = QuestMode(quest);")
            printAutoInd(f, "otherwise")
            printAutoInd(f, "error('Quest method should be of [1,2,3] for Quantile, mean, and mode, respectively');")
            printAutoInd(f, "end%switch ")
            printAutoInd(f, "if quest.isLog10Trans")
            printAutoInd(f, "quest.cValue = 10^quest.cValue;")
            printAutoInd(f, "end ")
            printAutoInd(f, "quest.cValue = max(quest.cValue,quest.minValue);")
            printAutoInd(f, "quest.cValue = min(quest.cValue,quest.maxValue);")
            printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)

            iSubFunNum += 1

            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: updateQuestValue", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "function quest = updateQuestValue(quest,stimIntensity,response)")
            printAutoInd(f, "if quest.isLog10Trans")
            printAutoInd(f, "stimIntensity = log10(stimIntensity);")
            printAutoInd(f, "end ")
            printAutoInd(f, "quest = QuestUpdate(quest,stimIntensity,response);")
            printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)

            iSubFunNum += 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: makeRespStruct", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "function makeRespStruct(beUpdatedVar,allowAble,corResp,rtWindow,endAction,"
                        "devType,index,isQueue,lastScrOnsettime,checkStatus,needTobeReset,right,wrong,noResp,respCodeDevType,"
                        "respCodeDevIdx,startRect,endRect,meanRect,isOval)")
        printAutoInd(f, "global beChkedRespDevs  %#ok<*REDEF>")
        printAutoInd(f, "% currently this method is not so beautiful, but it's faster than the struct function")
        printAutoInd(f, "cIdx = numel(beChkedRespDevs) + 1;")
        printAutoInd(f, "beChkedRespDevs(cIdx).beUpdatedVar     = beUpdatedVar; %#ok<*STRNU>")
        printAutoInd(f, "beChkedRespDevs(cIdx).allowAble        = allowAble;")
        printAutoInd(f, "beChkedRespDevs(cIdx).corResp          = corResp;")
        printAutoInd(f, "beChkedRespDevs(cIdx).rtWindow         = rtWindow;")
        printAutoInd(f, "beChkedRespDevs(cIdx).endAction        = endAction;")
        printAutoInd(f, "beChkedRespDevs(cIdx).type             = devType;")
        printAutoInd(f, "beChkedRespDevs(cIdx).index            = index;")
        printAutoInd(f, "beChkedRespDevs(cIdx).isQueue          = isQueue;")
        printAutoInd(f, "beChkedRespDevs(cIdx).startTime        = lastScrOnsettime;")
        printAutoInd(f, "beChkedRespDevs(cIdx).checkStatus      = checkStatus;")
        printAutoInd(f, "beChkedRespDevs(cIdx).needTobeReset    = needTobeReset;")
        printAutoInd(f, "beChkedRespDevs(cIdx).right            = right;")
        printAutoInd(f, "beChkedRespDevs(cIdx).wrong            = wrong;")
        printAutoInd(f, "beChkedRespDevs(cIdx).noResp           = noResp;")
        printAutoInd(f, "beChkedRespDevs(cIdx).respCodeDevType  = respCodeDevType;")
        printAutoInd(f, "beChkedRespDevs(cIdx).respCodeDevIdx   = respCodeDevIdx;")
        printAutoInd(f, "beChkedRespDevs(cIdx).start            = startRect;")
        printAutoInd(f, "beChkedRespDevs(cIdx).end              = endRect;")
        printAutoInd(f, "beChkedRespDevs(cIdx).mean             = meanRect;")
        printAutoInd(f, "beChkedRespDevs(cIdx).isOval           = isOval;")
        printAutoInd(f, "%beChkedRespDevs(cIdx).onsettime        = [];")
        printAutoInd(f, "%beChkedRespDevs(cIdx).resp             = [];")
        printAutoInd(f, "end %  end of subfun{0}", iSubFunNum)

        iSubFunNum += 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: responseCheck", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "function [secs, keyCode, fEventOr1stRelease]= responseCheck(respDevType,respDevIndex,isQueue)")
        if isEyelink:
            printAutoInd(f,"global tracker2PtbTimeCoefs")

        printAutoInd(f,"% respDevType 1,2,3,4,82 for keyboard, mouse, gamepad, response box and Eyelink eye action, respectively")
        printAutoInd(f, "fEventOr1stRelease = [];")
        printAutoInd(f, "switch respDevType")

        if Info.PLATFORM == 'windows':
            printAutoInd(f, "case 3 % under windows, check it via joystickMex")
            printAutoInd(f, "status    = joystickMex(respDevIndex); % index starts from 0")
            printAutoInd(f, "keyCode   = bitget(status(5),1:8);")
            printAutoInd(f, "secs      = GetSecs;")
            printAutoInd(f, "keyIsDown = any(keyCode);")

        printAutoInd(f, "case 4 % for Cedrus's response boxes")
        printAutoInd(f, "status    = CedrusResponseBox('FlushEvents', respDevIndex);")
        printAutoInd(f, "keyCode   = status(1,:);")
        printAutoInd(f, "secs      = GetSecs;")
        # printAutoInd(f, "keyIsDown = any(keyCode);")

        printAutoInd(f, "case 82 % for Eyekink eye action")
        printAutoInd(f, "isEyelinkOnline = Eyelink('CheckRecording');")
        printAutoInd(f, "if (isEyelinkOnline~=0)")
        printAutoInd(f, "error('Eyelink is not online!')")
        printAutoInd(f, "end \n")

        printAutoInd(f, "cDataType = Eyelink('GetNextDataType');")
        printAutoInd(f,
                     "% 3:9 for startBlink, endBlink, startSacc, end Sacc, startFix, endFix, and fixUpdate, respectively")
        printAutoInd(f, "if ismember(cDataType, 3:9)")
        printAutoInd(f, "fEventOr1stRelease = Eyelink('GetFloatData', cDataType);")
        printAutoInd(f, "keyCode = bitget(cDataType,1:9);")
        printAutoInd(f, "else")

        printAutoInd(f, "keyCode = zeros(1,9);")
        printAutoInd(f, "end \n")
        printAutoInd(f, "secs = GetSecs;")
        printAutoInd(f, "fEventOr1stRelease.time = tracker2PtbTimeCoefs(1) + tracker2PtbTimeCoefs(2)*fEventOr1stRelease.time;")
        # printAutoInd(f, "keyIsDown = any(keyCode);")

        printAutoInd(f, "otherwise % keyboard or mouse or gamepad (except for window OS)")
        printAutoInd(f, "if isQueue")
        printAutoInd(f, "[~, keyCode, fEventOr1stRelease] = KbQueueCheck(respDevIndex);")
        printAutoInd(f, "secs = GetSecs;")
        printAutoInd(f, "else")
        printAutoInd(f, "[~, secs, keyCode] = KbCheck(respDevIndex);")
        printAutoInd(f, "end ")
        printAutoInd(f, "end%switch \n")

        printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
        iSubFunNum += 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: makeImDestRect", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "function [dRect, sRect] = makeImDestRect(fRect,imDataSize,stretchMode)\n")
        printAutoInd(f, "sRect = [0 0 imDataSize(2) imDataSize(1)];")
        printAutoInd(f, "dRect   = CenterRect(sRect, fRect);")

        printAutoInd(f, "% calculate the width:")
        printAutoInd(f, "if ismember(stretchMode,[1 3])")
        printAutoInd(f, "dRect([1,3]) = fRect([1,3]);")
        printAutoInd(f, "end ")

        printAutoInd(f, "% calculate the height")
        printAutoInd(f, "if ismember(stretchMode,[2 3])")
        printAutoInd(f, "dRect([2,4]) = fRect([2,4]);")
        printAutoInd(f, "end")

        printAutoInd(f, "% in case of no stretch and the imData is larger than fRect")
        printAutoInd(f, "if stretchMode == 0")
        printAutoInd(f, "dRect = ClipRect(dRect, fRect);")
        # printAutoInd(f, "destWidth  = RectWidth(dRect);")
        # printAutoInd(f, "destHeight = RectHeight(dRect);\n")
        #
        # printAutoInd(f, "if destWidth < imDataSize(2)")
        # printAutoInd(f, "halfShrinkWPixes = (imDataSize(2) - destWidth)/2;\n")
        # printAutoInd(f, "sRect([1,3]) = sRect([1,3]) + [floor(halfShrinkWPixes), -ceil(halfShrinkWPixes)];")
        # printAutoInd(f, "dRect([1,3])    = fRect([1,3]);")
        # printAutoInd(f, "end ")
        #
        # printAutoInd(f, "if destHeight < imDataSize(1)")
        # printAutoInd(f, "halfShrinkHPixes = (imDataSize(1) - destHeight)/2;\n")
        # printAutoInd(f, "sRect([2,4]) = sRect([2,4]) + [floor(halfShrinkHPixes), -ceil(halfShrinkHPixes)];")
        # printAutoInd(f, "dRect([2,4])    = fRect([2,4]);")
        # printAutoInd(f, "end ")

        printAutoInd(f, "end % if stretchMode")
        printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
        iSubFunNum += 1

        if haveGaborStim:
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: makeGabor_bcl", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f,
                         "function stim = makeGabor_bcl(spFreq,Contrast,phase,orientation,pixsPerDeg,bkColor,stimSize,periodsCoveredByOneStandardDeviation)")
            printAutoInd(f,
                         "% function stim = makeGabor_bcl(spFreq,Contrast,phase,orientation,pixsPerDeg,bkColor,stimSize,periodsCoveredByOneStandardDeviation)")
            printAutoInd(f, "%")
            printAutoInd(f, "% argins:")
            printAutoInd(f, "% ")
            printAutoInd(f, "% spFreq      [double] : spatial frequency of the gratting cpd")
            printAutoInd(f, "% Contrast    [double] : Contrast of the gratting 0~1 [1]")
            printAutoInd(f, "% phase       [double] : phase of the gratting [0] ")
            printAutoInd(f, "% orientation [double] : orientation of the gratting [0] ")
            printAutoInd(f, "% pixsPerDeg  [double] : pixels per visual degree")
            printAutoInd(f, "% bkColor     [RGB]    : rgb values of the backgroud color")
            printAutoInd(f, "% stimSize    [double] : full stim size ")
            printAutoInd(f, "% periodsCoveredByOneStandardDeviation [double]:")
            printAutoInd(f, "% To enlarge the gaussian mask, increase periodsCoveredByOneStandardDeviation.")
            printAutoInd(f, "% ")
            printAutoInd(f, "% outargs:")
            printAutoInd(f, "% ")
            printAutoInd(f,
                         "% stim    [stimSize, stimsize, numel(bkColor)]: a 2D (Gray color) or 3D matrix (RGB) with values from 0 to 255")
            printAutoInd(f, "% ")
            printAutoInd(f, " % Written by Yang Zhang Sat Apr 16 23:00:04 2016")
            printAutoInd(f, " % Soochow University, China")
            printAutoInd(f, " ")
            printAutoInd(f, " % pixelsPerPeriod% How many pixels will each period/cycle occupy?")
            printAutoInd(f, "pixelsPerPeriod    = (1/spFreq)*pixsPerDeg;")
            printAutoInd(f, " ")
            printAutoInd(f, "gaussianSpaceConstant = periodsCoveredByOneStandardDeviation * pixelsPerPeriod;")
            printAutoInd(f, " ")
            printAutoInd(f, "% *** If the grating is clipped on the sides, increase stimSize.")
            printAutoInd(f, "if mod(stimSize,2)")
            printAutoInd(f, "stimSize = stimSize - 1;")
            printAutoInd(f, "end")
            printAutoInd(f, "halfWidthOfGrid = stimSize / 2;")
            printAutoInd(f,
                         "widthArray      = (-halfWidthOfGrid) : halfWidthOfGrid-1;  % widthArray is used in creating the meshgrid.")
            printAutoInd(f, "[x,y]           = meshgrid(widthArray, widthArray);")
            printAutoInd(f, " ")
            printAutoInd(f, "cicleMask = (x/halfWidthOfGrid).^2 + (y/halfWidthOfGrid).^2;")
            printAutoInd(f, "cicleMask = cicleMask >= 1;")
            printAutoInd(f, " ")
            printAutoInd(f,
                         "circularGaussianMaskMatrix            = exp(-((x .^ 2) + (y .^ 2)) / (gaussianSpaceConstant ^ 2));")
            printAutoInd(f, "circularGaussianMaskMatrix(cicleMask) = 0;")
            printAutoInd(f, " ")
            printAutoInd(f, "f = 2*pi*spFreq/pixsPerDeg;")
            printAutoInd(f, "a = cos(orientation)*f;")
            printAutoInd(f, "b = sin(orientation)*f;")
            printAutoInd(f, " ")
            printAutoInd(f, "layer = 255.*circularGaussianMaskMatrix.*(cos(a*x+b*y+phase)*Contrast+1)/2;	")
            printAutoInd(f, "stim  = repmat(layer,[1 1 numel(bkColor)]);")
            printAutoInd(f, " ")
            printAutoInd(f, "for iDim = 1:numel(bkColor)")
            printAutoInd(f, "stim(:,:,iDim) = stim(:,:,iDim) + (1-circularGaussianMaskMatrix).*bkColor(iDim);")
            printAutoInd(f, "end")
            printAutoInd(f, "% stim  = stim + (1-circularGaussianMaskMatrix).*bkColor(1);")
            printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
            iSubFunNum += 1

        if iSound > 1:
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: getOptimizedSoundDev", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "function soundDevs = getOptimizedSoundDev()")

            if Info.PLATFORM == 'linux':
                printAutoInd(f, "% the first choice: ALSA excellent")
                printAutoInd(f, "soundDevs = PsychPortAudio('GetDevices',8);")

                printAutoInd(f, "% the second choice: JACK excellent")
                printAutoInd(f, "if isempty(soundDevs)")
                printAutoInd(f, "soundDevs = PsychPortAudio('GetDevices',12);")
                printAutoInd(f, "end ")

                printAutoInd(f, "% OSS is less capable but not very widespread in use anymore")
                printAutoInd(f, "if isempty(soundDevs)")
                printAutoInd(f, "soundDevs = PsychPortAudio('GetDevices',12);")
                printAutoInd(f, "end ")

            elif Info.PLATFORM == 'windows':
                printAutoInd(f, "% WASAPI it's ok")
                printAutoInd(f, "soundDevs = PsychPortAudio('GetDevices',13);")

                printAutoInd(f, "% WdMKS it's ok")
                printAutoInd(f, "if isempty(soundDevs)")
                printAutoInd(f, "soundDevs = PsychPortAudio('GetDevices',11);")
                printAutoInd(f, "end ")

                printAutoInd(f, "% DirectSound: the next worst")
                printAutoInd(f, "if isempty(soundDevs)")
                printAutoInd(f, "soundDevs = PsychPortAudio('GetDevices',1);")
                printAutoInd(f, "end ")

                printAutoInd(f, "% MME: A completely unusable API")
                printAutoInd(f, "if isempty(soundDevs)")
                printAutoInd(f, "soundDevs = PsychPortAudio('GetDevices',2);")
                printAutoInd(f, "end ")
            else:
                printAutoInd(f, "soundDevs = PsychPortAudio('GetDevices',5);")

            printAutoInd(f, "if isempty(soundDevs)")
            printAutoInd(f, "error('failed to get any sound device!');")
            printAutoInd(f, "end \n")
            printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)

            iSubFunNum += 1

        if isEyelink:
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: initEyelink", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "function el = initEyelink(winIds, monitors, edfFile)")

            # 1) get the win id info in matlab format winIds(idNum)
            shouldNotBeCitationCheck('Screen', cEyeTrackerProperty.get('Screen'))

            cScreenName = cEyeTrackerProperty.get('Screen')

            cWinIdx = outputDevNameIdxDict.get(cScreenName)
            cWinStr = f"winIds({cWinIdx})"

            printAutoInd(f, "% Initialization of the connection with the Eyelink Gazetracker.")
            printAutoInd(f, "el = EyelinkInitDefaults({0});", cWinStr)
            printAutoInd(f, "el.backgroundcolour = monitors({0}).bkColor;", cWinIdx)
            printAutoInd(f, "el.subjectGamepad = 1;\n")
            printAutoInd(f, "% open file to record data to")
            printAutoInd(f, "cEdfId = Eyelink('Openfile', edfFile);")
            printAutoInd(f, "if cEdfId~=0")
            # printAutoInd(f, "cleanup;")
            printAutoInd(f, "error('Cannot create EDF file ''%s'' ', edfFile);")
            printAutoInd(f, "end")
            printAutoInd(f, "% make sure we're still connected.")

            printAutoInd(f, "if Eyelink('IsConnected')~=1")
            printAutoInd(f, "error('eyetracker is disconnected!');")
            printAutoInd(f, "end")

            printAutoInd(f, "Eyelink('command', 'add_file_preamble_text ''Recorded for experiment {0}''');",
                         cFilenameOnly)
            """
            todo list
            """
            physSizeList = parsePhysicSize(getDevPropertyValue(output_devices, cScreenName, 'Physic Size'))
            physDisList = parsePhysicSize(getDevPropertyValue(output_devices, cScreenName, 'Viewing Distance'))

            if len(physSizeList) > 1:
                printAutoInd(f, "Eyelink('command','screen_phys_coords = %ld %ld %ld %ld',"
                                " round(-{0}/2),round({1}/2),round({0}/2),round(-{1}/2)); % in mm\n",
                             physSizeList[0], physSizeList[1])

            if physDisList[0] != 'NaN':
                if len(physDisList) == 1:
                    printAutoInd(f, "Eyelink('command','simulation_screen_distance = %ld',{0});% in mm\n",
                                 physDisList[0])
                else:
                    printAutoInd(f, "Eyelink('command','simulation_screen_distance = %ld',{0},{1});% in mm\n",
                                 physDisList[0], physDisList[1])

            if cEyeTrackerProperty['Pupil Size Mode'] == 'area':
                printAutoInd(f, "Eyelink('command','pupil_size_diameter = NO');")
            else:
                printAutoInd(f, "Eyelink('command','pupil_size_diameter = YES');")

            velThrStr = cEyeTrackerProperty.get('Saccade Velocity Threshold', '30')
            if velThrStr == '':
                velThrStr = 30

            accelThrStr = cEyeTrackerProperty.get('Saccade Acceleration Threshold', '9500')
            if accelThrStr == '':
                accelThrStr = 9500

            printAutoInd(f, "Eyelink('command','saccade_velocity_threshold = ',{0});% in vd/s", velThrStr)
            printAutoInd(f, "Eyelink('command','saccade_acceleration_threshold = ',{0});%in vd/s/s\n", accelThrStr)

            printAutoInd(f, "%retrieve tracker version and tracker software version")
            printAutoInd(f, "[v,vs] = Eyelink('GetTrackerVersion');")
            printAutoInd(f, "vsn = regexp(vs,'\d','match');")
            printAutoInd(f, "if v ==3 && str2double(vsn{{1}}) == 4 % if Eyelink 1000 and tracker version 4.xx")
            printAutoInd(f, "% remote mode possible add HTARGET ( head target)")
            printAutoInd(f,
                         "Eyelink('command', 'file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT');")
            printAutoInd(f,
                         "Eyelink('command', 'file_sample_data  = LEFT,RIGHT,GAZE,HREF,AREA,GAZERES,STATUS,INPUT,HTARGET');")
            printAutoInd(f, "% set link data (used for gaze cursor)")
            printAutoInd(f,
                         "Eyelink('command', 'link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,FIXUPDATE,INPUT');")
            printAutoInd(f,
                         "Eyelink('command', 'link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT,HTARGET');")
            printAutoInd(f, "else")
            printAutoInd(f,
                         "Eyelink('command', 'file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT');")
            printAutoInd(f, "Eyelink('command', 'file_sample_data  = LEFT,RIGHT,GAZE,HREF,AREA,GAZERES,STATUS,INPUT');")
            printAutoInd(f, "% set link data (used for gaze cursor)")
            printAutoInd(f,
                         "Eyelink('command', 'link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,FIXUPDATE,INPUT');")
            printAutoInd(f, "Eyelink('command', 'link_sample_data  = LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT');")
            printAutoInd(f, "end")
            printAutoInd(f, "Eyelink('command', 'button_function 5 \"accept_target_fixation\"');\n")

            printAutoInd(f, "mappingEyelinkPtbTime;")

            printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
            iSubFunNum += 1

            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: mappingEyelinkPtbTime", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "function mappingEyelinkPtbTime()")
            printAutoInd(f, "global tracker2PtbTimeCoefs")
            printAutoInd(f, "testTimes = 50;")
            printAutoInd(f, "ptbTimes = zeros(testTimes,1);")
            printAutoInd(f, "trackerTimes = zeros(testTimes,1);")
            printAutoInd(f, "for iTime = 1:testTimes")
            printAutoInd(f, "beforeTime = GetSecs;")
            printAutoInd(f, "trackerTimes(iTime) = Eyelink('TrackerTime');")
            printAutoInd(f, "afterTime = GetSecs;")
            printAutoInd(f, "ptbTimes(iTime) = mean(beforeTime,afterTime);")
            printAutoInd(f, "tracker2PtbTimeCoefs = regress(ptbTimes,[ones(testTimes,1),trackerTimes]);")


            printAutoInd(f, "end ")

            printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
            iSubFunNum += 1



            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: eyelinkLog", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "function eyelinkLog(logVarNames, logVarValues, waitTime)")
            printAutoInd(f, "for iVar = 1:numel(logVarNames)")
            printAutoInd(f, "if waitTime > 0")
            printAutoInd(f, "WaitSecs(waitTime);")
            printAutoInd(f, "end")
            printAutoInd(f, "% Only chars and ints allowed in arguments of Eyelink('Message');")
            printAutoInd(f, "if ischar(logVarValues(iVar))")
            printAutoInd(f, "% for char")
            printAutoInd(f, "Eyelink('Message', ['!V TRIAL_VAR ',logVarNames{{iVar}},' %s'],logVarValues{{iVar}} );")
            printAutoInd(f, "elseif isfloat(logVarValues(iVar))")
            printAutoInd(f, "if logVarValues(iVar) == fix(logVarValues(iVar)) ")
            printAutoInd(f, "% for int")
            printAutoInd(f, "Eyelink('Message', ['!V TRIAL_VAR ',logVarNames{{iVar}},' %d'],logVarValues{{iVar}} );")
            printAutoInd(f, "else")
            printAutoInd(f, "% for float")
            printAutoInd(f,
                         "Eyelink('Message', ['!V TRIAL_VAR ',logVarNames{{iVar}},' %ld'],round(logVarValues{{iVar}}*1000) );")
            printAutoInd(f, "end")
            printAutoInd(f, "end")

            printAutoInd(f, "end % for iBeSentVar")
            printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
            iSubFunNum += 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: isEyeActionInROIs", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "function isInROIs = isEyeActionInROIs(fEvent, respDevs)")
        printAutoInd(f, "iEye = fEvent.eye + 1; % 0 1 for left and right")

        printAutoInd(f,
                     "isInROIs = isInRect_bcl(fEvent.gstx(iEye),fEvent.gsty(iEye),respDevs.start, respDevs.isOval) &...\n"
                     "           isInRect_bcl(fEvent.genx(iEye),fEvent.geny(iEye),respDevs.end, respDevs.isOval) &...\n"
                     "           isInRect_bcl(fEvent.gavx(iEye),fEvent.gavy(iEye),respDevs.mean, respDevs.isOval);")
        printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
        iSubFunNum += 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: isInRect_bcl", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "function isInRectArea = isInRect_bcl(x, y, cRect, isOval)")
        printAutoInd(f, "if numel(cRect) ~= 4")
        printAutoInd(f, "isInRectArea = true;")
        printAutoInd(f, "else")

        printAutoInd(f, "if isOval")
        printAutoInd(f, "[cx, cy] = RectCenterd(cRect);")
        # printAutoInd(f, "w = RectWidth(cRect)/2;")
        # printAutoInd(f, "h = RectHeight(cRect)/2;")
        printAutoInd(f, "isInRectArea = all(((x - cx)/RectWidth(cRect)).^2 + ((y - cy)/RectHeight(cRect)).^2 <= 0.25);")
        # printAutoInd(f, "isInRectArea = ((x - cx)/w)^2 + ((y - cy)/h)^2 <= 1;")
        printAutoInd(f, "else")
        printAutoInd(f, "isInRectArea = IsInRect(x, y, cRect);")
        printAutoInd(f, "end")

        printAutoInd(f, "end")

        printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
        iSubFunNum += 1

        if haveSnowStim:
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: makeSnow_bcl", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "function stim = makeSnow_bcl(stimWidth, stimHeight, scaleEf)")
            printAutoInd(f, " stim = rand(round([stimHeight, stimWidth]/scaleEf)) * 255;")
            printAutoInd(f, "end %  end of subfun{0}\n", iSubFunNum)
            iSubFunNum += 1

    # copy yanglab's supplementary files
    copyYanglabFile('subjectinfo.p')
    copyYanglabFile('OpenExp_BCL.p')
    copyYanglabFile('OverwriteOrNot.p')

    if Info.PLATFORM == 'windows':
        copyYanglabFile('ShowHideWinTaskbar.p')
        copyYanglabFile('ShowHideWinStartButtonMex.mexw64')
        copyYanglabFile('ShowHideWinTaskbarAndButtonMex.mexw64')

    if outDevCountsDict[Info.DEV_PARALLEL_PORT] > 0 and Info.PLATFORM == 'linux':
        copyYanglabFile('lptOut.p')
        copyYanglabFile('lptoutMex.mexa64')



    if not isDummyPrint:
        Func.printOut(f"Compile successful!:{compile_file_name}",1)  # print info to the output panel
