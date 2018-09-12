from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator, QFont
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QGroupBox, QGridLayout, QComboBox, QWidget, QSpinBox, QLabel, \
    QMessageBox, QCompleter

from center.iconTabs.colorBobox import ColorListEditor


class Tab2(QWidget):
    def __init__(self, parent=None):
        super(Tab2, self).__init__(parent)
        self.attributes = []
        # up
        self.x_pos = QComboBox()
        self.y_pos = QComboBox()
        self.width = QComboBox()
        self.height = QComboBox()
        # down
        self.border_color = ColorListEditor()
        self.border_width = QSpinBox()
        self.setUI()

    # 生成frame页面
    def setUI(self):
        self.x_pos.addItems(["0", "25", "50", "75", "100"])
        self.x_pos.setEditable(True)
        self.y_pos.addItems(["0", "25", "50", "75", "100"])
        self.y_pos.setEditable(True)
        valid_num = QRegExp("\[\w+\]|\d+%?")
        self.x_pos.setValidator(QRegExpValidator(valid_num))
        self.y_pos.setValidator(QRegExpValidator(valid_num))
        self.x_pos.setInsertPolicy(QComboBox.NoInsert)
        self.x_pos.lineEdit().returnPressed.connect(self.finalCheck)
        self.y_pos.setInsertPolicy(QComboBox.NoInsert)
        self.y_pos.lineEdit().returnPressed.connect(self.finalCheck)
        self.x_pos.lineEdit().textChanged.connect(self.findVar)
        self.x_pos.lineEdit().returnPressed.connect(self.finalCheck)
        self.y_pos.lineEdit().textChanged.connect(self.findVar)
        self.y_pos.lineEdit().returnPressed.connect(self.finalCheck)

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

        l1 = QLabel("X position:")
        l2 = QLabel("Y position:")
        l3 = QLabel("Width:")
        l4 = QLabel("Height:")
        l5 = QLabel("Border Color:")
        l6 = QLabel("Border Width:")
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        group1 = QGroupBox("Geometry")
        layout1 = QGridLayout()
        layout1.addWidget(l1, 0, 0)
        layout1.addWidget(self.x_pos, 0, 1)
        layout1.addWidget(l2, 1, 0)
        layout1.addWidget(self.y_pos, 1, 1)
        layout1.addWidget(l3, 0, 2)
        layout1.addWidget(self.width, 0, 3)
        layout1.addWidget(l4, 1, 2)
        layout1.addWidget(self.height, 1, 3)
        group1.setLayout(layout1)

        group2 = QGroupBox("Border")
        layout2 = QFormLayout()
        layout2.addRow(l5, self.border_color)
        layout2.addRow(l6, self.border_width)
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
            self.sender().setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.sender().setStyleSheet("color:black")
            self.sender().setFont(QFont("宋体", 9, QFont.Normal))

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
        self.x_pos.setCompleter(QCompleter(self.attributes))
        self.y_pos.setCompleter(QCompleter(self.attributes))
        self.width.setCompleter(QCompleter(self.attributes))
        self.height.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        return {
            "X position": self.x_pos.currentText(),
            "Y position": self.y_pos.currentText(),
            "Width": self.width.currentText(),
            "Height": self.height.currentText(),
            "Border color": self.border_color.currentText(),
            "Border width": self.border_width.value()
        }
