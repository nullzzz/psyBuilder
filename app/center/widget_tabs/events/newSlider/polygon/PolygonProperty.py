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
        self.plabels = []  # added by yang
        self.type = type
        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Point": [["0", "0"], ["0", "0"], ["0", "0"]],
            "start": "0",
            "end angle": "360",
            "Border color": "black",
            "Border width": '1',
            "Fill color": "white"
        }
        # print(f"{self.default_properties}")
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

        # 各个顶点位置的类
        self.pinfo = [[self.p1x_pos, self.p1y_pos], [self.p2x_pos, self.p2y_pos], [self.p3x_pos, self.p3y_pos]]
        # 各点坐标的布局
        self.playout = QGridLayout()

        # group1的布局
        self.glayout = QVBoxLayout()

        # down
        self.border_color = ColorListEditor()
        self.border_width = QSpinBox()
        self.border_width.setRange(0, 20)
        self.item_color = ColorListEditor()
        self.setUI()

    # 点位置的布局
    def setplayout(self):
        l1 = QLabel("Center X:")
        l2 = QLabel(" Y:")
        l3 = QLabel("P1 X:")
        l4 = QLabel(" Y:")
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.cx_pos.addItems(["0", "25", "50", "75", "100"])
        self.cx_pos.setEditable(True)
        self.cy_pos.addItems(["0", "25", "50", "75", "100"])
        self.cy_pos.setEditable(True)

        self.playout.addWidget(l1, 0, 0)
        self.playout.addWidget(self.cx_pos, 0, 1)
        self.playout.addWidget(l2, 0, 2)
        self.playout.addWidget(self.cy_pos, 0, 3)

        self.add_bt = QPushButton("+")
        self.add_bt.clicked.connect(self.addpoint)
        self.del_bt = QPushButton("-")
        self.del_bt.clicked.connect(self.delpoint)
        self.del_bt.setEnabled(False)

        below = QWidget()
        below_layout = QHBoxLayout()
        below_layout.addStretch(3)
        below_layout.addWidget(self.add_bt, 1)
        below_layout.addWidget(self.del_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        below.setLayout(below_layout)

        self.pinfo = []
        for i in range(len(self.default_properties["Point"])):
            # 顶点位置
            labelx = QLabel("P{} X:".format(i + 1))
            labely = QLabel("P{} Y:".format(i + 1))
            x_pos = PigComboBox()
            y_pos = PigComboBox()
            x_pos.addItems(["0", "25", "50", "75", "100"])
            x_pos.setEditable(True)
            y_pos.addItems(["0", "25", "50", "75", "100"])
            y_pos.setEditable(True)
            labelx.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            labely.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

            self.playout.addWidget(labelx, i + 1, 0)
            self.playout.addWidget(x_pos, i + 1, 1)
            self.playout.addWidget(labely, i + 1, 2)
            self.playout.addWidget(y_pos, i + 1, 3)
            p = [x_pos, y_pos]
            self.pinfo.append(p)

        top = QWidget()
        top.setLayout(self.playout)
        self.glayout.addWidget(top, 6)
        self.glayout.addWidget(below, 1)
        self.glayout.setSpacing(0)

    def addpoint(self):

        if len(self.pinfo) == 20:
            self.add_bt.setEnabled(False)
            return
        # 顶点位置改变
        self.default_properties["Point"].append(["0", "0"])

        x_pos = PigComboBox()
        y_pos = PigComboBox()
        x_pos.addItems(["0", "25", "50", "75", "100"])
        x_pos.setEditable(True)
        y_pos.addItems(["0", "25", "50", "75", "100"])
        y_pos.setEditable(True)
        p = [x_pos, y_pos]
        self.pinfo.append(p)

        # 给顶点赋值
        # 圆心
        x = int(self.default_properties["Center X"])
        y = int(self.default_properties["Center Y"])

        n = len(self.default_properties["Point"])
        for i in range(n):
            try:
                self.default_properties["Point"][i][0] = str(x + int(100 * np.cos(np.pi / 2 - i * 2 * np.pi / n)))
                self.default_properties["Point"][i][1] = str(y + int(100 * np.sin(i * 2 * np.pi / n - np.pi / 2)))
            except Exception as e:
                print(e)

        for i in range(len(self.pinfo)):
            self.pinfo[i][0].setCurrentText(self.default_properties["Point"][i][0])
            self.pinfo[i][1].setCurrentText(self.default_properties["Point"][i][1])

        labelX = QLabel("P{} X:".format(len(self.pinfo)))
        labelY = QLabel("P{} Y:".format(len(self.pinfo)))
        labelX.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        labelY.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        self.playout.addWidget(labelX, len(self.pinfo) + 1, 0)
        self.playout.addWidget(self.pinfo[-1][0], len(self.pinfo) + 1, 1)
        self.playout.addWidget(labelY, len(self.pinfo) + 1, 2)
        self.playout.addWidget(self.pinfo[-1][1], len(self.pinfo) + 1, 3)

        self.plabels.append([labelX, labelY])
        self.del_bt.setEnabled(True)

    def delpoint(self):
        self.default_properties["Point"].pop(-1)
        x1 = self.pinfo[-1][0]
        x2 = self.pinfo[-1][1]
        y1 = self.plabels[-1][0]
        y2 = self.plabels[-1][1]
        self.pinfo.pop(-1)
        self.plabels.pop(-1)
        x1.deleteLater()
        x2.deleteLater()
        y1.deleteLater()
        y2.deleteLater()

        # 给其他顶点赋值
        x = int(self.default_properties["Center X"])
        y = int(self.default_properties["Center Y"])
        n = len(self.default_properties["Point"])
        for i in range(len(self.default_properties["Point"])):
            try:
                self.default_properties["Point"][i][0] = str(x + int(100 * np.cos(np.pi / 2 - i * 2 * np.pi / n)))
                self.default_properties["Point"][i][1] = str(y + int(100 * np.sin(i * 2 * np.pi / n - np.pi / 2)))
            except Exception as e:
                print(e)

        for i in range(len(self.pinfo)):
            self.pinfo[i][0].setCurrentText(self.default_properties["Point"][i][0])
            self.pinfo[i][1].setCurrentText(self.default_properties["Point"][i][1])

        if len(self.pinfo) == 3:
            self.del_bt.setEnabled(False)

    # 生成frame页面
    def setUI(self):
        self.cx_pos.addItems(["0", "25", "50", "75", "100"])
        self.cx_pos.setEditable(True)
        self.cy_pos.addItems(["0", "25", "50", "75", "100"])
        self.cy_pos.setEditable(True)

        self.La.addItems(["0", "25", "50", "75", "100"])
        self.La.setEditable(True)
        self.Sa.addItems(["0", "25", "50", "75", "100"])
        self.Sa.setEditable(True)
        valid_num = QRegExp("\d+")
        self.cx_pos.setValidator(QRegExpValidator(valid_num))
        self.cy_pos.setValidator(QRegExpValidator(valid_num))
        # self.p1x_pos.setValidator(QRegExpValidator(valid_num))
        # self.p1y_pos.setValidator(QRegExpValidator(valid_num))
        # self.p2x_pos.setValidator(QRegExpValidator(valid_num))
        # self.p2y_pos.setValidator(QRegExpValidator(valid_num))
        # self.p3x_pos.setValidator(QRegExpValidator(valid_num))
        # self.p3y_pos.setValidator(QRegExpValidator(valid_num))
        # self.p4x_pos.setValidator(QRegExpValidator(valid_num))
        # self.p4y_pos.setValidator(QRegExpValidator(valid_num))
        self.La.setValidator(QRegExpValidator(valid_num))
        self.Sa.setValidator(QRegExpValidator(valid_num))

        for i in self.pinfo:
            i[0].addItems(["0", "25", "50", "75", "100"])
            i[0].setEditable(True)
            i[1].addItems(["0", "25", "50", "75", "100"])
            i[1].setEditable(True)
            i[0].setValidator(QRegExpValidator(valid_num))
            i[1].setValidator(QRegExpValidator(valid_num))

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
        _22 = QLabel("start:")
        _23 = QLabel("angle:")
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
        # 多边形
        if self.type == 'four':
            # layout1.addWidget(l1, 0, 0)
            # layout1.addWidget(self.cx_pos, 0, 1)
            # layout1.addWidget(l2, 0, 2)
            # layout1.addWidget(self.cy_pos, 0, 3)
            # layout1.addWidget(l3, 1, 0)
            # layout1.addWidget(self.p1x_pos, 1, 1)
            # layout1.addWidget(l4, 1, 2)
            # layout1.addWidget(self.p1y_pos, 1, 3)
            # layout1.addWidget(l5, 2, 0)
            # layout1.addWidget(self.p2x_pos, 2, 1)
            # layout1.addWidget(l6, 2, 2)
            # layout1.addWidget(self.p2y_pos, 2, 3)
            # layout1.addWidget(l7, 3, 0)
            # layout1.addWidget(self.p3x_pos, 3, 1)
            # layout1.addWidget(l8, 3, 2)
            # layout1.addWidget(self.p3y_pos, 3, 3)
            # layout1.addWidget(l9, 4, 0)
            # layout1.addWidget(self.p4x_pos, 4, 1)
            # layout1.addWidget(_21, 4, 2)
            # layout1.addWidget(self.p4y_pos, 4, 3)
            # 直线
            self.setplayout()
            layout1 = self.glayout
        elif self.type == 'two':
            # layout1.addWidget(l1, 0, 0)
            # layout1.addWidget(self.cx_pos, 0, 1)
            # layout1.addWidget(l2, 0, 2)
            # layout1.addWidget(self.cy_pos, 0, 3)
            layout1.addWidget(l3, 0, 0)
            layout1.addWidget(self.p1x_pos, 0, 1)
            layout1.addWidget(l4, 0, 2)
            layout1.addWidget(self.p1y_pos, 0, 3)
            layout1.addWidget(l5, 1, 0)
            layout1.addWidget(self.p2x_pos, 1, 1)
            layout1.addWidget(l6, 1, 2)
            layout1.addWidget(self.p2y_pos, 1, 3)
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
        # self.default_properties['P1 X'] = self.p1x_pos.currentText()
        # self.default_properties['P1 Y'] = self.p1y_pos.currentText()
        # self.default_properties['P2 X'] = self.p2x_pos.currentText()
        # self.default_properties['P2 Y'] = self.p2y_pos.currentText()
        # self.default_properties['P3 X'] = self.p3x_pos.currentText()
        # self.default_properties['P3 Y'] = self.p3y_pos.currentText()
        # self.default_properties['P4 X'] = self.p4x_pos.currentText()
        # self.default_properties['P4 Y'] = self.p4y_pos.currentText()
        # print(f"pinfo:{len(self.pinfo)}")
        # print(f"depro:{self.default_properties['Point']}")
        for iVertex in range(len(self.pinfo)):
            # print(f"{iVertex}:{self.pinfo[iVertex][0].currentText()}")
            # print(f"{self.default_properties['Point'][iVertex][0]}")
            self.default_properties["Point"][iVertex][0] = self.pinfo[iVertex][0].currentText()
            self.default_properties["Point"][iVertex][1] = self.pinfo[iVertex][1].currentText()

        self.default_properties['start'] = self.La.currentText()
        self.default_properties['end angle'] = self.Sa.currentText()
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
        # self.p1x_pos.setCurrentText(self.default_properties["P1 X"])
        # self.p1y_pos.setCurrentText(self.default_properties["P1 Y"])
        # self.p2x_pos.setCurrentText(self.default_properties["P2 X"])
        # self.p2y_pos.setCurrentText(self.default_properties["P2 Y"])
        # self.p3x_pos.setCurrentText(self.default_properties["P3 X"])
        # self.p3y_pos.setCurrentText(self.default_properties["P3 Y"])
        # self.p4x_pos.setCurrentText(self.default_properties["P4 X"])
        # self.p4y_pos.setCurrentText(self.default_properties["P4 Y"])
        # print(f"{self.pinfo}")
        print(f"slider 389: {self.default_properties['Point']}")
        for i in range(len(self.pinfo)):
            self.pinfo[i][0].setCurrentText(self.default_properties["Point"][i][0])
            self.pinfo[i][1].setCurrentText(self.default_properties["Point"][i][1])

        self.La.setCurrentText(self.default_properties["start"])
        self.Sa.setCurrentText(self.default_properties["end angle"])
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


class PolygonProperty(QWidget):
    def __init__(self, type, parent=None):
        super(PolygonProperty, self).__init__(parent)
        self.below = QWidget()

        self.frame = FramePage(type)
        self.default_properties = {**self.frame.default_properties}
        # print(f"line 429 {self.default_properties}")
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
