from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence
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
        # init menu bar
        self.initMenuBar()
        # set its title
        self.setWindowTitle("Psy Builder")
        # set its wait thread
        self.wait_dialog = WaitDialog()
        # init dock widget
        self.initDockWidget()

    def initMenuBar(self) -> None:
        """
        init its menu bar, including file, view, devices, building and help
        @return:
        """
        self.menu_bar = self.menuBar()
        # file menu
        self.file_menu = self.menu_bar.addMenu("File")
        self.file_menu.addAction("New", self.newActionFunc, QKeySequence(QKeySequence.New))
        self.file_menu.addAction("Open", self.openActionFunc, QKeySequence(QKeySequence.Open))
        self.file_menu.addAction("Save", self.saveActionFunc, QKeySequence(QKeySequence.Save))
        self.file_menu.addAction("Save As", self.saveAsActionFunc, QKeySequence(QKeySequence.SaveAs))
        # view
        self.view_menu = self.menu_bar.addMenu("View")
        self.view_menu.addAction("Default View", self.defaultViewAction, QKeySequence())
        # device
        self.device_menu = self.menu_bar.addMenu("Device")
        # building
        self.building_menu = self.menu_bar.addMenu("Building")
        # help
        self.help_menu = self.menu_bar.addMenu("Help")

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
        # link dock widgets' signals
        self.center.currentWidgetChanged.connect(self.dealCurrentTabChanged)
        self.structure.itemDoubleClicked.connect(self.dealItemDoubleClicked)
        self.structure.itemDeleted.connect(self.dealItemDeleted)
        self.structure.itemNameChanged.connect(self.dealItemNameChanged)
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
        return new_widget

    def referWidget(self, origin_widget_id: int, new_widget_id: int = -1) -> int:
        """
        refer widget
        @param origin_widget_id: origin widget's widget id
        @return: new widget id
        """
        # generate new widget id
        widget_type = Func.getWidgetType(origin_widget_id)
        widget_name = Func.getWidgetName(origin_widget_id)
        widget_id = new_widget_id
        if widget_id == -1:
            widget_id = Func.generateWidgetId(widget_type)
        # refer widget by mapping widget id to same widget (Kernel.Widgets, Kernel.Names)
        Kernel.Widgets[widget_id] = Kernel.Widgets[origin_widget_id]
        Kernel.Names[widget_name].append(widget_id)
        return widget_id

    def linkWidgetSignals(self, widget_type: int, widget):
        """
        link widget's signals according to its widget type.
        @param widget_type:
        @param widget:
        @return:
        """
        # todo link special widget's signals
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

    def newActionFunc(self):
        """
        new file
        @return:
        """
        print("new file")

    def openActionFunc(self):
        """
        open file
        @return:
        """
        print("open")

    def saveActionFunc(self):
        """
        save file
        @return:
        """
        print("save")

    def saveAsActionFunc(self):
        """
        save file as
        @return:
        """
        print("save as")

    def defaultViewAction(self):
        """

        @return:
        """
        print("default view")

    def dealItemAdded(self, parent_widget_id: int, widget_id: int, widget_name: str, index: int):
        """

        @param parent_widget_id:
        @param widget_id:
        @param widget_name:
        @param index:
        @param add_type:
        @return:
        """
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
        # delete node and reference nodes in reference parent nodes
        reference_parents = Func.getWidgetReference(Func.getWidgetParent(widget_id))
        for reference_parent in reference_parents:
            children = Func.getWidgetChildren(reference_parent)
            for child_widget_id, child_widget_name in children:
                if child_widget_name == widget_name:
                    self.deleteNodeRecursive(child_widget_id, child_widget_name)
                    break

    def deleteNodeRecursive(self, widget_id: int, widget_name: str):
        """

        @param widget_id: root node's widget id
        @param widget_name: root node's widget name
        @return:
        """
        if Func.isWidgetType(widget_id, Info.Cycle) or Func.isWidgetType(widget_id, Info.Timeline):
            for child_widget_id, child_widget_name in Func.getWidgetChildren(widget_id):
                self.deleteNodeRecursive(child_widget_id, child_widget_name)
        # delete data (Kernel.Nodes, Kernel.Widgets, Kernel.Name)
        self.structure.deleteNode(widget_id)
        del Kernel.Nodes[widget_id]
        reference: list = Kernel.Names[widget_name]
        if len(reference) == 1:
            del Kernel.Names[widget_name]
        else:
            if reference[0] == widget_id:
                # if widget is origin widget, we should change widget's widget id
                Kernel.Widgets[widget_id].changeWidgetId(reference[1])
            reference.remove(widget_id)
        del Kernel.Widgets[widget_id]

    def dealItemNameChanged(self, origin_widget: int, parent_widget_id: int, widget_id: int, widget_name: str):
        """
        when item's name changed, we deal some job. we forbid changing timeline's name
        @param origin_widget: where is the signal from, including timeline and structure
        @param parent_widget_id: item's parent
        @param widget_id:
        @param widget_name: new name
        @return:
        """
        # change widget's name
        widget = Kernel.Widgets[widget_id]
        old_widget_name = Func.getWidgetName(widget_id)
        widget.widget_name = widget_name
        # change tab's name
        self.center.changeTabName(widget_id, widget_name)
        if origin_widget == Info.StructureSignal:
            # we need change item's name if signal comes from structure
            timeline = Kernel.Widgets[parent_widget_id]
            timeline.renameItem(old_widget_name, widget_name)
        # change node's name in structure and reference parent's child
        # get it's old name to get its reference
        change_widget_ids = [widget_id]
        reference_parents = Func.getWidgetReference(Func.getWidgetParent(widget_id))
        for reference_parent in reference_parents:
            children = Func.getWidgetChildren(reference_parent)
            for child_widget_id, child_widget_name in children:
                if child_widget_name == old_widget_name:
                    # change node's text
                    self.structure.changeNodeName(child_widget_id, widget_name)
                    if child_widget_id != widget_id:
                        change_widget_ids.append(child_widget_id)
                    break
        # change data (Kernel.Names, [Kernel.Widget])
        # if reference widget change its name, we should change it to a copy widget
        if len(change_widget_ids) == len(Kernel.Names[old_widget_name]):
            # if we change all, we just need to change key in Kernel.Names
            Kernel.Names[widget_name] = Kernel.Names[old_widget_name]
            del Kernel.Names[old_widget_name]
        else:
            # we need change
            origin_widget_id = Kernel.Names[old_widget_name][0]
            # save new name
            Kernel.Names[widget_name] = change_widget_ids
            # copy widget and map widget id to widget
            # remove change widget id from Kernel.Names[old_widget_name]
            for change_widget_id in change_widget_ids:
                Kernel.Names[widget_name].remove(change_widget_id)
            if origin_widget_id in change_widget_ids:
                # copy new widget and widget's widget id is now Kernel.Names[old_widget_name][0]
                # and change it map
                # change origin widget's widget id
                Kernel.Widgets[widget_id].changeWidgetId(Kernel.Names[old_widget_name][0])
                # copy this widget
                copy_widget = self.copyWidget(Kernel.Names[old_widget_name][0], widget_id, widget_name)
                # map
                for change_widget_id in change_widget_ids:
                    Kernel.Widgets[change_widget_id] = copy_widget
            else:
                # copy widget and widget's widget id is change_widget_id[0], and map it to all
                copy_widget = self.copyWidget(origin_widget_id, widget_id, widget_name)
                for change_widget_id in change_widget_ids:
                    Kernel.Widgets[change_widget_id] = copy_widget

    def dealItemMoved(self, origin_parent, dest_parent, widget_id: int, origin_index: int, new_index: int):
        """

        @param origin_parent:
        @param dest_parent:
        @param widget_id:
        @param origin_index:
        @param new_index:
        @return:
        """
        widget_name = Func.getWidgetName(widget_id)
        if origin_parent == dest_parent:
            # move in its parent
            reference_parents = Func.getWidgetReference(origin_parent)
            for reference_parent in reference_parents:
                parent_node = Kernel.Nodes[reference_parent]
                for i in range(parent_node.childCount()):
                    child = parent_node.child(i)
                    if child.text(0) == widget_name:
                        self.structure.moveNode(child.widget_id, origin_index, new_index)
        else:
            # move to other parent, both origin widget and dest parent must be origin widget (first widget?).
            # delete node in origin parent, add node in dest parent (including reference)
            delete_children = []
            reference_parents = Func.getWidgetReference(origin_parent)
            for reference_parent in reference_parents:
                parent_node = Kernel.Nodes[reference_parent]
                for i in range(parent_node.childCount()):
                    child = parent_node.child(i)
                    if child.text(0) == widget_name:
                        delete_children.append(child.widget_id)
                        self.structure.deleteNode(child.widget_id)
            # add node in dest parent. However, we need add or delete some node.
            reference_parents = Func.getWidgetReference(dest_parent)
            if len(reference_parents) <= len(delete_children):
                # we need delete some children's widget id
                count = 0
                while count < len(reference_parents):
                    reference_parent = reference_parents[count]
                    child_widget_id = delete_children[count]
                    # add node in reference parent
                    self.structure.addNode(reference_parent, child_widget_id, widget_name, new_index)
                    count += 1
                # delete some children's widget id, (Kernel.Nodes, Kernel.Names)
                while count < len(delete_children):
                    Kernel.Names[widget_name].remove(delete_children[count])
                    del Kernel.Nodes[delete_children[count]]
                    count += 1
            else:
                # we need add some children's widget id
                count = 0
                while count < len(reference_parents):
                    reference_parent = reference_parents[count]
                    child_widget_id = delete_children[count]
                    # add node in reference parent
                    self.structure.addNode(reference_parent, child_widget_id, widget_name, new_index)
                    count += 1
                while count < len(reference_parents):
                    reference_parent = reference_parents[count]
                    child_widget_id = self.referWidget(widget_id)
                    self.structure.addNode(reference_parent, child_widget_id, widget_name, new_index)
                    count += 1

    def dealItemClicked(self, widget_id: int):
        """

        @param origin_widget:
        @param widget_id:
        @return:
        """
        # change attributes and properties
        self.attributes.showAttributes(widget_id)
        self.properties.showProperties(widget_id)

    def dealItemDoubleClicked(self, widget_id: int):
        """

        @param widget_id:
        @return:
        """
        # open tab
        self.center.openTab(widget_id)

    def dealCurrentTabChanged(self, widget_id: int):
        """

        @param widget_id:
        @return:
        """
        if widget_id == -1:
            # it means that user close all tab and we should clear attributes and properties
            # change attributes and properties
            self.attributes.clearAttributes()
            self.properties.clearProperties()
        else:
            # change attributes and properties
            self.attributes.showAttributes(widget_id)
            self.properties.showProperties(widget_id)

    def dealPropertiesChanged(self, widget_id: int):
        """
        when properties changed, refresh properties window.
        @param widget_id:
        @return:
        """
        self.properties.showProperties(widget_id)
