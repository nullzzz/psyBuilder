from PyQt5.QtWidgets import QComboBox, QWidget, QLineEdit, QVBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

from ..timeline.icon import Icon
from ..image import getImage


class IconChoose(QWidget):
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

                self.icon_name.setText("")
                self.icon_name.setEnabled(False)
            else:
                name = self.icon_comboBox.currentText()

                pixmap = getImage(name, "pixmap")
                self.icon.setPixmap(pixmap)
                self.icon.changeType(name)

                self.icon_name.setText(name)
                self.icon_name.setEnabled(True)
        except Exception as e:
            print("error {} happens in change icon. [condition/iconChoose.py]".format(e))
