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
        self.initMenuBar()
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
        widget_type = Func.getWidgetType(widget_id)
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

    def copyWidget(self, origin_widget_id, new_widget_id, new_widget_name):
        """
        copy widget
        @param origin_widget_id:
        @param new_widget_id:
        @param new_widget_name:
        @return:
        """
        new_widget = Kernel.Widgets[origin_widget_id].copy(new_widget_id, new_widget_name)
        Kernel.Widgets[new_widget_id] = new_widget

    def referWidget(self, origin_widget_id: int, new_widget_id: int = -1) -> int:
        """
        refer widget
        @param origin_widget_id: origin widget's widget id
        @return: new widget id
        """
        # generate new widget id
        widget_type = Func.getWidgetType(origin_widget_id)
        widget_id = new_widget_id
        if widget_id == -1:
            widget_id = Func.generateWidgetId(widget_type)
        # refer widget by mapping widget id to same widget
        Kernel.Widgets[widget_id] = Kernel.Widgets[origin_widget_id]
        return widget_id

    def linkWidgetSignals(self, widget_type: int, widget):
        """
        link widget's signals according to its widget type.
        @param widget_type:
        @param widget:
        @return:
        """
        # todo link widget's signals
        # common
        widget.propertiesChanged.connect(self.dealPropertiesChanged)
        widget.waitStart.connect(self.startWait)
        widget.waitEnd.connect(self.endWait)
        # unique
        if widget_type == Info.Timeline:
            # timeline
            widget.itemNameChanged.connect(self.dealItemNameChanged)
            widget.itemClicked.connect(self.dealItemClicked)
            widget.itemDoubleClicked.connect(self.dealItemDoubleClicked)
            widget.itemMoved.connect(self.dealItemMoved)
            widget.itemAdded.connect(self.dealItemAdded)
            widget.itemCopied.connect(self.dealItemCopied)
            widget.itemReferenced.connect(self.dealItemReferenced)
            widget.itemDeleted.connect(self.dealItemDeleted)
        elif widget_type == Info.Cycle:
            # cycle
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
        self.wait_dialog.close()
        QApplication.processEvents()

    def dealPropertiesChanged(self, widget_id: int):
        """
        when properties changed, refresh properties window.
        @param widget_id:
        @return:
        """
        self.properties.showProperties(widget_id)

    def dealItemAdded(self, parent_widget_id: int, widget_id: int, widget_name: str, index: int):
        """

        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @param index:
        @param add_type:
        @return:
        """
        print("item added:", parent_widget_id, widget_id, widget_name, index)
        # start wait
        self.startWait()
        # do job
        # create widget firstly
        self.createWidget(widget_id, widget_name)
        # we should consider a lot of things here because of reference.
        # we also need add node in those reference parents
        # add node in origin parent node
        self.structure.addNode(parent_widget_id, widget_id, widget_name, index)
        # add node in refer parent node
        refer_parent_widget_ids = Func.getWidgetReference(parent_widget_id)
        for refer_parent_widget_id in refer_parent_widget_ids:
            # we need exclude origin parent widget id
            if refer_parent_widget_id != parent_widget_id:
                # refer widget
                refer_widget_id = self.referWidget(widget_id)
                # add refer node in refer parent
                self.structure.addNode(refer_parent_widget_id, refer_widget_id, widget_name, index)
        # end wait
        self.endWait()

    def dealItemCopied(self, parent_widget_id: int, origin_widget_id: int, new_widget_id: int, new_widget_name: str,
                       index: int):
        """

        @param parent_widget_id:
        @param origin_widget_id:
        @param new_widget_id:
        @param new_widget_name:
        @param index:
        @return:
        """
        print("item copied: ", parent_widget_id, origin_widget_id, new_widget_id, new_widget_name, index)
        # start wait
        self.startWait()
        # do job
        # copy widget firstly
        self.copyWidget(origin_widget_id, new_widget_id, new_widget_name)
        # we should consider a lot of things here because of reference.
        # we also need add node in those reference parents
        # add node in origin parent node
        self.structure.addNode(parent_widget_id, new_widget_id, new_widget_name, index)
        # add node in refer parent node
        refer_parent_widget_ids = Func.getWidgetReference(parent_widget_id)
        for refer_parent_widget_id in refer_parent_widget_ids:
            # we need exclude origin parent widget id
            if refer_parent_widget_id != parent_widget_id:
                # refer widget
                refer_widget_id = self.referWidget(new_widget_id)
                # add refer node in refer parent
                self.structure.addNode(refer_parent_widget_id, refer_widget_id, new_widget_name, index)
        # end wait
        self.endWait()

    def dealItemReferenced(self, parent_widget_id: int, origin_widget_id: int, new_widget_id: int, index: int):
        """

        @param parent_widget_id:
        @param origin_widget_id:
        @param new_widget_id:
        @param index:
        @return:
        """
        print("item referenced: ", origin_widget_id, new_widget_id)
        # start wait
        self.startWait()
        # do job
        # copy widget firstly
        self.referWidget(origin_widget_id, new_widget_id)
        # we should consider a lot of things here because of reference.
        # we also need add node in those reference parents
        # add node in origin parent node
        widget_name = Func.getWidgetName(origin_widget_id)
        self.structure.addNode(parent_widget_id, new_widget_id, widget_name, index)
        # add node in refer parent node
        refer_parent_widget_ids = Func.getWidgetReference(parent_widget_id)
        for refer_parent_widget_id in refer_parent_widget_ids:
            # we need exclude origin parent widget id
            if refer_parent_widget_id != parent_widget_id:
                # refer widget
                refer_widget_id = self.referWidget(new_widget_id)
                # add refer node in refer parent
                self.structure.addNode(refer_parent_widget_id, refer_widget_id, widget_name, index)
        # end wait
        self.endWait()

    def dealItemDeleted(self, origin_widget: int, widget_id: int):
        """

        @param widget_id:
        @return:
        """
        print("item deleted:", origin_widget, widget_id)
        # close tab
        self.center.closeTab(widget_id)
        # delete node in structure (we need delete data in Kernel.Nodes and Kernel.Names) and item in timeline or timeline in cycle
        widget_name = Func.getWidgetName(widget_id)
        if origin_widget == Info.StructureSignal:
            # delete item in timeline or timeline in cycle
            if Func.isWidgetType(widget_id, Info.Timeline):
                # delete timeline in cycle
                cycle: Cycle = Kernel.Widgets[Func.getWidgetParent(widget_id)]
                cycle.deleteTimeline(widget_name)
            else:
                # delete item in timeline
                timeline: Timeline = Kernel.Widgets[Func.getWidgetParent(widget_id)]
                timeline.deleteItem(widget_name)
        # todo delete node and reference nodes in reference parent nodes
        pass
        # delete data (Kernel.Widgets Kernel.Names)
        pass

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
