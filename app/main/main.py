import os
import sys

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


class PsyApplication(QMainWindow):
    def __init__(self, parent=None):
        super(PsyApplication, self).__init__(parent)

        menu_bar = self.menuBar()

        # file menu
        file_menu = menu_bar.addMenu("&File")
        new_file_action = QAction("&New", self)
        new_file_action.triggered.connect(self.newFile)
        open_file_action = QAction("&Open", self)
        open_file_action.triggered.connect(self.loadIn)
        save_file_action = QAction("&Save", self)
        save_file_action.triggered.connect(self.save)
        save_as_file_action = QAction("&Save As", self)
        save_as_file_action.triggered.connect(self.saveAs)
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(QApplication.exit)

        file_menu.addAction(new_file_action)
        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)
        file_menu.addAction(save_as_file_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)

        # view menu
        view_menu = menu_bar.addMenu("&View")
        self.attribute_action = QAction("&Attribute", self)
        self.structure_action = QAction("&Structure", self)
        self.main_action = QAction("&Main", self)
        self.property_action = QAction("&Property", self)
        self.output_action = QAction("&Output", self)

        self.save_default_action = QAction("&Save as Default", self)
        self.default_action = QAction("&Default", self)

        self.attribute_action.setData("attribute")
        self.structure_action.setData("structure")
        self.main_action.setData("main")
        self.output_action.setData("output")
        self.property_action.setData("property")

        self.attribute_action.triggered.connect(self.setDockView)
        self.structure_action.triggered.connect(self.setDockView)
        self.main_action.triggered.connect(self.setDockView)
        self.output_action.triggered.connect(self.setDockView)
        self.property_action.triggered.connect(self.setDockView)

        self.save_default_action.triggered.connect(self.updateLayout)
        self.default_action.triggered.connect(self.resetView)

        view_menu.addAction(self.attribute_action)
        view_menu.addAction(self.structure_action)
        view_menu.addAction(self.main_action)
        view_menu.addAction(self.property_action)
        view_menu.addAction(self.output_action)
        view_menu.addSeparator()
        view_menu.addAction(self.default_action)

        # devices menu
        self.input_devices = GlobalDevice(io_type=0)
        self.input_devices.setWindowModality(Qt.ApplicationModal)
        self.input_devices.ok()
        self.output_devices = GlobalDevice(io_type=1)
        self.output_devices.setWindowModality(Qt.ApplicationModal)
        self.output_devices.ok()
        devices_menu = menu_bar.addMenu("&Devices")

        output_devices_action = QAction("&Output Devices", self)
        input_devices_action = QAction("&Input Devices", self)
        output_devices_action.triggered.connect(lambda: self.showDevices(1))
        input_devices_action.triggered.connect(lambda: self.showDevices(0))

        devices_menu.addAction(output_devices_action)
        devices_menu.addAction(input_devices_action)

        # build menu
        build_menu = menu_bar.addMenu("&Building")
        compile_action = QAction("&Compile", self)

        compile_action.triggered.connect(self.compile)

        build_menu.addAction(compile_action)

        # help menu
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)
        about_Qt_action = QAction("&About Qt", self)
        check_for_update = QAction("&Check for updates", self)

        about_action.triggered.connect(self.about)
        about_Qt_action.triggered.connect(QApplication.instance().aboutQt)
        check_for_update.triggered.connect(self.checkUpdate)

        help_menu.addAction(about_action)
        help_menu.addAction(about_Qt_action)
        help_menu.addAction(check_for_update)

        # attributes
        self.attributes = Attributes(self)
        self.attributes.setWindowTitle("Attributes")
        self.attributes.setObjectName("Attributes")
        # structure
        self.structure = Structure()
        self.structure.setWindowTitle("Structure")
        self.structure.setObjectName("Structure")
        # properties
        self.properties = Properties()
        self.properties.setWindowTitle("Properties")
        self.properties.setObjectName("Properties")
        # center
        self.center = Center()
        self.center.setWindowTitle("Main")
        self.center.setObjectName("Main")
        # output
        self.output = Output()
        # 控制台输出
        Func.log = self.output.print
        self.output.setWindowTitle("Output")
        self.output.setObjectName("Output")

        # 添加dock widget
        self.addDockWidget(Qt.LeftDockWidgetArea, self.structure)
        self.splitDockWidget(self.structure, self.center, Qt.Horizontal)
        self.splitDockWidget(self.center, self.attributes, Qt.Horizontal)
        self.splitDockWidget(self.structure, self.properties, Qt.Vertical)
        self.splitDockWidget(self.center, self.output, Qt.Vertical)

        self.attributes.visibilityChanged.connect(self.checkVisible)
        self.structure.visibilityChanged.connect(self.checkVisible)
        self.properties.visibilityChanged.connect(self.checkVisible)
        self.center.visibilityChanged.connect(self.checkVisible)
        self.output.visibilityChanged.connect(self.checkVisible)

        self.default_dock_widget_layout = self.saveState()

        # wait dialog
        self.wait_dialog = WaitDialog(self)

        self.linkSignals()

    def initialize(self):
        """
        开场的动画效果，及初始ui大小设置
        :return:
        """
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(1000)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()

    def linkSignals(self):
        """
        初始化时需要连接的信号，包括几个大的区域和初始的timeline
        :return:
        """
        # 初始化
        self.linkWidgetSignals(f'{Info.TIMELINE}.0')
        # structure
        self.structure.widgetSignalsLink.connect(self.linkWidgetSignals)
        self.structure.widgetCreatStart.connect(self.wait_dialog.start)
        self.structure.widgetCreatEnd.connect(self.wait_dialog.stop)
        self.structure.structure_tree.widgetOpen.connect(self.center.widget_tabs.openWidget)
        self.structure.structure_tree.nodeNameChange.connect(self.center.widget_tabs.changeTabName)
        self.structure.structure_tree.nodeDelete.connect(self.center.widget_tabs.closeTab)
        # center
        self.center.widget_tabs.tabChange.connect(self.properties.showProperties)
        self.center.widget_tabs.tabChange.connect(self.attributes.showAttributes)
        # output

    def linkWidgetSignals(self, widget_id: str):
        """
        为widget连接信号
        :param widget_id: 需要连接信号的widget的widget_id
        :return:
        """
        # 1：widget_tabs
        self.center.widget_tabs.linkWidgetSignals(widget_id)
        # 2：main
        widget = Info.WID_WIDGET[widget_id]
        # 通用信号
        widget.propertiesChange.connect(self.properties.showProperties)
        # 特有信号
        widget_type = widget_id.split('.')[0]
        if widget_type == Info.TIMELINE:
            self.linkTimelineSignals(widget_id)
        elif widget_type == Info.CYCLE:
            self.linkCycleSignals(widget_id)

    def linkTimelineSignals(self, widget_id):
        """
        为timeline连接与其他dock widget的信号
        :param widget_id:
        :return:
        """
        try:
            timeline: Timeline = Info.WID_WIDGET[widget_id]
            try:
                timeline.widget_icon_area.widgetIconAdd.disconnect(self.structure.addNode)
                timeline.widget_icon_area.widgetIconAdd.connect(self.structure.addNode)
            except Exception:
                timeline.widget_icon_area.widgetIconAdd.connect(self.structure.addNode)
                timeline.widget_icon_area.widgetIconMove.connect(self.structure.moveNode)
                timeline.widget_icon_area.widgetIconMove.connect(self.attributes.showAttributes)
                timeline.widget_icon_area.widget_icon_table.propertiesShow.connect(self.properties.showProperties)
                timeline.widget_icon_area.widget_icon_table.attributesShow.connect(self.attributes.showAttributes)
                timeline.widget_icon_area.widget_icon_table.widgetIconNameChange.connect(self.structure.renameNode)
                timeline.widget_icon_area.widget_icon_table.widgetIconDelete.connect(self.structure.deleteNode)
        except Exception as e:
            print(f"error {e} happens in link timeline signals. [main/main.py]")
            Func.log(f"error {e} happens in link timeline signals. [main/main.py]")

    def linkCycleSignals(self, widget_id):
        """
        为cycle连接与其他dock widget的信号
        :param widget_id:
        :return:
        """
        try:
            cycle: Cycle = Info.WID_WIDGET[widget_id]
            try:
                cycle.timeline_table.timeline_add.disconnect(self.structure.addNode)
                cycle.timeline_table.timeline_add.connect(self.structure.addNode)
            except Exception:
                cycle.timeline_table.timeline_add.connect(self.structure.addNode)
                cycle.timeline_table.timeline_delete.connect(self.structure.deleteNode)
        except Exception as e:
            print(f"error {e} happens in link timeline signals. [main/main.py]")

    def newFile(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def save(self):
        """
        这个就是在保存之前获取一下文件名
        :return:
        """
        if Info.FILE_NAME == "":
            self.getFileName()
        else:
            self.loadOut()

    def getFileName(self) -> bool:
        """
        获取文件名
        :return:
        """
        options = QFileDialog.Options()
        save_file_name, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Psy Files (*.ini);", options=options)
        if save_file_name:
            Info.FILE_NAME = save_file_name
            return True
        return False

    def saveAs(self):
        self.getFileName()
        if Info.FILE_NAME:
            self.loadOut()

    def loadIn(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose file", "", "Psy File (*.psy;*.ini)", options=options)

        if file_name:
            # 更新文件名
            Info.FILE_NAME = file_name
            file_name: str
            setting = QSettings(file_name, QSettings.IniFormat)

            # 复原根节点
            # 清空原编辑状态就在这儿做
            root = Info.WID_WIDGET[f"{Info.TIMELINE}.0"]
            root_info = setting.value(f"{Info.TIMELINE}.0")
            if root_info:
                root.restore(root_info)

            # 更新输入输出设备
            input_device_info = setting.value("INPUT_DEVICE_INFO")
            if input_device_info:
                self.input_devices.setProperties(input_device_info)
            output_device_info = setting.value("OUTPUT_DEVICE_INFO")
            if output_device_info:
                self.output_devices.setProperties(output_device_info)
            # 恢复布局
            dock_layout = setting.value("DOCK_LAYOUT")
            if dock_layout:
                self.restoreState(dock_layout)
            # 恢复name_wid
            name_wid: dict = setting.value("NAME_WID")
            if name_wid:
                Info.NAME_WID = name_wid.copy()
                Info.NAME_WID = Info.NAME_WID
            # 加载控件
            structure_tree: list = setting.value("STRUCTURE_TREE")
            self.structure.loadStructure(structure_tree)
        Func.log(f"{Info.FILE_NAME} loaded successful!")

    def loadOut(self):
        # 导出输入设备信息
        input_device_info: dict = Info.INPUT_DEVICE_INFO.copy()
        output_device_info: dict = Info.OUTPUT_DEVICE_INFO.copy()
        # 当前布局信息
        current_dock_layout = self.saveState()
        #
        name_wid = Info.NAME_WID.copy()

        setting = QSettings(Info.FILE_NAME, QSettings.IniFormat)
        setting.setValue("INPUT_DEVICE_INFO", input_device_info)
        setting.setValue("OUTPUT_DEVICE_INFO", output_device_info)
        setting.setValue("DOCK_LAYOUT", current_dock_layout)
        setting.setValue("NAME_WID", name_wid)

        structure_tree: list = self.structure.getStructure("李扬是个大瓜皮")
        self.loadOutTree(structure_tree)
        setting.setValue("STRUCTURE_TREE", structure_tree)

        Func.log(f"{Info.FILE_NAME} saved successful!")

    def loadOutTree(self, tree):
        if isinstance(tree, list):
            for i in tree:
                self.loadOutTree(i)
        elif isinstance(tree, tuple):
            widget_id = tree[1]
            setting = QSettings(Info.FILE_NAME, QSettings.IniFormat)
            setting.setValue(widget_id, Info.WID_WIDGET[widget_id].getInfo())

    def resetView(self):
        """
        恢复默认布局
        :return:
        """
        self.restoreState(self.default_dock_widget_layout)

    def updateLayout(self):
        """
        重新设置默认布局
        :return:
        """
        self.default_dock_widget_layout = self.saveState()

    def setDockView(self, checked):
        """
        单个dock的显示与隐藏
        :param checked:
        :return:
        """
        dock = self.sender().data()
        if dock == "attribute":
            self.attributes.setVisible(self.attributes.isHidden())
        elif dock == "structure":
            self.structure.setVisible(self.structure.isHidden())
        elif dock == "main":
            self.center.setVisible(self.center.isHidden())
        elif dock == "property":
            self.properties.setVisible(self.properties.isHidden())
        elif dock == "output":
            self.output.setVisible(self.output.isHidden())
        else:
            print(f"wtf{dock}")

    def checkVisible(self, is_visible):
        """
        通过判断dock的显示与隐藏来改变菜单栏view的图标
        :param is_visible:
        :return:
        """
        dock = self.sender().windowTitle()
        if is_visible:
            icon = QIcon(Func.getImage("dock_visible.png"))
        else:
            icon = QIcon("")
        if dock == "Attributes":
            self.attribute_action.setIcon(icon)
        elif dock == "Structure":
            self.structure_action.setIcon(icon)
        elif dock == "Main":
            self.main_action.setIcon(icon)
        elif dock == "Properties":
            self.property_action.setIcon(icon)
        elif dock == "Output":
            self.output_action.setIcon(icon)
        else:
            print(f"wtf{dock}")

    def showDevices(self, device_type):
        """
        显示设备选择框
        :param device_type:
        :return:
        """
        if device_type:
            self.output_devices.show()
        else:
            self.input_devices.show()

    @staticmethod
    def changeDevices(device_type, devices):
        # output device
        if device_type:
            DurationPage.OUTPUT_DEVICES = devices
        else:
            DurationPage.INPUT_DEVICES = devices

    def contextMenuEvent(self, QContextMenuEvent):
        super().contextMenuEvent(QContextMenuEvent)

    def compile(self):
        # check saved or not, if not saved, user should  save first.
        if not Info.FILE_NAME:
            if not self.getFileName():
                QMessageBox.information(self, "Warning", "File must be saved before compiling.", QMessageBox.Ok)
                return

        # get save path
        compile_file_name = ".".join(Info.FILE_NAME.split('.')[:-1]) + ".m"
        # open file
        with open(compile_file_name, "w") as f:
            # get output devices, such as global output devices.
            # you can get each widget's device you selected
            output_devices = Info.OUTPUT_DEVICE_INFO
            # print data to file
            count = 1
            for output_device in output_devices:
                # get output device index
                output_device_index = output_device.split('.')[-1]
                # print and set para: file = f
                print(f"outputDevs({count}).port = '{output_devices[output_device]['Device Port']}';", file=f)
                print(f"outputDevs({count}).name = '{output_devices[output_device]['Device Name']}';", file=f)
                print(f"outputDevs({count}).type = '{output_devices[output_device]['Device Type']}';", file=f)
                print(f"outputDevs({count}).index = '{output_device_index}';", file=f)
                # counter
                count += 1
        Func.log(f"Compile successful!\n{compile_file_name}")
        # except Exception as e:
        #     print(f"compile error {e}")

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

    def about(self):
        QMessageBox.about(self, "About PsyDemo", "NOTHING")

    def checkUpdate(self):
        self.bar = LoadingTip()
        self.bar.setWindowModality(Qt.ApplicationModal)
        self.bar.show()
        self.t = QTimer()
        self.t.timeout.connect(self.re)
        self.t.start(100)

    def re(self):
        self.bar.changeValue()
        self.bar.update()
        if self.bar.bar.value == 100:
            self.t.stop()
            self.bar.close()

    def closeEvent(self, QCloseEvent):
        """
        关闭时的动画效果
        :param QCloseEvent:
        :return:
        """
        try:
            self.animation.setDuration(1000)
            self.animation.setStartValue(0)
            self.animation.setEndValue(1)
            self.animation.start()
            self.close()
        except:
            self.close()
