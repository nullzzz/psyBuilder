from PyQt5.QtCore import Qt, pyqtSignal, QRegExp
from PyQt5.QtGui import QPixmap, QRegExpValidator
from PyQt5.QtWidgets import QComboBox, QWidget, QLineEdit, QGridLayout, QLabel, QMessageBox

from center.iconTabs.events.image.imageProperty import ImageProperty
from center.iconTabs.events.soundOut.soundProperty import SoundProperty
from center.iconTabs.events.text.textProperty import TextProperty
from center.iconTabs.events.video.videoProperty import VideoProperty
from getImage import getImage
from ..timeline.icon import Icon


class IconChoose(QWidget):
    # 发送到上一层, 由上一层再转至properties (properties)
    propertiesShow = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(IconChoose, self).__init__(parent)

        self.icon_comboBox = QComboBox()
        self.icon_comboBox.addItem("None")
        self.icon_comboBox.addItem("Image")
        self.icon_comboBox.addItem("Video")
        self.icon_comboBox.addItem("Text")
        self.icon_comboBox.addItem("SoundOut")
        self.icon_comboBox.currentIndexChanged.connect(self.changeIcon)

        self.icon = Icon(pixmap=QPixmap(0, 0))
        self.icon.setAlignment(Qt.AlignCenter)

        self.properties_window = None
        self.properties = {}

        self.icon_name = QLineEdit()
        self.icon_name.setEnabled(False)

        grid_layout = QGridLayout()

        label_1 = QLabel("Stim Type:")
        label_1.setAlignment(Qt.AlignRight)
        label_2 = QLabel("Object Name:")
        label_2.setAlignment(Qt.AlignRight)
        grid_layout.addWidget(label_1, 0, 0, 1, 1)
        grid_layout.addWidget(self.icon_comboBox, 0, 1, 1, 3)
        grid_layout.addWidget(self.icon, 1, 1, 3, 3)
        grid_layout.addWidget(label_2, 4, 0, 1, 1)
        grid_layout.addWidget(self.icon_name, 4, 1, 1, 3)

        self.setLayout(grid_layout)

    def changeIcon(self, current_index):
        try:
            if not current_index:
                self.icon.setPixmap(QPixmap(0, 0))
                self.icon.changeType("Other")

                self.properties_window = None

                self.icon_name.setText("")
                self.icon_name.setEnabled(False)
            else:
                name = self.icon_comboBox.currentText()

                pixmap = getImage(name, "pixmap").scaledToHeight(64)
                self.icon.setPixmap(pixmap)
                self.icon.setFixedHeight(64)
                self.icon.changeType(name)

                if name == "Image":
                    self.properties_window = ImageProperty()
                    self.properties_window.ok_bt.clicked.connect(self.ok)
                    self.properties_window.cancel_bt.clicked.connect(self.properties_window.close)
                    self.properties_window.apply_bt.clicked.connect(self.apply)
                elif name == "SoundOut":
                    self.properties_window = SoundProperty()
                    self.properties_window.ok_bt.clicked.connect(self.ok)
                    self.properties_window.cancel_bt.clicked.connect(self.properties_window.close)
                    self.properties_window.apply_bt.clicked.connect(self.apply)
                elif name == "Text":
                    self.properties_window = TextProperty()
                    self.properties_window.ok_bt.clicked.connect(self.ok)
                    self.properties_window.cancel_bt.clicked.connect(self.properties_window.close)
                    self.properties_window.apply_bt.clicked.connect(self.apply)
                elif name == "Video":
                    self.properties_window = VideoProperty()
                    self.properties_window.ok_bt.clicked.connect(self.ok)
                    self.properties_window.cancel_bt.clicked.connect(self.properties_window.close)
                    self.properties_window.apply_bt.clicked.connect(self.apply)

                # self.icon_name.setText(Structure.getName(self.icon.value, name))
                self.icon_name.setPlaceholderText(f'Untitled-{name}')
                self.icon_name.setEnabled(True)
        except Exception as e:
            print("error {} happens in change icon. [condition/iconChoose.py]".format(e))

    def checkPosInIcon(self, e):
        x = e.pos().x()
        y = e.pos().y()
        if self.icon.mapToParent(self.icon.rect().topLeft()).x() <= x <= self.icon.mapToParent(self.icon.rect().bottomRight()).x() \
                and self.icon.mapToParent(self.icon.rect().topLeft()).y() <= y <= self.icon.mapToParent(self.icon.rect().bottomRight()).y():
            return True
        return False

    def mouseDoubleClickEvent(self, e):
        try:
            if self.checkPosInIcon(e):
                if self.properties_window:
                    self.properties_window.setWindowModality(Qt.ApplicationModal)
                    self.properties_window.show()
        except Exception as e:
            print('error {} happen in show properties window. [condition/iconChoose.py]'.format(e))

    def mousePressEvent(self, e):
        try:
            if self.checkPosInIcon(e):
                if self.properties_window:
                    self.propertiesShow.emit(self.properties_window.getInfo())
        except Exception as e:
            print('error {} happen in show properties window\'properties. [condition/iconChoose.py]'.format(e))

    def ok(self):
        self.apply()
        self.properties_window.close()

    def apply(self):
        try:
            self.propertiesShow.emit(self.properties_window.getInfo())
        except Exception as e:
            print("error {} happens in apply properties window in iconChoose. [condition/iconChoose.py]".format(e))

    def cancel(self):
        self.properties_window.close()

    def copy(self, icon_choose_copy):
        pass
