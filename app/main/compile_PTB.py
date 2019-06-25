import os
import sys
import datetime

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
from .wait_dialog import WaitDialog
# class compilePTB:
def compilePTB(globalSelf):
    if not Info.FILE_NAME:
        if not globalSelf.getFileName():
            QMessageBox.information(globalSelf, "Warning", "File must be saved before compiling.", QMessageBox.Ok)
            return

    # get save path
    compile_file_name = ".".join(Info.FILE_NAME.split('.')[:-1]) + ".m"
    # open file
    with open(compile_file_name, "w") as f:
        #  print function start info
        # import datetime
        # print(Info.TIMELINE)

        cFilenameOnly = os.path.split(compile_file_name)[1].split('.')[0]
        # the help info
        print(f"function {cFilenameOnly}()", file=f)
        print(f"% function generated by PTB Builder 0.1", file=f)
        print(f"% If you use PTB Builder for your research, then we would appreciate your citing our work in your paper:",file=f)
        print(f"% , (2019) PTB builder: a free GUI to generate experimental codes for Psychoolbox. Behavior Research Methods\n",file=f)
        print(f"% To report possible bugs and any suggestions please send us e-mail:", file=f)
        print(f"% Yang Zhang", file=f)
        print(f"% Ph.D", file=f)
        print(f"% Department of Psychology, \n% SooChow University", file=f)
        print(f"% zhangyang873@gmail.com \n% Or yzhangpsy@suda.edu.cn", file=f)
        print(f"% {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", file=f)
        # begin of the function
        print(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", file=f)
        print(f"%      begin      ", file=f)
        print(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", file=f)
        # get subject information
        print(f"\t%----- get subject information -------/", file=f)
        print(f"\t{cFilenameOnly} = OpenExp_BCL('{cFilenameOnly}',pwd);", file=f)
        print(f"\tclose(gcf);", file=f)
        print(f"\t%-------------------------------------\\\n", file=f)

        # the function body try, catch end
        print(f"\ttry", file=f)

        print(f"\t\tKbName('UnifyKeyNames');\n", file=f)
        print(f"\t\tabortKeyCode = KbName('ESCAPE');\n", file=f)

        print(f"\t\texpStartTime = datestr(now,'dd-mmm-YYYY:HH:MM:SS'); % record start time \n", file=f)

        print(f"\t\t%--------Reinitialize the global random seed ---------/", file=f)
        print(f"\t\tcRandSeed = RandStream('mt19937ar','Seed','shuffle');", file=f)
        print(f"\t\tRandStream.setGlobalStream(cRandSeed);", file=f)
        print(f"\t\t%-----------------------------------------------------\\\n", file=f)
        print(f"\t\thideCursor;            % hide mouse cursor\n", file=f)
        print(f"\t\tif isWin", file=f)
        print(f"\t\t\tShowHideWinTaskbar(0); % hide the window taskbar\n", file=f)
        print(f"\t\tend", file=f)


        print(f"\t\t%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", file=f)
        print(f"\t\t% define and initialize input/output devices", file=f)
        print(f"\t\t%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", file=f)
        # get output devices, such as global output devices.
        # you can get each widget's device you selected
        print(f"\t\t%----- define output devices --------/", file=f)
        output_devices = Info.OUTPUT_DEVICE_INFO


        # print(Info.INPUT_DEVICE_INFO)
        # print(Info.OUTPUT_DEVICE_INFO)

        iMonitor = 1
        iParal   = 1
        iNetPort = 1
        iSerial  = 1

        for output_device in output_devices:
            # print(output_device)
            # get output device index
            output_device_index = output_device.split('.')[-1]

            if output_devices[output_device]['Device Type'] == 'screen':

                print(f"\t\tmonitors({iMonitor}).port       = {output_devices[output_device]['Device Port']};", file=f)
                print(f"\t\tmonitors({iMonitor}).name       = '{output_devices[output_device]['Device Name']}';", file=f)
                print(f"\t\tmonitors({iMonitor}).bkColor    = '{output_devices[output_device]['Back Color']}';", file=f)
                print(f"\t\tmonitors({iMonitor}).muliSample = {output_devices[output_device]['Multi Sample']};\n", file=f)
                iMonitor += 1

            elif output_devices[output_device]['Device Type'] == 'network_port':
                # try:
                #     Func.log(f"{output_devices[output_device]['Device Port']}")  # print info to the output panel
                #     cIpAddress, cPortValue = output_devices[output_device]['Device Port'].split(':')
                # except:
                #     QMessageBox.information(globalSelf, "Warning",  "Output device '{}''s IPPort '{}' should be in format:\n 'IPAdress:Port'".format(output_devices[output_device]['Device Name'],output_devices[output_device]['Device Port']),
                #                             QMessageBox.Ok)
                #     return

                print(f"\t\tTCPIPs({iNetPort}).ipAdd    = '{output_devices[output_device]['Device Port']}';", file=f)
                print(f"\t\tTCPIPs({iNetPort}).port     =  {output_devices[output_device]['IP Port']};", file=f)
                print(f"\t\tTCPIPs({iNetPort}).name     = '{output_devices[output_device]['Device Name']}';", file=f)
                print(f"\t\tTCPIPs({iNetPort}).isClient = {output_devices[output_device]['Is Client']};\n", file=f)
                # print(f"TCPIPs({iNetPort}).type = '{output_devices[output_device]['Device Type']}';", file=f)
                # print(f"TCPIPs({iNetPort}).index = '{output_device_index}';", file=f)
                iNetPort += 1

            elif output_devices[output_device]['Device Type'] == 'parallel_port':
                print(f"\t\tparPort({iParal}).port     = hex2dec('{output_devices[output_device]['Device Port']}');", file=f)
                print(f"\t\tparPort({iParal}).name     = '{output_devices[output_device]['Device Name']}';\n", file=f)
                # print(f"parPort({iParal}).type = '{output_devices[output_device]['Device Type']}';", file=f)
                # print(f"parPort({iParal}).index = '{output_device_index}';", file=f)
                iParal += 1

            elif output_devices[output_device]['Device Type'] == 'serial_port':
                print(f"\t\tserPort({iSerial}).port     = '{output_devices[output_device]['Device Port']}';", file=f)
                print(f"\t\tserPort({iSerial}).name     = '{output_devices[output_device]['Device Name']}';", file=f)
                print(f"\t\tserPort({iSerial}).baudRate = '{output_devices[output_device]['Baud Rate']}';", file=f)
                print(f"\t\tserPort({iSerial}).dataBits = '{output_devices[output_device]['Data Bits']}';\n", file=f)
                # print(f"serPort({iSerial}).type = '{output_devices[output_device]['Device Type']}';", file=f)
                # print(f"serPort({iSerial}).index = '{output_device_index}';", file=f)
                iSerial += 1

        print(f"\t\t%------------------------------------\\\n", file=f)

        print(f"\t\t%----- initalize output devices ---------/", file=f)
        print(f"\n\t\t%--- open windows ---/", file=f)
        print(f"\t\twinIds    = zeros({iMonitor-1},1);", file=f)
        print(f"\t\twinIFIs   = zeros({iMonitor-1},1);", file=f)
        print(f"\t\tfullRects = zeros({iMonitor-1},4);\n", file=f)

        print(f"\t\tfor iWin = 1:numel(monitors)", file=f)
        print(f"\t\t\t[winIds(iWin),fullRects(iWin,:)] = Screen('OpenWindow',monitors(iWin).port,monitors(iWin).bkColor,[],[],[],[],monitors(iWin).muliSample);", file=f)
        print(f"\t\t\tScreen('BlendFunction', winIds(iWin),'GL_SRC_ALPHA','GL_ONE_MINUS_SRC_ALPHA'); % force to most common alpha-blending factors", file=f)
        print(f"\t\t\twinIFIs(iWin) = Screen('GetFlipInterval',winIds(iWin));                        % get inter frame interval (i.e., 1/refresh rate)", file=f)
        print(f"\t\tend % for iWin ", file=f)

        print(f"\t\t%--------------------\\\n", file=f)

        # initialize TCPIP connections
        if iNetPort > 1:
            print(f"\n\t\t%--- open TCPIPs ----/", file=f)
            print(f"\t\ttcpipCons = zeros({iNetPort - 1},1);\n", file=f)

            print(f"\t\tfor iCount = 1:numel(TCPIPs)", file=f)

            if output_devices[output_device]['Is Client'] == 1:
                print(f"\t\t\ttcpipCons(iCount) = pnet('tcpconnect',TCPIPs(iCount).ipAdd,TCPIPs(iCount).port);", file=f)
            else:
                print(f"\t\t\ttcpipCons(iCount) = pnet('tcpsocket',TCPIPs(iCount).port);", file=f)

            print(f"\t\tend % iCount", file=f)

            print(f"\t\t%----------------------\\\n", file=f)

        # initialize serial ports
        if iSerial > 1:
            print(f"\n\t\t%--- open serial ports ----/", file=f)
            print(f"\t\tserialCons = zeros({iSerial-1},1);\n", file=f)

            print(f"\t\tfor iCount = 1:numel(serialCons)", file=f)
            print(f"\t\t\tserialCons(iCount) = IOPort('OpenSerialPort',serPort(iCount).port,['BaudRate=',serPort(iCount).baudRate,',DataBits=',serPort(iCount).dataBits]);", file=f)
            print(f"\t\tend % iCount", file=f)
            print(f"\t\t%--------------------------\\\n", file=f)
        # initialize parallel ports
        if iParal > 1:
            print(f"\n\t\t%--- open parallel ports ----/", file=f)
            print(f"\t\t% for linux we directly use outb under sodo mode ", file=f)
            print(f"\t\tif IsWin", file=f)
            print(f"\t\t\ttry", file=f)
            print(f"\t\t\t\tio64Obj = io64;", file=f)
            print(f"\t\t\tcatch", file=f)
            print(f"\t\t\t\terror('Failed to find io64, please see \"http://apps.usd.edu/coglab/psyc770/IO64.html\" for instruction of installation!');", file=f)
            print(f"\t\t\tend % try\n", file=f)
            print(f"\t\t\tif 0 ~= io64(ioObj)", file=f)
            print(f"\t\t\t\terror('inputout 64 installation failed!');", file=f)
            print(f"\t\t\tend % if 0 ~= ", file=f)
            print(f"\t\telseif IsOSX", file=f)
            print(f"\t\t\terror('curently, we did not support output via parallel under Mac OX!');", file=f)
            print(f"\t\tend % if IsWin", file=f)
            print(f"\t\t%----------------------------\\\n", file=f)
        print(f"\t\t%----------------------------------------\\\n", file=f)





        # get widgets in the main timeline
        cTimelineWidgetIds = Func.getWidgetIDInTimeline(f"{Info.TIMELINE}.0")

        for cWidgetId in cTimelineWidgetIds:
            cWidget = Info.WID_WIDGET[cWidgetId]
            print(Func.getWidgetName(cWidgetId))
            print(cWidget.widget_id)
            print(Func.getProperties(cWidgetId))
            print(cWidget.getPropertyByKey('Text'))
            # print(Func.getScreen)

            # print(dir(cWidget))

        """
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





        print(f"\t\tPriority(1);                % Turn the priority to high priority", file=f)


















        print(f"\t\texpEndTime = datestr(now,'dd-mmm-YYYY:HH:MM:SS'); % record the end time \n", file=f)
        print(f"\t\tsca;                        % Close opened windows", file=f)
        print(f"\t\tShowCursor;                 % Show the hided mouse cursor", file=f)
        print(f"\t\tPriority(0);                % Turn the priority back to normal", file=f)
        print(f"\t\tRestrictKeysForKbCheck([]); % Re-enable all keys\n", file=f)
        print(f"\t\tif isWin", file=f)
        print(f"\t\t\tShowHideWinTaskbar(1);      % show the window taskbar.", file=f)
        print(f"\t\tend\n", file=f)
        print(f"\t\tsave({cFilenameOnly}.filename); % save the results\n", file=f)


        #  close opend devices
        print(f"\t\t%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", file=f)
        print(f"\t\t% close opened devices", file=f)
        print(f"\t\t%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", file=f)
        # close TCPIP connections
        if iNetPort > 1:
            print(f"\n\t\t%-- close serial ports --/", file=f)

            print(f"\t\tfor iCount = 1:numel(tcpipCons)", file=f)
            print(f"\t\t\tpnet(tcpipCons(iCount),'close');", file=f)
            print(f"\t\tend % iCount", file=f)

            print(f"\t\t%------------------------\\\n", file=f)

        # close serial ports
        if iSerial > 1:
            print(f"\n\t\t%--- close serial ports ---/", file=f)

            print(f"\t\tfor iCount = 1:numel(serialCons)", file=f)
            print(f"\t\t\tIOPort('Close',serialCons(iCount));", file=f)
            print(f"\t\tend % iCount", file=f)
            print(f"\t\t%--------------------------\\\n", file=f)

        # close parallel ports
        if iParal > 1:
            print(f"\n\t\t%--- close parallel ports ---/", file=f)
            print(f"\t\t% Currently, Under windows io64 need to be closed", file=f)
            print(f"\t\t% Under Linux, we will use outp (which will require running matlab under the sodo mode) to send trigger via parallel ", file=f)
            print(f"\t\tif IsWin", file=f)
            print(f"\t\t\tclear io64;", file=f)
            print(f"\t\tend % if IsWin", file=f)
            print(f"\t\t% Under windows io64 need to be closed", file=f)
            print(f"\t\t%----------------------------\\\n", file=f)







        print(f"\t%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%", file=f)
        print(f"\t% end of the experiment", file=f)
        print(f"\t%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%\n", file=f)
        print(f"\tcatch {cFilenameOnly}_error\n", file=f)

        print(f"\t\tsca;                        % Close opened windows", file=f)
        print(f"\t\tShowCursor;                 % Show the hided mouse cursor", file=f)
        print(f"\t\tPriority(0);                % Turn the priority back to normal", file=f)
        print(f"\t\tRestrictKeysForKbCheck([]); % Re-enable all keys\n", file=f)
        print(f"\t\tif isWin", file=f)
        print(f"\t\t\tShowHideWinTaskbar(1);      % show the window taskbar", file=f)
        print(f"\t\tend\n", file=f)
        print(f"\t\tsave('{cFilenameOnly}_debug');", file=f)
        print(f"\t\trethrow({cFilenameOnly}_error);", file=f)

        print(f"\tend % try\n", file=f)

        print(f"end % function \n\n\n\n\n\n\n", file=f)

        print(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%", file=f)
        print(f"% subfun 1: detectAbortKey", file=f)
        print(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%", file=f)

        print(f"function detectAbortKey_bcl(abortKeyCode)\n", file=f)
        print(f"\t[keyIsDown, Noused, keyCode] = responseCheck(-1);", file=f)
        print(f"\tif keyCode(abortKeyCode)", file=f)
        print(f"\t\terror('The experiment was aborted by the experimenter!');", file=f)
        print(f"\tend", file=f)
        print(f"end\n", file=f)



    Func.log(f"Compile successful!\n{compile_file_name}") # print info to the output panel
    # except Exception as e:
    #     print(f"compile error {e}")

