from PyQt5.QtCore import Qt, QDataStream, QByteArray, QIODevice, QMimeData, QPoint, QSize
from PyQt5.QtWidgets import QListView, QListWidget, QListWidgetItem, QTabWidget, QFrame
from PyQt5.QtGui import QDrag, QIcon


class EventList(QListWidget):
    def __init__(self, parent=None):
        super(EventList, self).__init__(parent)
        # 以Icon为主进行展示
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setSpacing(20)
        # 设置横向
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(False)
        self.setMovement(QListView.Static)
        self.setSpacing(10)
        self.setFrameStyle(QFrame.NoFrame)
        # 允许拖拽
        self.setDragEnabled(True)

    def addItem(self, item):

        super().addItem(item)

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
        mimeData.setData("application/EventList-text-pixmap", data)
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)
        drag.exec(Qt.CopyAction)


class EventBar(QTabWidget):
    def __init__(self, parent=None):
        super(EventBar, self).__init__(parent)
        # 设置最大高度
        self.setMaximumHeight(125)
        # 数据
        self.event = EventList()
        self.eyeTracker = EventList()
        self.quest = EventList()

        # self.event.addItem(QListWidgetItem(QIcon(".\\.\\Image\\timeLine.png"), "TimeLine"))
        self.event.addItem(QListWidgetItem(QIcon(".\\.\\Image\\cycle.png"), "Cycle"))
        self.event.addItem(QListWidgetItem(QIcon(".\\.\\Image\\sound.png"), "SoundOut"))
        self.event.addItem(QListWidgetItem(QIcon(".\\.\\Image\\text.png"), "Text"))
        self.event.addItem(QListWidgetItem(QIcon(".\\.\\Image\\imageDisplay.png"), "Image"))
        self.event.addItem(QListWidgetItem(QIcon(".\\.\\Image\\video.png"), "Video"))

        self.eyeTracker.addItem(QListWidgetItem(QIcon(".\\.\\Image\\open_eye.png"), "Open"))
        self.eyeTracker.addItem(QListWidgetItem(QIcon(".\\.\\Image\\setup_eye.png"), "SetUp"))
        self.eyeTracker.addItem(QListWidgetItem(QIcon(".\\.\\Image\\DC_eye.png"), "DC"))
        self.eyeTracker.addItem(QListWidgetItem(QIcon(".\\.\\Image\\start_eye.png"), "StartR"))
        self.eyeTracker.addItem(QListWidgetItem(QIcon(".\\.\\Image\\end_eye.png"), "EndR"))
        self.eyeTracker.addItem(QListWidgetItem(QIcon(".\\.\\Image\\close_eye.png"), "Close"))

        self.quest.addItem(QListWidgetItem(QIcon(".\\.\\Image\\start_quest.png"), "QuestStart"))
        self.quest.addItem(QListWidgetItem(QIcon(".\\.\\Image\\update_quest.png"), "QuestUpdate"))

        self.addTab(self.event, "Events")
        self.addTab(self.eyeTracker, "Eye Tracker")
        self.addTab(self.quest, "Quest")