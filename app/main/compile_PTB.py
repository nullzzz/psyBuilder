import os
import sys
import datetime
import re

from PyQt5.QtCore import Qt, QSettings, QTimer, QPropertyAnimation
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QFileDialog, QMessageBox

from app.attributes.main import Attributes
from app.center.main import Center
from app.center.widget_tabs.events.cycle.main import Cycle
from app.center.widget_tabs.events.durationPage import DurationPage
from app.center.widget_tabs.timeline.main import Timeline
from app.deviceSelection.IODevice.globalDevices import GlobalDevice
from app.deviceSelection.progressBar import LoadingTip
from app.func import Func
from app.info import Info
from app.output.main import Output
from app.properties.main import Properties
from app.structure.main import Structure
from lib.wait_dialog import WaitDialog

cIndents = 0
isPreLineSwitch = 0
enabledKBKeysList = set()
isDummyPrint = False
spFormatVarDict = dict()
inputDevNameIdxDict = dict()
outputDevNameIdxDict = dict()
historyPropDict = dict()
cInfoDict = dict()


def throwCompileErrorInfo(inputStr):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowIcon(QIcon(Func.getImage("icon.png")))

    msg.setText(inputStr)
    msg.setWindowTitle("    Attention!   ")

    msg.setStandardButtons(QMessageBox.Ok)
    # msg.setInformativeText("This is additional information")
    # msg.setDetailedText("The details are as follows:")
    # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    # msg.buttonClicked.connect(msgbtn)
    msg.exec_()
    raise Exception(inputStr)


def debugPrint(input):
    isDebug = False

    if isDebug:
        print(input)


#
# def dontClearAfterTransStr(inputStr):
#     if inputStr == "'clear_0'":
#         inputStr = "0"
#     elif inputStr == "'notClear_1'":
#         inputStr = "1"
#     elif inputStr == "'doNothing_2'":
#         inputStr = "2"
#
#     return inputStr


def pyStr2MatlabStr(inputStr):
    #
    if isinstance(inputStr, str):
        if isSingleQuotedStr(inputStr):
            inputStr = inputStr[1:-1]

        inputStr = re.sub("'", "''", inputStr)
        inputStr = "\\n".join(inputStr.split("\n"))# replace the \n with \\n so that we chould print it with \n to matlab
        # inputStr = re.sub(r"\\\%","%",inputStr)
    return inputStr


# def parseDurationStr(cWidget,attributesSetDict):
#     isInfiniteDur = False
#
#     cRefedValue, isRef,valueSet = getRefValueSet(cWidget, cWidget.getDuration(), attributesSetDict)
#     duration                    = dataStrConvert(cRefedValue, isRef)
#
#     if isRef:
#         #----- check ref values -----/
#         for value in valueSet:
#             if isinstance(value, str):
#                 value = removeSingleQuotes(value)
#                 if value == "(Infinite)" :
#                     pass
#                 elif re.fullmatch("\d+~\d+", value):
#                     pass
#                 else:
#                     throwCompileErrorInfo(
#                         "Duration (ms) should be of: (Infinite), an int number,\n or an int range: startNum(int)~endNum(int) !!")
#         #----------------------------\
#     else:
#         if isinstance(duration,str):
#             duration = removeSingleQuotes(duration)
#
#             if duration == "(Infinite)":
#                 isInfiniteDur = True
#             elif re.fullmatch("\d+~\d+",duration):
#                 duration = duration.split('~')
#                 cRefedValue = f"Randi({int(duration[1])-int(duration[0]) +1}) + {int(duration[0])-1}"
#             else:
#                 throwCompileErrorInfo("Duration (ms) should be of ('Infinite'), an int number,\n or an int range: startNum(int)~endNum(int) !!")
#
#     return cRefedValue,isInfiniteDur,isRef
#
# def parseTransStr(inputStr):
#     if isinstance(inputStr,str):
#         if isPercentStr(inputStr):
#             outputValue = float(inputStr[:-1])/-100
#         elif isNumStr(inputStr):
#             outputValue = float(inputStr)
#         else:
#             outputValue = inputStr
#     else:
#         outputValue = inputStr
#
#     return outputValue


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

            elif isRgbStr(dataStr):
                outData = addSquBrackets(dataStr)

            elif isIntStr(dataStr):
                outData = int(dataStr)

            elif isFloatStr(dataStr):
                outData = float(dataStr)

            elif isRefStr(dataStr):
                outData = dataStr  # maybe a bug

            else:
                # debugPrint(f"{dataStr},{isRef}")
                if isRef:
                    outData = dataStr  # maybe a bug
                else:
                    if transMATStr:
                        outData = addSingleQuotes(pyStr2MatlabStr(dataStr))  # maybe a bug
                    else:
                        outData = addSingleQuotes(dataStr)  # maybe a bug
        else:
            outData = "[]"

            debugPrint(f"find an empty input:{dataStr}")

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


# add square brackets
def addSingleQuotes(inputStr):
    outputStr = f"'{inputStr}'"
    return outputStr


# add square brackets
def addSquBrackets(inputStr):
    outputStr = f"[{inputStr}]"
    return outputStr


def removeSingleQuotes(inputStr):
    if isinstance(inputStr, str):
        if re.fullmatch("'.+'", inputStr):  # any character except a new line
            inputStr = inputStr[1:-1]
    return inputStr


def removeSquBrackets(inputStr):
    if isinstance(inputStr, str):
        if re.fullmatch("\[.+\]", inputStr):  # any character except a new line
            inputStr = inputStr[1:-1]
    return inputStr


def getAllNestedVars(inputStr, opVars=[]) -> set:
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


def getCycleRealRows(widgetId) -> int:
    cCycle = Info.WID_WIDGET[widgetId]
    weightList = cCycle.getAttributeValues(0)

    sumValue = 0

    for cWeightStr in weightList:
        sumValue = sumValue + dataStrConvert(cWeightStr)

    return sumValue


def getMaxLoopLevel() -> int:
    maxLoopLevel = -1

    for cWidgetId in Info.WID_NODE.keys():
        maxLoopLevel = max(maxLoopLevel, getWidLoopLevel(cWidgetId))
    return maxLoopLevel


def getRefValue(cWidget, inputStr, attributesSetDict):
    isRefValue = False

    if isinstance(inputStr, str):

        isRefValue = isRefStr(inputStr)

        if isRefValue:
            inputStr = re.sub("[\[\]]", '', inputStr)

            if inputStr in attributesSetDict:
                inputStr = attributesSetDict[inputStr][1]
            else:
                throwCompileErrorInfo(
                    f"The cited attribute '{inputStr}' \nis not available for {Func.getWidgetName(cWidget.widget_id)}")

    return [inputStr, isRefValue]


def getRefValueSet(cWidget, inputStr, attributesSetDict):
    isRefValue = False
    valueSet = set()

    if isinstance(inputStr, str):

        isRefValue = isRefStr(inputStr)

        if isRefValue:
            inputStr = re.sub("[\[\]]", '', inputStr)

            if inputStr in attributesSetDict:
                valueSet = attributesSetDict[inputStr][2]
                inputStr = attributesSetDict[inputStr][1]
            else:
                throwCompileErrorInfo(
                    f"The cited attribute '{inputStr}' \nis not available for {Func.getWidgetName(cWidget.widget_id)}")

    return [inputStr, isRefValue, valueSet]


def getSepcialRespsFormatAtts(cInputDevices, spFormatVarDict) -> dict:
    # cInputDevices = cWidget.getInputDevice()
    for cRespProperties in cInputDevices.values():
        if cRespProperties['Device Type'] == 'keyboard':
            updateSpFormatVarDict(cRespProperties['Correct'], 'kbCorrectResp', spFormatVarDict)
            updateSpFormatVarDict(cRespProperties['Allowable'], 'kbAllowKeys', spFormatVarDict)
        else:
            updateSpFormatVarDict(cRespProperties['Correct'], 'noKbDevCorrectResp', spFormatVarDict)
            updateSpFormatVarDict(cRespProperties['Allowable'], 'noKbAllowKeys', spFormatVarDict)


    # return spFormatVarDict


def getSepcialFormatAtts():
    """
    : special varType:
    : percentage
    :
    """
    spFormatVarDict = dict()

    for widgetId, cWidget in Info.WID_WIDGET.items():

        cProperties = Func.getProperties(widgetId)

        if Func.isWidgetType(widgetId, Info.CYCLE):
            pass
        elif Func.isWidgetType(widgetId, Info.SWITCH):
            pass
        elif Func.isWidgetType(widgetId, Info.IF):
            cTrueWidget = cWidget.getTrueWidget()

            print(f"{cTrueWidget.getInfo()}")
            print(f"{cTrueWidget.getInputDevice()}")

        elif Func.isWidgetType(widgetId, Info.TEXT):
            updateSpFormatVarDict(cWidget.getTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getFrameTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Width'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Height'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['X position'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Y position'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Style'], 'fontStyle', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Clear after'], 'clearAfter', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Flip horizontal'], 'flipHorizontal', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Flip vertical'], 'flipVertical', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Right to left'], 'rightToLeft', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Enable'], 'enableFrame', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Text'], 'textContent', spFormatVarDict)

            getSepcialRespsFormatAtts(cWidget.getInputDevice(), spFormatVarDict)

            # cInputDevices = cWidget.getInputDevice()
            # for cRespProperties in cInputDevices.values():
            #     if cRespProperties['Device Type'] == 'keyboard':
            #         updateSpFormatVarDict(cRespProperties['Correct'], 'kbCorrectResp', spFormatVarDict)
            #         updateSpFormatVarDict(cRespProperties['Allowable'], 'kbAllowKeys', spFormatVarDict)
            #     else:
            #         updateSpFormatVarDict(cRespProperties['Correct'], 'noKbDevCorrectResp', spFormatVarDict)
            #         updateSpFormatVarDict(cRespProperties['Allowable'], 'noKbAllowKeys', spFormatVarDict)


        elif Func.isWidgetType(widgetId, Info.VIDEO):
            # updateSpFormatVarDict(cWidget.getTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getFrameTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Width'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Height'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['X position'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Y position'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Clear after'], 'clearAfter', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', spFormatVarDict)

            getSepcialRespsFormatAtts(cWidget.getInputDevice(), spFormatVarDict)

        elif Func.isWidgetType(widgetId, Info.SOUND):
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Wait for start'], 'waitForStart', spFormatVarDict)

            getSepcialRespsFormatAtts(cWidget.getInputDevice(), spFormatVarDict)

        elif Func.isWidgetType(widgetId, Info.IMAGE):
            updateSpFormatVarDict(cWidget.getTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getFrameTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Width'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Height'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['X position'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Y position'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Clear after'], 'clearAfter', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Enable'], 'enableFrame', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', spFormatVarDict)

            getSepcialRespsFormatAtts(cWidget.getInputDevice(), spFormatVarDict)

        elif Func.isWidgetType(widgetId, Info.SLIDER):
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', spFormatVarDict)
            updateSpFormatVarDict(cProperties['pro']['Clear after'], 'clearAfter', spFormatVarDict)

            getSepcialRespsFormatAtts(cWidget.getInputDevice(), spFormatVarDict)

    return spFormatVarDict


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

    return {Info.DEV_SCREEN:iMonitor,Info.DEV_NETWORK_PORT:iNetPort,Info.DEV_PARALLEL_PORT:iParal,Info.DEV_SERIAL_PORT:iSerial,Info.DEV_SOUND:iSound}



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
        if Func.isWidgetType(node.widget_id, Info.CYCLE):
            loopLevel += 1
    return loopLevel


"""
def getCycleColValueSet(cWidget,key,attributesSetDict):
    colValueSet = {}

    for iRow in range(cWidget.rowCount()):
        cRowDict = cWidget.getAttributes(iRow)

        cValue, isRefValue = getRefValue(cWidget, cRowDict[key], attributesSetDict)

        if isRefValue:
            foundStr = re.search('[\.a-zA-Z0-9_]*\{',cValue).group(0)[0:-1]
            if foundStr:
                attributesSetDict[foundStr][2]
            # f"{cWidgetName}.attr.{key}{{{cLoopIterStr}}}"

        else:
            colValueSet.add(cRowDict[key])

    return colValueSet
"""


def updateSpFormatVarDict(propertyValue, formatTypeStr, spFormatVarDict):
    if isRefStr(propertyValue):
        propertyValue = propertyValue[1:-1]  # remove the square brackets
        allRefedCycleAttrs = getAllNestedVars(propertyValue, [])
        for cAttrName in allRefedCycleAttrs:

            if cAttrName in spFormatVarDict:
                if spFormatVarDict[cAttrName] != formatTypeStr:
                    throwCompileErrorInfo(
                        f"attribute: {cAttrName} are not allowed to be both {formatTypeStr} or {spFormatVarDict[cAttrName]}")
            else:
                spFormatVarDict.update({cAttrName: formatTypeStr})


