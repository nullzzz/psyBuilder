from PyQt5.QtWidgets import (QWidget, QTabWidget, QFrame, QLineEdit, QPushButton, QCheckBox, QComboBox, QSpinBox,
                             QVBoxLayout, QHBoxLayout, QFileDialog, QDesktopWidget, QGroupBox, QGridLayout, QLabel)

from .imageTab2 import Tab2
from .imageTab3 import Tab3
from ..ColorBobox import ColorListEditor


class ImageProperty(QWidget):
    def __init__(self, parent=None):
        super(ImageProperty, self).__init__(parent)
        self.tab = QTabWidget()
        self.below = QWidget()

        # general
        self.file_name = QLineEdit()
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.setExistingDirectory)

        self.mirrorUD = QCheckBox("Mirror up/down")
        self.mirrorLR = QCheckBox("Mirror left/right")
        self.stretch = QCheckBox("Stretch")
        self.stretch_mode = QComboBox()
        # self.usck = QCheckBox("Use Source Color Key")
        # self.sck = ColorListEditor()

        self.align_h = QComboBox()
        self.align_v = QComboBox()
        self.clear_after = QComboBox()
        self.back_color = ColorListEditor()
        self.transparent = QSpinBox()
        self.screen_name = QComboBox()
        self.setGeneral()

        self.frame = Tab2()
        self.duration = Tab3()
        self.tab.addTab(self.frame, "frame")
        self.tab.addTab(self.duration, "duration")
        # bottom
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.setButtons()

        self.setUI()
        # self.center()

    # 生成主界面
    def setUI(self):
        self.setWindowTitle("Image property")
        self.resize(600, 800)
        # self.setFixedSize(600, 800)
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.tab, 6)
        # mainLayout.addStretch(2)
        mainLayout.addWidget(self.below, 1)
        mainLayout.setSpacing(0)
        self.setLayout(mainLayout)

    # 生成general页面
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
        general = QFrame()
        general.setLayout(layout)
        self.tab.addTab(general, "general")

    # 生成下方三个按钮
    def setButtons(self):
        belowLayout = QHBoxLayout()
        belowLayout.addStretch(10)
        belowLayout.addWidget(self.ok_bt, 1)
        belowLayout.addWidget(self.cancel_bt, 1)
        belowLayout.addWidget(self.apply_bt, 1)
        belowLayout.setContentsMargins(0, 0, 0, 0)
        self.below.setLayout(belowLayout)

    # 打开文件夹
    def setExistingDirectory(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Find the image file)", self.file_name.text(
        ), "Image File (*.bmp;*.jpeg;*.jpg;*.png;*.gif)", options=options)
        if fileName:
            self.file_name.setText(fileName)

    # 设置界面居中显示
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    # # 弹出设备选择框
    # def showDevices(self):
    #     items = ("Mouse", "Keyboard")
    #     item, ok = QInputDialog.getItem(
    #         self, "Choose device", "Device:", items, 0, False)
    #     if ok and item:
    #         self.devices.addItem(item)
    #     if self.devices.count():
    #         self.devices_bt2.setEnabled(True)
    #
    # # 移除设备
    # def removeDevices(self):
    #     item = self.devices.takeItem(self.devices.currentRow())
    #     if not self.devices.count():
    #         self.devices_bt2.setEnabled(False)
    #
    # # 选中设备改变
    # def deviceChanged(self, e):
    #     if e:
    #         self.device_label.setText(e.text())
    #     else:
    #         self.device_label.clear()

    def stretchChecked(self, e):
        if e == 2:
            self.stretch_mode.setEnabled(True)
        else:
            self.stretch_mode.setEnabled(False)

    # def colorChecked(self, e):
    #     if e == 2:
    #         self.sck.setEnabled(True)
    #     else:
    #         self.sck.setEnabled(False)

    def getInfo(self):
        pass
