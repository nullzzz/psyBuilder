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
from app.deviceSelection.globalSelection.globalDevices import GlobalDevice
from app.deviceSelection.progressBar import LoadingTip
from app.func import Func
from app.info import Info
from app.output.main import Output
from app.properties.main import Properties
from app.structure.main import Structure
from lib.wait_dialog import WaitDialog

cIndents = 0
isPreLineSwitch = 0
enabledKBKeysList = []
isDummyPrint = False
spFormatVarDict = dict()
inputDevNameIdxDict = {}
outputDevNameIdxDict = {}
previousColorFontDict = {}


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
    if isinstance(inputStr, str):
        if isSingleQuotedStr(inputStr):
            inputStr = inputStr[1:-1]
        inputStr = re.sub("'", "''", inputStr)
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
        if re.fullmatch("'\S+'", inputStr):  # anything but a space
            inputStr = inputStr[1:-1]
    return inputStr


def getAllNestedVars(inputStr, opVars=[]) -> set:
    # debugPrint(f"getallNestedVars: {inputStr}")
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
                # debugPrint(f"{inputStr}, {isRefValue}")
                # debugPrint(attributesSetDict)
                inputStr = attributesSetDict[inputStr][1]
                # valueSet = attributesSetDict[inputStr][2]
                # debugPrint(f"{inputStr},{isRefValue}")
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


def getSepcialFormatAtts():
    """
    : special varType:
    : percentage
    :
    """
    spFormatVarDict = dict()

    for widgetId, cWidget in Info.WID_WIDGET.items():
        # print(f"line 74 {widgetId}")
        cProperties = Func.getProperties(widgetId)
        # print(f"line 76: {cProperties}")
        if Func.isWidgetType(widgetId, Info.CYCLE):
            pass
        elif Func.isWidgetType(widgetId, Info.TEXT):
            updateSpFormatVarDict(cWidget.getTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getFrameTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Width'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Style'], 'fontStyle', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Clear after'], 'clearAfter', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Flip horizontal'], 'flipHorizontal', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Flip vertical'], 'flipVertical', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Right to left'], 'rightToLeft', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Enable'], 'enableFrame', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', spFormatVarDict)

        elif Func.isWidgetType(widgetId, Info.VIDEO):
            updateSpFormatVarDict(cWidget.getTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getFrameTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Width'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Clear after'], 'clearAfter', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', spFormatVarDict)

        elif Func.isWidgetType(widgetId, Info.SOUND):
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Wait for start'], 'waitForStart', spFormatVarDict)

        elif Info.IMAGE == widgetId.split('.')[0]:
            updateSpFormatVarDict(cWidget.getTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getFrameTransparent(), 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Width'], 'percent', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Clear after'], 'clearAfter', spFormatVarDict)
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', spFormatVarDict)

        elif Func.isWidgetType(widgetId, Info.SLIDER):
            updateSpFormatVarDict(cWidget.getDuration(), 'dur', spFormatVarDict)
            updateSpFormatVarDict(cProperties['Clear after'], 'clearAfter', spFormatVarDict)

    return spFormatVarDict


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

        if re.match("^\[.*\]$", inputStr):
            return True

    return False


def isContainCycleTL(widgetId) -> bool:
    cTimelineWidgetIds = Func.getWidgetIDInTimeline(widgetId)

    for cWidgetId in cTimelineWidgetIds:
        if Func.isWidgetType(cWidgetId, Info.CYCLE):
            return True
    return False


def parseAllowKeys(allowKeyStr):
    global enabledKBKeysList

    splittedStrs = re.split('({\w*})', allowKeyStr)

    for item in splittedStrs:
        if item[0] == '{':
            item = re.sub('[\{\}]', '', item)
            enabledKBKeysList.append(item)
        else:
            for char in item:
                enabledKBKeysList.append(char)


