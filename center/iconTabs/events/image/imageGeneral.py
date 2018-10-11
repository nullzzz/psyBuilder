from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QLineEdit, QPushButton, QCheckBox, \
    QComboBox, QSpinBox, QApplication, QFileDialog, QCompleter, QMessageBox

from ...colorBobox import ColorListEditor


# image event专属页面
class ImageTab1(QWidget):
    def __init__(self, parent=None):
        super(ImageTab1, self).__init__(parent)
        self.attributes = []
        self.default_properties = {
            "File name": "",
            "Mirror up/down": False,
            "Mirror left/right": False,
            "Stretch": False,
            "Stretch mode": "Both",
            "Back color": "white",
            "Transparent": 100,
            "Clear after": "Yes",
            "Screen name": "Display"
        }
        self.file_name = QLineEdit()
        self.file_name.textChanged.connect(self.findVar)
        self.file_name.returnPressed.connect(self.finalCheck)
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
        l1 = QLabel("Back Color:")
        l2 = QLabel("Transparent:")
        l3 = QLabel("Clear After:")
        l4 = QLabel("Screen Name:")
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout2.addWidget(l1, 0, 0)
        layout2.addWidget(self.back_color, 0, 1)
        layout2.addWidget(l2, 0, 2)
        layout2.addWidget(self.transparent, 0, 3)
        layout2.addWidget(l3, 1, 0)
        layout2.addWidget(self.clear_after, 1, 1)
        layout2.addWidget(l4, 1, 2)
        layout2.addWidget(self.screen_name, 1, 3)

        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Find the image file", self.file_name.text(),
                                                   "Image File (*.bmp;*.jpeg;*.jpg;*.png;*.gif)", options=options)
        if file_name:
            self.file_name.setText(file_name)

    def stretchChecked(self, e):
        if e == 2:
            self.stretch_mode.setEnabled(True)
        else:
            self.stretch_mode.setEnabled(False)

    # 检查变量
    def findVar(self, text):
        if text in self.attributes:
            self.sender().setStyleSheet("color: blue")
            self.sender().setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.sender().setStyleSheet("color: black")
            self.sender().setFont(QFont("宋体", 9, QFont.Normal))

    def finalCheck(self):
        temp = self.sender()
        text = temp.text()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    def setAttributes(self, attributes):
        self.attributes = attributes
        self.file_name.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Mirror up/down"] = bool(self.mirrorUD.checkState())
        self.default_properties["Mirror left/right"] = bool(self.mirrorLR.checkState())
        self.default_properties["Stretch"] = bool(self.stretch.checkState())
        self.default_properties["Stretch mode"] = self.stretch_mode.currentText()
        self.default_properties["Back color"] = self.back_color.currentText()
        self.default_properties["Transparent"] = self.transparent.value()
        self.default_properties["Clear after"] = self.clear_after.currentText()
        self.default_properties["Screen name"] = self.screen_name.currentText()

        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def loadSetting(self):
        self.file_name.setText(self.default_properties["File name"])
        self.mirrorUD.setChecked(self.default_properties["Mirror up/down"])
        self.mirrorLR.setChecked(self.default_properties["Mirror left/right"])
        self.stretch.setChecked(self.default_properties["Stretch"])
        self.stretch_mode.setCurrentText(self.default_properties["Stretch mode"])
        self.back_color.setCurrentText(self.default_properties["Back color"])
        self.transparent.setValue(self.default_properties["Transparent"])
        self.clear_after.setCurrentText(self.default_properties["Clear after"])
        self.screen_name.setCurrentText(self.default_properties["Screen name"])

    def clone(self):
        clone_page = ImageTab1()
        clone_page.setProperties(self.default_properties)
        return clone_page




if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = ImageTab1()

    t.show()

    sys.exit(app.exec())
