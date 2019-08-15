from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QCompleter
from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QDesktopWidget)

from app.lib import PigComboBox


class SnowGeneral(QWidget):
    def __init__(self, parent=None):
        super(SnowGeneral, self).__init__(parent)
        self.attributes = []
        self.type = type
        self.default_properties = {
            "Center X": "0",
            "Center Y": "0",
            "Width": "100",
            "Height": "100",
            "Scale": "1",
            "Rotation": "0",
            "Transparency": "0"
        }
        # up
        self.cx_pos = PigComboBox()
        self.cy_pos = PigComboBox()
        self._width = PigComboBox()
        self._height = PigComboBox()
        self.scale = PigComboBox()
        self.rotation = PigComboBox()
        self.transparency = PigComboBox()
        self.setUI()

    # 生成frame页面
    def setUI(self):
        self.cx_pos.addItems(["0", "25", "50", "75", "100"])
        self.cx_pos.setEditable(True)
        self.cy_pos.addItems(["0", "25", "50", "75", "100"])
        self.cy_pos.setEditable(True)
        self._width.addItems(["0", "25", "50", "75", "100"])
        self._width.setEditable(True)
        self._width.setCurrentText("100")
        self._height.addItems(["0", "25", "50", "75", "100"])
        self._height.setEditable(True)
        self._height.setCurrentText("100")
        self.rotation.addItems(["0", "25", "50", "75", "100"])
        self.rotation.setEditable(True)
        self.scale.addItems(["1", "2", "4", "6", "8"])
        self.scale.setEditable(True)
        self.scale.setCurrentText("1")
        self.transparency.addItems(["0", "2", "4", "6", "8"])
        self.transparency.setEditable(True)

        l1 = QLabel("Center X:")
        l2 = QLabel("Center Y:")
        l3 = QLabel("Width:")
        l4 = QLabel("Height:")
        l5 = QLabel("Scale:")
        l6 = QLabel("Rotation:")
        l7 = QLabel("Transparency")

        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout = QGridLayout()
        layout.addWidget(l1, 0, 0)
        layout.addWidget(self.cx_pos, 0, 1)
        layout.addWidget(l2, 0, 2)
        layout.addWidget(self.cy_pos, 0, 3)
        layout.addWidget(l3, 1, 0)
        layout.addWidget(self._width, 1, 1)
        layout.addWidget(l4, 1, 2)
        layout.addWidget(self._height, 1, 3)
        layout.addWidget(l5, 2, 0)
        layout.addWidget(self.scale, 2, 1)
        layout.addWidget(l6, 2, 2)
        layout.addWidget(self.rotation, 2, 3)
        layout.addWidget(l7, 3, 0)
        layout.addWidget(self.transparency, 3, 1)

        self.setLayout(layout)

    # 设置可选属性
    def setAttributes(self, attributes):
        self.attributes = attributes
        self.cx_pos.setCompleter(QCompleter(self.attributes))
        self.cy_pos.setCompleter(QCompleter(self.attributes))
        self._width.setCompleter(QCompleter(self.attributes))
        self._height.setCompleter(QCompleter(self.attributes))
        self.scale.setCompleter(QCompleter(self.attributes))
        self.rotation.setCompleter(QCompleter(self.attributes))
        self.transparency.setCompleter(QCompleter(self.attributes))

    def setPosition(self, x, y):
        self.cx_pos.setCurrentText(str(int(x)))
        self.cy_pos.setCurrentText(str(int(y)))

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties['Center X'] = self.cx_pos.currentText()
        self.default_properties['Center Y'] = self.cy_pos.currentText()
        self.default_properties['Width'] = self._width.currentText()
        self.default_properties['Height'] = self._height.currentText()
        self.default_properties['Scale'] = self.scale.currentText()
        self.default_properties['Rotation'] = self.rotation.currentText()
        self.default_properties['Transparency'] = self.transparency.currentText()

        return self.default_properties

    def setProperties(self, properties: dict):
        if isinstance(properties, dict):
            self.default_properties = properties
            self.loadSetting()

    # 加载参数设置
    def loadSetting(self):
        self.cx_pos.setCurrentText(self.default_properties["Center X"])
        self.cy_pos.setCurrentText(self.default_properties["Center Y"])
        self._width.setCurrentText(self.default_properties["Width"])
        self._height.setCurrentText(self.default_properties["Height"])
        self.scale.setCurrentText(self.default_properties["Scale"])
        self.rotation.setCurrentText(self.default_properties["Rotation"])
        self.transparency.setCurrentText(self.default_properties["Transparency"])

    # def clone(self):
    #     clone_page = FramePage()
    #     clone_page.setProperties(self.default_properties)
    #     return clone_page


class snowProperty(QWidget):
    def __init__(self, parent=None):
        super(snowProperty, self).__init__(parent)
        self.below = QWidget()

        self.frame = SnowGeneral()
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