def isContainChStr(inputStr):
    # :param check_str: {str}
    # :return: {bool} True and False for have and have not chinese characters respectively
    for ch in inputStr:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def isSingleQuotedStr(inputStr):
    if inputStr.startswith("'") and inputStr.endswith("'"):
        return True
    return False


def isRgbStr(inputStr):
    isRgbFormat = re.fullmatch("^\d+,\d+,\d+$", inputStr)
    return isRgbFormat


def isRgbWithBracketsStr(inputStr):
    isRgbFormat = re.fullmatch("^\[\d+,\d+,\d+\]$", inputStr)
    return isRgbFormat


def isNumStr(inputStr):
    if isinstance(inputStr, str):
        return re.fullmatch("([\d]*\.[\d$]+)|\d*", inputStr)

    return False


def isIntStr(inputStr):
    if isinstance(inputStr, str):
        return re.fullmatch("\d*", inputStr)

    return False


def isFloatStr(inputStr):
    if isinstance(inputStr, str):
        return re.fullmatch("([\d]*\.[\d$]+)", inputStr)

    return False


def isPercentStr(inputStr):
    if isinstance(inputStr, str):
        return re.fullmatch("([\d]*\.[\d]+%$)|(\d*%$)", inputStr)

    return False


def isRefStr(inputStr):
    if isinstance(inputStr, str):

        if isRgbWithBracketsStr(inputStr):
            return False

        if re.fullmatch("\[[A-Za-z]+[a-zA-Z\._0-9]*\]", inputStr):
            return True

    return False


def isContainCycleTL(widgetId) -> bool:
    cTimelineWidgetIds = Func.getWidgetIDInTimeline(widgetId)

    for cWidgetId in cTimelineWidgetIds:
        if Func.isWidgetType(cWidgetId, Info.CYCLE):
            return True
    return False


