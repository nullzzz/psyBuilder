import json

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication

from attributes.main import Attributes
from center.main import Center
from main.globalDevices import GlobalDevice
from output.main import Output
from properties.main import Properties
from structure.main import Structure


class MainWindow(QMainWindow):
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
        open_file_action = QAction("&Open", self)
        save_file_action = QAction("&Save", self)
        save_file_action.triggered.connect(self.getData)
        exit_action = QAction("Exit", self)
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

        view_menu.addAction(attribute_action)
        view_menu.addAction(structure_action)
        view_menu.addAction(main_action)
        view_menu.addAction(property_action)
        view_menu.addAction(output_action)
        view_menu.addSeparator()
        view_menu.addAction(default_action)

        # devices menu
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
        # icon tabs
        self.center.icon_tabs.cycleAdd.connect(self.linkCycleSignals)
        self.center.icon_tabs.propertiesShow.connect(self.properties.showProperties)
        self.center.icon_tabs.attributesShow.connect(self.attributes.showAttributes)
        # 将timeline中icon的变更与structure相连
        self.linkTimelineSignals('Timeline.10001')
        # structure中信号
        self.structure.nodeDoubleClick.connect(self.center.icon_tabs.openTab)
        self.structure.timelineAdd.connect(self.linkTimelineSignals)
        self.structure.structure_tree.itemDelete.connect(self.center.icon_tabs.deleteTab)
        self.structure.structure_tree.itemDelete.connect(self.center.icon_tabs.deleteIcon)
        self.structure.structure_tree.timelineDelete.connect(self.center.icon_tabs.deleteTimeline)
        self.structure.propertiesShow.connect(self.center.icon_tabs.getWidgetProperties)
        self.structure.nodeNameChange.connect(self.center.icon_tabs.changeTabName)

    def linkTimelineSignals(self, value):
        try:
            try:
                self.center.icon_tabs.value_widget[value].iconAdd.disconnect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].iconAdd.connect(self.structure.addNode)
            except Exception:
                self.center.icon_tabs.value_widget[value].iconAdd.connect(self.structure.addNode)
                self.center.icon_tabs.value_widget[value].iconRemove.connect(self.structure.removeNode)
                self.center.icon_tabs.value_widget[value].iconMove.connect(self.structure.moveNode)
                self.center.icon_tabs.value_widget[value].icon_area.icon_table.iconNameChange.connect(
                    self.structure.changeNodeName)
                self.structure.nodeNameChange.connect(self.center.icon_tabs.value_widget[value].changeIconName)
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

    def getData(self):
        node_value = self.structure.getNodeValue()
        self.output.text_area.setText(
            "Only show structure data, attributes or properties will be show in next version.\n" + json.dumps(
                node_value))
        # reset timer
        self.auto_save.start(MainWindow.AUTO_SAVE_TIME)

    def showDevices(self, device_type):
        self.devices = GlobalDevice(device_type)
        self.devices.setWindowModality(Qt.ApplicationModal)
        self.devices.show()
