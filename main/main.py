from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QTextEdit, QAction, QApplication

from attributes.main import Attributes
from center.main import Center
from properties.main import Properties
from structure.main import Structure
from output.main import Output

import json


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
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
        file_menu.addAction(exit_action)

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
