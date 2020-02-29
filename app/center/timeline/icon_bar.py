from PyQt5.QtCore import QDataStream, QByteArray, QIODevice, QMimeData, QPoint, QSize
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QListView, QListWidget, QListWidgetItem, QTabWidget, QFrame

from app.func import Func
from app.info import Info


class WidgetIconItem(QListWidgetItem):
    """
    icon item in icon lists
    """

    def __init__(self, widget_type: str):
        self.widget_type = widget_type
        icon = Func.getImage(f"widgets/{widget_type}", 1)
        super(WidgetIconItem, self).__init__(icon, widget_type)


class IconList(QListWidget):
    """
    a bar to place widgets' icon and we can drag icons to timeline area to create widget.
    """

    def __init__(self, parent=None):
        super(IconList, self).__init__(parent)
        # set its qss id
        self.setObjectName("IconList")
        # set view mode
        self.setViewMode(QListView.IconMode)
        # set orientation and base
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(False)
        self.setMovement(QListView.Static)
        # set no frame
        self.setFrameStyle(QFrame.NoFrame)
        # set draggable
        self.setDragEnabled(True)

    def startDrag(self, Union, Qt_DropActions=None, Qt_DropAction=None):
        # get widget type which is represented by icon
        item: WidgetIconItem = self.currentItem()
        # write data into an object which can be brought by draggable item
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(item.widget_type)
        mime_data = QMimeData()
        mime_data.setData(Info.IconBarToTimeline, data)
        # generate a draggable item
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(25, 25))
        drag.setPixmap(item.icon().pixmap(QSize(50, 50)))
        drag.exec()


class IconBar(QTabWidget):
    def __init__(self, parent=None):
        super(IconBar, self).__init__(parent)
        # set its id
        self.setObjectName("IconBar")
        # set its icon lists
        self.events = IconList()
        self.eye_tracker = IconList()
        self.quest = IconList()
        self.condition = IconList()
        # todo add events items
        self.events.addItem(WidgetIconItem(Info.CYCLE))

        # todo add eye_tracker items

        # todo add quest items

        # todo add condition items

        self.addTab(self.events, "Events")
        self.addTab(self.eye_tracker, "Eye Tracker")
        self.addTab(self.quest, "Quest")
        self.addTab(self.condition, "Condition")
