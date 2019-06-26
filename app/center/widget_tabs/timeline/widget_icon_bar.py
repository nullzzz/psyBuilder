from PyQt5.QtCore import Qt, QDataStream, QByteArray, QIODevice, QMimeData, QPoint, QSize
from PyQt5.QtGui import QDrag
from PyQt5.QtWidgets import QListView, QListWidget, QListWidgetItem, QTabWidget, QFrame

from app.func import Func
from app.info import Info


class WidgetIconList(QListWidget):
    def __init__(self, parent=None):
        super(WidgetIconList, self).__init__(parent)
        # 以Icon为主进行展示
        self.setViewMode(QListView.IconMode)
        # self.setResizeMode(QListView.Adjust)
        self.setStyleSheet("""
            margin-top:15px;
            background-color:transparent;
        """)
        # 设置横向
        self.setFlow(QListView.LeftToRight)
        self.setWrapping(False)
        self.setMovement(QListView.Static)

        self.setFrameStyle(QFrame.NoFrame)
        # 允许拖拽
        self.setDragEnabled(True)

    def startDrag(self, Union, Qt_DropActions=None, Qt_DropAction=None):
        # 传输widget type就行
        # 获取当前item的pixmap
        item = self.currentItem()
        pixmap = item.icon().pixmap(QSize(50, 50))
        # 生成drag对象及传输数据
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(item.text())
        mime_data = QMimeData()
        mime_data.setData("widget_icon_bar/widget_icon_type", data)
        drag = QDrag(self)
        drag.setMimeData(mime_data)
        drag.setHotSpot(QPoint(12, 12))
        drag.setPixmap(pixmap)
        drag.exec(Qt.CopyAction)


class WidgetIconBar(QTabWidget):
    def __init__(self, parent=None):
        super(WidgetIconBar, self).__init__(parent)
        # 设置最大高度
        self.setStyleSheet("""
            max-height:120px;
            border-color: rgb(236,236,236);
            border-bottom: 0px;
        """)
        # 数据
        self.events = WidgetIconList()
        self.eye_tracker = WidgetIconList()
        self.quest = WidgetIconList()
        self.condition = WidgetIconList()
        # events
        self.events.addItem(QListWidgetItem(Func.getWidgetImage(Info.CYCLE, 'icon'), Info.CYCLE))
        self.events.addItem(QListWidgetItem(Func.getWidgetImage(Info.SOUND, 'icon'), Info.SOUND))
        self.events.addItem(QListWidgetItem(Func.getWidgetImage(Info.TEXT, 'icon'), Info.TEXT))
        self.events.addItem(QListWidgetItem(Func.getWidgetImage(Info.IMAGE, 'icon'), Info.IMAGE))
        self.events.addItem(QListWidgetItem(Func.getWidgetImage(Info.VIDEO, 'icon'), Info.VIDEO))
        self.events.addItem(QListWidgetItem(Func.getWidgetImage(Info.SLIDER, 'icon'), Info.SLIDER))
        # eye_tracker
        self.eye_tracker.addItem(QListWidgetItem(Func.getWidgetImage(Info.OPEN, 'icon'), Info.OPEN))
        self.eye_tracker.addItem(QListWidgetItem(Func.getWidgetImage(Info.DC, 'icon'), Info.DC))
        self.eye_tracker.addItem(QListWidgetItem(Func.getWidgetImage(Info.CALIBRATION, 'icon'), Info.CALIBRATION))
        self.eye_tracker.addItem(QListWidgetItem(Func.getWidgetImage(Info.ACTION, 'icon'), Info.ACTION))
        self.eye_tracker.addItem(QListWidgetItem(Func.getWidgetImage(Info.STARTR, 'icon'), Info.STARTR))
        self.eye_tracker.addItem(QListWidgetItem(Func.getWidgetImage(Info.ENDR, 'icon'), Info.ENDR))
        self.eye_tracker.addItem(QListWidgetItem(Func.getWidgetImage(Info.CLOSE, 'icon'), Info.CLOSE))
        # quest
        self.quest.addItem(QListWidgetItem(Func.getWidgetImage(Info.QUEST_INIT, 'icon'), Info.QUEST_INIT))
        self.quest.addItem(QListWidgetItem(Func.getWidgetImage(Info.QUEST_UPDATE, 'icon'), Info.QUEST_UPDATE))
        self.quest.addItem(QListWidgetItem(Func.getWidgetImage(Info.QUEST_GET_VALUE, 'icon'), Info.QUEST_GET_VALUE))
        # condition
        self.condition.addItem(QListWidgetItem(Func.getWidgetImage('If', 'icon'), "If"))
        self.condition.addItem(QListWidgetItem(Func.getWidgetImage('Switch', 'icon'), "Switch"))

        self.addTab(self.events, "Events")
        self.addTab(self.eye_tracker, "Eye Tracker")
        self.addTab(self.quest, "Quest")
        self.addTab(self.condition, "Condition")