def parseBooleanStr(inputStr, isRef = False):
    if inputStr.lower() in ["'yes'", "'true'", 'yes', 'true']:
        inputStr = "1"
    elif inputStr.lower() in ["'no'", "'false'", 'no', 'false']:
        inputStr = "0"
    else:
        if not isRef:
            throwCompileErrorInfo(f"the value of '{inputStr}' should be of ['False','True','Yes','No','1', or '0'] ")

    return inputStr


def parseDurationStr(inputStr):
    if isinstance(inputStr, str):
        inputStr = removeSingleQuotes(inputStr)

        if inputStr == "(Infinite)":
            inputStr = "0"
        elif re.fullmatch("\d+~\d+", inputStr):
            cDurRange = re.fullmatch("\d+~\d+", inputStr)
            inputStr = f"{cDurRange[0]},{cDurRange[1]}"

    return inputStr


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


def printDelayedCodes(delayedPrintCodes, keyName, inputStr, *argins):
    global isDummyPrint

    # delayedPrintCodes = {'codesAfFip': [], 'respCodes': []}
    if not isDummyPrint:
        delayedPrintCodes[keyName].append = f"{inputStr}".format(*argins)


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
            print(f"{tabStrs}{inputStr}".format(*argins), file=f)

    if 'switch' == inputStr.split(' ')[0]:
        isPreLineSwitch = 1
    else:
        isPreLineSwitch = 0

    if cIndents < 0:
        cIndents = 0


def printTimelineWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes):
    cTimelineWidgetIds = Func.getWidgetIDInTimeline(cWidget.widget_id)

    for cWidgetId in cTimelineWidgetIds:
        cWidget = Info.WID_WIDGET[cWidgetId]

        if Info.CYCLE == cWidget.widget_id.split('.')[0]:
            delayedPrintCodes = printCycleWdiget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes)

        elif Info.TEXT == cWidget.widget_id.split('.')[0]:
            delayedPrintCodes = printTextWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes)

        elif Info.IMAGE == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.SOUND == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.IMAGE == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.SLIDER == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.OPEN == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.DC == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.CALIBRATION == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.ACTION == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.STARTR == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.ENDR == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.CLOSE == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.QUEST_INIT == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.QUEST_GET_VALUE == cWidget.widget_id.split('.')[0]:
            pass
        elif Info.QUEST_UPDATE == cWidget.widget_id.split('.')[0]:
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


