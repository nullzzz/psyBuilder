import numpy as np
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QGroupBox, QGridLayout, QVBoxLayout, QFormLayout, QHBoxLayout, \
    QCompleter, QSizePolicy

from lib import VarLineEdit, ColorListEditor


class Point:
    def __init__(self, x_l, y_l, x="0", y="0"):
        self.x_label = QLabel(x_l)
        self.y_label = QLabel(y_l)
        self.x_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.y_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.x = VarLineEdit(x)
        self.y = VarLineEdit(y)

    def getX(self):
        return self.x.text()

    def getY(self):
        return self.y.text()

    def set(self, x, y):
        self.x.setText(str(x))
        self.y.setText(str(y))

    def setAttributes(self, attributes):
        self.x.setCompleter(QCompleter(attributes))
        self.y.setCompleter(QCompleter(attributes))


class PolygonGeneral(QWidget):
    def __init__(self, parent=None):
        super(PolygonGeneral, self).__init__(parent)
        self.attributes = []
        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Points": [],
            "Border Color": "black",
            "Border Width": '1',
            "Fill Color": "0,0,0,0"
        }

        self.cx_pos = VarLineEdit("0")
        self.cy_pos = VarLineEdit("0")
        self.cx_pos.setEnabled(False)
        self.cy_pos.setEnabled(False)

        self.p1 = Point("X1:", "Y1:")
        self.p2 = Point("X2:", "Y2:")
        self.p3 = Point("X3:", "Y3:")

        self.points: list = [self.p1, self.p2, self.p3]

        self.add_bt = QPushButton("+")
        self.add_bt.clicked.connect(self.addPoint)
        self.del_bt = QPushButton("-")
        self.del_bt.clicked.connect(self.delPoint)
        self.del_bt.setEnabled(False)
        # down
        self.border_color = ColorListEditor()
        self.border_color.setCurrentText("0,0,0")
        self.border_width = VarLineEdit("1")

        self.fill_color = ColorListEditor()
        self.fill_color.addTransparent()

        self.setUI()

    def addPoint(self):
        n = len(self.points) + 1
        p = Point(f"X{n}:", f"Y{n}:")
        p.setAttributes(self.attributes)
        self.points.append(p)

        # 给顶点赋值
        # 圆心
        __x = self.cx_pos.text()
        x = 100 if __x.startswith("[") else int(__x)
        __y = self.cy_pos.text()
        y = 100 if __y.startswith("[") else int(__y)

        for i, p in enumerate(self.points):
            p: Point
            new_x = str(x + int(100 * np.cos(np.pi / 2 - i * 2 * np.pi / n)))
            new_y = str(y + int(100 * np.sin(i * 2 * np.pi / n - np.pi / 2)))
            p.set(new_x, new_y)

        self.point_layout.addWidget(p.x_label, n, 0)
        self.point_layout.addWidget(p.x, n, 1)
        self.point_layout.addWidget(p.y_label, n, 2)
        self.point_layout.addWidget(p.y, n, 3)

        self.del_bt.setEnabled(n > 3)
        self.add_bt.setEnabled(n <= 20)

    def delPoint(self):
        p = self.points.pop(-1)
        p.x_label.deleteLater()
        p.y_label.deleteLater()
        p.x.deleteLater()
        p.y.deleteLater()

        __x = self.cx_pos.text()
        x = 100 if __x.startswith("[") else int(__x)
        __y = self.cy_pos.text()
        y = 100 if __y.startswith("[") else int(__y)
        n = len(self.points)

        for i, p in enumerate(self.points):
            p: Point
            new_x = str(x + int(100 * np.cos(np.pi / 2 - i * 2 * np.pi / n)))
            new_y = str(y + int(100 * np.sin(i * 2 * np.pi / n - np.pi / 2)))
            p.set(new_x, new_y)

        self.del_bt.setEnabled(n > 3)
        self.add_bt.setEnabled(n < 20)

    # 生成frame页面
    def setUI(self):
        l00 = QLabel("Center X:")
        l01 = QLabel("Center Y:")

        l1 = QLabel("Border Color:")
        l2 = QLabel("Border Width:")
        l3 = QLabel("Fill Color:")
        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l01.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox("Geometry")

        self.point_layout = QGridLayout()
        self.point_layout.addWidget(self.p1.x_label, 1, 0)
        self.point_layout.addWidget(self.p1.x, 1, 1)
        self.point_layout.addWidget(self.p1.y_label, 1, 2)
        self.point_layout.addWidget(self.p1.y, 1, 3)
        self.point_layout.addWidget(self.p2.x_label, 2, 0)
        self.point_layout.addWidget(self.p2.x, 2, 1)
        self.point_layout.addWidget(self.p2.y_label, 2, 2)
        self.point_layout.addWidget(self.p2.y, 2, 3)
        self.point_layout.addWidget(self.p3.x_label, 3, 0)
        self.point_layout.addWidget(self.p3.x, 3, 1)
        self.point_layout.addWidget(self.p3.y_label, 3, 2)
        self.point_layout.addWidget(self.p3.y, 3, 3)

        bt_layout = QHBoxLayout()
        bt_layout.addStretch(5)
        bt_layout.addWidget(self.add_bt)
        bt_layout.addWidget(self.del_bt)
        bt_layout.setAlignment(Qt.AlignBottom)

        up_layout = QVBoxLayout()
        up_layout.addLayout(self.point_layout, 10)
        up_layout.addLayout(bt_layout, 11)

        group1.setLayout(up_layout)

        group2 = QGroupBox("Fill && Borderline")

        layout2 = QFormLayout()
        layout2.setRowWrapPolicy(QFormLayout.DontWrapRows)
        layout2.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        layout2.setLabelAlignment(Qt.AlignLeft)

        self.border_color.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.fill_color.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        layout2.addRow(l1, self.border_color)
        layout2.addRow(l2, self.border_width)
        layout2.addRow(l3, self.fill_color)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 设置可选属性
    def setAttributes(self, attributes: list):
        self.attributes = attributes
        self.cx_pos.setCompleter(QCompleter(attributes))
        self.cy_pos.setCompleter(QCompleter(attributes))
        self.p1.setAttributes(attributes)
        self.p2.setAttributes(attributes)
        self.p3.setAttributes(attributes)
        self.border_width.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        self.default_properties['Center X'] = self.cx_pos.text()
        self.default_properties['Center Y'] = self.cy_pos.text()

        points: list = []
        for p in self.points:
            points.append((p.getX(), p.getY()))

        self.default_properties["Points"] = points

        self.default_properties['Border Width'] = self.border_width.text()
        self.default_properties['Border Color'] = self.border_color.getColor()
        self.default_properties['Fill Color'] = self.fill_color.getColor()

    def setProperties(self, properties: dict):
        self.default_properties = properties
        self.loadSetting()

    def setPosition(self, x, y):
        if not self.cx_pos.text().startswith("["):
            self.cx_pos.setText(str(int(x)))
        if not self.cy_pos.text().startswith("["):
            self.cy_pos.setText(str(int(y)))

    def setVertex(self, points: list):
        for i, j in zip(self.points, points):
            if not i.x.text().startswith("["):
                i.x.setText(str(int(j[0])))
            if not i.y.text().startswith("["):
                i.y.setText(str(int(j[1])))

    def setItemColor(self, color):
        if not self.fill_color.currentText().startswith("["):
            r, g, b, a = color.getRgb()
            self.fill_color.setCurrentText(f"{r},{g},{b}")

    def setLineColor(self, color):
        if not self.border_color.currentText().startswith("["):
            r, g, b, a = color.getRgb()
            self.border_color.setCurrentText(f"{r},{g},{b}")

    # 加载参数设置
    def loadSetting(self):
        self.cx_pos.setText(self.default_properties["Center X"])
        self.cy_pos.setText(self.default_properties["Center Y"])

        l1 = len(self.points)
        l2 = len(self.default_properties["Points"])
        if l1 > l2:
            for i in range(l1 - l2):
                self.del_bt.click()
        else:
            for i in range(l2 - l1):
                self.add_bt.click()
        for i, j in zip(self.points, self.default_properties["Points"]):
            i.set(j[0], j[1])
        self.border_color.setCurrentText(self.default_properties["Border Color"])
        self.border_width.setText(self.default_properties["Border Width"])
        self.fill_color.setCurrentText(self.default_properties['Fill Color'])
