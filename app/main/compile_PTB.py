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

cIndents          = 0
isPreLineSwitch   = 0
enabledKBKeysList = []

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




def printAutoInd(f,inputStr,*argins):
    global cIndents
    global isPreLineSwitch

    incrAfterStr    = ('if','try','switch','for','while')
    decreAndIncrStr = ('else','elseif','otherwise','catch')

    # isinstance(f,'list')

    if inputStr.split(' ')[0] in incrAfterStr:
        tabStrs = '\t' * cIndents
        print(f"\n{tabStrs}{inputStr}".format(*argins), file=f)
        cIndents += 1

    elif inputStr.split(' ')[0] in decreAndIncrStr:
        cIndents -= 1
        tabStrs = '\t' * cIndents
        print(f"{tabStrs}{inputStr}".format(*argins), file=f)
        cIndents += 1

    elif 'end' == inputStr.split(' ')[0]:
        cIndents -= 1
        tabStrs = '\t' * cIndents
        print(f"{tabStrs}{inputStr}\n".format(*argins), file=f)
    elif 'end%switch' == inputStr.split(' ')[0]:
        cIndents -= 2
        tabStrs = '\t' * cIndents
        print(f"{tabStrs}{inputStr}\n".format(*argins), file=f)

    elif 'case' == inputStr.split(' ')[0]:

        if 0 == isPreLineSwitch:
            cIndents -= 1

        tabStrs = '\t' * cIndents
        print(f"{tabStrs}{inputStr}".format(*argins), file=f)
        cIndents += 1

    else:
        tabStrs = '\t' * cIndents
        print(f"{tabStrs}{inputStr}".format(*argins), file=f)

    if 'switch' == inputStr.split(' ')[0]:
        isPreLineSwitch = 1
    else:
        isPreLineSwitch = 0

    if cIndents < 0:
        cIndents = 0


def isContainChStr(inputStr):
    # :param check_str: {str}
    # :return: {bool} True and False for have and have not chinese characters respectively
    for ch in inputStr:
        if u'\u4e00' <= ch <= u'\u9fff':
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
    if isinstance(inputStr,str):

        if isRgbWithBracketsStr(inputStr):
            return False

        if re.match("^\[.*\]$", inputStr):
            return True

    return False

def booleanTransStr(inputStr,isRef):

    if inputStr.lower() in ["'yes'","'true'",'yes','true']:
        inputStr = "1"
    elif inputStr.lower() in ["'no'","'false'",'no','false']:
        inputStr = "0"
    else:
        if isRef == False:
            throwCompileErrorInfo(f"the value of '{inputStr}' should be of ['False' or 'True']  OR of ['1','0']")

    return inputStr

def pyStr2MatlabStr(inputStr):
    if isinstance(inputStr, str):
        inputStr = re.sub("'","''",inputStr)
    return inputStr

def parsePercentStr(inputStr):
    if isinstance(inputStr,str):
        if isPercentStr(inputStr):
            outputValue = float(inputStr[:-1])/100
        elif isNumStr(inputStr):
            outputValue = float(inputStr)
        else:
            outputValue = inputStr
    else:
        outputValue = inputStr

    return outputValue


def addedTransparentToRGBStr(RGBStr,transparentStr):

    transparentValue = parsePercentStr(transparentStr)

    if isinstance(transparentValue,(int,float)):
        if transparentValue == 1:
            return RGBStr
        else:
            transparentValue = transparentValue*255
    else:
        transparentValue = f"{transparentValue}*255"


    if isRgbStr(RGBStr):
        RGBStr = f"[{RGBStr},{transparentValue}]"
    elif isRgbWithBracketsStr(RGBStr):
        RGBStr = re.sub("]",f",{transparentValue}]",RGBStr)
    elif isRefStr(RGBStr):
        RGBStr = f"[{RGBStr},{transparentStr}]"
    else:
        raise Exception(f"the input parameter 'RGBStr' is not a RGB format String\n should be of R,G,B, [R,G,B], or referred values!")

    return RGBStr




