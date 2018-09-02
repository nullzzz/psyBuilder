import json
import sys
import os

from PyQt5.QtCore import Qt, QTimer, QSettings
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication

from attributes.main import Attributes
from center.iconTabs.events.durationPage import DurationPage
from center.main import Center
from main.globalDevices import GlobalDevice
from output.main import Output
from properties.main import Properties
from structure.main import Structure


class MainWindow(QMainWindow):
    # 每隔五分钟自动保存
    AUTO_SAVE_TIME = 300000

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # auto save
        self.auto_save = QTimer(self)
        self.auto_save.start(MainWindow.AUTO_SAVE_TIME)
        self.auto_save.timeout.connect(self.getData)
        # set UI
        self.setWindowTitle("PsyDemo")
        # menuBar
        menu_bar = self.menuBar()
        # file menu
        file_menu = menu_bar.addMenu("&File")

        new_file_action = QAction("&New", self)
        new_file_action.triggered.connect(self.newFile)
        open_file_action = QAction("&Open", self)
        save_file_action = QAction("&Save", self)
        save_file_action.triggered.connect(self.getData)
        exit_action = QAction("&Exit", self)
        exit_action.triggered.connect(QApplication.exit)

        file_menu.addAction(new_file_action)
        file_menu.addAction(open_file_action)
        file_menu.addAction(save_file_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        # view menu
        view_menu = menu_bar.addMenu("&View")

        attribute_action = QAction("&Attribute", self)
        structure_action = QAction("&Structure", self)
        main_action = QAction("&Main", self)
        property_action = QAction("&Property", self)
        output_action = QAction("&Output", self)
        default_action = QAction("&Default", self)
        default_action.triggered.connect(self.resetView)

        view_menu.addAction(attribute_action)
        view_menu.addAction(structure_action)
        view_menu.addAction(main_action)
        view_menu.addAction(property_action)
        view_menu.addAction(output_action)
        view_menu.addSeparator()
        view_menu.addAction(default_action)

        # devices menu
        self.input_devices = GlobalDevice(device_type=0)
        self.input_devices.setWindowModality(Qt.ApplicationModal)
        self.output_devices = GlobalDevice(device_type=1)
        self.output_devices.setWindowModality(Qt.ApplicationModal)
        devices_menu = menu_bar.addMenu("&Devices")

        output_devices_action = QAction("&Output Devices", self)
        input_devices_action = QAction("&Input Devices", self)
        output_devices_action.triggered.connect(lambda: self.showDevices(1))
        input_devices_action.triggered.connect(lambda: self.showDevices(0))

        devices_menu.addAction(output_devices_action)
        devices_menu.addAction(input_devices_action)

        # help menu
        help_menu = menu_bar.addMenu("&Help")
        about_action = QAction("&About", self)

        help_menu.addAction(about_action)

        # 设置dock widgets
        # attributes
        self.attributes = Attributes(self)
        self.attributes.setWindowTitle("Attributes")
        # structure
        self.structure = Structure()
        self.structure.setWindowTitle("Structure")
        # properties
        self.properties = Properties()
        self.properties.setWindowTitle("Properties")
        # center
        self.center = Center()
        self.center.setWindowTitle("Main")
        # output
        self.output = Output()
        self.output.setWindowTitle("Output")

        # 添加dock widget
        self.addDockWidget(Qt.LeftDockWidgetArea, self.structure)
        self.splitDockWidget(self.structure, self.center, Qt.Horizontal)
        self.splitDockWidget(self.center, self.attributes, Qt.Horizontal)
        self.splitDockWidget(self.structure, self.properties, Qt.Vertical)
        self.splitDockWidget(self.center, self.output, Qt.Vertical)

        # 连接信号
        self.linkSignals()

    def linkSignals(self):
        # devices
        self.input_devices.deviceSelect.connect(self.changeDevices)
        self.output_devices.deviceSelect.connect(self.changeDevices)
        # icon tabs
        self.center.icon_tabs.cycleAdd.connect(self.linkCycleSignals)
        self.center.icon_tabs.ifBranchAdd.connect(self.linkIFBranchSignals)
        self.center.icon_tabs.propertiesShow.connect(self.properties.showProperties)
        self.center.icon_tabs.attributesShow.connect(self.attributes.showAttributes)
        # 将timeline中icon的变更与structure相连
        self.linkTimelineSignals('Timeline.10001')
        # structure中信号
        self.structure.nodeDoubleClick.connect(self.center.icon_tabs.openTab)
        self.structure.timelineAdd.connect(self.linkTimelineSignals)
        self.structure.propertiesShow.connect(self.center.icon_tabs.getWidgetProperties)
        self.structure.structure_tree.itemDelete.connect(self.center.icon_tabs.deleteTab)
        self.structure.structure_tree.itemDelete.connect(self.center.icon_tabs.deleteIcon)
        self.structure.structure_tree.timelineDelete.connect(self.center.icon_tabs.deleteTimeline)
        self.structure.structure_tree.itemInIfBranchDelete.connect(self.center.icon_tabs.deleteItemInIfBranch)
        self.structure.iconNameChange.connect(self.center.icon_tabs.changeTabName)
        self.structure.iconNameChange.connect(self.center.icon_tabs.changeIconName)
        self.structure.timelineNameChange.connect(self.center.icon_tabs.changeTabName)
        self.structure.timelineNameChange.connect(self.center.icon_tabs.changeTimelineName)
        self.structure.itemInIfBranchNameChange.connect(self.center.icon_tabs.changeTabName)
        self.structure.itemInIfBranchNameChange.connect(self.center.icon_tabs.changeItemInIfBranchName)

    def linkTimelineSignals(self, value):
        try:
            try:
                self.center.icon_tabs.value_widget[value].iconAdd.disconnect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].iconAdd.connect(self.structure.addNode)
            except Exception:
                self.center.icon_tabs.value_widget[value].iconAdd.connect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].iconRemove.connect(self.structure.removeNode)
                self.center.icon_tabs.value_widget[value].iconMove.connect(self.structure.moveNode)
                self.center.icon_tabs.value_widget[value].iconNameChange.connect(self.structure.changeNodeName)
        except Exception:
            print("error happens in link timeline signals to structure. [main/main.py]")

    def linkCycleSignals(self, value):
        try:
            try:
                self.center.icon_tabs.value_widget[value].timelineAdd.disconnect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].timelineAdd.connect(self.structure.addNode)
            except Exception:
                self.center.icon_tabs.value_widget[value].timelineAdd.connect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].timelineNameChange.connect(self.structure.changeNodeName)
        except Exception:
            print("error happens in link cycle signals to structure. [main/main.py]")

    def linkIFBranchSignals(self, value):
        try:
            try:
                self.center.icon_tabs.value_widget[value].nodeChange.disconnect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].nodeChange.connect(self.structure.addNode)
            except Exception:
                self.center.icon_tabs.value_widget[value].nodeChange.connect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].nodeChange.connect(
                    self.center.icon_tabs.createTabForItemInIfBranch)
                self.center.icon_tabs.value_widget[value].nodeNameChange.connect(self.structure.changeNodeName)
                self.center.icon_tabs.value_widget[value].nodeDelete.connect(self.structure.removeNode)
        except Exception:
            print("error happens in link cycle signals to structure. [main/main.py]")

    def newFile(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def getData(self):
        node_value = self.structure.getNodeValue()
        self.output.text_area.setText(
            "Only show structure data, attributes or properties will be show in next version.\n" + json.dumps(
                node_value))
        # reset timer
        self.auto_save.start(MainWindow.AUTO_SAVE_TIME)

    def resetView(self):
        try:
            print("I can't finish it, AHHh.")
        except Exception:
            print("error happens in reset view. [main/main.py]")

    def showDevices(self, device_type):
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
