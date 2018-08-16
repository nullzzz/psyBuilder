from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QGroupBox, QGridLayout, QComboBox, QWidget, QSpinBox, QLabel, \
    QMessageBox, QCompleter

from center.iconTabs.colorBobox import ColorListEditor


class Tab2(QWidget):
    def __init__(self, parent=None):
        super(Tab2, self).__init__(parent)
        self.attributes = []
        # up
        self.xpos = QComboBox()
        self.ypos = QComboBox()
        self.width = QComboBox()
        self.height = QComboBox()
        # down
        self.border_color = ColorListEditor()
        self.border_width = QSpinBox()
        self.setUI()

    # 生成frame页面
    def setUI(self):
        self.xpos.addItems(["0", "25", "50", "75", "100"])
        self.xpos.setEditable(True)
        self.ypos.addItems(["0", "25", "50", "75", "100"])
        self.ypos.setEditable(True)
        valid_num = QRegExp("\[\w+\]|\d+%?")
        self.xpos.setValidator(QRegExpValidator(valid_num))
        self.ypos.setValidator(QRegExpValidator(valid_num))
        self.xpos.setInsertPolicy(QComboBox.NoInsert)
        self.xpos.lineEdit().returnPressed.connect(self.finalCheck)
        self.ypos.setInsertPolicy(QComboBox.NoInsert)
        self.ypos.lineEdit().returnPressed.connect(self.finalCheck)
        self.xpos.lineEdit().textChanged.connect(self.findVar)
        self.xpos.lineEdit().returnPressed.connect(self.finalCheck)
        self.ypos.lineEdit().textChanged.connect(self.findVar)
        self.ypos.lineEdit().returnPressed.connect(self.finalCheck)

        self.width.addItems(["100%", "75%", "50%", "25%"])
        self.width.setEditable(True)
        self.width.setValidator(QRegExpValidator(valid_num))
        self.width.setInsertPolicy(QComboBox.NoInsert)
        self.width.lineEdit().textChanged.connect(self.findVar)
        self.width.lineEdit().returnPressed.connect(self.finalCheck)
        self.height.addItems(["100%", "75%", "50%", "25%"])
        self.height.setEditable(True)
        self.height.setValidator(QRegExpValidator(valid_num))
        self.height.setInsertPolicy(QComboBox.NoInsert)
        self.height.lineEdit().textChanged.connect(self.findVar)
        self.height.lineEdit().returnPressed.connect(self.finalCheck)

        group1 = QGroupBox("Geometry")
        layout1 = QGridLayout()
        layout1.addWidget(QLabel("X position"), 0, 0)
        layout1.addWidget(self.xpos, 0, 1)
        layout1.addWidget(QLabel("Y position"), 1, 0)
        layout1.addWidget(self.ypos, 1, 1)
        layout1.addWidget(QLabel("Width"), 0, 2)
        layout1.addWidget(self.width, 0, 3)
        layout1.addWidget(QLabel("Height"), 1, 2)
        layout1.addWidget(self.height, 1, 3)
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

    # 检查变量
    def findVar(self, text):
        if text in self.attributes:
            self.sender().setStyleSheet("color: blue")
        else:
            self.sender().setStyleSheet("color:black")

    def finalCheck(self):
        temp = self.sender()
        text = temp.text()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    # 设置可选属性
    def setAttributes(self, attributes):
        self.attributes = attributes
        self.xpos.setCompleter(QCompleter(self.attributes))
        self.ypos.setCompleter(QCompleter(self.attributes))
        self.width.setCompleter(QCompleter(self.attributes))
        self.height.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        return {
            "X position": self.xpos.currentText(),
            "Y position": self.ypos.currentText(),
            "Width": self.width.currentText(),
            "Height": self.height.currentText(),
            "Border color:": self.border_color.currentText(),
            "Border width:": self.border_width.value()}