def dataStrConvert(dataStr,isRef = False, transMATStr = False):
    # convert string to neither a string or a num
    # e.g.,
    # 1） "2"    to 2
    # 2） "2.00" to 2.0
    # 3） "abcd" to "'abcd'"
    # 4） "[12,12,12]" to "[12,12,12]"
    # 5） "12,12,12"  to "[12,12,12]"
    # 6） is a referred value will do nothing
    if isinstance(dataStr,str):

        if dataStr:

            if isPercentStr(dataStr):
                outData = parsePercentStr(dataStr)

            elif isRgbWithBracketsStr(dataStr):
                outData = dataStr

            elif isRgbStr(dataStr):
                outData = addSquBrackets(dataStr)

            elif isIntStr(dataStr):
                outData = int(dataStr)

            elif isFloatStr(dataStr):
                outData = float(dataStr)

            elif isRefStr(dataStr):
                outData = dataStr # maybe a bug

            else:
                if isRef:
                    outData = dataStr  # maybe a bug
                else:
                    if transMATStr:
                        outData = addSingleQuotes(pyStr2MatlabStr(dataStr) ) # maybe a bug
                    else:
                        outData = addSingleQuotes(dataStr)  # maybe a bug
        else:
            outData = "'[]'"

    else: # in case there is something wrong
        # raise Exception(f"the input dataStr:{dataStr} is not a string!")
        outData = dataStr

    return outData



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




def getRefValue(cwidget, inputStr,attributesSetDict):
    isRefValue = False

    if isinstance(inputStr, str):

        isRefValue = isRefStr(inputStr)

        if isRefValue:
            inputStr = re.sub("[\[\]]", '', inputStr)

            if inputStr in attributesSetDict:
                inputStr = attributesSetDict[inputStr][2]
            else:
                throwCompileErrorInfo(f"The cited attribute '{inputStr}' \nis not available for {Func.getWidgetName(cwidget.widget_id)}")

    return [inputStr,isRefValue]



def parseAllowKeys(allowKeyStr):
    global enabledKBKeysList

    splittedStrs = re.split('({\w*})',allowKeyStr)

    for item in splittedStrs:
        if item[0] == '{':
            item = re.sub('[\{\}]','',item)
            enabledKBKeysList.append(item)
        else:
            for char in item:
                enabledKBKeysList.append(char)


def printTimelineWidget(cWidget,f,attributesSetDict,cLoopLevel):
    noStimRelatedCodes = []

    cTimelineWidgetIds = Func.getWidgetIDInTimeline(cWidget.widget_id)

    for cWidgetId in cTimelineWidgetIds:
        cWidget = Info.WID_WIDGET[cWidgetId]
        if Info.CYCLE == cWidget.widget_id.split('.')[0]:

            noStimRelatedCodes = printCycleWdiget(cWidget, f,attributesSetDict,cLoopLevel, noStimRelatedCodes)

        elif Info.TEXT == cWidget.widget_id.split('.')[0]:
            noStimRelatedCodes = printTextWidget(cWidget, f, attributesSetDict, cLoopLevel, noStimRelatedCodes)

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
            # noStimRelatedCodes = printImageWdiget(cWidget, f, noStimRelatedCodes)

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
    # print(cTimelineWidgetIds)
    # to be continue ...


