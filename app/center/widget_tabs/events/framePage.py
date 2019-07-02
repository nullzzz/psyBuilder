from PyQt5.QtCore import Qt, QObject, QEvent
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QGroupBox, QGridLayout, QComboBox, QWidget, QLabel, \
    QMessageBox, QCompleter

from app.lib import PigComboBox, PigLineEdit, ColorListEditor


class FramePage(QWidget):
    def __init__(self, parent=None):
        super(FramePage, self).__init__(parent)
        self.attributes = []
        self.default_properties = {
            "X position": "0",
            "Y position": "0",
            "Width": "100%",
            "Height": "100%",
            "Border color": "255,255,255",
            "Border width": "0"
        }
        # up
        self.x_pos = PigComboBox()
        self.y_pos = PigComboBox()
        self.width = PigComboBox()
        self.height = PigComboBox()
        self.x_pos.installEventFilter(self)
        self.y_pos.installEventFilter(self)
        self.width.installEventFilter(self)
        self.height.installEventFilter(self)
        # down
        self.border_color = ColorListEditor()
        self.border_width = PigLineEdit()
        self.back_color = ColorListEditor()
        self.setUI()

    # 生成frame页面
    def setUI(self):
        self.x_pos.addItems(["0", "25", "50", "75", "100"])
        self.x_pos.setEditable(True)
        self.y_pos.addItems(["0", "25", "50", "75", "100"])
        self.y_pos.setEditable(True)
        self.x_pos.setInsertPolicy(QComboBox.NoInsert)
        self.y_pos.setInsertPolicy(QComboBox.NoInsert)

        self.border_width.setText("0")

        self.width.addItems(("100%", "75%", "50%", "25%"))
        self.width.setEditable(True)
        self.width.setInsertPolicy(QComboBox.NoInsert)

        self.height.addItems(("100%", "75%", "50%", "25%"))
        self.height.setEditable(True)
        self.height.setInsertPolicy(QComboBox.NoInsert)

        l1 = QLabel("X position:")
        l2 = QLabel("Y position:")
        l3 = QLabel("Width:")
        l4 = QLabel("Height:")
        l5 = QLabel("Border Color:")
        l6 = QLabel("Border Width:")
        l7 = QLabel("Back Color:")
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
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
        layout2.addRow(l7, self.back_color)
        layout2.setVerticalSpacing(20)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 设置可选属性
    def setAttributes(self, attributes):
        self.attributes = attributes
        self.x_pos.setCompleter(QCompleter(self.attributes))
        self.y_pos.setCompleter(QCompleter(self.attributes))
        self.width.setCompleter(QCompleter(self.attributes))
        self.height.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        """
        写的这是什么shit
        :return:
        """
        self.default_properties.clear()
        x_pos = self.x_pos.currentText()
        y_pos = self.y_pos.currentText()
        width = self.width.currentText()
        height = self.height.currentText()
        if x_pos:
            self.default_properties["X position"] = x_pos
        else:
            self.default_properties["X position"] = "0"
            self.x_pos.setCurrentText("0")
        if y_pos:
            self.default_properties["Y position"] = y_pos
        else:
            self.default_properties["Y position"] = "0"
            self.y_pos.setCurrentText("0")
        if width:
            self.default_properties["Width"] = self.width.currentText()
        else:
            self.default_properties["Width"] = "100%"
            self.width.setCurrentText("100%")
        if height:
            self.default_properties["Height"] = self.height.currentText()
        else:
            self.default_properties["Height"] = "100%"
            self.height.setCurrentText("100%")
        self.default_properties["Border color"] = self.border_color.getColor()
        self.default_properties["Border width"] = self.border_width.text()
        self.default_properties["Frame color"] = self.back_color.getColor()
        return self.default_properties

    def getProperties(self):
        self.default_properties.clear()
        self.default_properties["X position"] = self.x_pos.currentText()
        self.default_properties["Y position"] = self.y_pos.currentText()
        self.default_properties["Width"] = self.width.currentText()
        self.default_properties["Height"] = self.height.currentText()
        self.default_properties["Border color"] = self.border_color.getColor()
        self.default_properties["Border width"] = self.border_width.text()
        self.default_properties["Frame color"] = self.back_color.getColor()
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties.copy()
        self.loadSetting()

    # 加载参数设置
    def loadSetting(self):
        self.x_pos.setCurrentText(self.default_properties["X position"])
        self.y_pos.setCurrentText(self.default_properties["Y position"])
        self.width.setCurrentText(self.default_properties["Width"])
        self.height.setCurrentText(self.default_properties["Height"])
        self.border_color.setCurrentText(self.default_properties["Border color"])
        self.border_width.setText(self.default_properties["Border width"])
        self.back_color.setText(self.default_properties["Frame color"])

    def clone(self):
        clone_page = FramePage()
        clone_page.setProperties(self.default_properties)
        return clone_page

    def eventFilter(self, obj: QObject, e: QEvent):
        if obj == self.x_pos or obj == self.y_pos:
            obj: QComboBox
            if e.type() == QEvent.FocusOut:
                text: str = obj.currentText()
                if text not in self.attributes:
                    if text:
                        if text[0] == "[":
                            QMessageBox.warning(self, "Warning", "Invalid Attribute!", buttons=QMessageBox.Ok)
                            obj.setCurrentIndex(0)
                    else:
                        QMessageBox.warning(self, "Warning", "Attribute cannot be none!", QMessageBox.Ok)
                        obj.setCurrentIndex(0)
        return QWidget.eventFilter(self, obj, e)
