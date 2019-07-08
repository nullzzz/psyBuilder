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
# cLoopLevel      = 0
def throwCompileErrorInfo(inputStr):
    msg = QMessageBox()
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowIcon(QIcon(Func.getImage("icon.png")))

    msg.setText(inputStr)
    # msg.setInformativeText("This is additional information")
    msg.setWindowTitle("    Attention!   ")
    # msg.setDetailedText("The details are as follows:")
    # msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    msg.setStandardButtons(QMessageBox.Ok)
    # msg.buttonClicked.connect(msgbtn)

    msg.exec_()
    raise Exception(inputStr)

def printAutoInd(f,inputStr,*argins):
    global cIndents
    global isPreLineSwitch

    incrAfterStr    = ('if','try','switch','for','while')
    decreAndIncrStr = ('else','elseif','otherwise','catch')

    #    print(inputStr.split(' ')[0])
    if inputStr.split(' ')[0] in incrAfterStr:
        # print(f"{inputStr}:{cIndents},increase 1")
        tabStrs = '\t' * cIndents
        print(f"\n{tabStrs}{inputStr}".format(*argins), file=f)
        cIndents += 1

    elif inputStr.split(' ')[0] in decreAndIncrStr:
        # print(f"{inputStr.split(' ')[0]}, -1 and +1")
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
            # print(f"{inputStr.split(' ')[0]}, -1")
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


def is_contain_ch(check_str):
    """
    :param check_str: {str}
    :return: {bool} True and False for have and have not chinese characters respectively
    """
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False


def dataStrConvert(dataStr):
    # convert string to neither a string or a num
    # e.g.,
    # 2.00 to 2.0
    # abcd to 'abcd'
    # [12,12,12] to [12,12,12]
    try:
        outData = float(dataStr)
    except:
        if re.match("^\[\d+,\d+,\d+\]$", dataStr):
            outData = dataStr
        else:
            outData = "'"+dataStr+"'"
    return outData

# add curly brackets
def addCurlyBrackets(inputStr):
    outputStr = "{"+str(inputStr)+"}"
    return outputStr

def getRefValue(inputStr):
    tempMatchObj = re.match("^\[.*\]$", inputStr)

    if tempMatchObj:
        inputStr = re.sub("[\[\]]", '', inputStr)
        return [True,inputStr]

    return [False,inputStr]

def isRgbStr(inputStr):
    isRgbFormat = re.match("^\d+,\d+,\d+$", inputStr)
    return isRgbFormat



def parseAllowKeys(enabledKBKeysList,allowKeyStr):
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
            noStimRelatedCodes = printTextWidget(cWidget, f, attributesSetDict, noStimRelatedCodes)

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


def printTextWidget(cWidget,f,attributesSetDict ,noStimRelatedCodes):
    global enabledKBKeysList
    cProperties = Func.getProperties(cWidget.widget_id)
    # to be continue ...



    return noStimRelatedCodes