def printTextWidget(cWidget,f,attributesSetDict,cLoopLevel ,noStimRelatedCodes):
    global enabledKBKeysList, inputDevNameIdxDict, outputDevNameIdxDict,previousColorFontDict

    # Step 1: print out previous widget's no stimuli related codes
    for cRowStr in noStimRelatedCodes:
        printAutoInd(f,cRowStr)
    # clear out the print buffer
    noStimRelatedCodes.clear()

    # Step 2: print out help info for the current widget
    printAutoInd(f,'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    printAutoInd(f,'%loop:{0}, event{1}: {2}',cLoopLevel,Func.getWidgetPosition(cWidget.widget_id) +1,Func.getWidgetName(cWidget.widget_id))
    printAutoInd(f,'%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')


    print(inputDevNameIdxDict)
    print(outputDevNameIdxDict)

    cProperties = Func.getProperties(cWidget.widget_id)

    # 1) get the win id info in matlab format winIds(idNum)
    cScreenName, noused = getRefValue(cWidget, cWidget.getScreenName(), attributesSetDict)

    cWinStr = f"winIds({outputDevNameIdxDict.get(cScreenName)})"

    # 2) handle the text content
    cProperties['Text'],noused = getRefValue(cWidget,cProperties['Text'],attributesSetDict)

    if isContainChStr(cProperties['Text']):
        cProperties['Text'] = "double('"+pyStr2MatlabStr(cProperties['Text'])+"')"
    else:
        cProperties['Text'] = "'" + pyStr2MatlabStr(cProperties['Text']) + "'"

    # 3) check the alignment X parameter:
    alignmentX =dataStrConvert(*getRefValue(cWidget, cProperties['Alignment X'], attributesSetDict))


    # 4) check the alignment X parameter:
    alignmentY =dataStrConvert(*getRefValue(cWidget, cProperties['Alignment Y'], attributesSetDict))


    # 5) check the color parameter:
    fontColorStr    = dataStrConvert(*getRefValue(cWidget, cProperties['Fore color'], attributesSetDict))
    fontTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Transparent'], attributesSetDict))
    # print(f"line 411  {fontTransparent}")

    # if isinstance(fontTransparent,(int,float)) and fontTransparent == 0:
    #     fontColorAll = fontColorStr
    # else:
    #     fontColorAll = addedTransparentToRGBStr(fontColorStr, f"{fontTransparent}*255")


    # 7) check the flip hor parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Flip horizontal'], attributesSetDict)
    flipHorStr = dataStrConvert(cRefedValue, isRef)
    flipHorStr = booleanTransStr(dataStrConvert(flipHorStr, isRef), isRef)

    # 8) check the flip ver parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Flip vertical'], attributesSetDict)
    flipVerStr = dataStrConvert(cRefedValue, isRef)
    flipVerStr = booleanTransStr(dataStrConvert(flipVerStr, isRef), isRef)

    """
    # 10) check the right to left parameter:
    cRefedValue, isRef = getRefValue(cWidget, cProperties['Right to left'], attributesSetDict)
    rightToLeft = dataStrConvert(cRefedValue, isRef)
    rightToLeft = booleanTransStr(dataStrConvert(rightToLeft, isRef), isRef)
    """
    rightToLeft = 0


    # 11) check the parameter winRect

    #
    sx      = dataStrConvert(*getRefValue(cWidget, cProperties['X position'], attributesSetDict))
    sy      = dataStrConvert(*getRefValue(cWidget, cProperties['Y position'], attributesSetDict))
    cWdith  = dataStrConvert(*getRefValue(cWidget, cProperties['Width'], attributesSetDict))
    cHeight = dataStrConvert(*getRefValue(cWidget, cProperties['Height'], attributesSetDict))


    frameRectStr = f"makeFrameRect({sx}, {sy}, {cWdith}, {cHeight}, fullRects({outputDevNameIdxDict.get(cScreenName)},:))"

    # before we draw the formattedtext， we draw the frame rect first:
    borderColor    = dataStrConvert(*getRefValue(cWidget, cProperties['Border color'], attributesSetDict))
    borderWidth    = dataStrConvert(*getRefValue(cWidget, cProperties['Border width'], attributesSetDict))
    frameFillColor = dataStrConvert(*getRefValue(cWidget, cProperties['Frame fill color'], attributesSetDict))

    # if f"preFrameFillColor" not in previousColorFontDict:
    # frameTransparent = dataStrConvert(*getRefValue(cWidget, cProperties['Frame transparent'], attributesSetDict))

    frameTransparent = 1



    if (frameFillColor == previousColorFontDict[cScreenName]) and (frameTransparent in [1,255]):
        printAutoInd(f, "Screen('FillRect',winIds({0}),{1},{2});",cWinStr,addedTransparentToRGBStr(frameFillColor,frameTransparent),frameRectStr)

    # draw the frame only when the frame color is different from the frame fill color
    if borderColor != frameFillColor:
        printAutoInd(f, "Screen('frameRect',winIds({0}),{1},{2},{3});",cWinStr,addedTransparentToRGBStr(frameFillColor,frameTransparent),frameRectStr,borderWidth)






    printAutoInd(f,"DrawFormattedText(winIds({0}),{1},{2},{3},{4},{5},{6},{7},[],{8},{9});", \
                 cWinStr, \
                 cProperties['Text'], \
                 alignmentX, \
                 alignmentY, \
                 addedTransparentToRGBStr(fontColorStr,fontTransparent), \
                 dataStrConvert(*getRefValue(cWidget,cProperties['Wrapat chars'],attributesSetDict)), \
                 flipHorStr, \
                 flipVerStr, \
                 rightToLeft, \
                 frameRectStr)

    # [nx, ny, textbounds, wordbounds] = DrawFormattedText(win, tstring[, sx][, sy][, color][, wrapat][, flipHorizontal]
    # [, flipVertical][, vSpacing][, righttoleft][, winRect])

    clearAfter = dataStrConvert(*getRefValue(cWidget, cProperties['Clear after'], attributesSetDict))
    clearAfter = booleanTransStr(dataStrConvert(clearAfter, isRef), isRef)

    printAutoInd(f, "Screen('DrawingFinished',winIds({0}),{1});",cWinStr,clearAfter)


    print(f"line 243: {cProperties}")

    output_device= cWidget.getOutputDevice()

    print(output_device)
    for device, properties in output_device.items():
        # print(device)
        value_or_msg   = properties.get("Value or Msg", "")
        pulse_duration = properties.get("Pulse Duration", "")
    # to be continue ...



    return noStimRelatedCodes


def printCycleWdiget(cWidget, f,attributesSetDict,cLoopLevel, noStimRelatedCodes):
    # start from 1 to compatible with MATLAB
    cLoopLevel += 1

    attributesSetDict       = attributesSetDict.copy()
    cWidgetName = Func.getWidgetName(cWidget.widget_id)


    attributesSetDict.setdefault(f"{cWidgetName}.cLoop",[cLoopLevel,f"iLoop_{cLoopLevel}"])
    attributesSetDict.setdefault(f"{cWidgetName}.rowNums",[cLoopLevel,f"size({cLoopLevel}.attr,1)"])

    cLoopIterStr = attributesSetDict[f"{cWidgetName}.cLoop"][1]

    # create the design matrix  (table) for the current cycle
    startExpStr = cWidgetName + '.attr = cell2table({...'
    printAutoInd(f, '% create the designMatrix of the current cycle (loop)')

    printAutoInd(f, '{0}', startExpStr)

    for iRow in range(cWidget.rowCount()):
        cRowDict = cWidget.getAttributes(iRow)
        if 0 == iRow:
            endExpStr = "},'VariableNames',{" + ''.join("'"+key+"' " for key in cRowDict.keys()) + "});"
            # update the attributes set dictionary
            for key in cRowDict.keys():
                attributesSetDict.setdefault(f"{cWidgetName}.attr.{key}",[cLoopLevel,f"{cWidgetName}.attr.{key}{{iLoop{cLoopLevel}}}"])
            # print('-----cAttributes set -----------')
            # print(attributesSetDict)
        # handle the references and the values in colorType
        for key, value in cRowDict.items():

            # get the referenced var value
            cValue = getRefValue(cWidget,value,attributesSetDict)

            if isPercentStr(cValue):
                cValue = parsePercentStr(cValue)

            cRowDict[key], noused = cValue


        if '' == cRowDict['Weight']:
            cRepeat = 1
        else:
            cRepeat = dataStrConvert(cRowDict['Weight'])

        for iRep in range(cRepeat):
            # print("".join(str(dataStrConvert(value)) + " " for key, value in cRowDict.items()))
            printAutoInd(f,'{0}',"".join(addCurlyBrackets(dataStrConvert(value)) + " " for key, value in cRowDict.items())+";...")


    printAutoInd(f,'{0}\n',endExpStr)
    # cycling
    printAutoInd(f, '% looping across each row of the {0}.attr:{1}',cWidgetName , cLoopIterStr)
    printAutoInd(f, 'for {0} = size({1},1)', cLoopIterStr, f"{cWidgetName}.attr")

    # handle each timeline
    cTimeLineList = cWidget.getTimelines()
    # squeeze the timelines
    cTimelineSet = set()

    for iTimeline in cTimeLineList:
        cTimelineSet.add(iTimeline[1])

    print(cTimelineSet)

    printAutoInd(f, '% switch across timeline types')
    printAutoInd(f, 'switch {0}', f"{cWidgetName}.attr.timeline{{{cLoopIterStr}}}")

    for iTimeline_id in cTimelineSet:
        if '' == iTimeline_id:
            throwCompileErrorInfo(f"In {cWidgetName}: Timeline should not be empty!")
        else:
            printAutoInd(f, 'case {0}', f"{addSingleQuotes(Func.getWidgetName(iTimeline_id))}")
            printTimelineWidget(Info.WID_WIDGET[iTimeline_id], f, attributesSetDict, cLoopLevel)

    printAutoInd(f, 'otherwise ')
    printAutoInd(f, '% do nothing ')
    printAutoInd(f, 'end%switch {0}', f"{cWidgetName}.attr.timeline{{{cLoopIterStr}}}")

    # cycle.getTimelines() -> list: 按顺序进行返回所有设置的timeline
    # 格式为[[timeline_name, timeline_widget_id], [], ...]
    # 如果某行为空则改行对应的数据为['', '']

    """
     # get widgets in the main timeline
     cTimelineWidgetIds = Func.getWidgetIDInTimeline(f"{Info.TIMELINE}.0")

     for cWidgetId in cTimelineWidgetIds:
         # usually the code section after drawing the current frame's stimuli
         noStimRelatedCodes = []

         cWidget = Info.WID_WIDGET[cWidgetId]
         print(Func.getWidgetName(cWidgetId))

         if 'Text' == cWidget.widget_id.split('.')[0]:
             noStimRelatedCodes = printTextWidget(cWidget,noStimRelatedCodes)

         elif 'Cycle' == cWidget.widget_id.split('.')[0]:
             print(cWidget.getTimelines())
             noStimRelatedCodes = printCycleWdiget(cWidget,f, noStimRelatedCodes)


         print(Func.getProperties(cWidgetId))
         # print(cWidget.getPropertyByKey('Text'))
         # print(Func.getScreen)
         # print(dir(cWidget))

         widget是具体的某个控件

         widget为Image时，Text\Video\Sound类似的
         filename: str = widget.getFilename()
         output_device: dict = widget.getOutputDevice()
         for device, properties in output_device.items():
             output_name: str = device
             value_or_msg: str = properties.get("Value or Msg", "")
             pulse_duration: str = properties.get("Pulse Duration", "")

         widget为If时
         condition: str = widget.getCondition()
         true_event: dict = widget.getTrueWidget() # false_event类似
         stim_type: str = true_event.get("stim type", "")
         event_name: str = true_event.get("event name", "")
         widget_id: str = true_event.get("widget id", "")
         widget: Widget = true_event.get("widget", None) # 这个widget就是Slider/Image/...具有若干上述getXXX方法

         widget为switch
         switch: str = widget.getSwitch()
         cases: list = widget.getCase()
         for case in cases:
             case: dict
             case_value: str = case.get("case value", "")
             stim_type: str = case.get("stim type", "")
             event_name: str = case.get("event name", "")
             widget_id: str = case.get("widget id", "")
             widget: Widget = case.get("widget", None)
         """







    printAutoInd(f, 'end % {0}', cLoopIterStr)
    # to be continue ...







    return noStimRelatedCodes









def compilePTB(globalSelf):
    global enabledKBKeysList,inputDevNameIdxDict,outputDevNameIdxDict,cIndents,previousColorFontDict

    previousColorFontDict.update({'clearAfter':"0"})

    cIndents = 0

    inputDevNameIdxDict = {}
    outputDevNameIdxDict = {}

    previousColorFontDict = {}

    enabledKBKeysList = []
    enabledKBKeysList.append('escape')

    attributesSetDict        = {'sessionNum':[0,'SubInfo.session'],'subAge':[0,'SubInfo.age'],'subName':[0,'SubInfo.name'],'subSex':[0,'SubInfo.sex'],'subNum':[0,'SubInfo.num'],'subHandness':[0,'SubInfo.hand']}


    if not Info.FILE_NAME:
        if not globalSelf.getFileName():
            QMessageBox.information(globalSelf, "Warning", "File must be saved before compiling.", QMessageBox.Ok)
            return

    globalSelf.save()
    # get save path
    compile_file_name = ".".join(Info.FILE_NAME.split('.')[:-1]) + ".m"
    # open file
    with open(compile_file_name, "w") as f:
        #  print function start info
        cFilenameOnly = os.path.split(compile_file_name)[1].split('.')[0]
        # the help info
        printAutoInd(f,"function {0}()",cFilenameOnly)
        printAutoInd(f,"% function generated by PTB Builder 0.1")
        printAutoInd(f,"% If you use PTB Builder for your research, then we would appreciate your citing our work in your paper:")
        printAutoInd(f,"% , (2019) PTB builder: a free GUI to generate experimental codes for Psychoolbox. Behavior Research Methods\n%")
        printAutoInd(f,"% To report possible bugs and any suggestions please send us e-mail:")
        printAutoInd(f,"% Yang Zhang")
        printAutoInd(f,"% Ph.D")
        printAutoInd(f,"% Department of Psychology, \n% SooChow University")
        printAutoInd(f,"% zhangyang873@gmail.com \n% Or yzhangpsy@suda.edu.cn")
        printAutoInd(f,"% {0}",datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        # begin of the function
        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f,"%      begin      ")
        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        #
        # get subject information
        printAutoInd(f,"%----- get subject information -------/",)
        printAutoInd(f,"subInfo = OpenExp_BCL('{0}',fileparts(mfilename('fullpath')));",cFilenameOnly)
        printAutoInd(f,"close(gcf);")
        printAutoInd(f,"%-------------------------------------\\\n")

        # the function body try, catch end
        printAutoInd(f,"try")
        printAutoInd(f,"KbName('UnifyKeyNames');\n")
        printAutoInd(f,"abortKeyCode = KbName('ESCAPE');\n")

        printAutoInd(f,"expStartTime = datestr(now,'dd-mmm-YYYY:HH:MM:SS'); % record start time \n")

        printAutoInd(f,"%--------Reinitialize the global random seed ---------/")
        printAutoInd(f,"cRandSeed = RandStream('mt19937ar','Seed','shuffle');")
        printAutoInd(f,"RandStream.setGlobalStream(cRandSeed);")
        printAutoInd(f,"%-----------------------------------------------------\\\n")
        printAutoInd(f,"hideCursor;            % hide mouse cursor")
        printAutoInd(f,"commandwindow;         % bring the command window into front")

        if
        printAutoInd(f,"ShowHideWinTaskbar(0); % hide the window taskbar")
        printAutoInd(f,"end")


        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f,"% define and initialize input/output devices")
        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # get output devices, such as global output devices.
        # you can get each widget's device you selected
        output_devices = Info.OUTPUT_DEVICE_INFO
        input_devices  = Info.INPUT_DEVICE_INFO
        # print('-------------')
        # print(output_devices)
        printAutoInd(f,"%------ define input devices --------/")
        iKeyboard = 1
        iGamepad  = 1
        iRespBox  = 1
        iMouse    = 1

        for input_device in input_devices:
            # create a map dict to map device name (key) to device ID (value)
            inputDevNameIdxDict.update({input_devices[input_device]['Device Name']:input_device})
            # print(input_device)
            if input_devices[input_device]['Device Type'] == 'keyboard':
                printAutoInd(f,"KBoards({0}).port     = '{1}';",iKeyboard,input_devices[input_device]['Device Port'])
                printAutoInd(f,"KBoards({0}).name     = '{1}';\n",iKeyboard,input_devices[input_device]['Device Name'])
                iKeyboard += 1
            elif input_devices[input_device]['Device Type'] == 'mouse':
                iMouse += 1
            elif input_devices[input_device]['Device Type'] == 'game pad':
                iGamepad += 1
            elif input_devices[input_device]['Device Type'] == 'response box':
                iRespBox += 1

        # if u'\u4e00' <= char <= u'\u9fa5':  # 判断是否是汉字

        printAutoInd(f,"%------------------------------------\\\n\n")

        printAutoInd(f,"%----- define output devices --------/")

        iMonitor = 1
        iParal   = 1
        iNetPort = 1
        iSerial  = 1

        print(output_devices)

        for output_device in output_devices:

            if output_devices[output_device]['Device Type'] == 'screen':
                outputDevNameIdxDict.update({output_devices[output_device]['Device Name']:f"{iMonitor}"})

                previousColorFontDict.update({output_devices[output_device]['Device Name']:addSquBrackets(output_devices[output_device]['Back Color'])})

                printAutoInd(f,"monitors({0}).port       =  {1};",iMonitor,output_devices[output_device]['Device Port'])
                printAutoInd(f,"monitors({0}).name       = '{1}';",iMonitor,output_devices[output_device]['Device Name'])
                printAutoInd(f,"monitors({0}).bkColor    = '{1}';",iMonitor,output_devices[output_device]['Back Color'])
                printAutoInd(f,"monitors({0}).muliSample =  {1};\n",iMonitor,output_devices[output_device]['Multi Sample'])
                iMonitor += 1
            elif output_devices[output_device]['Device Type'] == 'network_port':

                outputDevNameIdxDict.update({output_devices[output_device]['Device Name']:f"tcpipCons({iNetPort})"})
                printAutoInd(f,"TCPIPs({0}).ipAdd    = '{1}';",iNetPort,output_devices[output_device]['Device Port'])
                printAutoInd(f,"TCPIPs({0}).port     =  {1};",iNetPort,output_devices[output_device]['IP Port'])
                printAutoInd(f,"TCPIPs({0}).name     = '{1}';",iNetPort,output_devices[output_device]['Device Name'])
                printAutoInd(f,"TCPIPs({0}).isClient = {1};\n",iNetPort,output_devices[output_device]['Is Client'])
                iNetPort += 1

            elif output_devices[output_device]['Device Type'] == 'parallel_port':
                outputDevNameIdxDict.update({output_devices[output_device]['Device Name']:f"parPort({iParal}).port"})
                printAutoInd(f,"parPort({0}).port     = hex2dec('{1}');",iParal,output_devices[output_device]['Device Port'])
                printAutoInd(f,"parPort({0}).name     = '{1}';\n",iParal,output_devices[output_device]['Device Name'])
                iParal += 1

            elif output_devices[output_device]['Device Type'] == 'serial_port':

                outputDevNameIdxDict.update({output_devices[output_device]['Device Name']:f"serialCons({iSerial})"})
                printAutoInd(f,"serPort({0}).port     = '{1}';",iSerial,output_devices[output_device]['Device Port'])
                printAutoInd(f,"serPort({0}).name     = '{1}';",iSerial,output_devices[output_device]['Device Name'])
                printAutoInd(f,"serPort({0}).baudRate = '{1}';",iSerial,output_devices[output_device]['Baud Rate'])
                printAutoInd(f,"serPort({0}).dataBits = '{1}';\n",iSerial,output_devices[output_device]['Data Bits'])
                iSerial += 1

        printAutoInd(f,"%------------------------------------\\\n")

        printAutoInd(f,"disableSomeKbKeys; % restrictKeysForKbCheck")

        printAutoInd(f,"%----- initialize output devices --------/")
        printAutoInd(f,"%--- open windows ---/")
        printAutoInd(f,"winIds    = zeros({0},1);",iMonitor-1)
        printAutoInd(f,"winIFIs   = zeros({0},1);",iMonitor-1)
        printAutoInd(f,"fullRects = zeros({0},4);",iMonitor-1)

        printAutoInd(f,"for iWin = 1:numel(monitors)")
        printAutoInd(f,"[winIds(iWin),fullRects(iWin,:)] = Screen('OpenWindow',monitors(iWin).port,monitors(iWin).bkColor,[],[],[],[],monitors(iWin).muliSample);")
        printAutoInd(f,"Screen('BlendFunction', winIds(iWin),'GL_SRC_ALPHA','GL_ONE_MINUS_SRC_ALPHA'); % force to most common alpha-blending factors")
        printAutoInd(f,"winIFIs(iWin) = Screen('GetFlipInterval',winIds(iWin));                        % get inter frame interval (i.e., 1/refresh rate)")
        printAutoInd(f,"end % for iWin ")

        printAutoInd(f,"%--------------------\\\n")

        # initialize TCPIP connections
        if iNetPort > 1:
            printAutoInd(f,"%--- open TCPIPs ----/")
            printAutoInd(f,"tcpipCons = zeros({0},1);",iNetPort - 1)

            printAutoInd(f,"for iCount = 1:numel(TCPIPs)")

            if output_devices[output_device]['Is Client'] == 1:
                printAutoInd(f,"tcpipCons(iCount) = pnet('tcpconnect',TCPIPs(iCount).ipAdd,TCPIPs(iCount).port);")
            else:
                printAutoInd(f,"tcpipCons(iCount) = pnet('tcpsocket',TCPIPs(iCount).port);")


            printAutoInd(f,"end % iCount")

            printAutoInd(f,"%----------------------\\\n")

        # initialize serial ports
        if iSerial > 1:
            printAutoInd(f,"%--- open serial ports ----/")
            printAutoInd(f,"serialCons = zeros({0},1);",iSerial-1)

            printAutoInd(f,"for iCount = 1:numel(serialCons)")
            printAutoInd(f,"serialCons(iCount) = IOPort('OpenSerialPort',serPort(iCount).port,['BaudRate=',serPort(iCount).baudRate,',DataBits=',serPort(iCount).dataBits]);")
            printAutoInd(f,"end % iCount")
            printAutoInd(f,"%--------------------------\\\n")
        # initialize parallel ports
        if iParal > 1:
            printAutoInd(f,"%--- open parallel ports ----/")
            printAutoInd(f,"% for linux we directly use outb under sodo mode ")
            printAutoInd(f,"if IsWin")

            printAutoInd(f,"try")
            printAutoInd(f,"io64Obj = io64;")
            printAutoInd(f,"catch")
            printAutoInd(f,"error('Failed to find io64, please see \"http://apps.usd.edu/coglab/psyc770/IO64.html\" for instruction of installation!');")
            printAutoInd(f,"end % try")

            printAutoInd(f,"if 0 ~= io64(ioObj)")
            printAutoInd(f,"error('inputout 64 installation failed!');")
            printAutoInd(f,"end % if 0 ~= ")

            printAutoInd(f,"elseif IsOSX")
            printAutoInd(f,"error('curently, we did not support output via parallel under Mac OX!');")
            printAutoInd(f,"end % if IsWin")
            printAutoInd(f,"%----------------------------\\\n")

        printAutoInd(f,"%----------------------------------------\\\n")

        printAutoInd(f, "Priority(1);                % Turn the priority to high priority")


        # start to handle all the widgets
        printTimelineWidget( Info.WID_WIDGET[f"{Info.TIMELINE}.0"],f,attributesSetDict,0)


























        printAutoInd(f,"expEndTime = datestr(now,'dd-mmm-YYYY:HH:MM:SS'); % record the end time \n")
        printAutoInd(f,"sca;                        % Close opened windows")
        printAutoInd(f,"ShowCursor;                 % Show the hided mouse cursor")
        printAutoInd(f,"Priority(0);                % Turn the priority back to normal")
        printAutoInd(f,"RestrictKeysForKbCheck([]); % Re-enable all keys\n")

        printAutoInd(f,"if isWin",)
        printAutoInd(f,"ShowHideWinTaskbar(1);      % show the window taskbar.")
        printAutoInd(f,"end")

        printAutoInd(f,"save({0}.filename); % save the results\n",cFilenameOnly)


        #  close opend devices
        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f,"% close opened devices")
        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # close TCPIP connections
        if iNetPort > 1:
            printAutoInd(f,"%-- close serial ports --/")

            printAutoInd(f,"for iCount = 1:numel(tcpipCons)")
            printAutoInd(f,"pnet(tcpipCons(iCount),'close');")
            printAutoInd(f,"end % iCount")

            printAutoInd(f,"%------------------------\\\n")

        # close serial ports
        if iSerial > 1:
            printAutoInd(f,"%--- close serial ports ---/")
            printAutoInd(f,"for iCount = 1:numel(serialCons)")
            printAutoInd(f,"IOPort('Close',serialCons(iCount));")
            printAutoInd(f,"end % iCount")
            printAutoInd(f,"%--------------------------\\\n")

        # close parallel ports
        if iParal > 1:
            printAutoInd(f,"%--- close parallel ports ---/")
            printAutoInd(f,"% Currently, Under windows io64 need to be closed")
            printAutoInd(f,"% Under Linux, we will use outp (which will require running matlab under the sudo mode) to send trigger via parallel ")
            printAutoInd(f,"if IsWin")

            printAutoInd(f,"clear io64;")

            printAutoInd(f,"end % if IsWin")
            printAutoInd(f,"% Under windows io64 need to be closed")
            printAutoInd(f,"%----------------------------\\\n")







        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f,"% end of the experiment",)
        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n")

        printAutoInd(f,"catch {0}_error\n",cFilenameOnly)


        printAutoInd(f,"sca;                        % Close opened windows")
        printAutoInd(f,"ShowCursor;                 % Show the hided mouse cursor")
        printAutoInd(f,"Priority(0);                % Turn the priority back to normal")
        printAutoInd(f,"RestrictKeysForKbCheck([]); % Re-enable all keys")

        printAutoInd(f,"if isWin")
        printAutoInd(f,"ShowHideWinTaskbar(1);      % show the window taskbar")
        printAutoInd(f,"end")

        printAutoInd(f,"save('{0}_debug');",cFilenameOnly)
        printAutoInd(f,"rethrow({0}_error);",cFilenameOnly)


        printAutoInd(f,"end % try")


        printAutoInd(f,"end % function \n\n\n\n\n\n\n")

        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f,"% subfun 1: detectAbortKey")
        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f, "function detectAbortKey(abortKeyCode)")
        printAutoInd(f,"[keyIsDown, Noused, keyCode] = responseCheck(-1);")
        printAutoInd(f,"if keyCode(abortKeyCode)")

        printAutoInd(f,"error('The experiment was aborted by the experimenter!');")

        printAutoInd(f,"end")

        printAutoInd(f,"end %  end of subfunction\n\n\n")



        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f,"% subfun 2: disableSomeKeys")
        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f,"function disableSomeKbKeys()")
        printAutoInd(f,"{0}{1}{2}\n","RestrictKeysForKbCheck(KbName({",''.join("'"+ cItem +"'," for cItem in enabledKBKeysList)[:-1],"}));")
        printAutoInd(f,"end %  end of subfun2\n")


        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f,"% subfun 3: makeFrameRect")
        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f,"function outRect = makeFrameRect(x, y, frameWidth, frameHight, fullRect)")
        printAutoInd(f,"if x <= 1")
        printAutoInd(f,"x = x*fullRect(3);")
        printAutoInd(f,"end % if")

        printAutoInd(f,"if y <= 1")
        printAutoInd(f,"y = y*fullRect(4);")
        printAutoInd(f,"end % if")


        printAutoInd(f,"if frameWidth <= 1")
        printAutoInd(f,"frameWidth = frameWidth*fullRect(3);")
        printAutoInd(f,"end % if")

        printAutoInd(f,"if frameHight <= 1")
        printAutoInd(f,"frameHight = frameHigh*fullRect(4);")
        printAutoInd(f,"end % if")

        printAutoInd(f,"outRect = CenterRectOnPointd([0, 0, frameWidth, frameHight], x, y);")

        printAutoInd(f,"end %  end of subfun3")



    Func.log(f"Compile successful!:{compile_file_name}") # print info to the output panel
    # except Exception as e:
    #     printAutoInd(f,"compile error {e}")

