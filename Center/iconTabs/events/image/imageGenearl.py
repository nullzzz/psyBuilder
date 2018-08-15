from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QLineEdit, QPushButton, QCheckBox, \
    QComboBox, QSpinBox, QApplication, QFileDialog

from ...colorBobox import ColorListEditor


# image event专属页面


class ImageTab1(QWidget):
    def __init__(self, parent=None):
        super(ImageTab1, self).__init__(parent)
        self.file_name = QLineEdit()
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        self.mirrorUD = QCheckBox("Mirror up/down")
        self.mirrorLR = QCheckBox("Mirror left/right")
        self.stretch = QCheckBox("Stretch")
        self.stretch_mode = QComboBox()
        # self.usck = QCheckBox("Use Source Color Key")
        # self.sck = ColorListEditor()

        # self.align_h = QComboBox()
        # self.align_v = QComboBox()
        self.clear_after = QComboBox()
        self.back_color = ColorListEditor()
        self.transparent = QSpinBox()
        self.screen_name = QComboBox()
        self.setGeneral()

    def setGeneral(self):
        self.stretch_mode.addItems(["Both", "LeftRight", "UpDown"])
        # self.sck.addItems(["black", "maroon", "green", "olive"])

        # self.align_h.addItems(["center", "left", "right"])
        # self.align_v.addItems(["center", "left", "right"])
        self.clear_after.addItems(["Yes", "No"])

        self.transparent.setMaximum(100)
        self.transparent.setSuffix("%")
        self.transparent.setValue(100)
        self.screen_name.addItems(["Display"])

        group1 = QGroupBox("")
        layout1 = QGridLayout()
        layout1.addWidget(QLabel("File Name"), 0, 0, 1, 1)
        layout1.addWidget(self.file_name, 0, 1, 1, 4)
        layout1.addWidget(self.open_bt, 0, 5, 1, 1)
        ###

        self.stretch.stateChanged.connect(self.stretchChecked)
        self.stretch_mode.setEnabled(False)

        # self.usck.stateChanged.connect(self.colorChecked)
        # self.sck.setEnabled(False)
        ###
        layout1.addWidget(self.mirrorUD, 1, 0)
        layout1.addWidget(self.mirrorLR, 2, 0)
        layout1.addWidget(self.stretch, 3, 0)
        # layout1.addWidget(self.usck, 4, 0)
        layout1.addWidget(self.stretch_mode, 3, 2)
        # layout1.addWidget(self.sck, 4, 2)
        group1.setLayout(layout1)

        group2 = QGroupBox("")
        layout2 = QGridLayout()
        # layout2.addWidget(QLabel("AlignHorizontal:"), 0, 0)
        # layout2.addWidget(self.align_h, 0, 1)
        # layout2.addWidget(QLabel("AlignVertical:"), 1, 0)
        # layout2.addWidget(self.align_v, 1, 1)

        layout2.addWidget(QLabel("Back Color:"), 0, 0)
        layout2.addWidget(self.back_color, 0, 1)

        layout2.addWidget(QLabel("Transparent:"), 0, 2)
        layout2.addWidget(self.transparent, 0, 3)
        layout2.addWidget(QLabel("Clear After:"), 1, 0)
        layout2.addWidget(self.clear_after, 1, 1)
        layout2.addWidget(QLabel("Display Name:"), 1, 2)
        layout2.addWidget(self.screen_name, 1, 3)

        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Find the image file)", self.file_name.text(),
                                                   "Image File (*.bmp;*.jpeg;*.jpg;*.png;*.gif)", options=options)
        if file_name:
            self.file_name.setText(file_name)

    def stretchChecked(self, e):
        if e == 2:
            self.stretch_mode.setEnabled(True)
        else:
            self.stretch_mode.setEnabled(False)

    def getInfo(self):
        return {"File name": self.file_name.text(), "Mirror up/down": bool(
            self.mirrorUD.checkState()), "Mirror left/right": bool(self.mirrorLR.checkState()), "Stretch": bool(
            self.stretch.checkState()), "Stretch mode": self.stretch_mode.currentText(), "Back color":
            self.back_color.currentText(), "Transparent": "{}%".format(self.transparent.value()), "Clear after":
            self.clear_after.currentText(), "Screen name": self.screen_name.currentText()}


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = ImageTab1()

    t.show()

    sys.exit(app.exec())
