from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication

from app.func import Func
from app.info import Info
from lib import WaitDialog
from .attributes import Attributes
from .center import Center
from .output import Output
from .properties import Properties
from .structure import Structure


class Psy(QMainWindow):
    """

    """

    def __init__(self):
        super(Psy, self).__init__()
        # set its title
        self.setWindowTitle("Psy Builder")
        # set its wait thread
        self.wait_dialog = WaitDialog()
        # init menu bar

        # init dock widget
        self.initDockWidget()
        #
        self.linkSignals()

    def initMenuBar(self) -> None:
        """
        init its menu bar, including file, view, devices, building and help
        @return:
        """

    def initDockWidget(self) -> None:
        """
        init all dock widget, including structure, properties, center, output and center
        @return:
        """
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
        self.setCentralWidget(self.center)
        # output
        self.output = Output()
        self.output.setWindowTitle("Output")
        # its initial layout
        self.addDockWidget(Qt.LeftDockWidgetArea, self.structure)

        self.splitDockWidget(self.structure, self.properties, Qt.Vertical)
        self.splitDockWidget(self.properties, self.output, Qt.Horizontal)
        self.splitDockWidget(self.output, self.attributes, Qt.Horizontal)

        self.addDockWidget(Qt.RightDockWidgetArea, self.attributes)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.output)

    def initInitialTimeline(self):
        """
        init initial timeline for other items
        @return:
        """
        widget_id = Func.generateWidgetId(Info.Timeline)
        widget_name = Func.generateWidgetName(Info.Timeline)
        # create timeline widget
        Func.createWidget(widget_id, widget_name)
        # add node in structure
        self.structure.addNode(-1, widget_id, widget_name, Info.AddNode)
        # set timeline as a tab
        self.center.openTab(widget_id)

    def linkSignals(self):
        """
        link signals between dock widgets
        @return:
        """
        # todo link dock widgets' signals
        self.center.currentWidgetChanged.connect(self.dealCurrentTabChanged)

    def linkWidgetSignals(self, widget_type: int, widget):
        """
        link widget's signals according to its widget type.
        @param widget_type:
        @param widget:
        @return:
        """
        # todo link widget's signals
        # common
        # from lib import TabItemWidget
        # widget: TabItemWidget
        widget.waitStart.connect(self.startWait)
        widget.waitEnd.connect(self.endWait)
        # timeline
        if widget_type == Info.Timeline:
            widget.itemNameChanged.connect(self.dealItemNameChanged)
            widget.itemClicked.connect(self.dealItemClicked)
            widget.itemDoubleClicked.connect(self.dealItemDoubleClicked)
            widget.itemMoved.connect(self.dealItemMoved)

    def startWait(self):
        """
        show wait dialog
        @return:
        """
        self.wait_dialog.show()
        QApplication.processEvents()

    def endWait(self):
        """
        hide wait dialog
        @return:
        """
        self.wait_dialog.hide()
        QApplication.processEvents()

    def dealItemNameChanged(self, origin_widget: int, widget_id: int, widget_name: str):
        """

        @param origin_widget:
        @param widget_id:
        @param widget_name:
        @return:
        """
        print("item name change", origin_widget, widget_id, widget_name)
        # change widget's name
        Func.changeWidgetName(widget_id, widget_name)
        # change tab's name
        self.center.changeTabName(widget_id, widget_name)
        if origin_widget == Info.TimelineSignal:
            # if signal from timeline
            self.structure.changeNodeName(widget_id, widget_name)
        elif origin_widget == Info.StructureSignal:
            # if signal from timeline
            self.center.changeItemNameInTimeline(widget_id, widget_name)

    def dealItemClicked(self, widget_id: int):
        """

        @param origin_widget:
        @param widget_id:
        @return:
        """
        print("item click", widget_id)
        # change attributes and properties
        self.attributes.showAttributes(widget_id)
        self.properties.showProperties(widget_id)

    def dealItemDoubleClicked(self, widget_id: int):
        """

        @param widget_id:
        @return:
        """
        print("item double click", widget_id)
        # open tab
        self.center.openTab(widget_id)

    def dealItemMoved(self, widget_id: int, origin_index: int, new_index: int):
        """

        @param widget_id:
        @param origin_index:
        @param new_index:
        @return:
        """
        print("item move", widget_id, origin_index, new_index)
        # move node in structure
        self.structure.moveNode(widget_id, origin_index, new_index)

    def dealCurrentTabChanged(self, widget_id: int):
        """

        @param widget_id:
        @return:
        """
        print("current tab change", widget_id)
        if widget_id == -1:
            # it means that user close all tab and we should clear attributes and properties
            # change attributes and properties
            self.attributes.clearAttributes()
            self.properties.clearProperties()
        else:
            # change attributes and properties
            self.attributes.showAttributes(widget_id)
            self.properties.showProperties(widget_id)