def printCycleWdiget(cWidget, f,attributesSetDict,cLoopLevel, noStimRelatedCodes):
    # global cLoopLevel
    # start from 1 to compatible with MATLAB
    cLoopLevel += 1

    attributesSetDict       = attributesSetDict.copy()
    cWidgetName = Func.getWidgetName(cWidget.widget_id)

    # cLoopIterStr = f"iLoop_{cLoopLevel}"

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
            isRefValue, valueStr = getRefValue(value)

            if isRefValue:
                if valueStr in attributesSetDict:
                    # assign the refered value to the current rowDict
                    cRowDict[key] = attributesSetDict[valueStr][2]
                else:
                    throwCompileErrorInfo(f"The cited attribute '{valueStr}' \nis not available for {cWidgetName}")
                    # Func.log(f"The cited attribute '{valueStr}' was not exist for the current widget {cWidgetName}",1)

            # isRgbFormat = re.match("^\d+,\d+,\d+$", cRowDict[key])
            isRgbFormat = isRgbStr(cRowDict[key])

            if isRgbFormat:
                # transform the RGB to include a pair of square brackets
                # print('find RGB')
                # print(isRgbFormat[0])
                cRowDict[key] = f"[{isRgbFormat[0]}]"

        if '' == cRowDict['Weight']:
            cRepeat = 1
        else:
            cRepeat = dataStrConvert(cRowDict['Weight'])

        for iRep in range(int(cRepeat)):
            # print("".join(str(dataStrConvert(value)) + " " for key, value in cRowDict.items()))
            printAutoInd(f,'{0}',"".join(addCurlyBrackets(dataStrConvert(value)) + " " for key, value in cRowDict.items())+";...")


    printAutoInd(f,'{0}\n',endExpStr)
    # cycling
    printAutoInd(f, '% looping across each row of the {0}.attr:{1}',cWidgetName , cLoopIterStr)
    printAutoInd(f, 'for {0} = size({1},1)', cLoopIterStr, f"{cWidgetName}.attr")

    # handle each timeline
    cTimeLineList = cWidget.getTimelines()

    for iTimeline_name, iTimeline_id in cTimeLineList:
        if '' == iTimeline_id:
            throwCompileErrorInfo(f"In {cWidgetName}: Timeline should not be empty!")
        else:
            printTimelineWidget(Info.WID_WIDGET[iTimeline_id], f, attributesSetDict, cLoopLevel)

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
    attributesSetDict        = {'sessionNum':[0,'SubInfo.session'],'subAge':[0,'SubInfo.age'],'subName':[0,'SubInfo.name'],'subSex':[0,'SubInfo.sex'],'subNum':[0,'SubInfo.num'],'subHandness':[0,'SubInfo.hand']}
    # parsedAttributesSetDict  = {'sessionNum':[0,'SubInfo.session'],'subAge':[0,'SubInfo.age'],'subName':[0,'SubInfo.name'],'subSex':[0,'SubInfo.sex'],'subNum':[0,'SubInfo.num'],'subHandness':[0,'SubInfo.hand']}


    # attributesSetDict.setdefault('sessionNum',0)

    if not Info.FILE_NAME:
        if not globalSelf.getFileName():
            QMessageBox.information(globalSelf, "Warning", "File must be saved before compiling.", QMessageBox.Ok)
            return

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

        printAutoInd(f,"if isWin")
        printAutoInd(f,"ShowHideWinTaskbar(0); % hide the window taskbar")
        printAutoInd(f,"end")


        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f,"% define and initialize input/output devices")
        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        # get output devices, such as global output devices.
        # you can get each widget's device you selected
        output_devices = Info.OUTPUT_DEVICE_INFO
        input_devices  = Info.INPUT_DEVICE_INFO

        printAutoInd(f,"%------ define input devices --------/")
        iKeyboard = 1
        iGamepad  = 1
        iRespBox  = 1
        iMouse    = 1

        for input_device in input_devices:
            print(input_device)
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

        for output_device in output_devices:
            # print(output_device)
            # get output device index
            # output_device_index = output_device.split('.')[-1]

            if output_devices[output_device]['Device Type'] == 'screen':
                printAutoInd(f,"monitors({0}).port       =  {1};",iMonitor,output_devices[output_device]['Device Port'])
                printAutoInd(f,"monitors({0}).name       = '{1}';",iMonitor,output_devices[output_device]['Device Name'])
                printAutoInd(f,"monitors({0}).bkColor    = '{1}';",iMonitor,output_devices[output_device]['Back Color'])
                printAutoInd(f,"monitors({0}).muliSample =  {1};\n",iMonitor,output_devices[output_device]['Multi Sample'])
                iMonitor += 1

            elif output_devices[output_device]['Device Type'] == 'network_port':
                # try:
                #     Func.log(f"{output_devices[output_device]['Device Port']}")  # print info to the output panel
                #     cIpAddress, cPortValue = output_devices[output_device]['Device Port'].split(':')
                # except:
                #     QMessageBox.information(globalSelf, "Warning",  "Output device '{}''s IPPort '{}' should be in format:\n 'IPAdress:Port'".format(output_devices[output_device]['Device Name'],output_devices[output_device]['Device Port']),
                #                             QMessageBox.Ok)
                #     return

                printAutoInd(f,"TCPIPs({0}).ipAdd    = '{1}';",iNetPort,output_devices[output_device]['Device Port'])
                printAutoInd(f,"TCPIPs({0}).port     =  {1};",iNetPort,output_devices[output_device]['IP Port'])
                printAutoInd(f,"TCPIPs({0}).name     = '{1}';",iNetPort,output_devices[output_device]['Device Name'])
                printAutoInd(f,"TCPIPs({0}).isClient = {1};\n",iNetPort,output_devices[output_device]['Is Client'])
                # printAutoInd(f,"TCPIPs({iNetPort}).type = '{output_devices[output_device]['Device Type']}';",)
                # printAutoInd(f,"TCPIPs({iNetPort}).index = '{output_device_index}';",)
                iNetPort += 1

            elif output_devices[output_device]['Device Type'] == 'parallel_port':
                printAutoInd(f,"parPort({0}).port     = hex2dec('{1}');",iParal,output_devices[output_device]['Device Port'])
                printAutoInd(f,"parPort({0}).name     = '{1}';\n",iParal,output_devices[output_device]['Device Name'])
                # printAutoInd(f,"parPort({iParal}).type = '{output_devices[output_device]['Device Type']}';",)
                # printAutoInd(f,"parPort({iParal}).index = '{output_device_index}';",)
                iParal += 1

            elif output_devices[output_device]['Device Type'] == 'serial_port':
                printAutoInd(f,"serPort({0}).port     = '{1}';",iSerial,output_devices[output_device]['Device Port'])
                printAutoInd(f,"serPort({0}).name     = '{1}';",iSerial,output_devices[output_device]['Device Name'])
                printAutoInd(f,"serPort({0}).baudRate = '{1}';",iSerial,output_devices[output_device]['Baud Rate'])
                printAutoInd(f,"serPort({0}).dataBits = '{1}';\n",iSerial,output_devices[output_device]['Data Bits'])
                # printAutoInd(f,"serPort({iSerial}).type = '{output_devices[output_device]['Device Type']}';",)
                # printAutoInd(f,"serPort({iSerial}).index = '{output_device_index}';",)
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

        printAutoInd(f, "function detectAbortKey()\n")
        printAutoInd(f,"[keyIsDown, Noused, keyCode] = responseCheck(-1);")
        printAutoInd(f,"if keyCode(abortKeyCode)")

        printAutoInd(f,"error('The experiment was aborted by the experimenter!');")

        printAutoInd(f,"end")

        printAutoInd(f,"end %  end of subfunction\n\n\n")



        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        printAutoInd(f,"% subfun 2: disableSomeKeys")
        printAutoInd(f,"%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        printAutoInd(f,"function disableSomeKbKeys()\n")
        printAutoInd(f,"{0}{1}{2}\n","RestrictKeysForKbCheck(KbName({",''.join("'"+ cItem +"'," for cItem in enabledKBKeysList)[:-1],"}));")
        printAutoInd(f,"end %  end of subfun2\n")



    Func.log(f"Compile successful!:{compile_file_name}") # print info to the output panel
    # except Exception as e:
    #     printAutoInd(f,"compile error {e}")

