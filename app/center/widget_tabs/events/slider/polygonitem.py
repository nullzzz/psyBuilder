from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QFormLayout, QGroupBox, QGridLayout, QSpinBox, QLabel
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget)

from app.center.widget_tabs.colorBobox import ColorListEditor
from app.lib import PigComboBox


class FramePage(QWidget):
    def __init__(self, type, parent=None):
        super(FramePage, self).__init__(parent)
        self.attributes = []
        self.type = type
        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "P1 X": "0",
            "P1 Y": "0",
            "P2 X": "0",
            "P2 Y": "0",
            "P3 X": "0",
            "P3 Y": "0",
            "P4 X": "0",
            "P4 Y": "0",
            "Long axis": "0",
            "Short axis": "0",
            "Border color": "black",
            "Border width": '1',
            "Fill color": "white"
        }
        # up
        self.cx_pos = PigComboBox()
        self.cy_pos = PigComboBox()
        self.p1x_pos = PigComboBox()
        self.p1y_pos = PigComboBox()
        self.p2x_pos = PigComboBox()
        self.p2y_pos = PigComboBox()
        self.p3x_pos = PigComboBox()
        self.p3y_pos = PigComboBox()
        self.p4x_pos = PigComboBox()
        self.p4y_pos = PigComboBox()
        self.La = PigComboBox()
        self.Sa = PigComboBox()
        # self.cx_pos.installEventFilter(self)
        # self.cy_pos.installEventFilter(self)
        # self.p1x_pos.installEventFilter(self)
        # self.p1y_pos.installEventFilter(self)
        # self.p2x_pos.installEventFilter(self)
        # self.p2y_pos.installEventFilter(self)
        # self.p3x_pos.installEventFilter(self)
        # self.p3y_pos.installEventFilter(self)
        # self.p4x_pos.installEventFilter(self)
        # self.p4y_pos.installEventFilter(self)
        # self.La.installEventFilter(self)
        # self.Sa.installEventFilter(self)

        # down
        self.border_color = ColorListEditor()
        self.border_width = QSpinBox()
        self.border_width.setRange(0, 20)
        self.item_color = ColorListEditor()
        self.setUI()

    # 生成frame页面
    def setUI(self):
        self.cx_pos.addItems(["0", "25", "50", "75", "100"])
        self.cx_pos.setEditable(True)
        self.cy_pos.addItems(["0", "25", "50", "75", "100"])
        self.cy_pos.setEditable(True)
        self.p1x_pos.addItems(["0", "25", "50", "75", "100"])
        self.p1x_pos.setEditable(True)
        self.p1y_pos.addItems(["0", "25", "50", "75", "100"])
        self.p1y_pos.setEditable(True)
        self.p2x_pos.addItems(["0", "25", "50", "75", "100"])
        self.p2x_pos.setEditable(True)
        self.p2y_pos.addItems(["0", "25", "50", "75", "100"])
        self.p2y_pos.setEditable(True)
        self.p3x_pos.addItems(["0", "25", "50", "75", "100"])
        self.p3x_pos.setEditable(True)
        self.p3y_pos.addItems(["0", "25", "50", "75", "100"])
        self.p3y_pos.setEditable(True)
        self.p4x_pos.addItems(["0", "25", "50", "75", "100"])
        self.p4x_pos.setEditable(True)
        self.p4y_pos.addItems(["0", "25", "50", "75", "100"])
        self.p4y_pos.setEditable(True)
        self.La.addItems(["0", "25", "50", "75", "100"])
        self.La.setEditable(True)
        self.Sa.addItems(["0", "25", "50", "75", "100"])
        self.Sa.setEditable(True)
        valid_num = QRegExp("\d+")
        self.cx_pos.setValidator(QRegExpValidator(valid_num))
        self.cy_pos.setValidator(QRegExpValidator(valid_num))
        self.p1x_pos.setValidator(QRegExpValidator(valid_num))
        self.p1y_pos.setValidator(QRegExpValidator(valid_num))
        self.p2x_pos.setValidator(QRegExpValidator(valid_num))
        self.p2y_pos.setValidator(QRegExpValidator(valid_num))
        self.p3x_pos.setValidator(QRegExpValidator(valid_num))
        self.p3y_pos.setValidator(QRegExpValidator(valid_num))
        self.p4x_pos.setValidator(QRegExpValidator(valid_num))
        self.p4y_pos.setValidator(QRegExpValidator(valid_num))
        self.La.setValidator(QRegExpValidator(valid_num))
        self.Sa.setValidator(QRegExpValidator(valid_num))

        l1 = QLabel("Center X:")
        l2 = QLabel(" Y:")
        l3 = QLabel("P1 X:")
        l4 = QLabel(" Y:")
        l5 = QLabel("P2 X:")
        l6 = QLabel(" Y:")
        l7 = QLabel("P3 X:")
        l8 = QLabel(" Y:")
        l9 = QLabel("P4 X:")
        _21 = QLabel(" Y:")
        _22 = QLabel("Long axis:")
        _23 = QLabel("Short axis:")
        _24 = QLabel("Border Color:")
        _25 = QLabel("Border Width:")
        _26 = QLabel("Fill Color")
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l9.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _24.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _25.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _26.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox("Geometry")
        layout1 = QGridLayout()
        if self.type == 'four':
            layout1.addWidget(l1, 0, 0)
            layout1.addWidget(self.cx_pos, 0, 1)
            layout1.addWidget(l2, 0, 2)
            layout1.addWidget(self.cy_pos, 0, 3)
            layout1.addWidget(l3, 1, 0)
            layout1.addWidget(self.p1x_pos, 1, 1)
            layout1.addWidget(l4, 1, 2)
            layout1.addWidget(self.p1y_pos, 1, 3)
            layout1.addWidget(l5, 2, 0)
            layout1.addWidget(self.p2x_pos, 2, 1)
            layout1.addWidget(l6, 2, 2)
            layout1.addWidget(self.p2y_pos, 2, 3)
            layout1.addWidget(l7, 3, 0)
            layout1.addWidget(self.p3x_pos, 3, 1)
            layout1.addWidget(l8, 3, 2)
            layout1.addWidget(self.p3y_pos, 3, 3)
            layout1.addWidget(l9, 4, 0)
            layout1.addWidget(self.p4x_pos, 4, 1)
            layout1.addWidget(_21, 4, 2)
            layout1.addWidget(self.p4y_pos, 4, 3)
        elif self.type == 'two':
            layout1.addWidget(l1, 0, 0)
            layout1.addWidget(self.cx_pos, 0, 1)
            layout1.addWidget(l2, 0, 2)
            layout1.addWidget(self.cy_pos, 0, 3)
            layout1.addWidget(l3, 1, 0)
            layout1.addWidget(self.p1x_pos, 1, 1)
            layout1.addWidget(l4, 1, 2)
            layout1.addWidget(self.p1y_pos, 1, 3)
            layout1.addWidget(l5, 2, 0)
            layout1.addWidget(self.p2x_pos, 2, 1)
            layout1.addWidget(l6, 2, 2)
            layout1.addWidget(self.p2y_pos, 2, 3)
        else:
            layout1.addWidget(l1, 0, 0)
            layout1.addWidget(self.cx_pos, 0, 1)
            layout1.addWidget(l2, 0, 2)
            layout1.addWidget(self.cy_pos, 0, 3)
            layout1.addWidget(_22, 1, 0)
            layout1.addWidget(self.La, 1, 1)
            layout1.addWidget(_23, 1, 2)
            layout1.addWidget(self.Sa, 1, 3)

        group1.setLayout(layout1)

        group2 = QGroupBox("")
        layout2 = QFormLayout()
        layout2.addRow(_24, self.border_color)
        layout2.addRow(_25, self.border_width)
        if self.type != 'two':
            layout2.addRow(_26, self.item_color)
        layout2.setVerticalSpacing(20)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 检查变量
    # def findVar(self, text):
    #     if text in self.attributes:
    #         self.sender().setStyleSheet("color: blue")
    #         self.sender().setFont(QFont("Timers", 9, QFont.Bold))
    #     else:
    #         self.sender().setStyleSheet("color:black")
    #         self.sender().setFont(QFont("宋体", 9, QFont.Normal))

    # def finalCheck(self):
    #     temp = self.sender()
    #     text = temp.text()
    #     if text not in self.attributes:
    #         if text and text[0] == "[":
    #             QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
    #             temp.clear()

    # 设置可选属性
    def setAttributes(self, attributes):
        self.attributes = attributes
        # self.x_pos.setCompleter(QCompleter(self.attributes))
        # self.y_pos.setCompleter(QCompleter(self.attributes))
        # self.width.setCompleter(QCompleter(self.attributes))
        # self.height.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        self.default_properties['Center X'] = self.cx_pos.currentText()
        self.default_properties['Center Y'] = self.cy_pos.currentText()
        self.default_properties['P1 X'] = self.p1x_pos.currentText()
        self.default_properties['P1 Y'] = self.p1y_pos.currentText()
        self.default_properties['P2 X'] = self.p2x_pos.currentText()
        self.default_properties['P2 Y'] = self.p2y_pos.currentText()
        self.default_properties['P3 X'] = self.p3x_pos.currentText()
        self.default_properties['P3 Y'] = self.p3y_pos.currentText()
        self.default_properties['P4 X'] = self.p4x_pos.currentText()
        self.default_properties['P4 Y'] = self.p4y_pos.currentText()
        self.default_properties['Long axis'] = self.La.currentText()
        self.default_properties['Short axis'] = self.Sa.currentText()
        self.default_properties['Border width'] = str(self.border_width.value())
        self.default_properties['Border color'] = self.border_color.currentText()
        self.default_properties['Fill color'] = self.item_color.currentText()

        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def setPos(self, x, y):
        self.cx_pos.setCurrentText(str(int(x)))
        self.cy_pos.setCurrentText(str(int(y)))

    # 加载参数设置
    def loadSetting(self):
        self.cx_pos.setCurrentText(self.default_properties["Center X"])
        self.cy_pos.setCurrentText(self.default_properties["Center Y"])
        self.p1x_pos.setCurrentText(self.default_properties["P1 X"])
        self.p1y_pos.setCurrentText(self.default_properties["P1 Y"])
        self.p2x_pos.setCurrentText(self.default_properties["P2 X"])
        self.p2y_pos.setCurrentText(self.default_properties["P2 Y"])
        self.p3x_pos.setCurrentText(self.default_properties["P3 X"])
        self.p3y_pos.setCurrentText(self.default_properties["P3 Y"])
        self.p4x_pos.setCurrentText(self.default_properties["P4 X"])
        self.p4y_pos.setCurrentText(self.default_properties["P4 Y"])
        self.La.setCurrentText(self.default_properties["Long axis"])
        self.Sa.setCurrentText(self.default_properties["Short axis"])
        self.border_color.setCurrentText(self.default_properties["Border color"])
        self.border_width.setValue(int(self.default_properties["Border width"]))
        self.item_color.setCurrentText(self.default_properties['Fill color'])

    # def clone(self):
    #     clone_page = FramePage()
    #     clone_page.setProperties(self.default_properties)
    #     return clone_page

    # def eventFilter(self, obj: QObject, e: QEvent):
    #     if obj == self.x_pos or obj == self.y_pos:
    #         obj: PigComboBox
    #         if e.type() == QEvent.FocusOut:
    #             text: str = obj.currentText()
    #             if text not in self.attributes:
    #                 if text:
    #                     if text[0] == "[":
    #                         QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
    #                         obj.setCurrentIndex(0)
    #                 else:
    #                     QMessageBox.warning(self, "Warning", "Attribute cannot be none!", QMessageBox.Ok)
    #                     obj.setCurrentIndex(0)
    #     return QWidget.eventFilter(self, obj, e)


class polygonProperty(QWidget):
    def __init__(self, type, parent=None):
        super(polygonProperty, self).__init__(parent)
        self.below = QWidget()

        self.frame = FramePage(type)
        self.default_properties = {**self.frame.default_properties}
        # bottom
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.setButtons()

        self.setUI()

    # 生成主界面
    def setUI(self):
        self.setWindowTitle("Property")
        self.resize(600, 800)
        # self.setFixedSize(600, 800)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.frame, 6)
        # main_layout.addStretch(2)
        main_layout.addWidget(self.below, 1)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    # 生成下方三个按钮
    def setButtons(self):
        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        self.below.setLayout(below_layout)

    # 设置界面居中显示
    def center(self):
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def getInfo(self):
        self.default_properties = {**self.frame.getInfo()}
        return self.default_properties

    def setAttributes(self, attributes):
        self.frame.setAttributes(attributes)

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def loadSetting(self):
        self.frame.setProperties(self.default_properties)
