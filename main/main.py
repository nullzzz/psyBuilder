from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QTextEdit

from Attributes.main import Attributes
from Center.main import Center
from Properties.main import Properties
from Structure.main import Structure


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        # set UI
        self.setWindowTitle("PsyDemo")

        # 设置dock widgets
        # attributes及向其中添加数据
        self.attributes = Attributes(self)

        # other
        self.structure = Structure()
        self.structure.setWindowTitle("Structure")
        self.properties = Properties()
        self.properties.setWindowTitle("properties")

        self.center = Center()
        self.center.setWindowTitle("Main")
        self.output = QDockWidget()
        self.output.setWindowTitle("Output")

        self.output.setWidget(QTextEdit())

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
        # 将timeline中icon的变更与structure相连
        self.linkTimelineSignals('Timeline.10001')
        # structure中信号
        self.structure.nodeDoubleClick.connect(self.center.icon_tabs.openTab)
        self.structure.timelineAdd.connect(self.linkTimelineSignals)
        self.structure.structure_tree.itemDelete.connect(self.center.icon_tabs.deleteTab)
        self.structure.structure_tree.itemDelete.connect(self.center.icon_tabs.deleteIcon)
        self.structure.structure_tree.timelineDelete.connect(self.center.icon_tabs.deleteTimeline)
        self.structure.propertiesShow.connect(self.center.icon_tabs.getWidgetProperties)


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