def keyNameToCodes(keyNameList) -> dict:
    keyCodesDict = {'left_mouse': 1, 'right_mouse': 2, 'middle_mouse': 4, 'backspace': 8,
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
                    'f7': 118, 'f8': 119, 'f9': 120, 'f10': 121, 'f11': 122, 'f12': 123, 'f13': 124, 'f14': 125, 'f15': 126,
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

def replaceDot(screenNameStr, newSplitStr = "_") -> str:

    return newSplitStr.join(screenNameStr.split('.'))


def shouldNotBeCitationCheck(keyStr,value):
    if isRefStr(value):
        throwCompileErrorInfo(f"'{keyStr}': the value should NOT be a citation!")


def shouldNotBeEmptyCheck(keyStr,value):
    if value == '':
        throwCompileErrorInfo(f"'{keyStr}'should NOT be empty!")


def outPutTriggerCheck(cWidget) -> dict:
    '''
    : force the pulse dur to be 10 ms if the ppl device will be used to send responses triggers
    '''
    cOutPutDevices = cWidget.getOutputDevice()
    cInputDevices = cWidget.getInputDevice()

    # print(f"cOutPutDevices = {cOutPutDevices}")
    # print(f"cInputDevices = {cInputDevices}")

    respTriggerDevNames = set()
    for cInputDevInfo in cInputDevices.values():
        cRespTriggerDevName = cInputDevInfo['Output Device']

        shouldNotBeCitationCheck('Resp Trigger Device', cRespTriggerDevName)

        respTriggerDevNames.update(cRespTriggerDevName)

    shortPulseDurParallelsDict = dict()

    for cOpDevInfo in cOutPutDevices.values():
        if cOpDevInfo['Device Type'] == 'parallel_port':
            if cOpDevInfo['Device Name'] in respTriggerDevNames:
                shortPulseDurParallelsDict.update({cOpDevInfo['Device Id']: 10})
                Func.log('Currently we will force the pulse duration to be 10 ms', False)

    return shortPulseDurParallelsDict  # temp


def updateEnableKbKeysList(allowKeyStr):
    global enabledKBKeysList

    if len(allowKeyStr) > 0:
        if allowKeyStr.startswith('[') and allowKeyStr.endswith(']'):
            enabledKBKeysList.add(allowKeyStr[1:-1])
        else:
            enabledKBKeysList.add(allowKeyStr)
# splittedStrs = re.split('({\w*})', allowKeyStr)
        #
        # for item in splittedStrs:
        #     if item[0] == '{':
        #         item = re.sub('[\{\}]', '', item)
        #         enabledKBKeysList.add(item)
        #     else:
        #         for char in item:
        #             enabledKBKeysList.add(char)

def parseBooleanStr(inputStr, isRef=False):
    if isinstance(inputStr,str):
        if not isRef:
            if inputStr.lower() in ["'yes'", "'true'", 'yes', 'true']:
                inputStr = "1"
            elif inputStr.lower() in ["'no'", "'false'", 'no', 'false']:
                inputStr = "0"
            else:
                throwCompileErrorInfo(f"the value of '{inputStr}' should be of ['False','True','Yes','No','1', or '0'] ")
    elif isinstance(inputStr,bool):
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
        elif inputStr == "noNothing_2":
            inputStr = '2'
    return inputStr


def parseDurationStr(inputStr):
    if isinstance(inputStr, str):
        inputStr = removeSingleQuotes(inputStr)

        if inputStr == "(Infinite)":
            inputStr = "6000000" # an extramely impossible value
        elif re.fullmatch("\d+~\d+", inputStr):
            cDurRange = inputStr.split('~')
            inputStr = f"{cDurRange[0]},{cDurRange[1]}"

    return inputStr


def parseEndActionStr(endActionStr):
    if endActionStr == 'Terminate':
        endActionStr = '1'
    else:
        endActionStr = '0'

    return endActionStr


def parseFilenameStr(inputStr, isRef = False) -> str:

    if not isRef:
        toBeSavedDir = os.path.dirname(Info.FILE_NAME)

        if  len(toBeSavedDir) <= len(inputStr):
            if inputStr[:len(toBeSavedDir)] == toBeSavedDir:
                inputStr = inputStr[len(toBeSavedDir):]

    return [inputStr, toBeSavedDir]



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
            if devType == 'keyboard':
                splittedStrs = re.split('({\w*})', kbCorRespStr)
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
            kbCorRespCodesStr = "[" + kbCorRespCodesStr+f"{kbCorRespCodes[-1]}" + "]"

        else:
            kbCorRespCodesStr = "[0]"

    return kbCorRespCodesStr


def parsePercentStr(inputStr):
    if isinstance(inputStr, str):
        if isPercentStr(inputStr):
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


def parseStretchModeStr(inputStr, isRef = False):
    # ""、Both、LeftRight、UpDown、[attr]
    if not isRef:
        if isinstance(inputStr, str):
            if inputStr == "Both":
                inputStr = "3"
            elif inputStr == "LeftRight":
                inputStr = "1"
            elif inputStr == "UpDown":
                inputStr = "2"
            else:
                inputStr = "0"

    return inputStr


def parseTextContentStr(inputStr, isRef = False) -> str:
    if not isRef:
        if isContainChStr(inputStr):
            inputStr = "[" + "".join(f"{ord(value)} " for value in inputStr) + "]"
        else:
            #cinputStr = '\\n'.join(inputStr.split('\n')) have down in pyStr2MatlabStr
            inputStr = addSingleQuotes(pyStr2MatlabStr(inputStr))

    return inputStr

# noinspection PyStringFormat
def printAutoInd(f, inputStr, *argins):
    global cIndents, isPreLineSwitch, isDummyPrint

    incrAfterStr = ('if', 'try', 'switch', 'for', 'while')
    decreAndIncrStr = ('else', 'elseif', 'otherwise', 'catch')

    if inputStr.split(' ')[0] in incrAfterStr:
        tabStrs = '\t' * cIndents

        if not isDummyPrint:
            print(f"\n{tabStrs}{inputStr}".format(*argins), file=f)

        cIndents += 1

    elif inputStr.split(' ')[0] in decreAndIncrStr:
        cIndents -= 1
        tabStrs = '\t' * cIndents

        if not isDummyPrint:
            print(f"{tabStrs}{inputStr}".format(*argins), file=f)

        cIndents += 1

    elif 'end' == inputStr.split(' ')[0]:
        cIndents -= 1
        tabStrs = '\t' * cIndents

        if not isDummyPrint:
            print(f"{tabStrs}{inputStr}\n".format(*argins), file=f)

    elif 'end%switch' == inputStr.split(' ')[0]:
        cIndents -= 2
        tabStrs = '\t' * cIndents

        if not isDummyPrint:
            print(f"{tabStrs}{inputStr}\n".format(*argins), file=f)

    elif 'case' == inputStr.split(' ')[0]:

        if 0 == isPreLineSwitch:
            cIndents -= 1

        tabStrs = '\t' * cIndents

        if not isDummyPrint:
            print(f"{tabStrs}{inputStr}".format(*argins), file=f)

        cIndents += 1

    else:

        tabStrs = '\t' * cIndents

        if not isDummyPrint:
            # print(f"{tabStrs}{inputStr}".format(*argins))
            print(f"{tabStrs}{inputStr}".format(*argins), file=f)

    if 'switch' == inputStr.split(' ')[0]:
        isPreLineSwitch = 1
    else:
        isPreLineSwitch = 0

    if cIndents < 0:
        cIndents = 0


def printCycleWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes):
    global spFormatVarDict
    # start from 1 to compatible with MATLAB
    cLoopLevel += 1
    attributesSetDict = attributesSetDict.copy()
    cWidgetName = Func.getWidgetName(cWidget.widget_id)

    attributesSetDict.setdefault(f"{cWidgetName}.cLoop", [cLoopLevel, f"iLoop_{cLoopLevel}", {f"iLoop_{cLoopLevel}"}])
    attributesSetDict.setdefault(f"{cWidgetName}.rowNums",
                                 [cLoopLevel, f"size({cWidgetName}.attr,1)", {f"size({cWidgetName}.attr,1)"}])

    cLoopIterStr = attributesSetDict[f"{cWidgetName}.cLoop"][1]

    # create the design matrix  (table) for the current cycle
    startExpStr = cWidgetName + '.attr = cell2table({...'
    printAutoInd(f, '% create the designMatrix of the current cycle (loop)')

    printAutoInd(f, '{0}', startExpStr)

    for iRow in range(cWidget.rowCount()):
        cRowDict = cWidget.getAttributes(iRow)
        if 0 == iRow:
            endExpStr = "},'VariableNames',{" + ''.join("'" + key + "' " for key in cRowDict.keys()) + "});"

        for key, value in cRowDict.items():
            # get the referenced var value
            cValue, isRefValue, cRefValueSet = getRefValueSet(cWidget, value, attributesSetDict)

            cKeyAttrName = f"{Func.getWidgetName(cWidget.widget_id)}.attr.{key}"

            # handle the references and the values in special format (e.g., percent, duration)
            # --- replaced the percentageStr--------/
            if cKeyAttrName in spFormatVarDict:
                if spFormatVarDict[cKeyAttrName] == 'percent':
                    cValue = parsePercentStr(cValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'dur':
                    cValue = parseDurationStr(cValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'fontStyle':
                    cValue = parseFontStyleStr(cValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'clearAfter':
                    cValue = parseDontClearAfterStr(cValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'flipHorizontal':
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'flipVertical':
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'rightToLeft':
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'enableFrame':
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'waitForStart':
                    cValue = parseBooleanStr(cValue, isRefValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'kbCorrectResp':
                    cValue = parseKbCorRespStr(cValue,isRefValue,'keyboard')
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'noKbDevCorrectResp':
                    cValue = parseKbCorRespStr(cValue,isRefValue,'noneKbDevs')
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'kbAllowKeys':
                    cValue = parseKbCorRespStr(cValue,isRefValue,'keyboard')
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'noKbAllowKeys':
                    cValue = parseKbCorRespStr(cValue,isRefValue,'noneKbDevs')
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'textContent':
                    cValue = parseTextContentStr(cValue,isRefValue)
                    cRowDict[key] = cValue

            #     TO BE CONTINUING... FOR ALL OTHER Special Types
            # --------------------------------------\

            cAttributeName = f"{cWidgetName}.attr.{key}"

            if not isRefValue:
                cRefValueSet = {cValue}

            if cAttributeName in attributesSetDict:
                preValueSet = attributesSetDict[cAttributeName][2]
            else:
                preValueSet = set()

            attributesSetDict.update(
                {cAttributeName: [cLoopLevel, f"{cAttributeName}{{{cLoopIterStr}}}", cRefValueSet.union(preValueSet)]})

        # print out the design matrix of the current Cycle
        if '' == cRowDict['Weight']:
            cRepeat = 1
        else:
            cRepeat = dataStrConvert(cRowDict['Weight'])

        for iRep in range(cRepeat):
            printAutoInd(f, '{0}', "".join(
                addCurlyBrackets(dataStrConvert(*getRefValue(cWidget, value, attributesSetDict), False, False)) + " "
                for key, value in cRowDict.items()) + ";...")

    printAutoInd(f, '{0}\n', endExpStr)
    # Shuffle the designMatrix:
    cycleOrderStr = dataStrConvert(*getRefValue(cWidget, cWidget.getOrder(), attributesSetDict))
    cycleOrderByStr = dataStrConvert(*getRefValue(cWidget, cWidget.getOrderBy(), attributesSetDict))

    #  to make sure the weight is one for counterbalance selection of order ----/
    if cycleOrderStr == "'CounterBalance'":
        cCycleWeightList = cWidget.getAttributeValues(0)
        for cLineWeight in cCycleWeightList:
            if dataStrConvert(cLineWeight) != 1:
                throwCompileErrorInfo(
                    f"Found an uncompilable error in Cycle {Func.getWidgetName(cWidget.widget_id)}:\nFor CounterBalance selection, the timeline weight should be 1")
    # ------------------------------------------------------------------------\

    # attributesSetDict.setdefault(f"{cWidgetName}.rowNums", [cLoopLevel, f"size({cWidgetName}.attr,1)"])

    printAutoInd(f, "%---Shuffle the DesignMatrix-----/")
    printAutoInd(f, 'cShuffledIdx = ShuffleCycleOrder({0},{1},{2},subInfo);',
                 attributesSetDict[f"{cWidgetName}.rowNums"][1], cycleOrderStr, cycleOrderByStr)
    printAutoInd(f, '{0}.attr = {0}.attr(cShuffledIdx,:);', cWidgetName)
    printAutoInd(f, "%--------------------------------\\\n")

    # cycling
    printAutoInd(f, '% looping across each row of the {0}.attr:{1}', cWidgetName, cLoopIterStr)
    printAutoInd(f, 'for {0} = size({1},1)', cLoopIterStr, f"{cWidgetName}.attr")

    cLoopOpIdxStr = cLoopIterStr + "_cOpR"

    printAutoInd(f, "opRowIdx = opRowIdx + 1; % set the output variables row num")
    printAutoInd(f, "{0} = opRowIdx;", cLoopOpIdxStr)

    # handle each timeline
    cTimeLineList = cWidget.getTimelines()
    # squeeze the timelines
    cTimelineSet = set()

    for iTimeline in cTimeLineList:
        cTimelineSet.add(iTimeline[1])

    printAutoInd(f, '% switch across timeline types')
    printAutoInd(f, 'switch {0}', f"{cWidgetName}.attr.timeline{{{cLoopIterStr}}}")

    for iTimeline_id in cTimelineSet:
        if '' == iTimeline_id:
            throwCompileErrorInfo(f"In {cWidgetName}: Timeline should not be empty!")
        else:
            printAutoInd(f, 'case {0}', f"{addSingleQuotes(Func.getWidgetName(iTimeline_id))}")
            # printAutoInd(f, "{0}_rIdx    = opRowIdx;", Func.getWidgetName(iTimeline_id))
            printTimelineWidget(Info.WID_WIDGET[iTimeline_id], f, attributesSetDict, cLoopLevel, delayedPrintCodes)

    printAutoInd(f, 'otherwise ')
    printAutoInd(f, '% do nothing ')
    printAutoInd(f, 'end%switch {0}', f"{cWidgetName}.attr.timeline{{{cLoopIterStr}}}")

    printAutoInd(f, 'end % {0}', cLoopIterStr)
    # to be continue ...

    return delayedPrintCodes


def printDelayedCodes(delayedPrintCodes, keyName, inputStr, *argins):
    global isDummyPrint

    # delayedPrintCodes = {'codesAfFip': [], 'respCodes': []}
    if not isDummyPrint:
        delayedPrintCodes[keyName].append = f"{inputStr}".format(*argins)


def printRespCodes(f, delayedPrintCodes):
    # -------------------------------------------------------------
    # Step 1: print out previous widget's resp related codes
    # -------------------------------------------------------------
    if isinstance(delayedPrintCodes,dict):
        for cRowStr in delayedPrintCodes['respCodes']:
            cRowStr = "{{".join(cRowStr.split('{'))
            cRowStr = "}}".join(cRowStr.split('}'))
            printAutoInd(f,cRowStr)
        # clear out the print buffer
        delayedPrintCodes.update({'respCodes': []})
    elif isinstance(delayedPrintCodes, list):
        for cRowStr in delayedPrintCodes:
            cRowStr = "{{".join(cRowStr.split('{'))
            cRowStr = "}}".join(cRowStr.split('}'))
            printAutoInd(f,cRowStr)
        delayedPrintCodes = []

    return delayedPrintCodes


def flipScreen(cWidget, f, cLoopLevel):
    global historyPropDict, isDummyPrint
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num

    cWinIdx = historyPropDict['cWinIdx']
    cWinStr = historyPropDict['cWinStr']

    # transedScrName = replaceDot(historyPropDict['cScreenName'])
    clearAfter = historyPropDict['clearAfter']


    if Func.getWidgetPosition(cWidget.widget_id) > 0:
        # Step 2: print out help info for the current widget
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, Func.getWidgetPosition(cWidget.widget_id) + 1,
                     Func.getWidgetName(cWidget.widget_id))
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # Flip the Screen
    if Func.getWidgetPosition(cWidget.widget_id) == 0:
        printAutoInd(f, "% for first event, flip immediately.. ")
        # f"{Func.getWidgetName(cWidget.widget_id)}_onsettime({cOpRowIdxStr})"
        printAutoInd(f, "{0}.onsettime({1}) = Screen('Flip',{2},{3},{4}); %#ok<*STRNU>\n", Func.getWidgetName(cWidget.widget_id),
                     cOpRowIdxStr, cWinStr, 0, clearAfter)
    else:
        # printAutoInd(f, f"if cDurs({cWinIdx}) > 0")
        # printAutoInd(f, f"cScrFlipTime = cDurs({cWinIdx}) + lastScrOnsettime({cWinIdx}) - 0.003; % maybe 0.5*winIFIs({cWinIdx})")
        # printAutoInd(f, "else ")
        # printAutoInd(f, "cScrFlipTime = 0;  % flip immediately")
        # printAutoInd(f, "end ")
        #
        # printAutoInd(f, "{0}.onsettime({1}) = Screen('Flip',{2},cScrFlipTime,{3});\n",
        #              Func.getWidgetName(cWidget.widget_id),
        #              cOpRowIdxStr, cWinStr, clearAfter)
        # [VBLTimestamp StimulusOnsetTime FlipTimestamp Missed Beampos] =
        # Screen('Flip', windowPtr[, when] [, dontclear][, dontsync] [,
        #     multiflip]);
        printAutoInd(f, "{0}.onsettime({1}) = Screen('Flip',{2},cDurs({3}) + lastScrOnsettime({3}) - 0.003,{4}); %#ok<*STRNU>\n",
                     Func.getWidgetName(cWidget.widget_id),
                     cOpRowIdxStr, cWinStr, cWinIdx, clearAfter)



def flipAudio(cWidget, f, cLoopLevel, attributesSetDict):
    global historyPropDict, isDummyPrint
    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num

    cWinIdx = historyPropDict['cWinIdx']
    cWinStr = historyPropDict['cWinStr']

    clearAfter = historyPropDict['clearAfter']

    # 2) check the sound dev parameter:
    cSoundDevName, isRef = getRefValue(cWidget, cWidget.getSoundDeviceName(), attributesSetDict)
    cSoundIdxStr = outputDevNameIdxDict.get(cSoundDevName)

    # 3) check the repetitions parameter:
    repetitionsStr, isRef = getRefValue(cWidget, cWidget.getRepetitions(), attributesSetDict)

    # 4) get the isSyncToVbl parameter:
    isSyncToVbl = cWidget.getSyncToVbl()


    if Func.getWidgetPosition(cWidget.widget_id) > 0:
        # Step 2: print out help info for the current widget
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, Func.getWidgetPosition(cWidget.widget_id) + 1,
                     Func.getWidgetName(cWidget.widget_id))
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')


    if isSyncToVbl:
        # Flip the Screen
        printAutoInd(f, "% sync to the vertical blank of screen:{0}",cWidget.getScreenName())
        if Func.getWidgetPosition(cWidget.widget_id) == 0:
            printAutoInd(f, "% for first event, play the audio at the immediately VBL .. ")
            printAutoInd(f, "predictedVisOnset = PredictVisualOnsetForTime({0}, 0);",cWinStr)

            printAutoInd(f, " PsychPortAudio('Start', {0}, {1}, predictedVisOnset, 0); %\n", cSoundIdxStr, repetitionsStr)
            printAutoInd(f, "{0}.onsettime({1}) = Screen('Flip', {2}, predictedVisOnset, {3}); %\n", Func.getWidgetName(cWidget.widget_id),
                         cOpRowIdxStr, cWinStr, clearAfter)
        else:
            printAutoInd(f, "predictedVisOnset = PredictVisualOnsetForTime({0}, cDurs({1}) + lastScrOnsettime({1}) - 0.003);", cWinStr, cWinIdx)
            printAutoInd(f, "% schedule start of audio at exactly the predicted time caused by the next flip")
            printAutoInd(f, " PsychPortAudio('Start', {0}, {1}, predictedVisOnset, 0); %\n", cSoundIdxStr, repetitionsStr)
            printAutoInd(f, "{0}.onsettime({1}) = Screen('Flip',{2},cDurs({3}) + lastScrOnsettime({3}) - 0.003, {4}); %#ok<*STRNU>\n",
                         Func.getWidgetName(cWidget.widget_id), cOpRowIdxStr, cWinStr, cWinIdx, clearAfter)
    else:
        if Func.getWidgetPosition(cWidget.widget_id) == 0:
            printAutoInd(f, "% for first event, play the audio immediately.. ")
            printAutoInd(f, "{0}.onsettime({1}) = PsychPortAudio('Start', {2}, {3}, 0, 1); % wait for start and get the real start time\n",
                         Func.getWidgetName(cWidget.widget_id), cOpRowIdxStr, cSoundIdxStr, repetitionsStr)
        else:
            printAutoInd(f, "% for multiple screens, use the maximum of the predicted onsettime")
            printAutoInd(f,
                         "{0}.onsettime({1}) = PsychPortAudio('Start', {2}, {3}, max(cDurs + lastScrOnsettime), 1); % % wait for start and get the real start time\n",
                         Func.getWidgetName(cWidget.widget_id), cOpRowIdxStr, cSoundIdxStr,
                         repetitionsStr)



def printStimWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes):

    # print comments to indicate the current frame order
    # Step 1: draw the content of current frame
    cWidgetType = cWidget.widget_id.split('.')[0]

    if Info.TEXT == cWidgetType:
        delayedPrintCodes = drawTextWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes)
    elif Info.IMAGE == cWidgetType:
        delayedPrintCodes = drawImageWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes)
    elif Info.SOUND == cWidgetType:
        delayedPrintCodes = drawSoundWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes)


    # step 2: print delayed resp codes or none if the widget is the first one
    #         print comments to indicate the current frame order if it is not the first one
    delayedPrintCodes = printRespCodes(f, delayedPrintCodes)

    # STEP 3: flip screen
    if Info.SOUND == cWidgetType:
        flipAudio(cWidget, f, cLoopLevel, attributesSetDict)
    else:
        flipScreen(cWidget, f, cLoopLevel)

    # step 4: send trigger
    delayedPrintCodes = printStimTriggers(cWidget, f, cLoopLevel, attributesSetDict, delayedPrintCodes)


    # step 5: make the delayed resp codes for the current frame
    checkResponse(cWidget, f, cLoopLevel, attributesSetDict, delayedPrintCodes)

    return delayedPrintCodes


