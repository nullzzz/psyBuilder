from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator, QDoubleValidator, QIntValidator
from PyQt5.QtWidgets import QGroupBox, QGridLayout, QLabel
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget)

from app.lib import PigComboBox


class FramePage(QWidget):
    def __init__(self, parent=None):
        super(FramePage, self).__init__(parent)
        self.attributes = []
        self.type = type
        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Width": "100",
            "Height": "100",
            "spatialFreq(cycles/pixel)": "0.033",
            "Contrast": "1",
            "phase": "0",
            "orientation": "0",
            "bkColor": "128,128,128",
            "SDx(pixels)": "30",
            "SDy(pixels)": "30",
            "rotation": "0",
            "Transparency": "0"
        }
        # up
        self.cx_pos = PigComboBox()
        self.cy_pos = PigComboBox()
        self._width = PigComboBox()
        self._height = PigComboBox()
        self.spFreq = PigComboBox()
        self.contrast = PigComboBox()
        self.phase = PigComboBox()
        self.orientation = PigComboBox()
        self.bkcolor = PigComboBox()
        self.sdx = PigComboBox()
        self.sdy = PigComboBox()
        self.rotation = PigComboBox()
        self.transparency = PigComboBox()
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
        self.setUI()

    # 生成frame页面
    def setUI(self):
        self.cx_pos.addItems(["0", "25", "50", "75", "100"])
        self.cx_pos.setEditable(True)
        self.cy_pos.addItems(["0", "25", "50", "75", "100"])
        self.cy_pos.setEditable(True)
        self._width.addItems(["0", "25", "50", "75", "100"])
        self._width.setEditable(True)
        self._height.addItems(["0", "25", "50", "75", "100"])
        self._height.setEditable(True)
        self.spFreq.addItems(["0.01", "0.02", "0.04", "0.06", "0.08"])
        self.spFreq.setEditable(True)
        self.contrast.addItems(["0", "0.2", "0.4", "0.6", "0.8"])
        self.contrast.setEditable(True)
        self.phase.addItems(["0", "20", "40", "60", "80"])
        self.phase.setEditable(True)
        self.orientation.addItems(["0", "45", "90", "135", "180"])
        self.orientation.setEditable(True)
        self.sdx.addItems(["20", "30", "40", "60", "80"])
        self.sdx.setEditable(True)
        self.sdy.addItems(["20", "30", "40", "60", "80"])
        self.sdy.setEditable(True)
        self.rotation.addItems(["0", "45", "90", "135", "180"])
        self.rotation.setEditable(True)
        self.transparency.addItems(["0", "45", "90", "135", "180"])
        self.transparency.setEditable(True)
        self.bkcolor.addItems(["0,0,0", "64,64,64", "128,128,128", "192,192,192", "255,255,255"])
        self.bkcolor.setEditable(True)
        valid_num = QRegExp("\d+")
        valid_rgb = QRegExp("(([0-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5]))),\
                            (([0-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5]))),(([0-9]|([1-9]\d)|(1\d\d)|(2([0-4]\d|5[0-5])))")
        # 整数验证不可行
        v1 = QIntValidator(1, 20, self)
        v2 = QDoubleValidator()
        self.cx_pos.setValidator(QRegExpValidator(valid_num))
        self.cy_pos.setValidator(QRegExpValidator(valid_num))
        self._width.setValidator(QRegExpValidator(valid_num))
        self._height.setValidator(QRegExpValidator(valid_num))
        self.spFreq.setValidator(v2)
        self.contrast.setValidator(v2)
        self.phase.setValidator(v2)
        self.orientation.setValidator(v2)
        self.sdx.setValidator(v2)
        self.sdy.setValidator(v2)
        self.rotation.setValidator(v2)
        self.bkcolor.setValidator(QRegExpValidator(valid_rgb))

        l1 = QLabel("Center X:")
        l2 = QLabel(" Y:")
        l3 = QLabel("Width:")
        l4 = QLabel("Height:")
        l5 = QLabel("spatialFreq(cycles/pixel):")
        l6 = QLabel("Contrast(0~1）:")
        l7 = QLabel("phase:")
        l8 = QLabel("orientation:")
        _21 = QLabel("SDx(pixels):")
        _22 = QLabel("SDy(pixels):")
        _23 = QLabel("bkColor")
        _24 = QLabel("rotation")
        _25 = QLabel("Transparency")

        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l8.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _22.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _23.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _24.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        _25.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox("")
        layout1 = QGridLayout()
        layout1.addWidget(l1, 0, 0)
        layout1.addWidget(self.cx_pos, 0, 1)
        layout1.addWidget(l2, 0, 2)
        layout1.addWidget(self.cy_pos, 0, 3)
        layout1.addWidget(l3, 1, 0)
        layout1.addWidget(self._width, 1, 1)
        layout1.addWidget(l4, 1, 2)
        layout1.addWidget(self._height, 1, 3)

        layout1.addWidget(l5, 2, 0)
        layout1.addWidget(self.spFreq, 2, 1)
        layout1.addWidget(l6, 2, 2)
        layout1.addWidget(self.contrast, 2, 3)
        layout1.addWidget(l7, 3, 0)
        layout1.addWidget(self.phase, 3, 1)
        layout1.addWidget(l8, 3, 2)
        layout1.addWidget(self.orientation, 3, 3)

        layout1.addWidget(_23, 4, 0)
        layout1.addWidget(self.bkcolor, 4, 1)
        layout1.addWidget(_24, 4, 2)
        layout1.addWidget(self.rotation, 4, 3)
        layout1.addWidget(_21, 5, 0)
        layout1.addWidget(self.sdx, 5, 1)
        layout1.addWidget(_22, 5, 2)
        layout1.addWidget(self.sdy, 5, 3)
        layout1.addWidget(_25, 6, 0)
        layout1.addWidget(self.transparency, 6, 1)

        group1.setLayout(layout1)
        layout = QVBoxLayout()
        layout.addWidget(group1)
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

    def setPos(self, x, y):
        self.cx_pos.setCurrentText(str(int(x)))
        self.cy_pos.setCurrentText(str(int(y)))

    def getInfo(self):
        self.default_properties['Center X'] = self.cx_pos.currentText()
        self.default_properties['Center Y'] = self.cy_pos.currentText()
        self.default_properties['Width'] = self._width.currentText()
        self.default_properties['Height'] = self._height.currentText()
        self.default_properties['spatialFreq(cycles/pixel)'] = self.spFreq.currentText()
        self.default_properties['Contrast'] = self.contrast.currentText()
        self.default_properties['phase'] = self.phase.currentText()
        self.default_properties['orientation'] = self.orientation.currentText()
        self.default_properties['bkColor'] = self.bkcolor.currentText()
        self.default_properties['SDx(pixels)'] = self.sdx.currentText()
        self.default_properties['SDy(pixels)'] = self.sdy.currentText()
        self.default_properties['rotation'] = self.rotation.currentText()

        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    # 加载参数设置
    def loadSetting(self):
        self.cx_pos.setCurrentText(self.default_properties["Center X"])
        self.cy_pos.setCurrentText(self.default_properties["Center Y"])
        self._width.setCurrentText(self.default_properties["Width"])
        self._height.setCurrentText(self.default_properties["Height"])

        self.spFreq.setCurrentText(self.default_properties["spatialFreq(cycles/pixel)"])
        self.contrast.setCurrentText(self.default_properties["Contrast"])
        self.phase.setCurrentText(self.default_properties["phase"])
        self.orientation.setCurrentText(self.default_properties["orientation"])

        self.bkcolor.setCurrentText(self.default_properties["bkColor"])
        self.sdx.setCurrentText(self.default_properties['SDx(pixels)'])
        self.sdy.setCurrentText(self.default_properties['SDy(pixels)'])
        self.rotation.setCurrentText(self.default_properties["rotation"])

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


class gaborProperty(QWidget):
    def __init__(self, parent=None):
        super(gaborProperty, self).__init__(parent)
        self.below = QWidget()

        self.frame = FramePage()
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
