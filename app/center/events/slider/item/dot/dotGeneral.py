from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QGridLayout, QFormLayout, QVBoxLayout, QCompleter, QSizePolicy

from lib import ColorListEditor, VarLineEdit, VarComboBox


class DotGeneral(QWidget):
    def __init__(self, parent=None):
        super(DotGeneral, self).__init__(parent)

        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Width": "100",
            "Height": "100",
            "Is Oval": "yes",
            "Dot Num": "50",
            "Dot Type": "1",
            "Dot Size": "1",
            "Dot Color": "0,0,0",
            "Back Color": '192,192,192',
            "Move Direction": "0"
        }

        self.cx_pos = VarLineEdit("0")
        self.cy_pos = VarLineEdit("0")

        self._width = VarLineEdit("200")
        self._height = VarLineEdit("200")

        self.is_oval = VarComboBox()
        self.is_oval.addItems(("yes", "no"))

        self.dot_num = VarLineEdit("50")
        self.dot_type = VarComboBox()
        self.dot_type.addItems(("1", "2", "3", "4"))
        self.dot_size = VarLineEdit("5")

        # down
        self.dot_color = ColorListEditor()
        self.dot_color.setCurrentText("0,0,0")

        self.back_color = ColorListEditor()
        self.back_color.addTransparent()
        self.back_color.setCurrentText("192,192,192")
        self.move_direction = VarLineEdit("0")
        self.setUI()

    def setUI(self):
        l00 = QLabel("Center X:")
        l01 = QLabel("Center Y:")
        l10 = QLabel("Width:")
        l11 = QLabel("Height:")
        l20 = QLabel("Is Oval:")
        l21 = QLabel("Dot Num:")
        l30 = QLabel("Dot Type:")
        l31 = QLabel("Dot Size:")
        l4 = QLabel("Dot Color:")
        l5 = QLabel("Back Color:")
        l6 = QLabel("Move Direction:")

        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l01.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l20.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l21.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l30.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l31.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group1 = QGroupBox("Geometry")
        layout1 = QGridLayout()

        layout1.addWidget(l00, 0, 0)
        layout1.addWidget(self.cx_pos, 0, 1)
        layout1.addWidget(l01, 0, 2)
        layout1.addWidget(self.cy_pos, 0, 3)
        layout1.addWidget(l10, 1, 0)
        layout1.addWidget(self._width, 1, 1)
        layout1.addWidget(l11, 1, 2)
        layout1.addWidget(self._height, 1, 3)
        layout1.addWidget(l20, 2, 0)
        layout1.addWidget(self.is_oval, 2, 1)
        layout1.addWidget(l21, 2, 2)
        layout1.addWidget(self.dot_num, 2, 3)
        layout1.addWidget(l30, 3, 0)
        layout1.addWidget(self.dot_type, 3, 1)
        layout1.addWidget(l31, 3, 2)
        layout1.addWidget(self.dot_size, 3, 3)

        group1.setLayout(layout1)

        group2 = QGroupBox("somethings")
        layout2 = QFormLayout()
        layout2.setRowWrapPolicy(QFormLayout.DontWrapRows)
        layout2.setFieldGrowthPolicy(QFormLayout.ExpandingFieldsGrow)
        layout2.setLabelAlignment(Qt.AlignLeft)

        self.dot_color.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.back_color.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)

        layout2.addRow(l4, self.dot_color)
        layout2.addRow(l5, self.back_color)
        layout2.addRow(l6, self.move_direction)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 设置可选属性
    def setAttributes(self, attributes):
        self.cx_pos.setCompleter(QCompleter(attributes))
        self.cy_pos.setCompleter(QCompleter(attributes))
        self._width.setCompleter(QCompleter(attributes))
        self._height.setCompleter(QCompleter(attributes))
        self.is_oval.setCompleter(QCompleter(attributes))
        self.dot_num.setCompleter(QCompleter(attributes))
        self.dot_type.setCompleter(QCompleter(attributes))
        self.dot_size.setCompleter(QCompleter(attributes))
        self.dot_color.setCompleter(QCompleter(attributes))
        self.back_color.setCompleter(QCompleter(attributes))
        self.move_direction.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        self.default_properties['Center X'] = self.cx_pos.text()
        self.default_properties['Center Y'] = self.cy_pos.text()
        self.default_properties["Width"] = self._width.text()
        self.default_properties["Height"] = self._height.text()
        self.default_properties["Is Oval"] = self.is_oval.currentText()
        self.default_properties["Dot Num"] = self.dot_num.text()
        self.default_properties["Dot Type"] = self.dot_type.currentText()
        self.default_properties["Dot Size"] = self.dot_size.text()

        self.default_properties['Dot Color'] = self.dot_color.getColor()
        self.default_properties['Back Color'] = self.back_color.getColor()
        self.default_properties['Move Direction'] = self.move_direction.text()

    def setProperties(self, properties: dict):
        self.default_properties.update(properties)
        self.loadSetting()

    def setPosition(self, x, y):
        if not self.cx_pos.text().startswith("["):
            self.cx_pos.setText(str(int(x)))
        if not self.cy_pos.text().startswith("["):
            self.cy_pos.setText(str(int(y)))

    def setWh(self, w, h):
        if not self._width.text().startswith("["):
            self._width.setText(str(int(w)))
        if not self._height.text().startswith("["):
            self._height.setText(str(int(h)))

    def setBackColor(self, rgb: str):
        if not self.back_color.currentText().startswith("["):
            self.back_color.setCurrentText(rgb)

    def setBorderColor(self, rgb: str):
        if not self.dot_color.currentText().startswith("["):
            self.dot_color.setCurrentText(rgb)

    # 加载参数设置
    def loadSetting(self):
        self.cx_pos.setText(self.default_properties["Center X"])
        self.cy_pos.setText(self.default_properties["Center Y"])
        self._width.setText(self.default_properties["Width"])
        self._height.setText(self.default_properties["Height"])

        self.is_oval.setCurrentText(self.default_properties["Is Oval"])
        self.dot_num.setText(self.default_properties["Dot Num"])
        self.dot_type.setCurrentText(self.default_properties["Dot Type"])
        self.dot_size.setText(self.default_properties["Dot Size"])

        self.dot_color.setCurrentText(self.default_properties["Dot Color"])
        self.back_color.setCurrentText(self.default_properties["Back Color"])
        self.move_direction.setText(self.default_properties["Move Direction"])
