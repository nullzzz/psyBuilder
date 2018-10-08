import json
import os
import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QMessageBox

from attributes.main import Attributes
from center.iconTabs.events.durationPage import DurationPage
from center.main import Center
from main.deviceSelection.globalDevices import GlobalDevice
from main.deviceSelection.progressBar import LoadingTip
from output.main import Output
from properties.main import Properties
from structure.main import Structure


class MainWindow(QMainWindow):
    # 每隔五分钟自动保存
    AUTO_SAVE_TIME = 3000000

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
        self.attribute_action = QAction("&Attribute", self)
        self.structure_action = QAction("&Structure", self)
        self.main_action = QAction("&Main", self)
        self.property_action = QAction("&Property", self)
        self.output_action = QAction("&Output", self)
        self.default_action = QAction("&Default", self)
        # self.attribute_action.setCheckable(True)
        # self.attribute_action.setChecked(True)
        self.attribute_action.setData("attribute")
        # self.structure_action.setCheckable(True)
        # self.structure_action.setChecked(True)
        self.structure_action.setData("structure")
        # self.main_action.setCheckable(True)
        # self.main_action.setChecked(True)
        # self.main_action.setData("main")
        # self.output_action.setCheckable(True)
        # self.output_action.setChecked(True)
        self.output_action.setData("output")
        # self.property_action.setCheckable(True)
        # self.property_action.setChecked(True)
        self.property_action.setData("property")

        self.attribute_action.triggered.connect(self.setDockView)
        self.structure_action.triggered.connect(self.setDockView)
        self.main_action.triggered.connect(self.setDockView)
        self.output_action.triggered.connect(self.setDockView)
        self.property_action.triggered.connect(self.setDockView)

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
        self.output_devices = GlobalDevice(io_type=1)
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
        about_Qt_action = QAction("&About Qt", self)
        check_for_update = QAction("&Check for updates", self)

        about_action.triggered.connect(self.about)
        about_Qt_action.triggered.connect(QApplication.instance().aboutQt)
        check_for_update.triggered.connect(self.checkUpdate)

        help_menu.addAction(about_action)
        help_menu.addAction(about_Qt_action)
        help_menu.addAction(check_for_update)

        # 设置dock widgets
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

        # 连接信号
        self.linkSignals()

    def linkSignals(self):
        # devices
        self.input_devices.deviceSelect.connect(self.changeDevices)
        self.output_devices.deviceSelect.connect(self.changeDevices)
        # icon tabs
        self.center.icon_tabs.cycleAdd.connect(self.linkCycleSignals)
        self.center.icon_tabs.ifBranchAdd.connect(self.linkIFBranchSignals)
        self.center.icon_tabs.timelineAdd.connect(self.linkTimelineSignals)
        self.center.icon_tabs.switchBranchAdd.connect(self.linkSwitchBranchSignals)
        self.center.icon_tabs.propertiesShow.connect(self.properties.showProperties)
        # self.center.icon_tabs.attributesShow.connect(self.structure.showTimelineAttributes)
        self.center.icon_tabs.attributesShow.connect(self.attributes.showAttributes)
        self.center.icon_tabs.iconNodeCopy.connect(self.structure.copyNode)
        # 将timeline中icon的变更与structure相连
        self.linkTimelineSignals('Timeline.10001')
        # structure中信号
        self.structure.iconRemove.connect(self.center.icon_tabs.removeInWidget)
        self.structure.nodeDoubleClick.connect(self.center.icon_tabs.openTab)
        self.structure.timelineAdd.connect(self.linkTimelineSignals)
        self.structure.propertiesShow.connect(self.center.icon_tabs.getWidgetProperties)
        self.structure.structure_tree.itemDelete.connect(self.center.icon_tabs.deleteTab)
        self.structure.structure_tree.itemDelete.connect(self.center.icon_tabs.deleteIcon)
        self.structure.structure_tree.timelineDelete.connect(self.center.icon_tabs.deleteTimeline)
        self.structure.structure_tree.itemInIfBranchDelete.connect(self.center.icon_tabs.deleteItemInIfBranch)
        self.structure.structure_tree.itemInSwitchBranchDelete.connect(self.center.icon_tabs.deleteItemInSwitchBranch)
        self.structure.iconNameChange.connect(self.center.icon_tabs.changeTabName)
        self.structure.iconNameChange.connect(self.center.icon_tabs.changeIconName)
        self.structure.timelineNameChange.connect(self.center.icon_tabs.changeTabName)
        self.structure.timelineNameChange.connect(self.center.icon_tabs.changeTimelineName)
        self.structure.itemInIfBranchNameChange.connect(self.center.icon_tabs.changeTabName)
        self.structure.itemInIfBranchNameChange.connect(self.center.icon_tabs.changeItemInIfBranchName)
        self.structure.itemInSwitchBranchNameChange.connect(self.center.icon_tabs.changeTabName)
        self.structure.itemInSwitchBranchNameChange.connect(self.center.icon_tabs.changeItemInSwitchBranchName)
        self.structure.nodeWidgetMerge.connect(self.center.icon_tabs.mergeValueWidget)
        self.structure.nodeWidgetSplit.connect(self.center.icon_tabs.splitValueWidget)
        self.structure.nodeWidgetCopy.connect(self.center.icon_tabs.copyWidget)
        self.structure.timelineAttributesShow.connect(self.attributes.showAttributes)

    def linkTimelineSignals(self, value):
        try:
            try:
                self.center.icon_tabs.value_widget[value].iconAdd.disconnect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].iconAdd.connect(self.structure.addNode)
            except Exception:
                self.center.icon_tabs.value_widget[value].iconAdd.connect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].iconRemove.connect(self.structure.removeNode)
                self.center.icon_tabs.value_widget[value].iconMove.connect(self.structure.moveNode)
                self.center.icon_tabs.value_widget[value].iconChange.connect(self.structure.changeNode)
                self.center.icon_tabs.value_widget[value].iconNameChange.connect(self.structure.changeNodeName)
                self.center.icon_tabs.value_widget[value].icon_area.icon_table.iconWidgetMerge.connect(
                    self.structure.copyNode)
        except Exception:
            print("error happens in link timeline signals. [main/main.py]")

    def linkCycleSignals(self, value):
        try:
            try:
                self.center.icon_tabs.value_widget[value].timelineAdd.disconnect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].timelineAdd.connect(self.structure.addNode)
            except Exception:
                self.center.icon_tabs.value_widget[value].timelineAdd.connect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].timelineNameChange.connect(self.structure.changeNodeName)
                self.center.icon_tabs.value_widget[value].timelineWidgetMerge.connect(self.structure.copyNode)
        except Exception:
            print("error happens in link cycle signals. [main/main.py]")

    def linkIFBranchSignals(self, value):
        try:
            try:
                self.center.icon_tabs.value_widget[value].nodeAdd.disconnect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].nodeAdd.connect(self.structure.addNode)
            except Exception:
                self.center.icon_tabs.value_widget[value].nodeAdd.connect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].nodeNameChange.connect(self.structure.changeNodeName)
                self.center.icon_tabs.value_widget[value].nodeDelete.connect(self.structure.removeNode)
        except Exception:
            print("error happens in link if branch signals. [main/main.py]")

    def linkSwitchBranchSignals(self, value):
        try:
            try:
                self.center.icon_tabs.value_widget[value].caseAdd.disconnect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].caseAdd.connect(self.structure.addNode)
            except Exception:
                self.center.icon_tabs.value_widget[value].caseAdd.connect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].caseNameChange.connect(self.structure.changeNodeName)
                self.center.icon_tabs.value_widget[value].caseDelete.connect(self.structure.removeNode)
        except Exception:
            print("error happens in link if branch signals. [main/main.py]")

    def newFile(self):
        python = sys.executable
        os.execl(python, python, *sys.argv)

    def getData(self):
        try:
            node_value = self.structure.getNodeValue()
            self.output.text_area.setText(
                "Only show structure data, attributes or properties will be show in next version.\n" + json.dumps(
                    node_value))
            # reset timer
            self.auto_save.start(MainWindow.AUTO_SAVE_TIME)
        except Exception as e:
            print(f"error {e} happens in get data and reset timer. [main/main.py]")

    # 恢复默认布局
    def resetView(self):
        self.restoreState(self.default_dock_widget_layout)

    # 单个dock的显示与隐藏
    def setDockView(self, checked):
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

    # 通过判断dock的显示与隐藏来改变菜单栏view的图标
    def checkVisible(self, is_visible):
        dock = self.sender().windowTitle()
        if is_visible:
            icon = QIcon("image/dock_visible.png")
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

    # 显示设备选择框
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

    def about(self):
        QMessageBox.about(self, "About PsyDemo", "This is a bad project")

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
