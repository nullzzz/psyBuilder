from PyQt5.QtCore import Qt, QDataStream, QByteArray, QIODevice, QMimeData, QPoint, QSize
from PyQt5.QtGui import QDrag, QIcon
from PyQt5.QtWidgets import QListView, QListWidget, QListWidgetItem, QTabWidget, QFrame
from ..image import getImage

class IconList(QListWidget):
    def __init__(self, parent=None):
        super(IconList, self).__init__(parent)
        # 以Icon为主进行展示
        self.setViewMode(QListView.IconMode)
        # self.setResizeMode(QListView.Adjust)
        # 设置横向
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(False)
        self.setMovement(QListView.Static)
        self.setSpacing(10)

        self.setFrameStyle(QFrame.NoFrame)
        # 允许拖拽
        self.setDragEnabled(True)

    def startDrag(self, dropActions):
        # 获取当前item的pixmap
        item = self.currentItem()
        pixmap = item.icon().pixmap(QSize(50, 50))
        # 生成drag对象及传输数据
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        # 传入文字及图标
        stream.writeQString(item.text())
        stream << pixmap
        mimeData = QMimeData()
        mimeData.setData("application/IconBar-text-pixmap", data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)
        drag.exec(Qt.CopyAction)


class IconBar(QTabWidget):
    def __init__(self, parent=None):
        super(IconBar, self).__init__(parent)
        # 设置最大高度
        self.setMaximumHeight(125)
        # 数据
        self.events = IconList()
        self.eye_tracker = IconList()
        self.quest = IconList()
        self.condition = IconList()

        self.events.addItem(QListWidgetItem(getImage("Cycle", 'icon'), "Cycle"))
        self.events.addItem(QListWidgetItem(getImage("SoundOut", 'icon'), "SoundOut"))
        self.events.addItem(QListWidgetItem(getImage("Text", 'icon'), "Text"))
        self.events.addItem(QListWidgetItem(getImage("Image", 'icon'), "Image"))
        self.events.addItem(QListWidgetItem(getImage("Video", 'icon'), "Video"))

        self.eye_tracker.addItem(QListWidgetItem(getImage("Open", 'icon'), "Open"))
        self.eye_tracker.addItem(QListWidgetItem(getImage("DC", 'icon'), "DC"))
        self.eye_tracker.addItem(QListWidgetItem(getImage("Calibration", 'icon'), "Calibration"))
        self.eye_tracker.addItem(QListWidgetItem(getImage("Action", 'icon'), "Action"))
        self.eye_tracker.addItem(QListWidgetItem(getImage("StartR", 'icon'), "StartR"))
        self.eye_tracker.addItem(QListWidgetItem(getImage("EndR", 'icon'), "EndR"))
        self.eye_tracker.addItem(QListWidgetItem(getImage("Close", 'icon'), "Close"))

        self.quest.addItem(QListWidgetItem(getImage("QuestInit", 'icon'), "QuestInit"))
        self.quest.addItem(QListWidgetItem(getImage("QuestUpdate", 'icon'), "QuestUpdate"))
        self.quest.addItem(QListWidgetItem(getImage("QuestGetValue", 'icon'), "QuestGetValue"))

        self.condition.addItem(QListWidgetItem(getImage("If_else", 'icon'), "If_else"))
        self.condition.addItem(QListWidgetItem(getImage("Switch", 'icon'), "Switch"))

        self.addTab(self.events, "Events")
        self.addTab(self.eye_tracker, "Eye Tracker")
        self.addTab(self.quest, "Quest")
        self.addTab(self.condition, "Condition")