def printStimTriggers(cWidget, f, cLoopLevel, attributesSetDict, delayedPrintCodes):
    global outputDevNameIdxDict, historyPropDict

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"
    cWidgetName = Func.getWidgetName(cWidget.widget_id)

    cWinIdx = historyPropDict['cWinIdx']

    # ---------------------------------------------------------------------------------------
    # Step 1: print out previous widget's codes that suppose to be print just after the Flip
    # ----------------------------------------------------------------------------------------
    for cRowStr in delayedPrintCodes['codesAfFip']:
        printAutoInd(f, cRowStr)
    # clear out the print buffer
    delayedPrintCodes.update({'codesAfFip': []})

    # ------------------------------------------------------------
    # Step 2: send output triggers and messages
    # ------------------------------------------------------------

    debugPrint(f"------------------------\\")

    output_device = cWidget.getOutputDevice()
    if len(output_device) > 0:
        printAutoInd(f, "% -- send output trigger and msg: --/")

    debugPrint(f"{cWidget.widget_id}: outputDevice:\n a = {output_device}")
    debugPrint(f"b = {cWidget.getInputDevice()}")

    # initializing the outDevices that could be used to store the outDev info
    cOutDeviceDict = dict()

    for device, properties in output_device.items():
        msgValue = dataStrConvert(*getRefValue(cWidget, properties['Value or Msg'], attributesSetDict), True)
        pulseDur = dataStrConvert(*getRefValue(cWidget, properties['Pulse Duration'], attributesSetDict), False)

        cDevName = properties.get("Device Name", "")
        devType = properties.get("Device Type", "")


        if devType == 'parallel_port':
            # currently only ppl need to be reset to zero
            cOutDeviceDict[cDevName] = ['1', pulseDur,
                                        re.split('(\(\d*\))', outputDevNameIdxDict.get(cDevName))[1][1:-1]]
            # cOutDeviceDict[cDevName] = [devType,pulseDur, parallelPortNumInMatlab]
            if Info.PLATFORM == 'linux':
                printAutoInd(f, "lptoutMex({0},{1});", outputDevNameIdxDict.get(cDevName), msgValue)
            elif Info.PLATFORM == 'windows':
                printAutoInd(f, "io64(io64Obj,{0},{1});", outputDevNameIdxDict.get(cDevName), msgValue)
            elif Info.PLATFORM == 'mac':
                printAutoInd(f, "% currently, under Mac OX we just do nothing for parallel ports")

            # printAutoInd(f, "isParallelOn = true; ")

        elif devType == 'network_port':
            printAutoInd(f, "pnet({0},'write',{1});", outputDevNameIdxDict.get(cDevName), msgValue)
            cOutDeviceDict[cDevName] = ['2', pulseDur,
                                        re.split('(\(\d*\))', outputDevNameIdxDict.get(cDevName))[1][1:-1]]

        elif devType == 'serial_port':
            printAutoInd(f, "[ign, when] = IOPort('Write', {0}, {1});", outputDevNameIdxDict.get(cDevName), msgValue)
            cOutDeviceDict[cDevName] = ['3', pulseDur,
                                        re.split('(\(\d*\))', outputDevNameIdxDict.get(cDevName))[1][1:-1]]

    historyPropDict.update({'cOutDevices':cOutDeviceDict})

    if len(output_device) > 0:
        printAutoInd(f, "{0}_msgEndTime({1}) = GetSecs;", cWidgetName, cOpRowIdxStr)
        printAutoInd(f, "% ----------------------------------\\\n")

    cWidgetType = cWidget.widget_id.split('.')[0]
    # updated the screen flip times in matlab
    if Info.SOUND == cWidgetType:
        printAutoInd(f, "% for event type of sound, make it to all lastScrOnsetime")
        printAutoInd(f, "lastScrOnsettime(:) = {0}.onsettime({1}); % temp save the last screen onsettimes\n",
                     Func.getWidgetName(cWidget.widget_id),
                     cOpRowIdxStr)
    else:
        printAutoInd(f, "lastScrOnsettime({0}) = {1}.onsettime({2}); %temp save the last screen onsettimes\n",
                     cWinIdx,
                     Func.getWidgetName(cWidget.widget_id),
                     cOpRowIdxStr)

    return delayedPrintCodes


def printTimelineWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes):
    global cInfoDict, isDummyPrint

    cTimelineWidgetIds = Func.getWidgetIDInTimeline(cWidget.widget_id)

    for cWidgetId in cTimelineWidgetIds:
        cWidget = Info.WID_WIDGET[cWidgetId]

        # for dummyPrint get the last widget id and loopNum
        if isDummyPrint:
            cInfoDict.update({'lastWidgetId':cWidgetId})

        cWidgetType = cWidget.widget_id.split('.')[0]


        if Info.CYCLE == cWidgetType:
            delayedPrintCodes = printCycleWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes)

        elif cWidgetType in [Info.TEXT, Info.IMAGE, Info.SOUND, Info.SLIDER, Info.VIDEO]:
            delayedPrintCodes = printStimWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes)

        elif Info.OPEN == cWidgetType:
            pass
        elif Info.DC == cWidgetType:
            pass
        elif Info.CALIBRATION == cWidgetType:
            pass
        elif Info.ACTION == cWidgetType:
            pass
        elif Info.STARTR == cWidgetType:
            pass
        elif Info.ENDR == cWidgetType:
            pass
        elif Info.Log == cWidgetType:
            pass
        elif Info.QUEST_INIT == cWidgetType:
            pass
        elif Info.QUEST_GET_VALUE == cWidgetType:
            pass
        elif Info.QUEST_UPDATE == cWidgetType:
            pass
            # delayedPrintCodes = printImageWdiget(cWidget, f, delayedPrintCodes)

    # CYCLE = "Cycle"
    # SOUND = "Sound"
    # TEXT = "Text"
    # IMAGE = "Image"
    # VIDEO = "Video"
    # SLIDER = "Slider"
    # OPEN = "Open"
    # DC = "DC"
    # CALIBRATION = "Calibration"
    # ACTION = "Action"
    # STARTR = "StartR"
    # ENDR = "EndR"
    # CLOSE = "Close"
    # QUEST_INIT = "QuestInit"
    # QUEST_UPDATE = "QuestUpdate"
    # QUEST_GET_VALUE = "QuestGetValue"
    # IF = "If"
    # SWITCH = "Switch"
    # TIMELINE = "Timeline"
    # to be continue ...


def checkResponse(cWidget, f, cLoopLevel, attributesSetDict, delayedPrintCodes):
    global outputDevNameIdxDict, historyPropDict, isDummyPrint

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"

    cWidgetName = Func.getWidgetName(cWidget.widget_id)

    cAfFlipCodes = delayedPrintCodes.get('codesAfFlip',[])
    cRespCodes = delayedPrintCodes.get('respCodes',[])

    cOutDeviceDict = historyPropDict.get('cOutDevices',{})
    historyPropDict.update({'cOutDevices': {}})

    outDevCountsDict = getOutputDevCountsDict()

    # allInputDevs = historyPropDict.get('allInputDevs',{})

    cWinIdx = historyPropDict['cWinIdx']

    cInputDevices = cWidget.getInputDevice()

    # -------------------------------------------------------------------------------
    # Step 1: check parameters that should not be a citation value
    # -------------------------------------------------------------------------------
    nKbs = 0
    nMouses = 0

    for key, value in cInputDevices.items():
        shouldNotBeCitationCheck('RT Window',value['RT Window'])
        shouldNotBeCitationCheck('End Action',value['End Action'])

        shouldNotBeEmptyCheck(f"the allow able keys in {cWidgetName}:{value['Device Name']}", value['Allowable'])


        # check if the end action and rt window parameters are compatible
        if value.get('End Action') == 'Terminate':
            if value.get('RT Window') != '(Same as duration)':
                throwCompileErrorInfo(f"{cWidgetName}:{value.get('Device Name')} when 'End Action' == 'Terminate', 'RT Window' should be '(Same as duration)'")

        if value['Device Type'] == 'keyboard':
            nKbs += 1

        if value['Device Type'] == 'mouse':
            nMouses += 1

        value.update({'Widget Name':cWidgetName})
        cInputDevices.update({key:value})


    # under windows: all keyboards and mouses will be treated as a single device
    if Info.PLATFORM == 'windows':
        if nKbs > 1 or nMouses > 1:
            tobeShowStr = 'Input devices: \n For windows, specify multiple kbs or mice separately are not allowed!\n you can specify only one keyboard and/or one mouse here!'
            throwCompileErrorInfo(f"{cWidgetName}: {tobeShowStr}")
    # -------------------------------------------------------------------------------

    # allInputDevs.update(cInputDevices)

    # Step 2: get the current screen duration that determined by the next flip
    # after drawing the next widget's stimuli, get the duration first
    durStr, isRefValue, cRefValueSet = getRefValueSet(cWidget, cWidget.getDuration(), attributesSetDict)
    durStr = parseDurationStr(durStr)

    cWidgetType = cWidget.widget_id.split('.')[0]
    # updated the screen flip times in matlab
    if Info.SOUND == cWidgetType:
        if re.fullmatch("\d+,\d+", durStr):
            cRespCodes.append(f"cDurs(:) = getDurValue([{durStr}],winIFIs({cWinIdx}), true);\n")
        else:
            cRespCodes.append(f"cDurs(:) = getDurValue({durStr},winIFIs({cWinIdx}), true);\n")
    else:
        if re.fullmatch("\d+,\d+", durStr):
            cRespCodes.append(f"cDurs({cWinIdx}) = getDurValue([{durStr}],winIFIs({cWinIdx}));\n")
        else:
            cRespCodes.append(f"cDurs({cWinIdx}) = getDurValue({durStr},winIFIs({cWinIdx}));\n")


    # Step 3:

    cRespCodes.append("%============ acquire responses ==================/")

    if len(cInputDevices) > 0:

        cRespCodes.append("%-- make respDev struct --/")
        # cRespCodes.append("cRespDevs = []; \n")

        iRespDev = 1
        for cInputDev, cProperties in cInputDevices.items():
            # get allowable keys
            allowableKeysStr, isRefValue, cRefValueSet = getRefValueSet(cWidget, cProperties.get('Allowable'),attributesSetDict)
            allowableKeysStr = parseKbCorRespStr(allowableKeysStr, isRefValue, cProperties['Device Type'])

            # update the allowableKeysList
            if cProperties['Device Type'] != 'response box':

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

            # print(f"{corRespStr}")
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

            # get resp output dev name
            respOutDevNameStr, isRefValue = getRefValue(cWidget, cProperties['Output Device'], attributesSetDict)

            # get dev type and devIndexesVarName
            if cProperties['Device Type'] == 'keyboard':
                devIndexesVarName = "kbIndices"
                cDevType = 1

            elif cProperties['Device Type'] == 'mouse':
                devIndexesVarName = "miceIndices"
                cDevType = 2

            elif cProperties['Device Type'] == 'game pad':
                devIndexesVarName = "gamepadIndices"
                cDevType = 3

            elif cProperties['Device Type'] == 'response box':
                devIndexesVarName = "rbIndices"
                cDevType = 4

            # if the response code send port is a parallel
            if respOutDevNameStr == '' or respOutDevNameStr == 'none':
                needTobeRetStr = 'false'
                respCodeDevIdxStr = '0'
            else:
                respCodeDevIdxStr = cOutDeviceDict[respOutDevNameStr][2]

                if cOutDeviceDict[respOutDevNameStr][2] == '1':
                    needTobeRetStr = 'true'
                else:
                    needTobeRetStr = 'false'

            cRespCodes.append(
                f"cRespDevs({iRespDev}) = struct('beUpdatedVar','{cWidgetName}({cOpRowIdxStr})','allowAble',{allowableKeysStr},'corResp',{corRespStr},'rtWindow',{rtWindowStr},'endAction',{endActionStr},'type',{cDevType},'index',{devIndexesVarName}({inputDevNameIdxDict[cProperties['Device Name']]}),'startTime',lastScrOnsettime({cWinIdx}),'isOn',true,'needTobeReset',{needTobeRetStr},'right',{rightStr},'wrong',{wrongStr},'noResp',{noRespStr},'respCodeDevIdx',{respCodeDevIdxStr}  );")
            iRespDev += 1


        cRespCodes.append("%-------------------------\\\n")
        cRespCodes.append(f"beCheckedRespDevs = [beCheckedRespDevs, cRespDevs];")
        # cRespCodes.append(f"beCheckedRespDevs = beCheckedRespDevs([beCheckedRespDevs(:).isOn]);")

    cRespCodes.append(f"secs = GetSecs; ")
    cRespCodes.append(f"while numel(beCheckedRespDevs) > 1 && (secs < cDurs({cWinIdx}) + lastScrOnsettime({cWinIdx}) - 0.003)")


    cRespCodes.append(f"for iRespDev = 1:numel(beCheckedRespDevs) ")
    cRespCodes.append(f"if beCheckedRespDevs(iRespDev).isOn")
    cRespCodes.append(f"[~,secs,keyCode] = responseCheck(beCheckedRespDevs(iRespDev).type,beCheckedRespDevs(iRespDev).index);")

    if outDevCountsDict[Info.DEV_PARALLEL_PORT]>0 and len(cOutDeviceDict) > 0:
        cRespCodes.append(f"if beCheckedRespDevs(iRespDev).needTobeReset && (secs - beCheckedRespDevs(iRespDev).startTime) > 0.01 % currently set to 10 ms")
        if Info.PLATFORM == 'linux':
            cRespCodes.append(f"lptoutMex(parPort(beCheckedRespDevs(iRespDev).respCodeDevIdx).port, 0);")
        elif Info.PLATFORM == 'windows':
            cRespCodes.append(f"io64(io64Obj, parPort(beCheckedRespDevs(iRespDev).respCodeDevIdx).port, 0);")
        elif Info.PLATFORM == 'mac':
            cRespCodes.append("% currently, under Mac OX we just do nothing for parallel ports")
        cRespCodes.append(f"end")

    cRespCodes.append(f"if beCheckedRespDevs(iRespDev).rtWindow > 0 && (secs - beCheckedRespDevs(iRespDev).startTime) > beCheckedRespDevs(iRespDev).rtWindow")
    cRespCodes.append(f"beCheckedRespDevs(iRespDev).isOn = false;")
    cRespCodes.append(f"end % if RT window is not negative and cTime is out of RT Window")

    cRespCodes.append(f"if any(keyCodes(beCheckedRespDevs(iRespDev).allowAble))")
    cRespCodes.append(f"cFrame.Rt   = secs - beCheckedRespDevs(iRespDev).startTime;")
    cRespCodes.append(f"cFrame.Resp = find(keyCode);")
    cRespCodes.append(f"cFrame.Acc  = all(ismember(beCheckedRespDevs(iRespDev).resp, beCheckedRespDevs(iRespDev).corResp));\n")

    cRespCodes.append(f"eval([beCheckedRespDevs(iRespDev).beUpatedVar,' = cFrame;']);")

    cRespCodes.append(f"beCheckedRespDevs(iRespDev).isOn = false;")
    cRespCodes.append(f"if beCheckedRespDevs(iRespDev).endAction")
    cRespCodes.append(f"break; % break out while")
    cRespCodes.append(f"end % end action")
    cRespCodes.append(f"end % if there was a response")
    cRespCodes.append(f"end % if the check switch is on")
    cRespCodes.append(f"end % for iRespDev")
    cRespCodes.append(f"WaitSecs(0.001); % to give the cpu a little bit break ")
    cRespCodes.append(f"end % while")
    cRespCodes.append(f"%------ remove unchecked respDevs ------/")
    cRespCodes.append(f"if ~isempty(beCheckedRespDevs)")
    cRespCodes.append(f"beCheckedRespDevs(~[beCheckedRespDevs(:).isOn])          = [];")
    cRespCodes.append(f"beCheckedRespDevs([beCheckedRespDevs(:).rtWindow] == -1) = []; % excluded '(Same as duration)' ")
    cRespCodes.append(f"end ")
    cRespCodes.append(f"%---------------------------------------\\\n")

    if outDevCountsDict[Info.DEV_PARALLEL_PORT]>0 and len(cOutDeviceDict) > 0:
        cRespCodes.append(f"if cDurs({cWinIdx}) < 0.01 ")
        cRespCodes.append(f"for iRespDev = 1:numel(beCheckedRespDevs) ")
        cRespCodes.append(f"if beCheckedRespDevs(iRespDev).needTobeReset")
        if Info.PLATFORM == 'linux':
            cRespCodes.append(f"lptoutMex(parPort(beCheckedRespDevs(iRespDev).respCodeDevIdx).port, 0);")
        elif Info.PLATFORM == 'windows':
            cRespCodes.append(f"io64(io64Obj, parPort(beCheckedRespDevs(iRespDev).respCodeDevIdx).port, 0);")
        elif Info.PLATFORM == 'mac':
            cRespCodes.append("% currently, under Mac OX we just do nothing for parallel ports")
        cRespCodes.append(f"end % if needTobeSet")
        cRespCodes.append(f"end % for iRespDev")
        cRespCodes.append(f"end % if cFrame Dur less than 10 ms")

    cRespCodes.append("%=================================================\\\n")

    shortPulseDurParallelsDict = outPutTriggerCheck(cWidget)

    # to be continue ...
    # if not isDummyPrint and cWidget.widget_id == cInfoDict.get("lastWidgetId"):
    #     cRespCodes.append(f"WaitSecs(cDurs({cWinIdx})); for the last event in all Exp, just wait for duration")
    #

    # if the current widget is the last one in the timeline, just print response codes here
    if Func.getNextWidgetId(cWidget.widget_id) is None:

        cRespCodes.append(f"if numel(beCheckedRespDevs) < 1")
        cRespCodes.append(f"WaitSecs(cDurs({cWinIdx})); for the last event in timeline just wait for duration")
        cRespCodes.append(f"end")
        cRespCodes.append(f"beCheckedRespDevs = []; % empty the to be checked response devices")

        cRespCodes = printRespCodes(f, cRespCodes)
    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------
    delayedPrintCodes.update({'codesAfFip': cAfFlipCodes})
    delayedPrintCodes.update({'respCodes': cRespCodes})

    return delayedPrintCodes


def drawSoundWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes):
    global enabledKBKeysList, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    cRespCodes = []
    cAfFlipCodes = []

    cAfFlipCodes = delayedPrintCodes.get('codesAfFlip',[])
    cRespCodes = delayedPrintCodes.get('respCodes',[])

    if Func.getWidgetPosition(cWidget.widget_id) == 0:
        # Step 2: print out help info for the current widget
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, Func.getWidgetPosition(cWidget.widget_id) + 1,
                     Func.getWidgetName(cWidget.widget_id))
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    debugPrint("-- dev name id map---/")
    debugPrint(inputDevNameIdxDict)
    debugPrint(outputDevNameIdxDict)
    debugPrint("----------------------\\")

    cProperties = Func.getProperties(cWidget.widget_id)
    debugPrint(f"{cWidget.widget_id} properties:")
    debugPrint(f"{cProperties}")
    debugPrint("-------------------------------\\")

    debugPrint(f"line 714: {attributesSetDict}")
    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    shouldNotBeCitationCheck('Screen Name',cWidget.getScreenName())

    cScreenName, ign = getRefValue(cWidget, cWidget.getScreenName(), attributesSetDict)

    # currently we just used the nearest previous flipped screen info
    # cWinIdx = historyPropDict.get("cWinIdx")
    cWinIdx = outputDevNameIdxDict.get(cScreenName)
    cWinStr = f"winIds({cWinIdx})"



    # historyPropDict.update({"cScreenName": cScreenName})
    historyPropDict.update({"cWinIdx": cWinIdx})
    historyPropDict.update({"cWinStr": cWinStr})


    # 2) handle file name:
    cFilenameStr, isRef = getRefValue(cWidget, cWidget.getFilename(), attributesSetDict)
    cFilenameStr, toBeSavedDir = parseFilenameStr(cFilenameStr,isRef)

    # # 3) check the Buffer Size parameter:
    # bufferSizeStr, isRef = getRefValue(cWidget, cWidget.getBufferSize(), attributesSetDict)

    # 3) check the Stream refill parameter:
    streamRefillStr, isRef = getRefValue(cWidget, cWidget.getRefillMode(), attributesSetDict)

    # 4) check the start offset in ms parameter:
    startOffsetStr, isRef = getRefValue(cWidget, cWidget.getStartOffset(), attributesSetDict)

    # 5) check the stop offset in ms parameter:
    StopOffsetStr, isRef = getRefValue(cWidget, cWidget.getStopOffset(), attributesSetDict)

    # # 6) check the repetitions parameter:
    # repetitionsStr, isRef = getRefValue(cWidget, cWidget.getRepetitions(), attributesSetDict)

    # 7) check the volume control parameter:
    isVolumeControl, isRef = getRefValue(cWidget, cWidget.getIsVolumeControl(), attributesSetDict)

    # 8) check the volume parameter:
    volumeStr, isRef = getRefValue(cWidget, cWidget.getVolume(), attributesSetDict)

    # 9) check the latencyBias control parameter:
    isLantencyBiasControl, isRef = getRefValue(cWidget, cWidget.getIsLatencyBias(), attributesSetDict)

    # 10) check the volume parameter:
    latencyBiasStr, isRef = getRefValue(cWidget, cWidget.getBiasTime(), attributesSetDict)

    # 11) check the sound device name parameter:
    shouldNotBeCitationCheck('Sound device', cWidget.getSoundDeviceName())
    cSoundDevName, isRef = getRefValue(cWidget, cWidget.getSoundDeviceName(), attributesSetDict)
    cSoundIdxStr = outputDevNameIdxDict.get(cSoundDevName)

    # 12) check the volume parameter:
    waitForStartStr = parseBooleanStr(*getRefValue(cWidget, cWidget.getWaitForStart(), attributesSetDict))

    clearAfter = dataStrConvert(*getRefValue(cWidget, cProperties['Clear after'], attributesSetDict))
    clearAfter = parseDontClearAfterStr(clearAfter)

    historyPropDict.update({"clearAfter": clearAfter})


    # read audio file
    printAutoInd(f, "cAudioData    = audioread(fullfile(cFolder,{0}) );", addSingleQuotes(cFilenameStr))

    # make audio buffer
    # printAutoInd(f, "cAudioIdx     = PsychPortAudio('CreateBuffer', {0}, cAudioData);",cSoundIdxStr)

    #  draw buffer to  hw
    # printAutoInd(f, "PsychPortAudio('FillBuffer', {0}, cAudioIdx, {1});",cSoundIdxStr, streamRefillStr)
    printAutoInd(f, "PsychPortAudio('FillBuffer', {0}, cAudioData, {1});",cSoundIdxStr, streamRefillStr)

    if isVolumeControl:
        printAutoInd(f, "PsychPortAudio('Volume', {0}, {1});\n", cSoundIdxStr, volumeStr)

    if isLantencyBiasControl:
        printAutoInd(f, "PsychPortAudio('LatencyBias', {0}, {1}/1000);\n", cSoundIdxStr, latencyBiasStr)


    printAutoInd(f, "detectAbortKey(abortKeyCode); % check abort key in the start of every event\n")


    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------

    # cRespCodes.append(f"% delete audio buffer corresponding to {cFilenameStr}")
    # cRespCodes.append(f"PsychPortAudio('DeleteBuffer', cAudioIdx, 0);\n")

    delayedPrintCodes.update({'codesAfFip': cAfFlipCodes})
    delayedPrintCodes.update({'respCodes': cRespCodes})

    return delayedPrintCodes



def drawImageWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes):
    global enabledKBKeysList, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    cRespCodes = []
    cAfFlipCodes = []

    cAfFlipCodes = delayedPrintCodes.get('codesAfFlip',[])
    cRespCodes = delayedPrintCodes.get('respCodes',[])

    if Func.getWidgetPosition(cWidget.widget_id) == 0:
        # Step 2: print out help info for the current widget
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, Func.getWidgetPosition(cWidget.widget_id) + 1,
                     Func.getWidgetName(cWidget.widget_id))
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    debugPrint("-- dev name id map---/")
    debugPrint(inputDevNameIdxDict)
    debugPrint(outputDevNameIdxDict)
    debugPrint("----------------------\\")

    cProperties = Func.getProperties(cWidget.widget_id)
    debugPrint(f"{cWidget.widget_id} properties:")
    debugPrint(f"{cProperties}")
    debugPrint("-------------------------------\\")

    debugPrint(f"line 714: {attributesSetDict}")
    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    shouldNotBeCitationCheck('Screen Name',cWidget.getScreenName())

    cScreenName, ign = getRefValue(cWidget, cWidget.getScreenName(), attributesSetDict)

    cWinIdx = outputDevNameIdxDict.get(cScreenName)
    cWinStr = f"winIds({cWinIdx})"

    historyPropDict.update({"cScreenName": cScreenName})
    historyPropDict.update({"cWinIdx": cWinIdx})
    historyPropDict.update({"cWinStr": cWinStr})


    # 2) handle file name:
    cFilenameStr, isRef = getRefValue(cWidget, cWidget.getFilename(), attributesSetDict)
    cFilenameStr, toBeSavedDir = parseFilenameStr(cFilenameStr,isRef)

    # 3) check the mirror up/down parameter:
    isMirrorUpDownStr = parseBooleanStr(cWidget.getIsMirrorUpAndDown())

    # 3) check the mirror left/right parameter:
    isMirrorLeftRightStr = parseBooleanStr(cWidget.getIsMirrorLeftAndRight())

    # 4) check the rotate parameter:
    rotateStr, isRef = getRefValue(cWidget, cWidget.getRotate(), attributesSetDict)

    # 5) check the stretch mode parameter:
    if cProperties['Stretch']:
        # ""、Both、LeftRight、UpDown、[attr]
        stretchModeStr = parseStretchModeStr(*getRefValue(cWidget, cProperties['Stretch mode'], attributesSetDict))
    else:
        stretchModeStr = "0"

    # 6) check the Transparent parameter:
    imageTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Transparent'], attributesSetDict))


    # 7) check the parameter winRect
    sx = dataStrConvert(*getRefValue(cWidget, cProperties['X position'], attributesSetDict))
    sy = dataStrConvert(*getRefValue(cWidget, cProperties['Y position'], attributesSetDict))
    cWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Width'], attributesSetDict))
    cHeight = dataStrConvert(*getRefValue(cWidget, cProperties['Height'], attributesSetDict))

    printAutoInd(f, "cFrameRect = makeFrameRect({0}, {1}, {2}, {3}, fullRects({4},:));",sx,sy,cWidth,cHeight,cWinIdx)

    # before we draw the image， we draw the frame rect first:
    borderColor = dataStrConvert(*getRefValue(cWidget, cProperties['Border color'], attributesSetDict))
    borderWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Border width'], attributesSetDict))
    frameFillColor = dataStrConvert(*getRefValue(cWidget, cProperties['Frame fill color'], attributesSetDict))
    frameTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Frame transparent'], attributesSetDict))

    # get enable parameter
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Enable'], attributesSetDict)
    isBkFrameEnable = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    if isBkFrameEnable == '1':

        # if (frameFillColor == historyPropDict[cScreenName]) and (frameTransparent in [1,255]):
        if (frameFillColor != historyPropDict[f"{cScreenName}_bkColor"]):
            printAutoInd(f, "Screen('FillRect',{0},{1}, cFrameRect);", cWinStr,
                         addedTransparentToRGBStr(frameFillColor, frameTransparent))

        # draw the frame only when the frame color is different from the frame fill color
        if borderColor != frameFillColor:
            printAutoInd(f, "Screen('frameRect',{0},{1},cFrameRect,{2});", cWinStr,
                         addedTransparentToRGBStr(frameFillColor, frameTransparent), borderWidth)

    # make texture
    printAutoInd(f, "cImData    = imread(fullfile(cFolder,{0}) );",addSingleQuotes(cFilenameStr))
    printAutoInd(f, "cImIndex   = MakeTexture({0}, cImData);",cWinStr)

    printAutoInd(f, "cDestRect  = makeImDestRect(cFrameRect, size(cImData), {0});", stretchModeStr)
    #  print out the text

    if isMirrorUpDownStr == '1' or isMirrorLeftRightStr == '1':
        printAutoInd(f, "[xc, yc] = RectCenter(cDestRect);        % get the center of the destRect")
        printAutoInd(f, "Screen('glPushMatrix', {0});             % enter into mirror mode",cWinStr)
        printAutoInd(f, "Screen('glTranslate', {0}, xc, yc, 0);   % translate origin into the center of destRect",cWinStr)
        if isMirrorLeftRightStr == '1':
            leftRightStr = '-1'
        else:
            leftRightStr = '1'

        if isMirrorUpDownStr == '1':
            upDownStr = '-1'
        else:
            upDownStr = '1'

        printAutoInd(f, "Screen('glScale', {0}, {1}, {2}, 1);     % mirror the drawn image",cWinStr,leftRightStr,upDownStr)
        printAutoInd(f, "Screen('glTranslate', {0}, -xc, -yc, 0); % undo the translations",cWinStr)

    printAutoInd(f, "DrawTexture({0}, cImIndex ,[] ,cDestRect ,{1} ,[] , abs({2}));",
                 cWinStr,
                 rotateStr,
                 imageTransparent)

    if isMirrorUpDownStr == '1' or isMirrorLeftRightStr == '1':
        printAutoInd(f, "Screen('glPopMatrix', {0}); % restore to non mirror mode", cWinStr)


    clearAfter = dataStrConvert(*getRefValue(cWidget, cProperties['Clear after'], attributesSetDict))
    clearAfter = parseDontClearAfterStr(clearAfter)

    historyPropDict.update({"clearAfter": clearAfter})

    printAutoInd(f, "Screen('DrawingFinished',{0},{1});", cWinStr, clearAfter)
    printAutoInd(f, "detectAbortKey(abortKeyCode); % check abort key in the start of every event\n")


    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------

    cRespCodes.append(f"% close the texture corresponding to {cFilenameStr}")
    cRespCodes.append(f"Screen('Close', cImIndex);\n")

    delayedPrintCodes.update({'codesAfFip': cAfFlipCodes})
    delayedPrintCodes.update({'respCodes': cRespCodes})

    return delayedPrintCodes


def drawTextWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes):
    global enabledKBKeysList, inputDevNameIdxDict, outputDevNameIdxDict, historyPropDict, isDummyPrint

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the output var's row num
    cRespCodes = []
    cAfFlipCodes = []

    cAfFlipCodes = delayedPrintCodes.get('codesAfFlip',[])
    cRespCodes = delayedPrintCodes.get('respCodes',[])

    if Func.getWidgetPosition(cWidget.widget_id) == 0:
        # Step 2: print out help info for the current widget
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, Func.getWidgetPosition(cWidget.widget_id) + 1,
                     Func.getWidgetName(cWidget.widget_id))
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')

    debugPrint("-- dev name id map---/")
    debugPrint(inputDevNameIdxDict)
    debugPrint(outputDevNameIdxDict)
    debugPrint("----------------------\\")

    cProperties = Func.getProperties(cWidget.widget_id)
    debugPrint(f"{cWidget.widget_id} properties:")
    debugPrint(f"{cProperties}")
    debugPrint("-------------------------------\\")

    debugPrint(f"line 714: {attributesSetDict}")
    # ------------------------------------------------
    # Step 1: draw the stimuli for the current widget
    # -------------------------------------------------
    # 1) get the win id info in matlab format winIds(idNum)
    shouldNotBeCitationCheck('Screen Name',cWidget.getScreenName())

    cScreenName, ign = getRefValue(cWidget, cWidget.getScreenName(), attributesSetDict)

    cWinIdx = outputDevNameIdxDict.get(cScreenName)
    cWinStr = f"winIds({cWinIdx})"

    historyPropDict.update({"cScreenName": cScreenName})
    historyPropDict.update({"cWinIdx": cWinIdx})
    historyPropDict.update({"cWinStr": cWinStr})


    # 2) handle the text content
    cTextContentStr = parseTextContentStr(*getRefValue(cWidget, cProperties['Text'], attributesSetDict))

    # 3) check the alignment X parameter:
    alignmentX = dataStrConvert(*getRefValue(cWidget, cProperties['Alignment X'], attributesSetDict))

    # 4) check the alignment X parameter:
    alignmentY = dataStrConvert(*getRefValue(cWidget, cProperties['Alignment Y'], attributesSetDict))

    # 5) check the color parameter:
    fontColorStr = dataStrConvert(*getRefValue(cWidget, cProperties['Fore color'], attributesSetDict))
    fontTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Transparent'], attributesSetDict))

    # 7) check the flip hor parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Flip horizontal'], attributesSetDict)
    flipHorStr = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 8) check the flip ver parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Flip vertical'], attributesSetDict)
    flipVerStr = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 10) check the right to left parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Right to left'], attributesSetDict)
    rightToLeft = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    # 11) check the parameter winRect
    sx = dataStrConvert(*getRefValue(cWidget, cProperties['X position'], attributesSetDict))
    sy = dataStrConvert(*getRefValue(cWidget, cProperties['Y position'], attributesSetDict))
    cWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Width'], attributesSetDict))
    cHeight = dataStrConvert(*getRefValue(cWidget, cProperties['Height'], attributesSetDict))

    frameRectStr = f"makeFrameRect({sx}, {sy}, {cWidth}, {cHeight}, fullRects({cWinIdx},:))"

    # set the font name size color style:
    fontName = dataStrConvert(*getRefValue(cWidget, cProperties['Font family'], attributesSetDict))
    fontSize = dataStrConvert(*getRefValue(cWidget, cProperties['Font size'], attributesSetDict))
    fontStyle = dataStrConvert(*getRefValue(cWidget, cProperties['Style'], attributesSetDict))
    fontStyle = parseFontStyleStr(fontStyle)

    fontBkColor = dataStrConvert(*getRefValue(cWidget, cProperties['Back color'], attributesSetDict))

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
    borderColor = dataStrConvert(*getRefValue(cWidget, cProperties['Border color'], attributesSetDict))
    borderWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Border width'], attributesSetDict))
    frameFillColor = dataStrConvert(*getRefValue(cWidget, cProperties['Frame fill color'], attributesSetDict))
    # if f"preFrameFillColor" not in historyPropDict:
    frameTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Frame transparent'], attributesSetDict))

    debugPrint(f"frameTransparent: {frameTransparent}")

    cRefedValue, isRef = getRefValue(cWidget, cProperties['Enable'], attributesSetDict)
    isBkFrameEnable = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    if isBkFrameEnable == '1':

        # if (frameFillColor == historyPropDict[cScreenName]) and (frameTransparent in [1,255]):
        if (frameFillColor != historyPropDict[f"{cScreenName}_bkColor"]):
            printAutoInd(f, "Screen('FillRect',{0},{1},{2});", cWinStr,
                         addedTransparentToRGBStr(frameFillColor, frameTransparent), frameRectStr)

        # draw the frame only when the frame color is different from the frame fill color
        if borderColor != frameFillColor:
            printAutoInd(f, "Screen('frameRect',{0},{1},{2},{3});", cWinStr,
                         addedTransparentToRGBStr(frameFillColor, frameTransparent), frameRectStr, borderWidth)

    #  print out the text
    printAutoInd(f, "DrawFormattedText({0},{1},{2},{3},{4},{5},{6},{7},[],{8},{9});",
                 cWinStr,
                 cTextContentStr,
                 alignmentX,
                 alignmentY,
                 addedTransparentToRGBStr(fontColorStr, fontTransparent),
                 dataStrConvert(*getRefValue(cWidget, cProperties['Wrapat chars'], attributesSetDict)),
                 flipHorStr,
                 flipVerStr,
                 rightToLeft,
                 frameRectStr)

    clearAfter = dataStrConvert(*getRefValue(cWidget, cProperties['Clear after'], attributesSetDict))
    clearAfter = parseDontClearAfterStr(clearAfter)

    historyPropDict.update({"clearAfter": clearAfter})

    printAutoInd(f, "Screen('DrawingFinished',{0},{1});", cWinStr, clearAfter)
    printAutoInd(f, "detectAbortKey(abortKeyCode); % check abort key in the start of every event\n")


    # -------------------------------------------------------------
    #  we need to dummy draw stim for the next widget
    # so here after we will print any code into delayedPrintCodes
    # -------------------------------------------------------------

    # ------------------------------------------------------------------
    # Step 6: acquire responses
    # ------------------------------------------------------------------
    # after drawing the next widget's stimuli, get the duration first
    # durStr, isRefValue, cRefValueSet = getRefValueSet(cWidget, cWidget.getDuration(), attributesSetDict)
    # durStr = parseDurationStr(durStr)

    # cRespCodes.append(f"cDurs({cWinIdx}) = getDurValue([{durStr}],winIFIs({cWinIdx}) );")



    # shortPulseDurParallelsDict = outPutTriggerCheck(cWidget)

    # to be continue ...

    # if the current widget is the last one in the timeline, just print response codes here
    # if Func.getNextWidgetId(cWidget.widget_id) is None:
    #     for cValue in cRespCodes:
    #         printAutoInd(f, cValue)
    #     cRespCodes = []
    # ------------------------------------------
    # the last step: upload the delayed codes
    # ------------------------------------------
    delayedPrintCodes.update({'codesAfFip': cAfFlipCodes})
    delayedPrintCodes.update({'respCodes': cRespCodes})

    return delayedPrintCodes







""" useless, because the timeline type will dependent on selected input when the selection order is counterbalanced
def dummyRunTimeline(cWidget):
    global incrOpRowNum

    incrOpRowNum   += 1
    cTimelineRowIdx = incrOpRowNum

    cTimelineWidgetIds = Func.getWidgetIDInTimeline(cWidget.widget_id)

    for cWidgetId in cTimelineWidgetIds:
        cWidget = Info.WID_WIDGET[cWidgetId]

        if Info.CYCLE == cWidget.widget_id.split('.')[0]:
            dummyRunCycle(cWidget)
        else:
            pass

def dummyRunCycle(cWidget):


def getOutputnRows(globalSelf):
    global  incrOpRowNum
    incrOpRowNum = 0

    dummyRunTimeline(Info.WID_WIDGET[f"{Info.TIMELINE}.0"])


    return incrOpRowNum
"""


def compilePTB(globalSelf):
    global cInfoDict
    cInfoDict.clear()

    compileCode(globalSelf,True)

    compileCode(globalSelf, False)

    cInfoDict.clear()



