import os
import re
import sys
import traceback

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QFileDialog, QMenu

from lib import MessageBox, WaitDialog, Settings
from .attributes import Attributes
from .center import Center
from .center.condition import IfBranch, Switch
from .center.events import Cycle, ImageDisplay, Slider, SoundDisplay, TextDisplay, VideoDisplay
from .center.eyeTracker import EyeCalibrate, EyeDC, EndR, Close, StartR
from .center.quest import QuestUpdate
from .center.timeline import Timeline
from .deviceSystem.Yun import TianBianYiDuoYun
from .func import Func
from .info import Info
from .menubar.aboutUs import AboutUs
from .menubar.compile_PTB import compilePTB
from .menubar.update import Update
from .output import Output
from .properties import Properties
from .structure import Structure


class Psy(QMainWindow):
    def __init__(self):
        super(Psy, self).__init__(None)
        # title and icon
        self.setWindowTitle("PsyBuilder 0.1")
        self.setWindowIcon(Func.getImageObject("common/icon.png", type=1))
        # init menu bar
        self.initMenubar()
        # init dock widget
        self.initDockWidget()
        # wait dialog
        self.wait_dialog = WaitDialog(self)
        # save init state to restore the variable environment to its initial state
        # without any widgets even Timeline_0
        if not os.path.exists(Info.VarEnvFile):
            self.store(Info.VarEnvFile, False)
        # load config
        Info.Psy = self
        Info.FILE_NAME = Settings("config.ini", Settings.IniFormat).value("file_path", "")
        Info.FILE_DIRECTORY = Settings("config.ini", Settings.IniFormat).value("file_directory", "")
        # if file name not none, we restore data from this file
        if Info.FILE_NAME:
            new = Settings("config.ini", Settings.IniFormat).value("new", False)
            if new != "false":
                # we init initial timeline => Timeline_0
                self.initInitialTimeline()
                self.store(Info.FILE_NAME, False)
                Settings("config.ini", Settings.IniFormat).setValue("new", False)
            else:
                if not self.restore(Info.FILE_NAME):
                    self.clear()
                    Func.print(
                        f"The file {Info.FILE_NAME} you selected may be damaged, please check whether the file is correct.",
                        2)
        else:
            # we init initial timeline => Timeline_0
            self.initInitialTimeline()

    def initMenubar(self):
        """
        init top menubar
        """
        menubar = self.menuBar()
        # file menu
        file_menu: QMenu = menubar.addMenu("File")
        file_menu.addAction("New", self.newFile, QKeySequence(QKeySequence.New))
        file_menu.addAction("Open", self.openFile, QKeySequence(QKeySequence.Open))
        file_menu.addAction("Save", self.saveFile, QKeySequence(QKeySequence.Save))
        file_menu.addAction("Save As", self.saveAsFile, QKeySequence(QKeySequence.SaveAs))
        file_menu.addSeparator()
        open_mode_menu: QMenu = file_menu.addMenu("Open Mode")
        self.default_mode_action = open_mode_menu.addAction("Default Mode", lambda: self.changeOpenMode("default mode"))
        self.open_blank_file_action = open_mode_menu.addAction("Open Blank File",
                                                               lambda: self.changeOpenMode("open blank file"))
        open_mode = Settings("config.ini", Settings.IniFormat).value("open_mode", "default mode")
        self.changeOpenMode(open_mode)
        file_menu.addSeparator()
        file_menu.addAction("Exit", sys.exit, QKeySequence("Ctrl+Q"))
        # view menu
        view_menu = menubar.addMenu("&View")
        self.attribute_action = QAction("&Attribute", self)
        self.structure_action = QAction("&Structure", self)
        self.property_action = QAction("&Property", self)
        self.output_action = QAction("&Output", self)

        self.attribute_action.setData("attribute")
        self.structure_action.setData("structure")
        self.output_action.setData("output")
        self.property_action.setData("property")

        self.attribute_action.triggered.connect(self.setDockView)
        self.structure_action.triggered.connect(self.setDockView)
        self.output_action.triggered.connect(self.setDockView)
        self.property_action.triggered.connect(self.setDockView)

        view_menu.addAction(self.attribute_action)
        view_menu.addAction(self.structure_action)
        view_menu.addAction(self.property_action)
        view_menu.addAction(self.output_action)

        # devices menu
        self.device_cloud = TianBianYiDuoYun()
        devices_menu = menubar.addMenu("&Devices")
        t1_action = QAction("&Input", self)
        t1_action.triggered.connect(self.device_cloud.input.show)
        t2_action = QAction("&Output", self)
        t2_action.triggered.connect(self.device_cloud.output.show)
        t3_action = QAction("&Quest", self)
        t3_action.triggered.connect(self.device_cloud.quest.show)
        t4_action = QAction("&Tracker", self)
        t4_action.triggered.connect(self.device_cloud.tracker.show)

        devices_menu.addAction(t1_action)
        devices_menu.addAction(t2_action)
        devices_menu.addAction(t3_action)
        devices_menu.addAction(t4_action)

        # build menu
        build_menu = menubar.addMenu("&Building")
        build_menu.addSection("what")

        platform_menu = build_menu.addMenu("&Platform")

        self.linux_action = QAction("&Linux", self)
        self.linux_action.setChecked(True)

        self.windows_action = QAction("&Windows", self)
        self.mac_action = QAction("&Mac", self)

        icon = QIcon(Func.getImage("dock_visible.png"))

        self.linux_action.setIcon(icon)

        self.windows_action.setIcon(icon)
        self.windows_action.setIconVisibleInMenu(False)

        self.mac_action.setIcon(icon)
        self.mac_action.setIconVisibleInMenu(False)

        self.linux_action.triggered.connect(self.changePlatform)
        self.windows_action.triggered.connect(self.changePlatform)
        self.mac_action.triggered.connect(self.changePlatform)

        platform_menu.addAction(self.linux_action)
        platform_menu.addAction(self.windows_action)
        platform_menu.addAction(self.mac_action)

        # load image mode
        image_load_menu = build_menu.addMenu("&image Load Mode")

        self.before_event_action = QAction("&before_event", self)
        self.before_event_action.setChecked(True)

        self.before_trial_action = QAction("&before_trial", self)
        self.before_exp_action = QAction("&before_exp", self)

        # icon = QIcon(Func.getImage("dock_visible.png"))

        self.before_event_action.setIcon(icon)

        self.before_trial_action.setIcon(icon)
        self.before_trial_action.setIconVisibleInMenu(False)

        self.before_exp_action.setIcon(icon)
        self.before_exp_action.setIconVisibleInMenu(False)

        self.before_event_action.triggered.connect(self.changeImageLoadMode)
        self.before_trial_action.triggered.connect(self.changeImageLoadMode)
        self.before_exp_action.triggered.connect(self.changeImageLoadMode)

        image_load_menu.addAction(self.before_event_action)
        image_load_menu.addAction(self.before_trial_action)
        image_load_menu.addAction(self.before_exp_action)

        # compile
        compile_action = QAction("&Compile", self)
        compile_action.setShortcut("Ctrl+F5")
        compile_action.triggered.connect(self.compile)
        build_menu.addAction(compile_action)

        # help menu
        help_menu = menubar.addMenu("&Help")
        about_action = QAction("&About Us", self)
        about_Qt_action = QAction("&About Qt", self)
        check_for_update = QAction("&Check for updates", self)

        self.about_us = AboutUs()
        self.check_update = Update()
        about_action.triggered.connect(self.about_us.show)
        about_Qt_action.triggered.connect(QApplication.instance().aboutQt)
        check_for_update.triggered.connect(self.check_update.show)

        help_menu.addAction(about_action)
        help_menu.addAction(about_Qt_action)
        help_menu.addAction(check_for_update)

    def initDockWidget(self):
        """
        init dock widgets, including linking signals
        """
        # attributes
        self.attributes = Attributes()
        # structure
        self.structure = Structure()
        # properties
        self.properties = Properties()
        # center
        self.center = Center()
        self.setCentralWidget(self.center)
        # output
        self.output = Output()

        # its initial layout
        self.addDockWidget(Qt.LeftDockWidgetArea, self.structure)
        self.splitDockWidget(self.structure, self.properties, Qt.Vertical)
        self.splitDockWidget(self.properties, self.output, Qt.Horizontal)
        self.splitDockWidget(self.output, self.attributes, Qt.Horizontal)
        self.addDockWidget(Qt.RightDockWidgetArea, self.attributes)
        self.addDockWidget(Qt.BottomDockWidgetArea, self.output)
        # link signals
        self.center.currentWidgetChanged.connect(self.handleCurrentTabChanged)
        self.structure.itemDoubleClicked.connect(self.handleItemDoubleClicked)
        self.structure.itemDeleted.connect(self.handleItemDeleted)
        self.structure.itemNameChanged.connect(self.handleItemNameChanged)
        self.attributes.visibilityChanged.connect(self.checkVisible)
        self.structure.visibilityChanged.connect(self.checkVisible)
        self.properties.visibilityChanged.connect(self.checkVisible)
        self.output.visibilityChanged.connect(self.checkVisible)

    def createWidget(self, widget_id: str, widget_name: str):
        """
        create widget, link its signals and store it into some data
        """
        QApplication.processEvents()
        widget_type = Func.getWidgetType(widget_id)
        QApplication.processEvents()
        widget = None
        QApplication.processEvents()
        # try:
        if widget_type == Info.TIMELINE:
            widget = Timeline(widget_id, widget_name)
        elif widget_type == Info.IF:
            widget = IfBranch(widget_id, widget_name)
        elif widget_type == Info.SWITCH:
            widget = Switch(widget_id, widget_name)
        elif widget_type == Info.CYCLE:
            widget = Cycle(widget_id, widget_name)
        elif widget_type == Info.IMAGE:
            widget = ImageDisplay(widget_id, widget_name)
        elif widget_type == Info.VIDEO:
            widget = VideoDisplay(widget_id, widget_name)
        elif widget_type == Info.TEXT:
            widget = TextDisplay(widget_id, widget_name)
        elif widget_type == Info.SOUND:
            widget = SoundDisplay(widget_id, widget_name)
        elif widget_type == Info.SLIDER:
            widget = Slider(widget_id, widget_name)
        elif widget_type == Info.CALIBRATION:
            widget = EyeCalibrate(widget_id, widget_name)
        elif widget_type == Info.ENDR:
            widget = EndR(widget_id, widget_name)
        elif widget_type == Info.DC:
            widget = EyeDC(widget_id, widget_name)
        elif widget_type == Info.STARTR:
            widget = StartR(widget_id, widget_name)
        elif widget_type == Info.LOG:
            widget = Close(widget_id, widget_name)
        elif widget_type == Info.QUEST_UPDATE:
            widget = QuestUpdate(widget_id, widget_name)
        else:
            # if fail to create widget, exit.
            exit()
        # except Exception as e:
        #     raise Exception(f"create {widget_type} fail => widget_id: {widget_id}, widget_name: {widget_name}")
        # change data set in Kernel
        QApplication.processEvents()
        Info.Widgets[widget_id] = widget
        Info.Names[widget_name] = [widget_id]
        # link necessary signals
        QApplication.processEvents()
        self.linkWidgetSignals(widget_id, widget)
        QApplication.processEvents()
        return widget

    def cloneWidget(self, origin_widget_id: str, new_widget_id: str, new_widget_name: str):
        """
        copy widget, link its signals and store it into some data
        """
        # copy widget
        new_widget = Info.Widgets[origin_widget_id].clone(new_widget_id, new_widget_name)
        Info.Widgets[new_widget_id] = new_widget
        # link signals
        self.linkWidgetSignals(new_widget_id, new_widget)
        return new_widget

    def referWidget(self, origin_widget_id: str, new_widget_id: str = Info.ERROR_WIDGET_ID):
        """
        refer widget and update some data, if new_widget_id is Info.ERROR_WIDGET_ID, we generate new one
        """
        # generate new widget id
        widget_type = Func.getWidgetType(origin_widget_id)
        widget_name = Func.getWidgetName(origin_widget_id)
        widget_id = new_widget_id
        if widget_id == Info.ERROR_WIDGET_ID:
            widget_id = Func.generateWidgetId(widget_type)
        # refer widget by mapping widget id to same widget (Kernel.Widgets, Kernel.Names)
        Info.Widgets[widget_id] = Info.Widgets[origin_widget_id]
        Info.Names[widget_name].append(widget_id)
        return widget_id

    def linkWidgetSignals(self, widget_id: str, widget):
        """
        link widget's signals
        """
        widget_type = Func.getWidgetType(widget_id)
        # link common signals
        widget.propertiesChanged.connect(self.handlePropertiesChanged)
        widget.waitStart.connect(self.startWait)
        widget.waitEnd.connect(self.endWait)
        widget.tabClosed.connect(self.handleTabClosed)
        # link special signals
        if widget_type == Info.TIMELINE:
            # timeline
            widget.itemNameChanged.connect(self.handleItemNameChanged)
            widget.itemClicked.connect(self.handleItemClicked)
            widget.itemDoubleClicked.connect(self.handleItemDoubleClicked)
            widget.itemMoved.connect(self.handleItemMoved)
            widget.itemAdded.connect(self.handleItemAdded)
            widget.itemCopied.connect(self.handleItemCopied)
            widget.itemReferenced.connect(self.handleItemReferenced)
            widget.itemDeleted.connect(self.handleItemDeleted)
        elif widget_type == Info.CYCLE:
            # cycle
            widget.itemAdded.connect(self.handleItemAdded)
            widget.itemDeleted.connect(self.handleItemDeleted)
        elif widget_type == Info.IF or widget_type == Info.SWITCH:
            widget.itemAdded.connect(self.handleItemAdded)
            widget.itemDeleted.connect(self.handleItemDeleted)
            widget.itemNameChanged.connect(self.handleItemNameChanged)

    def initInitialTimeline(self):
        """
        init initial timeline => Timeline_0
        :return:
        """
        # init initial timeline
        widget_id = Func.generateWidgetId(Info.TIMELINE)
        widget_name = Func.generateWidgetName(Info.TIMELINE)
        # add node in structure
        self.structure.addNode(Info.ERROR_WIDGET_ID, widget_id, widget_name, 0)
        # create timeline widget
        self.createWidget(widget_id, widget_name)
        # set timeline as a tab
        self.center.openTab(widget_id)

    def handleItemAdded(self, parent_widget_id: str, widget_id: str, widget_name: str, index: int = -1):
        """
        When item is added, handle related affairs
        """
        # start wait
        self.startWait()
        # do job
        # add node in origin parent node firstly, because some widgets need to get attributes in __init__ function.
        show = True
        # if Func.isWidgetType(parent_widget_id, Info.IF) or Func.isWidgetType(parent_widget_id, Info.SWITCH):
        #     show = False
        self.structure.addNode(parent_widget_id, widget_id, widget_name, index, show)
        # create widget secondly
        self.createWidget(widget_id, widget_name)
        # we should consider a lot of things here because of reference.
        # we also need add node in those reference parents
        # add node in refer parent node
        refer_parent_widget_ids = Func.getWidgetReference(parent_widget_id)
        for refer_parent_widget_id in refer_parent_widget_ids:
            # we need exclude origin parent widget id
            if refer_parent_widget_id != parent_widget_id:
                # refer widget
                refer_widget_id = self.referWidget(widget_id)
                # add refer node in refer parent
                self.structure.addNode(refer_parent_widget_id, refer_widget_id, widget_name, index, show)
        # end wait
        self.endWait()

    def handleItemCopied(self, parent_widget_id: str, origin_widget_id: str, new_widget_id: str, new_widget_name: str,
                         index: int):
        """
        When item is copied, handle related affairs
        """
        # start wait
        self.startWait()
        # do job
        # copy widget firstly
        self.cloneWidget(origin_widget_id, new_widget_id, new_widget_name)
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

    def handleItemReferenced(self, parent_widget_id: str, origin_widget_id: str, new_widget_id: str, index: int):
        """
        When item is referenced, handle related affairs
        """
        # start wait
        self.startWait()
        # do job
        widget_name = Func.getWidgetName(origin_widget_id)
        origin_children = Func.getWidgetChildren(origin_widget_id)
        self.referNodeRecursive(parent_widget_id, new_widget_id, origin_widget_id, widget_name, index, origin_children)
        # we should consider a lot of things here because of reference.
        # we also need add node in those reference parents
        # add node in refer parent node
        refer_parent_widget_ids = Func.getWidgetReference(parent_widget_id)
        for refer_parent_widget_id in refer_parent_widget_ids:
            # we need exclude origin parent widget id
            if refer_parent_widget_id != parent_widget_id:
                self.referNodeRecursive(refer_parent_widget_id, Info.ERROR_WIDGET_ID, origin_widget_id, widget_name,
                                        index, origin_children)
        # end wait
        self.endWait()

    def referNodeRecursive(self, parent_widget_id: str, widget_id: str, origin_widget_id: str,
                           widget_name: str, index: int, origin_children: list):
        """
        refer node and children
        """
        # refer widget firstly
        widget_id = self.referWidget(origin_widget_id, widget_id)
        self.structure.addNode(parent_widget_id, widget_id, widget_name, index)
        # if reference node has children, we also need to refer those nodes
        for i in range(len(origin_children)):
            origin_child_widget_id, child_widget_name = origin_children[i]
            origin_child_children = Func.getWidgetChildren(origin_child_widget_id)
            self.referNodeRecursive(widget_id, Info.ERROR_WIDGET_ID, origin_child_widget_id, child_widget_name, i,
                                    origin_child_children)

    def handleItemMoved(self, origin_parent_widget_id: str, dest_parent_widget_id: str, widget_id: str,
                        origin_index: int, dest_index: int):
        """
        When item is moved, handle related affairs
        """
        widget_name = Func.getWidgetName(widget_id)
        if origin_parent_widget_id == dest_parent_widget_id:
            # move in its parent
            reference_parents = Func.getWidgetReference(origin_parent_widget_id)
            for reference_parent in reference_parents:
                parent_node = Info.Nodes[reference_parent]
                for i in range(parent_node.childCount()):
                    child = parent_node.child(i)
                    if child.text(0) == widget_name:
                        self.structure.moveNode(child.widget_id, origin_index, dest_index)
        else:
            # move to other parent, both origin widget and dest parent must be origin widget (first widget?).
            # delete node in origin parent, add node in dest parent (including reference)
            delete_children = []
            reference_parents = Func.getWidgetReference(origin_parent_widget_id)
            for reference_parent in reference_parents:
                parent_node = Info.Nodes[reference_parent]
                for i in range(parent_node.childCount()):
                    child = parent_node.child(i)
                    if child.text(0) == widget_name:
                        delete_children.append(child.widget_id)
                        self.structure.deleteNode(child.widget_id)
            # add node in dest parent. However, we need add or delete some node.
            reference_parents = Func.getWidgetReference(dest_parent_widget_id)
            if len(reference_parents) <= len(delete_children):
                # we need delete some children's widget id
                count = 0
                while count < len(reference_parents):
                    reference_parent = reference_parents[count]
                    child_widget_id = delete_children[count]
                    # add node in reference parent
                    self.structure.addNode(reference_parent, child_widget_id, widget_name, dest_index)
                    count += 1
                # delete some children's widget id, (Kernel.Nodes, Kernel.Names)
                while count < len(delete_children):
                    Info.Names[widget_name].remove(delete_children[count])
                    del Info.Nodes[delete_children[count]]
                    count += 1
            else:
                # we need add some children's widget id
                count = 0
                while count < len(reference_parents):
                    reference_parent = reference_parents[count]
                    child_widget_id = delete_children[count]
                    # add node in reference parent
                    self.structure.addNode(reference_parent, child_widget_id, widget_name, dest_index)
                    count += 1
                while count < len(reference_parents):
                    reference_parent = reference_parents[count]
                    child_widget_id = self.referWidget(widget_id)
                    self.structure.addNode(reference_parent, child_widget_id, widget_name, dest_index)
                    count += 1
            # delete item in origin timeline (not graceful)
            timeline: Timeline = Info.Widgets[origin_parent_widget_id]
            timeline.deleteItemByWidgetName(widget_name)
        # refresh attributes
        self.attributes.refresh()

    def handleItemDeleted(self, sender_widget: int, widget_id: str):
        """
        When item is deleted, handle related affairs
        """
        # close tab
        self.center.closeTab(widget_id)
        # delete node in structure (we need delete data in Kernel.Nodes and Kernel.Names) and item in timeline or timeline in cycle
        widget_name = Func.getWidgetName(widget_id)
        if sender_widget != Info.CycleSend and widget_id == self.attributes.current_widget_id:
            # we may need to clear attributes and properties if we delete showing widget
            self.attributes.showAttributes(Func.getWidgetParent(widget_id))
            self.properties.clear()
        if sender_widget == Info.StructureSend:
            # delete item in timeline or timeline in cycle
            if Func.isWidgetType(widget_id, Info.TIMELINE):
                # delete timeline in cycle
                cycle: Cycle = Info.Widgets[Func.getWidgetParent(widget_id)]
                cycle.deleteTimeline(widget_name)
            else:
                # delete item in timeline
                timeline: Timeline = Info.Widgets[Func.getWidgetParent(widget_id)]
                timeline.deleteItemByWidgetName(widget_name)
        # delete node and reference nodes in reference parent nodes
        reference_parents = Func.getWidgetReference(Func.getWidgetParent(widget_id))
        for reference_parent in reference_parents:
            children = Func.getWidgetChildren(reference_parent)
            for child_widget_id, child_widget_name in children:
                if child_widget_name == widget_name:
                    self.deleteNodeRecursive(child_widget_id, child_widget_name)
                    break

    def deleteNodeRecursive(self, widget_id: str, widget_name: str):
        """
        @param widget_id: root node's widget id
        @param widget_name: root node's widget name
        @return:
        """
        if Func.isWidgetType(widget_id, Info.CYCLE) or Func.isWidgetType(widget_id, Info.TIMELINE):
            for child_widget_id, child_widget_name in Func.getWidgetChildren(widget_id):
                self.deleteNodeRecursive(child_widget_id, child_widget_name)
        # delete data (Kernel.Nodes, Kernel.Widgets, Kernel.Name)
        self.structure.deleteNode(widget_id)
        Info.Nodes.pop(widget_id)
        reference: list = Info.Names[widget_name]
        if len(reference) == 1:
            Info.Names.pop(widget_name)
        else:
            if reference[0] == widget_id:
                # if widget is origin widget, we should change widget's widget id
                Info.Widgets[widget_id].changeWidgetId(reference[1])
            reference.remove(widget_id)
        Info.Widgets.pop(widget_id)

    def handleItemNameChanged(self, sender_widget: int, widget_id: str, new_widget_name: str):
        """
        When item'name is changed, handle related affairs
        """
        # change widget's name
        widget = Info.Widgets[widget_id]
        old_widget_name = Func.getWidgetName(widget_id)
        widget.widget_name = new_widget_name
        # change tab's name
        self.center.changeTabName(widget_id, new_widget_name)
        #
        parent_widget_id = Func.getWidgetParent(widget_id)
        if sender_widget == Info.StructureSend:
            # we need change item's name if signal comes from structure
            timeline = Info.Widgets[parent_widget_id]
            timeline.renameItem(old_widget_name, new_widget_name)
        # change node's name in structure and reference parent's child
        # get it's old name to get its reference
        change_widget_ids = [widget_id]
        reference_parents = Func.getWidgetReference(Func.getWidgetParent(widget_id))
        for reference_parent in reference_parents:
            children = Func.getWidgetChildren(reference_parent)
            for child_widget_id, child_widget_name in children:
                if child_widget_name == old_widget_name:
                    # change node's text
                    self.structure.changeNodeName(child_widget_id, new_widget_name)
                    if child_widget_id != widget_id:
                        change_widget_ids.append(child_widget_id)
                    break
        # change data (Kernel.Names, [Kernel.Widget])
        # if reference widget change its name, we should change it to a copy widget
        if len(change_widget_ids) == len(Info.Names[old_widget_name]):
            # if we change all, we just need to change key in Kernel.Names
            Info.Names[new_widget_name] = Info.Names[old_widget_name]
            del Info.Names[old_widget_name]
        else:
            # we need change
            origin_widget_id = Info.Names[old_widget_name][0]
            # save new name
            Info.Names[new_widget_name] = change_widget_ids
            # copy widget and map widget id to widget
            # remove change widget id from Kernel.Names[old_widget_name]
            for change_widget_id in change_widget_ids:
                Info.Names[new_widget_name].remove(change_widget_id)
            if origin_widget_id in change_widget_ids:
                # copy new widget and widget's widget id is now Kernel.Names[old_widget_name][0]
                # and change it map
                # change origin widget's widget id
                Info.Widgets[widget_id].changeWidgetId(Info.Names[old_widget_name][0])
                # copy this widget
                copy_widget = self.cloneWidget(Info.Names[old_widget_name][0], widget_id, new_widget_name)
                # map
                for change_widget_id in change_widget_ids:
                    Info.Widgets[change_widget_id] = copy_widget
            else:
                # copy widget and widget's widget id is change_widget_id[0], and map it to all
                copy_widget = self.cloneWidget(origin_widget_id, widget_id, new_widget_name)
                for change_widget_id in change_widget_ids:
                    Info.Widgets[change_widget_id] = copy_widget
        # refresh attributes
        self.attributes.refresh()

    def handleItemClicked(self, widget_id: str):
        """
        When item is clicked, handle related affairs
        """
        # change attributes and properties
        self.attributes.showAttributes(widget_id)
        self.properties.showProperties(widget_id)

    def handleItemDoubleClicked(self, widget_id: str):
        """
        When item is double clicked, handle related affairs
        """
        # open tab
        self.center.openTab(widget_id)

    def handlePropertiesChanged(self, widget_id: str):
        """
        When item'properties is changed or to show it, handle related affairs
        """
        self.properties.showProperties(widget_id)

    def handleCurrentTabChanged(self, widget_id: str):
        """

        """
        if widget_id == Info.ERROR_WIDGET_ID:
            # it means that user close all tab and we should clear attributes and properties
            # change attributes and properties
            self.attributes.clear()
            self.properties.clear()
        else:
            # change attributes and properties
            self.attributes.showAttributes(widget_id)
            self.properties.showProperties(widget_id)

    def handleTabClosed(self, widget_id: str):
        """

        """
        self.center.closeTab(widget_id)

    def newFile(self):
        """
        restart software
        """
        # choose directory
        file_directory = Info.FILE_DIRECTORY
        if not file_directory:
            # file_directory = os.getcwd()
            file_directory = os.path.dirname(os.path.abspath(__file__))
        # get new file's directory
        file_directory = QFileDialog().getExistingDirectory(None, "Choose Directory", file_directory,
                                                            QFileDialog.ShowDirsOnly)
        if file_directory:
            # change config
            Settings("config.ini", Settings.IniFormat).setValue("file_path", "")
            Settings("config.ini", Settings.IniFormat).setValue("file_directory", file_directory)
            # reset this software
            self.reset()
            Info.FILE_NAME = ""
            Info.FILE_DIRECTORY = file_directory

    def saveFile(self):
        """
        get file name and store data
        """
        if Info.FILE_NAME:
            self.store(Info.FILE_NAME)
        else:
            file_directory = Info.FILE_DIRECTORY
            if not file_directory:
                # file_directory = os.getcwd()
                file_directory = os.path.dirname(os.path.abspath(__file__))
            file_path, _ = QFileDialog().getSaveFileName(self, "Save file", file_directory, "Psy Files (*.psy);")
            if file_path:
                if not re.search(r"\.psy$", file_path):
                    file_path = file_path + ".psy"
                # store data to file
                if self.store(file_path):
                    # change config
                    Settings("config.ini", Settings.IniFormat).setValue("file_path", file_path)
                    Settings("config.ini", Settings.IniFormat).setValue("file_directory", os.path.dirname(file_path))
                    Info.FILE_NAME = file_path
                    Info.FILE_DIRECTORY = os.path.dirname(file_path)
                    # add file_path into file_paths
                    file_paths = Settings("config.ini", Settings.IniFormat).value("file_paths", [])
                    if file_path not in file_paths:
                        file_paths.insert(0, file_path)
                    else:
                        # move it to first
                        file_paths.remove(file_path)
                        file_paths.insert(0, file_path)
                    Settings("config.ini", Settings.IniFormat).setValue("file_paths", file_paths)

    def saveAsFile(self):
        """
        save as other file, but we don't change current file.
        :return:
        :rtype:
        """
        directory = Info.FILE_DIRECTORY
        if not directory:
            # directory = os.getcwd()
            directory = os.path.dirname(os.path.abspath(__file__))
        file_path, _ = QFileDialog().getSaveFileName(self, "Save As file", directory, "Psy Files (*.psy);")
        if file_path:
            if not re.search(r"(\.psy|\.ini)$", file_path):
                file_path = file_path + ".psy"
            # just store
            if self.store(file_path):
                # add file_path into file_paths
                file_paths = Settings("config.ini", Settings.IniFormat).value("file_paths", [])
                if file_path not in file_paths:
                    file_paths.insert(0, file_path)
                else:
                    # move it to first
                    file_paths.remove(file_path)
                    file_paths.insert(0, file_path)
                Settings("config.ini", Settings.IniFormat).setValue("file_paths", file_paths)

    def openFile(self):
        """
        open file through restart software
        """
        file_path, _ = QFileDialog().getOpenFileName(self, "Choose file", os.path.dirname(os.path.abspath(__file__)), "Psy File (*.psy)")
        if file_path and file_path != Info.FILE_NAME:
            # store current state
            self.store(Info.TempFile, False)
            # clear software
            self.clear()
            # restore data from opening file
            if not self.restore(file_path):
                # if store failed, restore to latest state
                self.restore(Info.TempFile, False)
            else:
                # change config
                Settings("config.ini", Settings.IniFormat).setValue("file_path", file_path)
                Settings("config.ini", Settings.IniFormat).setValue("file_directory", os.path.dirname(file_path))
                # add file_path into file_paths
                file_paths = Settings("config.ini", Settings.IniFormat).value("file_paths", [])
                if file_path not in file_paths:
                    file_paths.insert(0, file_path)
                else:
                    # move it to first
                    file_paths.remove(file_path)
                    file_paths.insert(0, file_path)
                Settings("config.ini", Settings.IniFormat).setValue("file_paths", file_paths)
                Info.FILE_NAME = file_path
                Info.FILE_DIRECTORY = os.path.dirname(file_path)

    def store(self, file_path: str, show=True) -> bool:
        """
        store data to file
        """
        try:
            setting = Settings(file_path, Settings.IniFormat)
            # some data in Info save to file directly
            setting.setValue("Names", Info.Names)
            setting.setValue("WidgetTypeCount", Info.WidgetTypeCount)
            setting.setValue("WidgetNameCount", Info.WidgetNameCount)
            setting.setValue("InputDeviceInfo", Info.INPUT_DEVICE_INFO)
            setting.setValue("OutputDeviceInfo", Info.OUTPUT_DEVICE_INFO)
            setting.setValue("QuestDeviceInfo", Info.QUEST_DEVICE_INFO)
            setting.setValue("TrackerDeviceInfo", Info.TRACKER_DEVICE_INFO)
            setting.setValue("SliderCount", Info.SLIDER_COUNT)
            # Info.Widgets: we just need to save origin widget
            widgets_data = {}
            for name in Info.Names:
                widget_id = Info.Names[name][0]
                widget = Info.Widgets[widget_id]
                widget_data = widget.store()
                widgets_data[f"{widget_id}&{name}"] = widget_data
            setting.setValue("Widgets", widgets_data)
            # structure
            structure = self.structure.store()
            setting.setValue("Structure", structure)
            # tabs
            # tabs = self.center.store()
            # setting.setValue("Tabs", tabs)
            if show:
                Func.print(f"File '{file_path}' saved successfully.", 1)
            return True
        except Exception as e:
            Func.print(f"Due to error {e}. File {file_path} saving failed.", 2)
            return False

    def restore(self, file_path: str, show=True) -> bool:
        """
        restore data from file(it changes Info.FileName and Info.FILE_DIRECTORY
        """
        try:
            setting = Settings(file_path, Settings.IniFormat)
        except:
            return False
        # restore data firstly
        names = setting.value("Names", -1)
        Info.WidgetTypeCount = setting.value("WidgetTypeCount", -1)
        Info.WidgetNameCount = setting.value("WidgetNameCount", -1)
        # do not change these device info object.
        input_device_info = setting.value("InputDeviceInfo", -1)
        output_device_info = setting.value("OutputDeviceInfo", -1)
        quest_device_info = setting.value("QuestDeviceInfo", -1)
        tracker_device_info = setting.value("TrackerDeviceInfo", -1)

        Info.SLIDER_COUNT = setting.value("SliderCount", -1)
        widgets_data = setting.value("Widgets", -1)
        structure = setting.value("Structure", -1)
        # tabs = setting.value("Tabs", -1)
        # any one equal -1, fail
        if names == -1 or \
                Info.WidgetTypeCount == -1 or \
                Info.WidgetNameCount == -1 or \
                input_device_info == -1 or \
                output_device_info == -1 or \
                quest_device_info == -1 or \
                tracker_device_info == -1 or \
                Info.SLIDER_COUNT == -1 or \
                widgets_data == -1 or \
                structure == -1:
            if show:
                Func.print(
                    f"The file '{file_path}' you selected may be damaged, please check whether the file is correct.",
                    2)
            return False
        # restore widgets: create origin widget and map to right widget ids
        # try:
        # restore device
        self.device_cloud.input.setProperties(input_device_info)
        self.device_cloud.output.setProperties(output_device_info)
        self.device_cloud.quest.setProperties(quest_device_info)
        self.device_cloud.tracker.setProperties(tracker_device_info)
        # end restore device
        # restore structure
        self.structure.restore(structure)
        # restore widgets according to structure, because some widget need to get attributes in __init__ function
        root_widget_id, root_widget_name, children = structure
        created_widgets = {}
        self.restoreWidget(names, widgets_data, created_widgets, root_widget_id, root_widget_name, children)
        # restore Info.Name
        Info.Names = names
        # restore tabs
        # self.center.restore(tabs)
        self.center.openTab(f"{Info.TIMELINE}.0")
        if show:
            Func.print(f"File '{file_path}' loaded successfully.", 1)
        return True
        # except Exception as e:
        #     Func.print(f"Due to error '{e}', the file {file_path} failed to load.", 2)
        #     return False

    def restoreWidget(self, names: dict, widgets_data: dict, created_widgets: dict, widget_id: str, widget_name: str,
                      children: list):
        """
        restore all widgets (dfs) according to structure, because some widget need to get attributes in __init__ function
        """
        # we just store origin widgets data.
        # create or map widget firstly
        if widget_name not in created_widgets:
            # create widget

            widget = self.createWidget(widget_id, widget_name)
            # restore widget data
            widget_data = widgets_data[f"{names[widget_name][0]}&{widget_name}"]
            widget.restore(widget_data)
            # log in created widgets
            created_widgets[widget_name] = widget
        else:
            # widget has been created, map firstly
            widget = created_widgets[widget_name]
            Info.Widgets[widget_id] = widget
            if widget_id == names[widget_name][0]:
                # if this is origin widget, change widget's widget id
                widget.changeWidgetId(widget_id)
        # handle its children
        for child_widget_id, child_widget_name, child_children in children:
            self.restoreWidget(names, widgets_data, created_widgets, child_widget_id, child_widget_name, child_children)

    def reset(self):
        """
        reset this software to initial Timeline_0
        :return:
        """
        self.clear()
        self.restore(Info.VarEnvFile, False)
        self.initInitialTimeline()

    def setDockView(self, checked):
        """
        单个dock的显示与隐藏
        :param checked:
        :return:
        """
        dock = self.sender().data()
        if dock == "attribute":
            self.attributes.setVisible(self.attributes.isHidden())
        elif dock == "structure":
            self.structure.setVisible(self.structure.isHidden())
        elif dock == "property":
            self.properties.setVisible(self.properties.isHidden())
        elif dock == "output":
            self.output.setVisible(self.output.isHidden())

    def changeOpenMode(self, mode: str):
        """
        change open mode in config and menu
        """
        # config
        Settings("config.ini", Settings.IniFormat).setValue("open_mode", mode)
        # menu
        checked_icon = Func.getImageObject("menu/checked", 1)
        if "default mode" == mode:
            self.default_mode_action.setIcon(checked_icon)
            self.open_blank_file_action.setIcon(QIcon(""))
        else:
            self.default_mode_action.setIcon(QIcon(""))
            self.open_blank_file_action.setIcon(checked_icon)

    def checkVisible(self, is_visible):
        """
        通过判断dock的显示与隐藏来改变菜单栏view的图标
        :param is_visible:
        :return:
        """
        dock = self.sender().windowTitle()
        if is_visible:
            icon = QIcon(Func.getImage("dock_visible.png"))
        else:
            icon = QIcon("")
        if dock == "Attributes":
            self.attribute_action.setIcon(icon)
        elif dock == "Structure":
            self.structure_action.setIcon(icon)
        elif dock == "Properties":
            self.property_action.setIcon(icon)
        elif dock == "Output":
            self.output_action.setIcon(icon)

    def changePlatform(self, c):
        if isinstance(c, bool):
            self.linux_action.setIconVisibleInMenu(self.sender() is self.linux_action)
            self.windows_action.setIconVisibleInMenu(self.sender() is self.windows_action)
            self.mac_action.setIconVisibleInMenu(self.sender() is self.mac_action)
            Info.PLATFORM = self.sender().text().lstrip("&").lower()
        elif isinstance(c, str):
            platform = c if c else "linux"
            self.linux_action.setIconVisibleInMenu(platform == "linux")
            self.windows_action.setIconVisibleInMenu(platform == "windows")
            self.mac_action.setIconVisibleInMenu(platform == "mac")

    def changeImageLoadMode(self, c):
        if isinstance(c, bool):
            self.before_event_action.setIconVisibleInMenu(self.sender() is self.before_event_action)
            self.before_trial_action.setIconVisibleInMenu(self.sender() is self.before_trial_action)
            self.before_exp_action.setIconVisibleInMenu(self.sender() is self.before_exp_action)
            Info.ImageLoadMode = self.sender().text().lstrip("&").lower()
        elif isinstance(c, str):
            imageLoadMode = c if c else "before_event"
            self.before_event_action.setIconVisibleInMenu(imageLoadMode == "before_event")
            self.before_trial_action.setIconVisibleInMenu(imageLoadMode == "before_trial")
            self.before_exp_action.setIconVisibleInMenu(imageLoadMode == "before_exp")

    def compile(self):
        try:
            compilePTB(self)
        except Exception as compileError:
            Func.print(str(compileError), 2)
            traceback.print_exc()

    def startWait(self):
        """
        show loading window
        """
        self.wait_dialog.show()

    def endWait(self):
        """
        close loading window
        """
        self.wait_dialog.close()

    def clear(self):
        """
        clear this software at all.
        if you want to reset this software, you should use reset function.
        :return:
        """
        # center
        self.center.clear()
        # structure
        self.structure.clear()
        # properties
        self.properties.clear()
        # attributes
        self.attributes.clear()
        # output
        # self.output.clear()
        # Info's data
        Info.PLATFORM = "linux"
        Info.IMAGE_LOAD_MODE = "before_event"
        Info.INPUT_DEVICE_INFO.clear()
        Info.OUTPUT_DEVICE_INFO.clear()
        Info.QUEST_DEVICE_INFO.clear()
        Info.TRACKER_DEVICE_INFO.clear()
        Info.FILE_NAME = ""
        Info.FILE_DIRECTORY = ""
        Info.device_count.clear()
        Info.SLIDER_COUNT.clear()
        Info.Widgets.clear()
        Info.Names.clear()
        Info.Nodes.clear()
        Info.WidgetTypeCount.clear()
        Info.WidgetNameCount.clear()

    # def showMaximized(self):
    #     """
    #
    #     :return:
    #     """
    #     super(Psy, self).showMaximized()
    #     self.animation = QPropertyAnimation(self, b"windowOpacity")
    #     self.animation.setDuration(0)
    #     self.animation.setStartValue(0)
    #     self.animation.setEndValue(1)
    #     self.animation.start()
