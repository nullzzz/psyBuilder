from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QFormLayout, QGroupBox, QGridLayout, QSpinBox, QLabel
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget)

import numpy as np
from app.lib import PigComboBox, ColorListEditor


class FramePage(QWidget):
    def __init__(self, type, parent=None):
        super(FramePage, self).__init__(parent)
        self.attributes = []
        self.pLabels    = [] # added by yang
        self.type       = type
        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Point": [["0", "0"], ["0", "0"], ["0", "0"]],
            "Width": "200",
            "Height": "200",
            "Start angle": "0",
            "End angle": "360",
            "Border color": "black",
            "Border width": '1',
            "Fill color": "white"
        }
        # up
        self.cx_pos  = PigComboBox()
        self.cy_pos  = PigComboBox()
        self.p1x_pos = PigComboBox()
        self.p1y_pos = PigComboBox()
        self.p2x_pos = PigComboBox()
        self.p2y_pos = PigComboBox()
        self.p3x_pos = PigComboBox()
        self.p3y_pos = PigComboBox()
        # self.p4x_pos = PigComboBox()
        # self.p4y_pos = PigComboBox()

        self.width = PigComboBox()
        self.height = PigComboBox()

        self.start_angle = PigComboBox()
        self.end_angle = PigComboBox()

        #各个顶点位置的类
        self.pInfo = [[self.p1x_pos, self.p1y_pos], [self.p2x_pos, self.p2y_pos], [self.p3x_pos, self.p3y_pos]]
        #各点坐标的布局
        self.pLayout = QGridLayout()

        #group1的布局
        self.gLayout = QVBoxLayout()

        # down
        self.border_color = ColorListEditor()
        self.border_width = QSpinBox()
        self.border_width.setRange(0, 20)
        self.item_color = ColorListEditor()
        self.setUI()



    #点位置的布局
    def setPointsLayout(self):
        l_cX = QLabel("Center X:")
        l_cY = QLabel("Center Y:")
        l_p1X = QLabel("P1 X:")
        l_p1Y = QLabel("P1 Y:")

        l_cX.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_cY.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_p1X.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_p1Y.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.cx_pos.addItems(["0", "25", "50", "75", "100"])
        self.cx_pos.setEditable(True)
        self.cy_pos.addItems(["0", "25", "50", "75", "100"])
        self.cy_pos.setEditable(True)

        self.pLayout.addWidget(l_cX, 0, 0)
        self.pLayout.addWidget(self.cx_pos, 0, 1)
        self.pLayout.addWidget(l_cY, 0, 2)
        self.pLayout.addWidget(self.cy_pos, 0, 3)

        self.add_bt = QPushButton("+")
        self.add_bt.clicked.connect(self.addPoint)
        self.del_bt = QPushButton("-")
        self.del_bt.clicked.connect(self.delPoint)
        self.del_bt.setEnabled(False)

        below = QWidget()
        below_layout = QHBoxLayout()
        below_layout.addStretch(3)
        below_layout.addWidget(self.add_bt, 1)
        below_layout.addWidget(self.del_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        below.setLayout(below_layout)


        self.pInfo = []

        for iVertex in range(len(self.default_properties["Point"])):
            #顶点位置
            labelX = QLabel("P{} X:".format(iVertex+1))
            labelY = QLabel("P{} Y:".format(iVertex+1))

            x_pos = PigComboBox()
            y_pos = PigComboBox()

            x_pos.addItems(["0", "25", "50", "75", "100"])
            x_pos.setEditable(True)
            y_pos.addItems(["0", "25", "50", "75", "100"])
            y_pos.setEditable(True)

            labelX.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            labelY.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.pLayout.addWidget(labelX, iVertex + 1, 0)
            self.pLayout.addWidget(x_pos, iVertex + 1, 1)
            self.pLayout.addWidget(labelY, iVertex + 1, 2)
            self.pLayout.addWidget(y_pos, iVertex + 1, 3)

            p = [x_pos, y_pos]
            self.pInfo.append(p)

        top = QWidget()
        top.setLayout(self.pLayout)

        self.gLayout.addWidget(top, 6)
        self.gLayout.addWidget(below, 1)
        self.gLayout.setSpacing(0)

    def addPoint(self):

        if len(self.pInfo) == 20:
            self.add_bt.setEnabled(False)
            return
        #顶点位置改变
        self.default_properties["Point"].append(["0", "0"])

        x_pos = PigComboBox()
        y_pos = PigComboBox()

        x_pos.addItems(["0", "25", "50", "75", "100"])
        x_pos.setEditable(True)
        y_pos.addItems(["0", "25", "50", "75", "100"])
        y_pos.setEditable(True)
        p = [x_pos, y_pos]

        self.pInfo.append(p)

        #给顶点赋值
        # get center axis of the stimulus
        x = int(self.default_properties["Center X"])
        y = int(self.default_properties["Center Y"])

        nVertices = len(self.default_properties["Point"])
        for iVertex in range(nVertices):
            try:
                self.default_properties["Point"][iVertex][0] = str(x + int(100 * np.cos(np.pi/2 - iVertex*2*np.pi/nVertices)))
                self.default_properties["Point"][iVertex][1] = str(y + int(100 * np.sin(iVertex * 2 * np.pi / nVertices - np.pi / 2)))
            except Exception as e:
                print(e)

        for iVertex in range(len(self.pInfo)):
            self.pInfo[iVertex][0].setCurrentText(self.default_properties["Point"][iVertex][0])
            self.pInfo[iVertex][1].setCurrentText(self.default_properties["Point"][iVertex][1])

        labelX = QLabel("P{} X:".format(len(self.pInfo)))
        labelY = QLabel("P{} Y:".format(len(self.pInfo)))

        labelX.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        labelY.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.pLayout.addWidget(labelX, len(self.pInfo) + 1, 0)
        self.pLayout.addWidget(self.pInfo[-1][0], len(self.pInfo) + 1, 1)
        self.pLayout.addWidget(labelY, len(self.pInfo) + 1, 2)
        self.pLayout.addWidget(self.pInfo[-1][1], len(self.pInfo) + 1, 3)

        # self.plabels = [] # a bug here
        self.pLabels.append([labelX, labelY])
        self.del_bt.setEnabled(True)


    def delPoint(self):
        self.default_properties["Point"].pop(-1)
        x1 = self.pInfo[-1][0]
        x2 = self.pInfo[-1][1]

        y1 = self.pLabels[-1][0]
        y2 = self.pLabels[-1][1]

        self.pInfo.pop(-1)
        self.pLabels.pop(-1)

        x1.deleteLater()
        x2.deleteLater()
        y1.deleteLater()
        y2.deleteLater()

        #给其他顶点赋值
        x = int(self.default_properties["Center X"])
        y = int(self.default_properties["Center Y"])
        n = len(self.default_properties["Point"])

        for iVertex in range(n):
            try:
                self.default_properties["Point"][iVertex][0] = str(x + int(100 * np.cos(np.pi / 2 - iVertex * 2 * np.pi / n)))
                self.default_properties["Point"][iVertex][1] = str(y + int(100 * np.sin(iVertex * 2 * np.pi / n - np.pi / 2)))
            except Exception as e:
                print(e)

        for iVertex in range(len(self.pInfo)):
            self.pInfo[iVertex][0].setCurrentText(self.default_properties["Point"][iVertex][0])
            self.pInfo[iVertex][1].setCurrentText(self.default_properties["Point"][iVertex][1])

        if len(self.pInfo) == 3:
            self.del_bt.setEnabled(False)

    # 生成frame页面
    def setUI(self):
        self.cx_pos.addItems(["0", "25", "50", "75", "100"])
        self.cx_pos.setEditable(True)
        self.cy_pos.addItems(["0", "25", "50", "75", "100"])
        self.cy_pos.setEditable(True)

        self.width.addItems(["200", "300", "400","500", "600"])
        self.width.setEditable(True)
        self.height.addItems(["200", "300", "400","500", "600"])
        self.height.setEditable(True)

        self.start_angle.addItems(["0", "90", "180","270", "360"])
        self.start_angle.setEditable(True)
        self.end_angle.addItems(["0", "90", "180","270", "360"])
        self.end_angle.setEditable(True)

        valid_num = QRegExp("\d+")
        self.cx_pos.setValidator(QRegExpValidator(valid_num))
        self.cy_pos.setValidator(QRegExpValidator(valid_num))

        self.width.setValidator(QRegExpValidator(valid_num))
        self.height.setValidator(QRegExpValidator(valid_num))

        self.start_angle.setValidator(QRegExpValidator(valid_num))
        self.end_angle.setValidator(QRegExpValidator(valid_num))

        for vertex in self.pInfo:
            vertex[0].addItems(["0", "25", "50", "75", "100"])
            vertex[0].setEditable(True)
            vertex[1].addItems(["0", "25", "50", "75", "100"])
            vertex[1].setEditable(True)
            vertex[0].setValidator(QRegExpValidator(valid_num))
            vertex[1].setValidator(QRegExpValidator(valid_num))

        l_cX = QLabel("Center X:")
        l_cY = QLabel("Center Y:")
        l_p1X = QLabel("P1 X:")
        l_p1Y = QLabel(" Y:")
        l_p2X = QLabel("P2 X:")
        l_p2Y = QLabel(" Y:")
        l_p3X = QLabel("P3 X:")
        l_p3Y = QLabel(" Y:")

        l_p4X = QLabel("P4 X:")
        l_p4Y = QLabel(" Y:")

        l_width = QLabel("Width:")
        l_height = QLabel("Height:")

        l_start_angle = QLabel("Start Angle°:")
        l_end_angle = QLabel("End Angle°:")

        l_borderColor = QLabel("Border Color:")
        l_borderWidth = QLabel("Border Width:")
        l_fillColor = QLabel("Fill Color")

        l_cX.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_cY.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_p1X.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_p1Y.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_p2X.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_p2Y.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_p3X.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_p3Y.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l_p4X.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_p4Y.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l_width.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_height.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l_start_angle.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_end_angle.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l_borderColor.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_borderWidth.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_fillColor.setAlignment(Qt.AlignRight | Qt.AlignVCenter)


        group1  = QGroupBox("Geometry")
        layout1 = QGridLayout()
        #polygons
        if self.type == 'polygonStim':
            self.setPointsLayout()
            layout1 = self.gLayout

        # lines
        elif self.type == 'line':
            layout1.addWidget(l_p1X, 0, 0)
            layout1.addWidget(self.p1x_pos, 0, 1)
            layout1.addWidget(l_p1Y, 0, 2)
            layout1.addWidget(self.p1y_pos, 0, 3)
            layout1.addWidget(l_p2X, 1, 0)
            layout1.addWidget(self.p2x_pos, 1, 1)
            layout1.addWidget(l_p2Y, 1, 2)
            layout1.addWidget(self.p2y_pos, 1, 3)
        elif self.type == 'arc':
            layout1.addWidget(l_cX, 0, 0)
            layout1.addWidget(self.cx_pos, 0, 1)
            layout1.addWidget(l_cY, 0, 2)
            layout1.addWidget(self.cy_pos, 0, 3)

            layout1.addWidget(l_width, 1, 0)
            layout1.addWidget(self.width, 1, 1)
            layout1.addWidget(l_height, 1, 2)
            layout1.addWidget(self.height, 1, 3)

            layout1.addWidget(l_start_angle, 2, 0)
            layout1.addWidget(self.start_angle, 2, 1)
            layout1.addWidget(l_end_angle, 2, 2)
            layout1.addWidget(self.end_angle, 2, 3)
        else:
            layout1.addWidget(l_cX, 0, 0)
            layout1.addWidget(self.cx_pos, 0, 1)
            layout1.addWidget(l_cY, 0, 2)
            layout1.addWidget(self.cy_pos, 0, 3)

            layout1.addWidget(l_width, 1, 0)
            layout1.addWidget(self.width, 1, 1)
            layout1.addWidget(l_height, 1, 2)
            layout1.addWidget(self.height, 1, 3)

        group1.setLayout(layout1)

        group2 = QGroupBox("")
        layout2 = QFormLayout()
        layout2.addRow(l_borderColor, self.border_color)
        layout2.addRow(l_borderWidth, self.border_width)

        if self.type != 'line':
            layout2.addRow(l_fillColor, self.item_color)

        layout2.setVerticalSpacing(20)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)


    # 设置可选属性
    def setAttributes(self, attributes):
        self.attributes = attributes

    def getInfo(self):
        self.default_properties['Center X'] = self.cx_pos.currentText()
        self.default_properties['Center Y'] = self.cy_pos.currentText()

        for iVertex in range(len(self.pInfo)):
            self.default_properties["Point"][iVertex][0] = self.pInfo[iVertex][0].currentText()
            self.default_properties["Point"][iVertex][1] = self.pInfo[iVertex][1].currentText()

        self.default_properties['Width']        = self.width.currentText()
        self.default_properties['Height']       = self.height.currentText()
        self.default_properties['Start angle']  = self.start_angle.currentText()
        self.default_properties['End angle']    = self.end_angle.currentText()
        self.default_properties['Border width'] = str(self.border_width.value())
        self.default_properties['Border color'] = self.border_color.currentText()
        self.default_properties['Fill color']   = self.item_color.currentText()

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

        for i in range(len(self.pInfo)):
            self.pInfo[i][0].setCurrentText(self.default_properties["Point"][i][0])
            self.pInfo[i][1].setCurrentText(self.default_properties["Point"][i][1])

        self.width.setCurrentText(self.default_properties["Width"])
        self.height.setCurrentText(self.default_properties["Height"])

        self.start_angle.setCurrentText(self.default_properties["Start angle"])
        self.end_angle.setCurrentText(self.default_properties["End angle"])

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
        self.ok_bt     = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt  = QPushButton("Apply")
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
