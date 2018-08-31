from PyQt5.QtWidgets import QComboBox, QWidget, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal

from center.iconTabs.events.image.imageProperty import ImageProperty
from center.iconTabs.events.soundOut.soundProperty import SoundProperty
from center.iconTabs.events.text.textProperty import TextProperty
from center.iconTabs.events.video.videoProperty import VideoProperty

from ..timeline.icon import Icon
from ..image import getImage


class IconChoose(QWidget):
    # 发送到上一层, 由上一层再转至iconTabs (value)
    propertiesShow = pyqtSignal(str)
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

        vBox_layout = QVBoxLayout()

        vBox_layout.addWidget(self.icon_comboBox)
        vBox_layout.addStretch(1)
        vBox_layout.addWidget(self.icon)
        vBox_layout.addStretch(1)
        vBox_layout.addWidget(self.icon_name)

        self.setLayout(vBox_layout)

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

                pixmap = getImage(name, "pixmap")
                self.icon.setPixmap(pixmap)
                self.icon.changeType(name)

                if name == "Image":
                    self.properties_window = ImageProperty()
                elif name == "SoundOut":
                    self.properties_window = SoundProperty()
                elif name == "Text":
                    self.properties_window = TextProperty()
                elif name == "Video":
                    self.properties_window = VideoProperty()

                self.icon_name.setText(name)
                self.icon_name.setEnabled(True)
        except Exception as e:
            print("error {} happens in change icon. [condition/iconChoose.py]".format(e))

    def checkPosInIcon(self, e):
        x = e.pos().x()
        y = e.pos().y()
        if x <= self.icon.rect().right() and x >= self.icon.rect().left() \
                and y >= self.icon_name.rect().top() and y <= self.icon.rect().bottom():
            return True
        return False

    def mouseDoubleClickEvent(self, e):
        if self.checkPosInIcon(e):
            if self.properties_window:
                self.properties_window.show()

    def mousePressEvent(self, e):
        if self.checkPosInIcon(e):
            if self.properties_window:
                self.propertiesShow.emit(self.icon.value)
