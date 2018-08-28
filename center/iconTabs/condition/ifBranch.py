from PyQt5.QtCore import Qt, pyqtSignal, QObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGroupBox, QComboBox, QLineEdit, QPushButton, QGridLayout, QApplication, QLabel, \
    QVBoxLayout, QHBoxLayout

from center.iconTabs.events.image.imageProperty import ImageProperty
from center.iconTabs.events.soundOut.soundProperty import SoundProperty
from center.iconTabs.events.text.textProperty import TextProperty
from center.iconTabs.events.video.videoProperty import VideoProperty


class IfBranch(QWidget):
    propertiesChange = pyqtSignal(dict)
    tabClose = pyqtSignal(QWidget)

    def __init__(self, parent=None):
        super(IfBranch, self).__init__(parent)
        self.add_condition = QPushButton("&Add")
        self.add_condition.clicked.connect(self.addCondition)
        # condition1
        self.var1 = QComboBox()
        self.compare1 = QComboBox()
        self.value1 = QLineEdit()

        self.cnt = 2
        # 这里就限制最多选择六个条件
        self.condition2 = OneCondition()
        self.condition3 = OneCondition()
        self.condition4 = OneCondition()
        self.condition5 = OneCondition()
        self.condition6 = OneCondition()
        self.condition2.add_condition.connect(self.addCondition)
        self.condition3.add_condition.connect(self.addCondition)
        self.condition4.add_condition.connect(self.addCondition)
        self.condition5.add_condition.connect(self.addCondition)
        self.condition6.add_condition.connect(self.addCondition)
        # 条件的true执行的event
        self.t_event = QComboBox()
        self.t_event.currentTextChanged.connect(self.changeImage)
        self.t_event_image = MyLabel()
        self.t_event_image.double_click.connect(self.showProperty)
        # 条件为false执行的event
        self.f_event = QComboBox()
        self.f_event.currentTextChanged.connect(self.changeImage)
        self.f_event_image = MyLabel()
        self.f_event_image.double_click.connect(self.showProperty)

        self.bt_ok = QPushButton("Ok")
        self.bt_ok.clicked.connect(self.ok)
        self.bt_cancel = QPushButton("Cancel")
        self.bt_cancel.clicked.connect(self.cancel)
        self.bt_apply = QPushButton("Apply")
        self.bt_apply.clicked.connect(self.apply)

        self.setUI()

    def setUI(self):
        self.compare1.addItems((">", "<", "=="))

        self.t_event.addItems(["Image", "SoundOut", "Text", "Video"])
        self.t_event.setObjectName("t_event")
        self.f_event.addItems(["Image", "SoundOut", "Text", "Video"])

        group1 = QGroupBox("Condition")
        self.layout1 = QGridLayout()
        self.layout1.addWidget(self.var1, 0, 1)
        self.layout1.addWidget(self.compare1, 0, 2)
        self.layout1.addWidget(self.value1, 0, 3)
        self.layout1.addWidget(self.add_condition, 0, 4)

        group1.setLayout(self.layout1)

        group2 = QGroupBox("True")
        layout2 = QVBoxLayout()
        layout2.addWidget(self.t_event)
        layout2.addWidget(self.t_event_image, Qt.AlignHCenter)
        group2.setLayout(layout2)

        group3 = QGroupBox("False")
        layout3 = QVBoxLayout()
        layout3.addWidget(self.f_event)
        layout3.addWidget(self.f_event_image, Qt.AlignHCenter)
        group3.setLayout(layout3)

        layout23 = QHBoxLayout()
        layout23.addWidget(group2)
        layout23.addWidget(group3)

        layout4 = QHBoxLayout()
        layout4.addStretch(10)
        layout4.addWidget(self.bt_ok)
        layout4.addWidget(self.bt_cancel)
        layout4.addWidget(self.bt_apply)
        layout4.setContentsMargins(0, 0, 0, 0)

        layout = QVBoxLayout()
        layout.addWidget(group1, 1)
        layout.addLayout(layout23, 2)
        layout.addLayout(layout4, 1)
        self.setLayout(layout)

    # 改变下方label的图标
    # 并改变事件属性
    def changeImage(self, event_name):
        pix = QPixmap()
        pix.load(r"D:\PsyDemo\image\{}".format(event_name))
        if self.sender() == self.t_event:
            self.t_event_image.setPixmap(pix)
            if event_name == "Image":
                self.t_pro = ImageProperty()
            elif event_name == "SoundOut":
                self.t_pro = SoundProperty()
            elif event_name == "Text":
                self.t_pro = TextProperty()
            else:
                self.t_pro = VideoProperty()
        else:
            self.f_event_image.setPixmap(pix)
            if event_name == "Image":
                self.f_pro = ImageProperty()
            elif event_name == "SoundOut":
                self.f_pro = SoundProperty()
            elif event_name == "Text":
                self.f_pro = TextProperty()
            else:
                self.f_pro = VideoProperty()

    # 双击event的图标打开event的属性设置
    # 1、直接跳出properties设置的弹窗
    def showProperty(self):
        if self.sender() == self.t_event_image:
            self.t_pro.show()
            self.t_pro.setWindowModality(Qt.ApplicationModal)
            # 这里或许还有别的事要做
            self.t_pro.ok_bt.clicked.connect(self.t_pro.close)
            self.t_pro.cancel_bt.clicked.connect(self.t_pro.close)
            # self.t_pro.apply_bt.clicked.connect(self.t_pro.close)
        else:
            self.f_pro.show()
            self.f_pro.setWindowModality(Qt.ApplicationModal)
            self.f_pro.ok_bt.clicked.connect(self.f_pro.close)
            self.f_pro.cancel_bt.clicked.connect(self.f_pro.close)

    def addCondition(self):
        if self.cnt <= 6:
            self.layout1.addWidget(eval("self.condition{}".format(self.cnt)).and_or, self.cnt - 1, 0)
            self.layout1.addWidget(eval("self.condition{}".format(self.cnt)).var, self.cnt - 1, 1)
            self.layout1.addWidget(eval("self.condition{}".format(self.cnt)).compare, self.cnt - 1, 2)
            self.layout1.addWidget(eval("self.condition{}".format(self.cnt)).value, self.cnt - 1, 3)
            self.layout1.addWidget(eval("self.condition{}".format(self.cnt)).add, self.cnt - 1, 4)
            self.cnt += 1

    # tab 页面的信号
    def ok(self):
        self.apply()
        self.close()
        # 关闭信号
        self.tabClose.emit(self)

    def cancel(self):
        self.close()
        # 关闭信号
        self.tabClose.emit(self)

    def apply(self):
        self.propertiesChange.emit(self.getInfo())

    # 返回条件
    # 实践属性
    def getInfo(self):
        return {
        }


# 对label添加双击信号，打开event的属性设置
class MyLabel(QLabel):
    double_click = pyqtSignal()

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self.setAlignment(Qt.AlignCenter)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.double_click.emit()


class OneCondition(QObject):
    add_condition = pyqtSignal()

    def __init__(self):
        super(OneCondition, self).__init__()
        self.and_or = QComboBox()
        self.var = QComboBox()
        self.compare = QComboBox()
        self.value = QLineEdit()
        self.add = QPushButton("&Add")
        self.add.clicked.connect(lambda: self.add_condition.emit())
        self.setUI()

    def setUI(self):
        self.and_or.addItems(["and", "or"])
        self.compare.addItems([">", "<", "="])

    # 返回当前条件的真值
    def getBool(self):
        return


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = IfBranch()

    t.show()

    sys.exit(app.exec())
