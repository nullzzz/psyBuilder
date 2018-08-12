from PyQt5.QtWidgets import QMainWindow, QDockWidget, QTextEdit
from PyQt5.QtCore import Qt
from Attributes.Attributes import Attributes
from Center.Center import Center
from Structure.Structure import Structure
from Properties.Properties import Properties


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
        self.properties = Properties()
        self.properties.setWindowTitle("Properties")

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
        self.linkSignal()

    def linkSignal(self):
        # TimeLine
        self.center.eventTabs.timeLine.eventAdd.connect(self.structure.addNode)
        self.center.eventTabs.timeLine.eventArea.eventTable.eventNameChanged.connect(self.structure.changeEventName)
        # 接受structure的信号到eventTabs来打开新tab
        self.structure.sendTabToEventTabs.connect(self.center.eventTabs.openTab)
        # 接受eventTable的信号
        self.center.eventTabs.timeLine.eventRemove.connect(self.structure.removeNode)
        self.center.eventTabs.timeLine.eventMove.connect(self.structure.moveNode)
        #
        self.center.eventTabs.properties.connect(self.properties.setProperties)
        # 从structure得value得properties
        self.structure.getProperties.connect(self.center.eventTabs.getProperties)
        # 新增cycle, 要对于他的timelineAdded信号串接到structure
        self.center.eventTabs.cycleAdded.connect(self.cycleAdded)
        # 对于cycle中的新增timeLine, 要对其进行相应信号串接, 其打开只能通过structure
        self.structure.timeLineAdd.connect(self.linkTimeLineSignal)
        self.structure.timeLineAdd.connect(self.center.eventTabs.linkNewSignal)
        # structure中item删除关联eventTabs中的tab删除
        self.structure.structureTree.itemDeleted.connect(self.center.eventTabs.deleteTab)
        # 关联timeLine中的event删除
        self.structure.structureTree.itemDeleted.connect(self.center.eventTabs.deleteEvent)
        # 删除cycle中timeLine
        self.structure.structureTree.timeLineDeleted.connect(self.center.eventTabs.deleteTimeLineInCycle)

    # 当有新的cycle被打开时对其两个信号进行串接
    def cycleAdded(self, value):
        try:
            self.center.eventTabs.tabs[value].timelineAdded.disconnect(self.structure.addNode)
            self.center.eventTabs.tabs[value].timelineAdded.connect(self.structure.addNode)
        except Exception:
            # 新增timeLine
            self.center.eventTabs.tabs[value].timelineAdded.connect(self.structure.addNode)
            # 表格中timeLine name修改
            self.center.eventTabs.tabs[value].nameChanged.connect(self.structure.changeEventName)

    def linkTimeLineSignal(self, value):
        try:
            self.center.eventTabs.tabs[value].eventAdd.disconnect(self.structure.addNode)
            self.center.eventTabs.tabs[value].eventAdd.connect(self.structure.addNode)
        except Exception:
            self.center.eventTabs.tabs[value].eventAdd.connect(self.structure.addNode)
            self.center.eventTabs.tabs[value].eventArea.eventTable.eventNameChanged.connect(
                self.structure.changeEventName)
            self.center.eventTabs.tabs[value].eventRemove.connect(self.structure.removeNode)
            self.center.eventTabs.tabs[value].eventMove.connect(self.structure.moveNode)