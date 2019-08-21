from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel, QGroupBox, QGridLayout, QFormLayout, QVBoxLayout, QCompleter

from app.lib import ColorListEditor, PigLineEdit


class RectGeneral(QWidget):
    def __init__(self, parent=None):
        super(RectGeneral, self).__init__(parent)
        self.attributes = []
        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Border color": "black",
            "Border width": '1',
            "Fill color": "0,0,0,0"
        }

        self.cx_pos = PigLineEdit("0")
        self.cy_pos = PigLineEdit("0")

        self._width = PigLineEdit("200")
        self._height = PigLineEdit("200")

        # down
        self.border_color = ColorListEditor()
        self.border_color.setCurrentText("0,0,0")
        self.border_width = PigLineEdit("1")
        self.fill_color = ColorListEditor()
        self.fill_color.addTransparent()
        self.setUI()

    def setUI(self):
        l00 = QLabel("Center X:")
        l01 = QLabel("Center Y:")
        l10 = QLabel("Width:")
        l11 = QLabel("Height:")
        l2 = QLabel("Border Color:")
        l3 = QLabel("Border Width:")
        l4 = QLabel("Fill Color:")

        l00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l01.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l11.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

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

        group1.setLayout(layout1)

        group2 = QGroupBox("")
        layout2 = QFormLayout()
        layout2.addRow(l2, self.border_color)
        layout2.addRow(l3, self.border_width)
        layout2.addRow(l4, self.fill_color)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 设置可选属性
    def setAttributes(self, attributes):
        self.attributes = attributes
        self.cx_pos.setCompleter(QCompleter(self.attributes))
        self.cy_pos.setCompleter(QCompleter(self.attributes))
        self._width.setCompleter(QCompleter(self.attributes))
        self._height.setCompleter(QCompleter(self.attributes))
        self.border_width.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties['Center X'] = self.cx_pos.text()
        self.default_properties['Center Y'] = self.cy_pos.text()
        self.default_properties["Width"] = self._width.text()
        self.default_properties["Height"] = self._height.text()

        self.default_properties['Border width'] = self.border_width.text()
        self.default_properties['Border color'] = self.border_color.getColor()
        self.default_properties['Fill color'] = self.fill_color.getColor()

        return self.default_properties

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
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

    # 加载参数设置
    def loadSetting(self):
        self.cx_pos.setText(self.default_properties["Center X"])
        self.cy_pos.setText(self.default_properties["Center Y"])
        self._width.setText(self.default_properties["Width"])
        self._height.setText(self.default_properties["Height"])

        self.border_color.setCurrentText(self.default_properties["Border color"])
        self.border_width.setText(self.default_properties["Border width"])
        self.fill_color.setCurrentText(self.default_properties["Fill color"])
