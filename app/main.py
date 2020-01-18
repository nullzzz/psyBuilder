from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication

from app.center.events import Cycle
from app.center.timeline import Timeline
from app.func import Func
from app.info import Info
from app.kernel import Kernel
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
        self.createWidget(widget_id, widget_name)
        # add node in structure
        self.structure.addNode(-1, widget_id, widget_name, 0)
        # set timeline as a tab
        self.center.openTab(widget_id)

    def linkSignals(self):
        """
        link signals between dock widgets
        @return:
        """
        # todo link dock widgets' signals
        self.center.currentWidgetChanged.connect(self.dealCurrentTabChanged)
        self.structure.itemDoubleClicked.connect(self.dealItemDoubleClicked)
        self.structure.itemDeleted.connect(self.dealItemDeleted)

    def createWidget(self, widget_id: int, widget_name: str) -> None:
        """
        create widget according to its widget id and set its name
        @param widget_id:
        @param widget_name: its name
        @return:
        """
        widget_type = widget_id // Info.MaxWidgetCount
        # todo add other items into this function
        widget = None
        if widget_type == Info.Timeline:
            widget = Timeline(widget_id, widget_name)
        elif widget_type == Info.Cycle:
            widget = Cycle(widget_id, widget_name)
        else:
            # if fail to create widget, exit.
            exit()
        # change data set in Kernel
        Kernel.Widgets[widget_id] = widget
        Kernel.Names[widget_name] = [widget_id]
        # link necessary signals
        self.linkWidgetSignals(widget_type, widget)

    def cloneWidget(self, origin_widget_id, new_widget_id, widget_name):
        """
        clone widget
        @param origin_widget_id:
        @param new_widget_id:
        @param widget_name:
        @return:
        """

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
            widget.itemAdded.connect(self.dealItemAdded)
            widget.itemDeleted.connect(self.dealItemDeleted)

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

    def dealItemAdded(self, parent_widget_id: int, widget_id: int, widget_name: str, index: int, add_type: int):
        """

        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @param index:
        @param add_type:
        @return:
        """
        print("item added:", parent_widget_id, widget_id, widget_name, index, add_type)
        # start wait
        self.startWait()
        # do job
        if add_type == Info.AddItem:
            # create widget firstly
            self.createWidget(widget_id, widget_name)
            # todo add node in structure
            self.structure.addNode(parent_widget_id, widget_id, widget_name, index)
        elif add_type == Info.CopyItem:
            # clone widget firstly
            pass
        elif add_type == Info.ReferItem:
            pass
        # end wait
        self.endWait()

    def dealItemDeleted(self, origin_widget: int, widget_id: int):
        """

        @param widget_id:
        @return:
        """
        print("item deleted:", origin_widget, widget_id)

    def dealItemNameChanged(self, origin_widget: int, parent_widget_id: int, widget_id: int, widget_name: str):
        """
        when item's name changed, we deal some job.
        @param origin_widget: where is the signal from, including timeline and structure
        @param parent_widget_id: item's parent
        @param widget_id:
        @param widget_name: new name
        @return:
        """
        print("item name change:", origin_widget, parent_widget_id, widget_id, widget_name)
        # change widget's name
        widget = Kernel.Widgets[widget_id]
        widget.widget_name = widget_name
        # change tab's name
        self.center.changeTabName(widget_id, widget_name)
        # change item's and nodes' name
        if origin_widget == Info.StructureSignal:
            # we need change item's name if signal comes from structure
            timeline = Kernel.Widgets[parent_widget_id]
            timeline.renameItem()

    def dealItemClicked(self, widget_id: int):
        """

        @param origin_widget:
        @param widget_id:
        @return:
        """
        print("item click:", widget_id)
        # change attributes and properties
        self.attributes.showAttributes(widget_id)
        self.properties.showProperties(widget_id)

    def dealItemDoubleClicked(self, widget_id: int):
        """

        @param widget_id:
        @return:
        """
        print("item double click:", widget_id)
        # open tab
        self.center.openTab(widget_id)

    def dealItemMoved(self, widget_id: int, origin_index: int, new_index: int):
        """

        @param widget_id:
        @param origin_index:
        @param new_index:
        @return:
        """
        print("item move:", widget_id, origin_index, new_index)
        # todo move node in structure
        self.structure.moveNode(widget_id, origin_index, new_index)

    def dealCurrentTabChanged(self, widget_id: int):
        """

        @param widget_id:
        @return:
        """
        print("current tab change:", widget_id)
        if widget_id == -1:
            # it means that user close all tab and we should clear attributes and properties
            # change attributes and properties
            self.attributes.clearAttributes()
            self.properties.clearProperties()
        else:
            # change attributes and properties
            self.attributes.showAttributes(widget_id)
            self.properties.showProperties(widget_id)