def printTextWidget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes):
    global enabledKBKeysList, inputDevNameIdxDict, outputDevNameIdxDict, previousColorFontDict, isDummyPrint

    cOpRowIdxStr = f"iLoop_{cLoopLevel}_cOpR"  # define the ouput var's row num

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
    cScreenName, ign = getRefValue(cWidget, cWidget.getScreenName(), attributesSetDict)

    cWinStr = f"winIds({outputDevNameIdxDict.get(cScreenName)})"

    # 2) handle the text content
    cProperties['Text'], ign = getRefValue(cWidget, cProperties['Text'], attributesSetDict)

    if isContainChStr(cProperties['Text']):
        cProperties['Text'] = "[" + "".join(f"{ord(value)} " for value in cProperties['Text']) + "]"
    else:
        cProperties['Text'] = addSingleQuotes(pyStr2MatlabStr(cProperties['Text']))

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
    cWdith = dataStrConvert(*getRefValue(cWidget, cProperties['Width'], attributesSetDict))
    cHeight = dataStrConvert(*getRefValue(cWidget, cProperties['Height'], attributesSetDict))

    frameRectStr = f"makeFrameRect({sx}, {sy}, {cWdith}, {cHeight}, fullRects({outputDevNameIdxDict.get(cScreenName)},:))"

    # set the font name size color style:
    fontName = dataStrConvert(*getRefValue(cWidget, cProperties['Font family'], attributesSetDict))

    fontSize = dataStrConvert(*getRefValue(cWidget, cProperties['Font size'], attributesSetDict))

    fontStyle = dataStrConvert(*getRefValue(cWidget, cProperties['Style'], attributesSetDict))
    fontStyle = parseFontStyleStr(fontStyle)

    fontBkColor = dataStrConvert(*getRefValue(cWidget, cProperties['Back color'], attributesSetDict))

    # debugPrint('------------------------------------/')
    # debugPrint(fontName)
    # debugPrint(fontSize)
    # debugPrint(fontStyle)
    # debugPrint(fontBkColor)
    #
    # debugPrint('previous saved color font info:')
    # debugPrint(previousColorFontDict)
    # debugPrint('------------------------------------\\')
    isChangeFontPars = False
    #  font name
    if previousColorFontDict['fontName'] != fontName:
        printAutoInd(f, "Screen('TextFont',{0},{1});", cWinStr, fontName)
        previousColorFontDict.update({'fontName': fontName})
        isChangeFontPars = True

    # font size
    if previousColorFontDict['fontSize'] != fontSize:
        printAutoInd(f, "Screen('TextSize',{0},{1});", cWinStr, fontSize)
        previousColorFontDict.update({'fontSize': fontSize})
        isChangeFontPars = True

    # font style
    if previousColorFontDict['fontStyle'] != fontStyle:
        printAutoInd(f, "Screen('TextStyle',{0},{1});", cWinStr, fontStyle)
        previousColorFontDict.update({'fontStyle': fontStyle})
        isChangeFontPars = True

    # font background color
    if previousColorFontDict['fontBkColor'] != fontBkColor:
        printAutoInd(f, "Screen('TextBackgroundColor',{0},{1});", cWinStr, fontBkColor)
        previousColorFontDict.update({'fontBkColor': fontBkColor})
        isChangeFontPars = True

    if isChangeFontPars:
        printAutoInd(f, "")

    # before we draw the formattedtext， we draw the frame rect first:
    borderColor = dataStrConvert(*getRefValue(cWidget, cProperties['Border color'], attributesSetDict))
    borderWidth = dataStrConvert(*getRefValue(cWidget, cProperties['Border width'], attributesSetDict))
    frameFillColor = dataStrConvert(*getRefValue(cWidget, cProperties['Frame fill color'], attributesSetDict))

    # if f"preFrameFillColor" not in previousColorFontDict:
    frameTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Frame transparent'], attributesSetDict))

    debugPrint(f"frameTransparent: {frameTransparent}")

    cRefedValue, isRef = getRefValue(cWidget, cProperties['Enable'], attributesSetDict)
    isBkFrameEnable = parseBooleanStr(dataStrConvert(cRefedValue, isRef), isRef)

    if isBkFrameEnable == '1':

        # if (frameFillColor == previousColorFontDict[cScreenName]) and (frameTransparent in [1,255]):
        if (frameFillColor != previousColorFontDict[cScreenName]):
            printAutoInd(f, "Screen('FillRect',{0},{1},{2});", cWinStr,
                         addedTransparentToRGBStr(frameFillColor, frameTransparent), frameRectStr)

        # draw the frame only when the frame color is different from the frame fill color
        if borderColor != frameFillColor:
            printAutoInd(f, "Screen('frameRect',{0},{1},{2},{3});", cWinStr,
                         addedTransparentToRGBStr(frameFillColor, frameTransparent), frameRectStr, borderWidth)

    #  print out the text
    printAutoInd(f, "DrawFormattedText({0},{1},{2},{3},{4},{5},{6},{7},[],{8},{9});", \
                 cWinStr, \
                 cProperties['Text'], \
                 alignmentX, \
                 alignmentY, \
                 addedTransparentToRGBStr(fontColorStr, fontTransparent), \
                 dataStrConvert(*getRefValue(cWidget, cProperties['Wrapat chars'], attributesSetDict)), \
                 flipHorStr, \
                 flipVerStr, \
                 rightToLeft, \
                 frameRectStr)
    # [nx, ny, textbounds, wordbounds] = DrawFormattedText(win, tstring[, sx][, sy][, color][, wrapat][, flipHorizontal]
    # [, flipVertical][, vSpacing][, righttoleft][, winRect])

    clearAfter = dataStrConvert(*getRefValue(cWidget, cProperties['Clear after'], attributesSetDict))
    clearAfter = parseDontClearAfterStr(clearAfter)

    printAutoInd(f, "Screen('DrawingFinished',{0},{1});\n", cWinStr, clearAfter)
    printAutoInd(f, "detectAbortKey(abortKeyCode); % check abort key in the start of every event")
    # -------------------------------------------------------------
    # Step 2: print out previous widget's no stimuli related codes
    # -------------------------------------------------------------
    for cRowStr in delayedPrintCodes['respCodes']:
        printAutoInd(f, cRowStr)
    # clear out the print buffer
    delayedPrintCodes.update({'respCodes': []})

    # -------------------------------------------------------------
    # Step 3: print out title of the current widget
    # -------------------------------------------------------------
    if Func.getWidgetPosition(cWidget.widget_id) > 0:
        # Step 2: print out help info for the current widget
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        printAutoInd(f, '%loop:{0}, event{1}: {2}', cLoopLevel, Func.getWidgetPosition(cWidget.widget_id) + 1,
                     Func.getWidgetName(cWidget.widget_id))
        printAutoInd(f, '%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    # Flip the Screen
    if Func.getWidgetPosition(cWidget.widget_id) == 0:
        printAutoInd(f, "% for first event, flip immediately.. ")
        f"{Func.getWidgetName(cWidget.widget_id)}_onsettime({cOpRowIdxStr})"
        printAutoInd(f, "{0}_onsettime({1}) = Screen('Flip',{2},{3},{4});\n", Func.getWidgetName(cWidget.widget_id),
                     cOpRowIdxStr, cWinStr, 0, clearAfter)
    else:

        printAutoInd(f, "{0}_onsettime({1}) = Screen('Flip',{2},{3},{4});\n", Func.getWidgetName(cWidget.widget_id),
                     cOpRowIdxStr, cWinStr, 0, clearAfter)

    # durValue, isInfiniteDur, isRef= parseDurationStr(cWidget, attributesSetDict)
    # -------------------------------------------------------------
    # Step 4: print out previous widget's no stimuli related codes
    # -------------------------------------------------------------
    for cRowStr in delayedPrintCodes['codesAfFip']:
        printAutoInd(f, cRowStr)
    # clear out the print buffer
    delayedPrintCodes.update({'codesAfFip': []})

    # ------------------------------------------------------------
    # Step 5: send output messages
    # ------------------------------------------------------------

    debugPrint(f"------------------------\\")

    output_device = cWidget.getOutputDevice()
    debugPrint(f" b= {output_device}")

    if len(output_device) > 0:
        printAutoInd(f, "% send output trigger and msg:")

    debugPrint(f"{cWidget.widget_id}: outputDevice:\n o ={output_device}")

    for device, properties in output_device.items():
        msgValue = dataStrConvert(*getRefValue(cWidget, properties['Value or Msg'], attributesSetDict), True)
        pulseDur = dataStrConvert(*getRefValue(cWidget, properties['Pulse Duration'], attributesSetDict), False)

        cDevName = properties.get("Device Name", "")
        devType = properties.get("Device Type", "")

        if devType == 'parallel_port':

            if Info.PLATFORM == 'linux':
                printAutoInd(f, "lptoutMex({0},{1});", outputDevNameIdxDict.get(cDevName), msgValue)
            elif Info.PLATFORM == 'windows':
                printAutoInd(f, "io64(io64Obj,{0},{1});", outputDevNameIdxDict.get(cDevName), msgValue)
            elif Info.PLATFORM == 'mac':
                printAutoInd(f, "% currently, under Mac OX we just do nothing for parallel ports")


        elif devType == 'network_port':
            printAutoInd(f, "pnet({0},'write',{1});", outputDevNameIdxDict.get(cDevName), msgValue)

        elif devType == 'serial_port':
            printAutoInd(f, "[ign, when] = IOPort('Write', {0}, {1});", outputDevNameIdxDict.get(cDevName), msgValue)

    # -------------------------------------------------------------
    #  we need to dummily draw stim for the next widget
    # so here after we will print any code into delayedPrintCodes
    # -------------------------------------------------------------

    # ------------------------------------------------------------------
    # Step 6: acquire responses
    # ------------------------------------------------------------------

    debugPrint(f"{cWidget.widget_id}: cProperties:")
    debugPrint(f" a= {cProperties}")

    # to be continue ...

    return delayedPrintCodes


def printCycleWdiget(cWidget, f, attributesSetDict, cLoopLevel, delayedPrintCodes):
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
                    cValue = parseBooleanStr(cValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'flipVertical':
                    cValue = parseBooleanStr(cValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'rightToLeft':
                    cValue = parseBooleanStr(cValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'enableFrame':
                    cValue = parseBooleanStr(cValue)
                    cRowDict[key] = cValue

                elif spFormatVarDict[cKeyAttrName] == 'waitForStart':
                    cValue = parseBooleanStr(cValue)
                    cRowDict[key] = cValue

            #     TO BE CONTINUING... FOR ALL OTHER Special Types
            # --------------------------------------\

            cAttributeName = f"{cWidgetName}.attr.{key}"

            if not isRefValue:
                cRefValueSet = set([cValue])

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

    #  to make sure the weight is one for countbalance selection of order ----/
    if cycleOrderStr == "'CounterBalance'":
        cCycleWeightList = cWidget.getAttributeValues(0)
        for cLineWeight in cCycleWeightList:
            if dataStrConvert(cLineWeight) != 1:
                throwCompileErrorInfo(
                    f"Found an uncompatible error in Cycle {Func.getWidgetName(cWidget.widget_id)}:\nFor CounterBalance selection, the timeline weight should be 1")
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


""" unuseless, because the timeline type will dependent on selected input when the selection order is counterbalanced
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
    # cInfo = compileCode(globalSelf,True,{})
    cInfo = {}
    compileCode(globalSelf, False, cInfo)


def compileCode(globalSelf, isDummyCompile, cInfo):
    global enabledKBKeysList, inputDevNameIdxDict, outputDevNameIdxDict, cIndents, previousColorFontDict, isRealPrint, spFormatVarDict

    # -----------initialize global variables ------/
    isDummyPrint = isDummyCompile

    delayedPrintCodes = {'codesAfFip': [], 'respCodes': []}

    previousColorFontDict = dict()

    previousColorFontDict.update({'clearAfter': "0"})
    previousColorFontDict.update({'fontName': "simSun"})
    previousColorFontDict.update({'fontSize': "12"})
    previousColorFontDict.update({'fontStyle': "0"})
    previousColorFontDict.update({'fontBkColor': "[259,0,0]"})  # we give the bkcolor an impossible initial value

    cIndents = 0
    cLoopLevel = 0

    inputDevNameIdxDict = dict()
    outputDevNameIdxDict = dict()

    enabledKBKeysList = list()
    enabledKBKeysList.append('escape')

    attributesSetDict = {'sessionNum': [0, 'SubInfo.session', {'SubInfo.session'}],
                         'subAge': [0, 'SubInfo.age', {'SubInfo.age'}],
                         'subName': [0, 'SubInfo.name', {'SubInfo.name'}],
                         'subSex': [0, 'SubInfo.sex', {'SubInfo.sex'}], 'subNum': [0, 'SubInfo.num', {'SubInfo.num'}],
                         'subHandness': [0, 'SubInfo.hand', {'SubInfo.hand'}]}
    spFormatVarDict = dict()
    # -------------------------------------------\
    debugPrint(f"cCompilePlantform: {Info.PLATFORM}")

    # only replaced percent vars that will be reffred by % with - value /100
    spFormatVarDict = getSepcialFormatAtts()

    debugPrint(f"line 1148: {spFormatVarDict}")

    # debugPrint(f"b = {Info.WID_NODE}")
    # debugPrint(f"c = {Info.WID_WIDGET}")

    # bePrintList = []
    # for key in Info.WID_NODE.keys():
    #     bePrintList.append(key)
    #
    # print(f"{bePrintList}")
    #
    # checkCycleAtt()
    # for key in Info.WID_NODE.keys():
    #     print("----- wdiget info -----")
    #     try:
    #         node = Info.WID_NODE[key]
    #         level = 0
    #         # node = node.parent()
    #         print(f"{node.widget_id}:{level}")
    #         while node:
    #             node = node.parent()
    #             level += 1
    #             print(f"{node.widget_id}:{level}")
    #     except:
    #         pass
    #     # 不断迭代，直至父结点为空

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
        printAutoInd(f, "% Ph.D")
        printAutoInd(f, "% Department of Psychology, \n% SooChow University")
        printAutoInd(f, "% zhangyang873@gmail.com \n% Or yzhangpsy@suda.edu.cn")
        printAutoInd(f, "% {0}", datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # begin of the function
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "%      begin      ")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        #
        # get subject information
        printAutoInd(f, "%----- get subject information -------/", )
        printAutoInd(f, "subInfo = OpenExp_BCL('{0}',fileparts(mfilename('fullpath')));", cFilenameOnly)
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
        printAutoInd(f, "hideCursor;            % hide mouse cursor")

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
        debugPrint('-------------/')
        debugPrint(output_devices)
        debugPrint('-------------\\\n')
        printAutoInd(f, "%------ define input devices --------/")
        iKeyboard = 1
        iGamepad = 1
        iRespBox = 1
        iMouse = 1

        for inputDevId, cDevice in input_devices.items():

            # create a map dict to map device name (key) to device ID (value)
            inputDevNameIdxDict.update({cDevice['Device Name']: inputDevId})
            # debugPrint(input_device)
            if cDevice['Device Type'] == 'keyboard':
                printAutoInd(f, "KBoards({0}).port     = '{1}';", iKeyboard, cDevice['Device Port'])
                printAutoInd(f, "KBoards({0}).name     = '{1}';\n", iKeyboard, cDevice['Device Name'])
                iKeyboard += 1
            elif cDevice['Device Type'] == 'mouse':
                iMouse += 1
            elif cDevice['Device Type'] == 'game pad':
                iGamepad += 1
            elif cDevice['Device Type'] == 'response box':
                iRespBox += 1

        # if u'\u4e00' <= char <= u'\u9fa5':  # 判断是否是汉字

        printAutoInd(f, "%------------------------------------\\\n\n")

        printAutoInd(f, "%----- define output devices --------/")

        iMonitor = 1
        iParal = 1
        iNetPort = 1
        iSerial = 1
        iSound = 1

        debugPrint(output_devices)

        for outDev_Id, cDevice in output_devices.items():

            if cDevice['Device Type'] == 'screen':
                outputDevNameIdxDict.update({cDevice['Device Name']: f"{iMonitor}"})

                previousColorFontDict.update({cDevice['Device Name']: addSquBrackets(cDevice['Back Color'])})

                printAutoInd(f, "monitors({0}).port       =  {1};", iMonitor, cDevice['Device Port'])
                printAutoInd(f, "monitors({0}).name       = '{1}';", iMonitor, cDevice['Device Name'])
                printAutoInd(f, "monitors({0}).bkColor    = [{1}];", iMonitor, cDevice['Back Color'])
                printAutoInd(f, "monitors({0}).muliSample =  {1};\n", iMonitor, cDevice['Multi Sample'])
                iMonitor += 1
            elif cDevice['Device Type'] == 'network_port':

                outputDevNameIdxDict.update({cDevice['Device Name']: f"tcpipCons({iNetPort})"})
                printAutoInd(f, "TCPIPs({0}).ipAdd    = '{1}';", iNetPort, cDevice['Device Port'])
                printAutoInd(f, "TCPIPs({0}).port     =  {1};", iNetPort, cDevice['IP Port'])
                printAutoInd(f, "TCPIPs({0}).name     = '{1}';", iNetPort, cDevice['Device Name'])
                printAutoInd(f, "TCPIPs({0}).isClient = {1};\n", iNetPort, cDevice['Is Client'])
                iNetPort += 1

            elif cDevice['Device Type'] == 'parallel_port':
                outputDevNameIdxDict.update({cDevice['Device Name']: f"parPort({iParal}).port"})
                printAutoInd(f, "parPort({0}).port     = hex2dec('{1}');", iParal, cDevice['Device Port'])
                printAutoInd(f, "parPort({0}).name     = '{1}';\n", iParal, cDevice['Device Name'])
                iParal += 1

            elif cDevice['Device Type'] == 'serial_port':

                outputDevNameIdxDict.update({cDevice['Device Name']: f"serialCons({iSerial})"})
                printAutoInd(f, "serPort({0}).port     = '{1}';", iSerial, cDevice['Device Port'])
                printAutoInd(f, "serPort({0}).name     = '{1}';", iSerial, cDevice['Device Name'])
                printAutoInd(f, "serPort({0}).baudRate = '{1}';", iSerial, cDevice['Baud Rate'])
                printAutoInd(f, "serPort({0}).dataBits = '{1}';\n", iSerial, cDevice['Data Bits'])
                iSerial += 1

            elif cDevice['Device Type'] == 'sound':

                outputDevNameIdxDict.update({cDevice['Device Name']: f"audioDevs({iSound})"})
                printAutoInd(f, "audioDevs({0}).idx      = {1};", iSound, cDevice['Device Port'])
                printAutoInd(f, "audioDevs({0}).name     = '{1}';", iSound, cDevice['Device Name'])
                if 'auto' == cDevice['Sampling Rate']:
                    printAutoInd(f, "audioDevs({0}).fs       = []; % the default value in PTB is 48000 Hz\n", iSound)
                else:
                    printAutoInd(f, "audioDevs({0}).fs       = {1};\n", iSound, cDevice['Sampling Rate'])

                iSound += 1

        printAutoInd(f, "%------------------------------------\\\n")

        printAutoInd(f, "disableSomeKbKeys; % restrictKeysForKbCheck")

        printAutoInd(f, "%----- initialize output devices --------/")
        printAutoInd(f, "%--- open windows ---/")
        printAutoInd(f, "winIds    = zeros({0},1);", iMonitor - 1)
        printAutoInd(f, "winIFIs   = zeros({0},1);", iMonitor - 1)
        printAutoInd(f, "fullRects = zeros({0},4);", iMonitor - 1)

        printAutoInd(f, "for iWin = 1:numel(monitors)")
        printAutoInd(f,
                     "[winIds(iWin),fullRects(iWin,:)] = Screen('OpenWindow',monitors(iWin).port,monitors(iWin).bkColor,[],[],[],[],monitors(iWin).muliSample);")
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
            printAutoInd(f, "InitializePsychSound(1);\n")
            printAutoInd(f, "audioDevs = zeros({0},1);", iSound - 1)
            # printAutoInd(f,"audioFs = getAudioFsFromFristAudioFile;")

            printAutoInd(f, "for iCount = 1:numel(audioDevs)")
            printAutoInd(f,
                         "audioDevs(iCount) = PsychPortAudio('Open',audioDevs(iCount).idx,1,[],audioDevs(iCount).fs,2);", )
            printAutoInd(f, "end % iCount")
            printAutoInd(f, "%----------------------------\\\n")

        printAutoInd(f, "%----------------------------------------\\\n")

        printAutoInd(f, "Priority(1);      % Turn the priority to high priority")
        printAutoInd(f, "opRowIdx = 1; % set the output variables row num")
        printAutoInd(f, "iLoop_0_cOpR = opRowIdx;")

        # start to handle all the widgets
        printTimelineWidget(Info.WID_WIDGET[f"{Info.TIMELINE}.0"], f, attributesSetDict, cLoopLevel, delayedPrintCodes)

        printAutoInd(f, "expEndTime = datestr(now,'dd-mmm-YYYY:HH:MM:SS'); % record the end time \n")
        printAutoInd(f, "sca;                        % Close opened windows")
        printAutoInd(f, "ShowCursor;                 % Show the hided mouse cursor")
        printAutoInd(f, "Priority(0);                % Turn the priority back to normal")
        printAutoInd(f, "RestrictKeysForKbCheck([]); % Re-enable all keys\n")

        if Info.PLATFORM == 'windows':
            printAutoInd(f, "ShowHideWinTaskbar(1);      % show the window taskbar.")

        printAutoInd(f, "save({0}.filename); % save the results\n", cFilenameOnly)

        #  close opend devices
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

        # close psychPortAudio device
        if iSound > 1:
            printAutoInd(f, "%--- close outputAudio devs--/")

            printAutoInd(f, "for iCount = 1:numel(serialCons)")
            printAutoInd(f, "PsychPortAudio('Close', audioDevs(iCount));")
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

            printAutoInd(f, "for iCount = 1:numel(serialCons)")
            printAutoInd(f, "PsychPortAudio('Close', audioDevs(iCount));")
            printAutoInd(f, "end % iCount")
            # printAutoInd(f, "%----------------------------\\\n")

        printAutoInd(f, "save('{0}_debug');", cFilenameOnly)
        printAutoInd(f, "rethrow({0}_error);", cFilenameOnly)

        #

        printAutoInd(f, "end % try")

        printAutoInd(f, "end % function \n\n\n\n\n\n\n")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun 1: detectAbortKey")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f, "function detectAbortKey(abortKeyCode)")
        printAutoInd(f, "[keyIsDown, ign, keyCode] = responseCheck(-1);")
        printAutoInd(f, "if keyCode(abortKeyCode)")

        printAutoInd(f, "error('The experiment was aborted by the experimenter!');")

        printAutoInd(f, "end")

        printAutoInd(f, "end %  end of subfunction\n\n\n")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun 2: disableSomeKeys")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f, "function disableSomeKbKeys()")
        printAutoInd(f, "{0}{1}{2}\n", "RestrictKeysForKbCheck(KbName({",
                     ''.join("'" + cItem + "'," for cItem in enabledKBKeysList)[:-1], "}));")
        printAutoInd(f, "end %  end of subfun2\n")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun 3: makeFrameRect")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f, "function outRect = makeFrameRect(x, y, frameWidth, frameHight, fullRect)")
        printAutoInd(f, "if x <= 0")
        printAutoInd(f, "x = x*fullRect(3);")
        printAutoInd(f, "end % if")

        printAutoInd(f, "if y <= 0")
        printAutoInd(f, "y = y*fullRect(4);")
        printAutoInd(f, "end % if")

        printAutoInd(f, "if frameWidth <= 0")
        printAutoInd(f, "frameWidth = frameWidth*fullRect(3);")
        printAutoInd(f, "end % if")

        printAutoInd(f, "if frameHight <= 0")
        printAutoInd(f, "frameHight = frameHigh*fullRect(4);")
        printAutoInd(f, "end % if")

        printAutoInd(f, "outRect = CenterRectOnPointd([0, 0, frameWidth, frameHight], x, y);")

        printAutoInd(f, "end %  end of subfun3")

        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f, "% subfun 4: ShuffleCycleOrder")
        printAutoInd(f, "%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f, "function cShuffledIdx = ShuffleCycleOrder(nRows,orderStr,orderByStr,subInfo)")
        printAutoInd(f, "cShuffledIdx = 1:nRows;")
        printAutoInd(f, "switch orderStr")
        printAutoInd(f, "case 'Sequential'")
        # printAutoInd(f,"cShuffledIdx = 1:nRows;")

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

        printAutoInd(f, "end %  end of subfun3")

    if not isDummyPrint:
        Func.log(f"Compile successful!:{compile_file_name}")  # print info to the output panel

    return cInfo
