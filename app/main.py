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

    def initInitialTimeline(self):
        """
        init initial timeline for other items
        @return:
        """
        widget_id = Func.generateWidgetId(Info.Timeline)
        widget_name = f"{Info.WidgetType[Info.Timeline]}.0"
        # create timeline widget
        Func.createWidget(widget_id, widget_name)
        # set timeline as a tab
        self.center.openTab(widget_id)

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

    def linkSignals(self):
        """
        link signals between dock widgets
        @return:
        """
        # todo link dock widgets' signals

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

    def dealItemNameChanged(self, origin_widget: int, widget_id: int, text: str):
        """

        @param origin_widget:
        @param widget_id:
        @param text:
        @return:
        """
        print("item name change", origin_widget, widget_id, text)

    def dealItemClicked(self, origin_widget: int, widget_id: int):
        """

        @param origin_widget:
        @param widget_id:
        @return:
        """
        print("item click", origin_widget, widget_id)
