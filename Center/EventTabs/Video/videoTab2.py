from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import (QVBoxLayout, QFormLayout, QGroupBox, QGridLayout, QComboBox, QWidget,
                             QSpinBox, QLabel)
from ..ColorBobox import ColorListEditor


class VideoTab2(QWidget):
    def __init__(self, parent=None):
        super(VideoTab2, self).__init__(parent)
        # up
        self.width = QComboBox()
        self.height = QComboBox()
        self.xpos = QComboBox()
        self.ypos = QComboBox()
        # down
        self.border_color = ColorListEditor()
        self.border_width = QSpinBox()
        self.setUI()

    # 生成frame页面
    def setUI(self):
        group1 = QGroupBox("Geometry")
        layout1 = QGridLayout()

        self.xpos.addItems(["0", "25", "50", "75", "100"])
        self.xpos.setEditable(True)
        self.ypos.addItems(["0", "25", "50", "75", "100"])
        self.ypos.setEditable(True)
        valid_num = QRegExp("\d+%?")
        self.xpos.setValidator(QRegExpValidator(valid_num))
        self.ypos.setValidator(QRegExpValidator(valid_num))

        self.width.addItems(["100%", "75%", "50%", "25%"])
        self.width.setEditable(True)
        self.width.setValidator(QRegExpValidator(valid_num))
        self.height.addItems(["100%", "75%", "50%", "25%"])
        self.height.setEditable(True)
        self.height.setValidator(QRegExpValidator(valid_num))
        layout1.addWidget(QLabel("Width"), 0, 2)
        layout1.addWidget(self.width, 0, 3)
        layout1.addWidget(QLabel("Height"), 1, 2)
        layout1.addWidget(self.height, 1, 3)
        layout1.addWidget(QLabel("X position"), 0, 0)
        layout1.addWidget(self.xpos, 0, 1)
        layout1.addWidget(QLabel("Y position"), 1, 0)
        layout1.addWidget(self.ypos, 1, 1)
        group1.setLayout(layout1)

        group2 = QGroupBox("Border")
        layout2 = QFormLayout()
        layout2.addRow(QLabel("Border Color"), self.border_color)
        layout2.addRow(QLabel("Border Width"), self.border_width)
        layout2.setVerticalSpacing(20)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)