def compileCode(globalSelf, isDummyCompile):
    global enabledKBKeysList, inputDevNameIdxDict, outputDevNameIdxDict, cIndents, historyPropDict, isDummyPrint, spFormatVarDict

    # -----------initialize global variables ------/
    isDummyPrint = isDummyCompile

    delayedPrintCodes = {'codesAfFip': [], 'respCodes': []}

    historyPropDict = dict()

    historyPropDict.update({'clearAfter': "0"})
    historyPropDict.update({'fontName': "simSun"})
    historyPropDict.update({'fontSize': "12"})
    historyPropDict.update({'fontStyle': "0"})
    historyPropDict.update({'fontBkColor': "[259,0,0]"})  # we give the bkcolor an impossible initial value

    cIndents = 0
    cLoopLevel = 0

    inputDevNameIdxDict = dict()
    outputDevNameIdxDict = dict()

    enabledKBKeysList.clear()

    enabledKBKeysList.add(parseKbCorRespStr('{escape}', False, 'keyboard')[1:-1])

    attributesSetDict = {'sessionNum': [0, 'SubInfo.session', {'SubInfo.session'}],
                         'subAge': [0, 'SubInfo.age', {'SubInfo.age'}],
                         'subName': [0, 'SubInfo.name', {'SubInfo.name'}],
                         'subSex': [0, 'SubInfo.sex', {'SubInfo.sex'}], 'subNum': [0, 'SubInfo.num', {'SubInfo.num'}],
                         'subHandness': [0, 'SubInfo.hand', {'SubInfo.hand'}]}
    spFormatVarDict = dict()
    # -------------------------------------------\

    # only replaced percent vars that will be reffed by % with - value /100
    spFormatVarDict = getSepcialFormatAtts()

    debugPrint(f"line 1148: {spFormatVarDict}")

    if not Info.FILE_NAME:
        if not globalSelf.getFileName():
            QMessageBox.information(globalSelf, "Warning", "File must be saved before compiling.", QMessageBox.Ok)
            return

    globalSelf.save()
    # get save path
    compile_file_name = ".".join(Info.FILE_NAME.split('.')[:-1]) + ".m"
    # open file
    with open(compile_file_name, "w", encoding="GBK") as f:
        #  print function start info
        cFilenameOnly = os.path.split(compile_file_name)[1].split('.')[0]
        # the help info

        printAutoInd(f, "function {0}()", cFilenameOnly)
        printAutoInd(f, "% function generated by PTB Builder 0.1")
        printAutoInd(f,
                     "% If you use PTB Builder for your research, then we would appreciate your citing our work in your paper:")
        printAutoInd(f,
                     "% , (2019) PTB builder: a free GUI to generate experimental codes for Psychoolbox. Behavior Research Methods\n%")
        printAutoInd(f, "% To report possible bugs and any suggestions please send us e-mail:")
        printAutoInd(f, "% Yang Zhang")
        printAutoInd(f, "% Ph.D, Prof.")
        printAutoInd(f, "% Department of Psychology, \n% SooChow University")
        printAutoInd(f, "% zhangyang873@gmail.com \n% Or\n% yzhangpsy@suda.edu.cn")
        printAutoInd(f, "% {0}", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # begin of the function
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "%      begin      ")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        # get subject information
        printAutoInd(f, "%----- get subject information -------/", )
        printAutoInd(f, "cFolder = fileparts(mfilename('fullpath'));")
        printAutoInd(f, "subInfo = OpenExp_BCL('{0}', cFolder);", cFilenameOnly)
        printAutoInd(f, "close(gcf);")
        printAutoInd(f, "%-------------------------------------\\\n")

        # the function body try, catch end
        printAutoInd(f, "try")
        printAutoInd(f, "KbName('UnifyKeyNames');\n")
        printAutoInd(f, "abortKeyCode = KbName('ESCAPE');\n")

        printAutoInd(f, "expStartTime = datestr(now,'dd-mmm-YYYY:HH:MM:SS'); % record start time \n")

        printAutoInd(f, "%--------Reinitialize the global random seed ---------/")
        printAutoInd(f, "cRandSeed = RandStream('mt19937ar','Seed','shuffle');")
        printAutoInd(f, "RandStream.setGlobalStream(cRandSeed);")
        printAutoInd(f, "%-----------------------------------------------------\\\n")
        printAutoInd(f, "HideCursor;            % hide mouse cursor")

        if Info.PLATFORM == 'windows':
            printAutoInd(f, "ShowHideWinTaskbar(0); % hide the window taskbar")

        printAutoInd(f, "commandwindow;         % bring the command window into front")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% define and initialize input/output devices")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # get output devices, such as global output devices.
        # you can get each widget's device you selected
        output_devices = Info.OUTPUT_DEVICE_INFO
        input_devices = Info.INPUT_DEVICE_INFO
        eyetracker_devices = Info.TRACKER_INFO
        quest_devices = Info.QUEST_INFO

        print(f"eyetracker: {eyetracker_devices}")
        print(f"quest: {quest_devices}")

        debugPrint('-------------/')
        debugPrint(output_devices)
        debugPrint('-------------\\\n')

        iQuest = 1
        if len(quest_devices) > 0:
            printAutoInd(f, "%------- initialize Quests ----------/")

            for quest in quest_devices.values():
                outputDevNameIdxDict.update({f"{quest['Quest Type']}-{quest['Quest Name']}": f"{iQuest}"})

                printAutoInd(f, "quest({0}) = QuestCreate({1},{2},{3},{4},{5},{6});",
                             iQuest,
                             quest['Estimated threshold'],
                             quest['Std dev'],
                             quest['Desired proportion'],
                             quest['Steepness'],
                             quest['Proportion'],
                             quest['Chance level'])

                if quest['Is log10 transform'] == 'yes':
                    printAutoInd(f, "quest({0}).isLog10Trans     = True;", iQuest)
                else:
                    printAutoInd(f, "quest({0}).isLog10Trans     = False;", iQuest)

                printAutoInd(f, "quest({0}).maxStimIntensity = {1};", iQuest, quest['Maximum'])
                printAutoInd(f, "quest({0}).minStimIntensity = {1};\n", iQuest, quest['Minimum'])

                printAutoInd(f, "% get the first stimulus intensity")
                if quest['Method'] == 'quantile':
                    printAutoInd(f, "quest({0}).cValue = QuestQuantile(quest({1}));", iQuest, iQuest)
                elif quest['Method'] == 'mean':
                    printAutoInd(f, "quest({0}).cValue = QuestMean(quest({1}));", iQuest, iQuest)
                elif quest['Method'] == 'mode':
                    printAutoInd(f, "quest({0}).cValue = QuestMode(quest({1}));", iQuest, iQuest)
                else:
                    throwCompileErrorInfo("quest method should be of {'quantile', 'mean', or 'mode'}!!")

                #  intensity transform:
                printAutoInd(f, "quest({0}) = questValueTrans(quest({1}));\n", iQuest, iQuest)

                attributesSetDict.update(
                    {f"{quest['Quest Name']}.cValue": [0, f"quest({iQuest}).cValue", {f"quest({iQuest}).cValue"}]})

                iQuest += 1
            printAutoInd(f, "%------------------------------------\\")

        printAutoInd(f, "%====== define input devices ========/")
        iKeyboard = 1
        iGamepad = 1
        iRespBox = 1
        iMouse = 1

        debugPrint(f"line 1581 a = {input_devices}")

        for inputDevId, cDevice in input_devices.items():

            # create a map dict to map device name (key) to device ID (value)
            if cDevice['Device Type'] == 'response box':
                # for response box (port address)
                inputDevNameIdxDict.update({cDevice['Device Name']: f"{iRespBox}"})
            else:
                # for keyboards, game-pads, mice (indices)
                inputDevNameIdxDict.update({cDevice['Device Name']: f"{int(cDevice['Device Port'])+1}"})


            if cDevice['Device Type'] == 'keyboard':
                iKeyboard += 1
            elif cDevice['Device Type'] == 'mouse':
                iMouse += 1
            elif cDevice['Device Type'] == 'game pad':
                iGamepad += 1
            elif cDevice['Device Type'] == 'response box':
                printAutoInd(f, "rbIndices({0})   = CedrusResponseBox('Open', '{1}');", iRespBox, cDevice['Device Port'])
                iRespBox += 1

        # if u'\u4e00' <= char <= u'\u9fa5':  # 判断是否是汉字

        # printAutoInd(f, "% get input device indices")
        printAutoInd(f, "kbIndices      = unique(GetKeyboardIndices);")

        if iGamepad > 1:
            if Info.PLATFORM == 'windows':
                if iGamepad == 2:
                    printAutoInd(f, "gamepadIndices = 0; % joystickMex starts from 0 ")
                else:
                    printAutoInd(f, "gamepadIndices = 0:{0}; % getGamepadIndices does not work on windows ",iGamepad - 2)
            else:
                printAutoInd(f, "gamepadIndices = unique(GetGamepadIndices);")

        if Info.PLATFORM == "linux":
            printAutoInd(f, "miceIndices    = unique(GetMouseIndices('slavePointer'));")
        else:
            printAutoInd(f, "miceIndices    = unique(GetMouseIndices);")

        printAutoInd(f, "%====================================\\\n\n")

        printAutoInd(f, "%===== define output devices ========/")

        iMonitor = 1
        iParal = 1
        iNetPort = 1
        iSerial = 1
        iSound = 1

        # debugPrint(output_devices)

        for outDev_Id, cDevice in output_devices.items():

            if cDevice['Device Type'] == Info.DEV_SCREEN:
                outputDevNameIdxDict.update({cDevice['Device Name']: f"{iMonitor}"})

                historyPropDict.update({f"{cDevice['Device Name']}_bkColor": addSquBrackets(cDevice['Back Color'])})
                # historyPropDict.update({f"{cDevice['Device Name']}_lastFlipTimeVar": []})

                printAutoInd(f, "monitors({0}).port        =  {1};", iMonitor, cDevice['Device Port'])
                printAutoInd(f, "monitors({0}).name        = '{1}';", iMonitor, cDevice['Device Name'])
                printAutoInd(f, "monitors({0}).bkColor     = [{1}];", iMonitor, cDevice['Back Color'])
                printAutoInd(f, "monitors({0}).multiSample =  {1};\n", iMonitor, cDevice['Multi Sample'])
                iMonitor += 1
            elif cDevice['Device Type'] == Info.DEV_NETWORK_PORT:

                outputDevNameIdxDict.update({cDevice['Device Name']: f"tcpipCons({iNetPort})"})
                printAutoInd(f, "TCPIPs({0}).ipAdd    = '{1}';", iNetPort, cDevice['Device Port'])
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

                outputDevNameIdxDict.update({cDevice['Device Name']: f"audioIds({iSound})"})
                printAutoInd(f, "audioDevs({0}).port     = {1};", iSound, cDevice['Device Port'])
                printAutoInd(f, "audioDevs({0}).name     = '{1}';", iSound, cDevice['Device Name'])
                if 'auto' == cDevice['Sampling Rate']:
                    printAutoInd(f, "audioDevs({0}).fs       = []; % the default value in PTB is 48000 Hz\n", iSound)
                else:
                    printAutoInd(f, "audioDevs({0}).fs       = {1};\n", iSound, cDevice['Sampling Rate'])

                iSound += 1

        printAutoInd(f, "%====================================\\\n")

        printAutoInd(f, "disableSomeKbKeys; % restrictKeysForKbCheck")

        printAutoInd(f, "%===== initialize output devices ========/")
        printAutoInd(f, "winIds            = zeros({0},1);", iMonitor - 1)
        printAutoInd(f, "lastScrOnsettime  = zeros({0},1);", iMonitor - 1)
        printAutoInd(f, "cDurs             = zeros({0},1);", iMonitor - 1)
        printAutoInd(f, "winIFIs           = zeros({0},1);", iMonitor - 1)
        printAutoInd(f, "fullRects         = zeros({0},4);\n", iMonitor - 1)
        # printAutoInd(f, "beCheckedRespDevs = [];")
        printAutoInd(f,"beCheckedRespDevs    = struct('beUpdatedVar','','allowAble',[],'corResp',[],'rtWindow',[],'endAction',[],'type',[],'index',[],'startTime',[],'isOn',[],'needTobeReset',[],'right',[],'wrong',[],'noResp',[],'respCodeDevIdx',[]);")
        printAutoInd(f,"beCheckedRespDevs(1) = [];")
        printAutoInd(f, "cFrame    = struct('rt',[],'acc',[],'resp',[]);")
        printAutoInd(f, "cFrame(1) = [];")

        printAutoInd(f, "%--- open windows ---/")
        printAutoInd(f, "for iWin = 1:numel(monitors)")
        printAutoInd(f,
                     "[winIds(iWin),fullRects(iWin,:)] = Screen('OpenWindow',monitors(iWin).port,monitors(iWin).bkColor,[],[],[],[],monitors(iWin).multiSample);")
        printAutoInd(f,
                     "Screen('BlendFunction', winIds(iWin),'GL_SRC_ALPHA','GL_ONE_MINUS_SRC_ALPHA'); % force to most common alpha-blending factors")
        printAutoInd(f,
                     "winIFIs(iWin) = Screen('GetFlipInterval',winIds(iWin));                        % get inter frame interval (i.e., 1/refresh rate)")
        printAutoInd(f, "end % for iWin ")

        printAutoInd(f, "%--------------------\\\n")

        # initialize TCPIP connections
        if iNetPort > 1:
            printAutoInd(f, "%--- open TCPIPs ----/")
            printAutoInd(f, "tcpipCons = zeros({0},1);", iNetPort - 1)

            printAutoInd(f, "for iCount = 1:numel(TCPIPs)")

            if cDevice['Is Client'] == 'yes':
                printAutoInd(f, "tcpipCons(iCount) = pnet('tcpconnect',TCPIPs(iCount).ipAdd,TCPIPs(iCount).port);")
            else:
                printAutoInd(f, "tcpipCons(iCount) = pnet('tcpsocket',TCPIPs(iCount).port);")

            printAutoInd(f, "end % iCount")

            printAutoInd(f, "%----------------------\\\n")

        # initialize serial ports
        if iSerial > 1:
            printAutoInd(f, "%--- open serial ports ----/")
            printAutoInd(f, "serialCons = zeros({0},1);", iSerial - 1)

            printAutoInd(f, "for iCount = 1:numel(serialCons)")
            printAutoInd(f,
                         "serialCons(iCount) = IOPort('OpenSerialPort',serPort(iCount).port,['BaudRate=',serPort(iCount).baudRate,',DataBits=',serPort(iCount).dataBits]);")
            printAutoInd(f, "end % iCount")
            printAutoInd(f, "%--------------------------\\\n")
        # initialize parallel ports
        if iParal > 1:
            printAutoInd(f, "%--- open parallel ports ----/")
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
            printAutoInd(f, "%----------------------------\\\n")

        #  initialize audio output devices
        if iSound > 1:
            printAutoInd(f, "%--open output audio devs----/")
            printAutoInd(f, "InitializePsychSound(1); % Initialize the audio driver, require low-latency preinit\n")
            printAutoInd(f, "audioIds = zeros({0},1);", iSound - 1)
            # printAutoInd(f,"audioFs = getAudioFsFromFirstAudioFile;")

            printAutoInd(f, "for iCount = 1:numel(audioDevs)")
            printAutoInd(f,
                         "audioIds(iCount) = PsychPortAudio('Open',audioDevs(iCount).port,1,[],audioDevs(iCount).fs,2);" )
            printAutoInd(f, "end % iCount")
            printAutoInd(f, "%----------------------------\\\n")

        printAutoInd(f, "%========================================\\\n")

        printAutoInd(f, "Priority(1);      % Turn the priority to high priority")
        printAutoInd(f, "opRowIdx     = 1; % set the output variables row num")
        printAutoInd(f, "iLoop_0_cOpR = opRowIdx;")

        # start to handle all the widgets
        printTimelineWidget(Info.WID_WIDGET[f"{Info.TIMELINE}.0"], f, attributesSetDict, cLoopLevel, delayedPrintCodes)

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

        printAutoInd(f, "save(subInfo.filename); % save the results\n")

        #  close opened devices
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% close opened devices")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
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
            printAutoInd(f, "%--- close outputAudio devs--/")

            printAutoInd(f, "for iCount = 1:numel(audioIds)")
            printAutoInd(f, "PsychPortAudio('Close', audioIds(iCount));")
            printAutoInd(f, "end % iCount")
            printAutoInd(f, "%----------------------------\\\n")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% end of the experiment", )
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

        printAutoInd(f, "catch {0}_error\n", cFilenameOnly)

        printAutoInd(f, "sca;                        % Close opened windows")
        printAutoInd(f, "ShowCursor;                 % Show the hided mouse cursor")
        printAutoInd(f, "Priority(0);                % Turn the priority back to normal")
        printAutoInd(f, "RestrictKeysForKbCheck([]); % Re-enable all keys")

        if Info.PLATFORM == 'windows':
            printAutoInd(f, "ShowHideWinTaskbar(1);      % show the window taskbar")

        # close TCPIP connections
        if iNetPort > 1:
            printAutoInd(f, "close serial ports:")

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
            printAutoInd(f, "%close outputAudio devs:")

            printAutoInd(f, "for iCount = 1:numel(audioIds)")
            printAutoInd(f, "PsychPortAudio('Close', audioIds(iCount));")
            printAutoInd(f, "end % iCount")
            # close Cedrus response box
            if iRespBox > 1:
                printAutoInd(f, "%close Cedrus response boxes:")
                printAutoInd(f, "CedrusResponseBox('CloseAll');\n")

        printAutoInd(f, "save([subInfo.filename,'_debug']);")
        printAutoInd(f, "rethrow({0}_error);", cFilenameOnly)

        #

        printAutoInd(f, "end % try")

        printAutoInd(f, "end % function \n\n\n\n\n\n\n")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun 1: detectAbortKey")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f, "function detectAbortKey(abortKeyCode)")
        printAutoInd(f, "[keyIsDown, ~, keyCode] = KbCheck(-1);")
        printAutoInd(f, "if keyIsDown && keyCode(abortKeyCode)")

        printAutoInd(f, "error('The experiment was aborted by the experimenter!');")

        printAutoInd(f, "end")

        printAutoInd(f, "end %  end of subfunction\n\n\n")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun 2: disableSomeKeys")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f, "function disableSomeKbKeys()")
        # printAutoInd(f, "{0}{1}{2}\n", "RestrictKeysForKbCheck(KbName({",
        #              ''.join("'" + cItem + "'," for cItem in enabledKBKeysList)[:-1], "}));")
        debugPrint(enabledKBKeysList)
        enabledKBKeysList = enabledKBKeysList.difference({'','0'})
        enabledKBKeysList = set(enabledKBKeysList)
        # printAutoInd(f, "{0}{1}{2}\n", "RestrictKeysForKbCheck(unique([",
        #              ''.join(cItem + ", " for cItem in enabledKBKeysList)[:-2], "]));")
        printAutoInd(f, "{0}{1}{2}\n", "RestrictKeysForKbCheck([",
                     ''.join(cItem + ", " for cItem in enabledKBKeysList)[:-2], "]);")
        printAutoInd(f, "end %  end of subfun2\n")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun 3: makeFrameRect")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

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

        printAutoInd(f, "end %  end of subfun3")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun 4: ShuffleCycleOrder")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f, "function cShuffledIdx = ShuffleCycleOrder(nRows,orderStr,orderByStr,subInfo)")
        printAutoInd(f, "cShuffledIdx = 1:nRows;")
        printAutoInd(f, "switch orderStr")
        printAutoInd(f, "case 'Sequential'")
        printAutoInd(f, "% do nothing")

        printAutoInd(f, "case 'Random'")
        printAutoInd(f, "cShuffledIdx = Shuffle(cShuffledIdx);")

        printAutoInd(f, "case 'Random with Replacement'")
        printAutoInd(f, "cShuffledIdx = Randi(nRows,[nRows,1]);")

        printAutoInd(f, "case 'CounterBalance'")
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
        printAutoInd(f, "end%switch")

        printAutoInd(f, "otherwise")
        printAutoInd(f,
                     "error('order methods should be of {{''Sequential'',''Random'',''Random with Replacement'',''CounterBalance''}}');")
        printAutoInd(f, "end%switch")

        printAutoInd(f, "end %  end of subfun4")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun 5: getDurValue")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "function cDur = getDurValue(cDur,cIFI, isSound)")
        printAutoInd(f, "if nargin < 3")
        printAutoInd(f, "isSound = false;")
        printAutoInd(f, "end")

        printAutoInd(f, "if numel(cDur) == 1 && cDur == 0")
        printAutoInd(f, "return;")
        printAutoInd(f, "end")
        printAutoInd(f, "return;")

        printAutoInd(f, "cDur = cDur./1000; % transform the unit from ms to sec")
        printAutoInd(f, "if numel(cDur) > 1")
        printAutoInd(f, "cDur = rand*(cDur(2) - cDur(1)) + cDur(1);")
        printAutoInd(f, "end ")

        printAutoInd(f, "if isSound")
        printAutoInd(f, "cDur = round(cDur/cIFI)*cIFI;")
        printAutoInd(f, "end ")

        printAutoInd(f, "end %  end of subfun5")

        iSubFunNum = 6

        if iQuest > 1:
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "% subfun {0}: questValueTrans", iSubFunNum)
            printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            printAutoInd(f, "function quest = questValueTrans(quest)")
            printAutoInd(f, "if quest.isLog10Trans")
            printAutoInd(f, "quest.cValue = 10^quest.cValue;")
            printAutoInd(f, "end ")
            printAutoInd(f, "quest.cValue = max(quest.cValue,quest.minValue);")
            printAutoInd(f, "quest.cValue = min(quest.cValue,quest.maxValue);")
            printAutoInd(f, "end %  end of subfun{0}", iSubFunNum)

            iSubFunNum += 1

        # printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # printAutoInd(f, "% subfun {0}: makeRespDevStruct", iSubFunNum)
        # printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # printAutoInd(f, "function  cRespDev = makeRespDevStruct(beUpatedVar, allowAble,corResp,rtWindow,endAction,devType,devIndex,respDevIndexes,startTime,isOn)")
        # printAutoInd(f, "cRespDev.beUpatedVar = beUpatedVar;")
        # printAutoInd(f, "cRespDev.allowAble   = allowAble;")
        # printAutoInd(f, "cRespDev.corResp     = corResp;")
        # printAutoInd(f, "cRespDev.rtWindow    = rtWindow;")
        # printAutoInd(f, "cRespDev.endAction   = endAction;")
        # printAutoInd(f, "cRespDev.type        = devType;")
        # printAutoInd(f, "cRespDev.index       = respDevIndexes(devIndex);")
        # printAutoInd(f, "cRespDev.startTime   = startTime;")
        # printAutoInd(f, "cRespDev.isOn        = isOn;")
        # printAutoInd(f, "end %  end of subfun{0}", iSubFunNum)
        #
        # iSubFunNum += 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: responseCheck", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f,"function [keyIsDown,secs,keyCode]= responseCheck(respDevType,respDevIndex)")
        printAutoInd(f,"% respDevType 1,2,3,4 for keyboard, mouse, gamepad, and response box respectively")
        printAutoInd(f,"switch respDevType")

        if Info.PLATFORM == 'windows':
            printAutoInd(f,"case 3 % under windows, check it via joystickMex")
            printAutoInd(f,"status    = joystickMex(respDevIndex); % index starts from 0")
            printAutoInd(f,"keyCode   = bitget(status(5),1:8);")
            printAutoInd(f,"secs      = GetSecs;")
            printAutoInd(f,"keyIsDown = any(keyCode);")

        printAutoInd(f,"case 4 % for Cedrus''s response boxes")
        printAutoInd(f,"status    = CedrusResponseBox('FlushEvents', respDeviceIndices);")
        printAutoInd(f,"keyCode   = status(1,:);")
        printAutoInd(f,"secs      = GetSecs;")
        printAutoInd(f,"keyIsDown = any(keyCode);")
        printAutoInd(f,"otherwise")
        printAutoInd(f,"[keyIsDown, secs, keyCode] = KbCheck(respDevIndex);")
        printAutoInd(f,"end%switch")
        printAutoInd(f, "end %  end of subfun{0}", iSubFunNum)
        iSubFunNum += 1

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun {0}: makeImDestRect", iSubFunNum)
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f,"function destRect = makeImDestRect(cFrameRect,imDataSize,stretchMode)")
        printAutoInd(f,"destRect = centerRect([0 0 imDataSize(1) imDataSize(2)], cFrameRect);")

        printAutoInd(f,"% caculate the width:")
        printAutoInd(f,"if ismember(stretchMode,[1 3])")
        printAutoInd(f,"destRect([1,3]) = cFrameRect([1,3]);")
        printAutoInd(f,"end ")

        printAutoInd(f,"% caculate the height")
        printAutoInd(f,"if ismember(stretchMode,[2 3])")
        printAutoInd(f,"destRect([2,4]) = cFrameRect([2,4]);")
        printAutoInd(f,"end")
        printAutoInd(f, "end %  end of subfun{0}", iSubFunNum)
        iSubFunNum += 1



        # print(Info.WIDGET_TYPE_NAME_COUNT)
        # print(Info.IMAGE_LOAD_MODE)

    if not isDummyPrint:
        Func.log(f"Compile successful!:{compile_file_name}")  # print info to the output panel

