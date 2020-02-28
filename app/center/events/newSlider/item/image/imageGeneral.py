from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QPushButton, QCheckBox, \
    QFileDialog, QCompleter

from lib import VarLineEdit, VarComboBox


# image event专属页面
class ImageGeneral(QWidget):
    def __init__(self, parent=None):
        super(ImageGeneral, self).__init__(parent)

        # 当前可使用attribute
        self.attributes = []
        # 当前页面属性
        self.default_properties = {
            "File name": "",
            "Mirror up/down": False,
            "Mirror left/right": False,
            "Rotate": "0",
            "Stretch": False,
            "Stretch mode": "Both",
            "Back color": "white",
            "Transparent": "100%",
            "Center X": "50%",
            "Center Y": "50%",
            "Width": "100%",
            "Height": "100%",
        }
        # 打开文件
        self.file_name = VarLineEdit()

        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        # 镜像模式
        self.mirrorUD = QCheckBox("Mirror up/down")
        self.mirrorLR = QCheckBox("Mirror left/right")

        # Rotate
        self.rotate = VarComboBox()

        # 拉伸模式
        self.stretch = QCheckBox("Stretch")
        self.stretch_mode = VarComboBox()

        # 背景色、透明度
        self.transparent = VarComboBox()

        self.x_pos = VarComboBox()
        self.y_pos = VarComboBox()
        self._width = VarComboBox()
        self._height = VarComboBox()

        self.setGeneral()

    def setGeneral(self):
        self.stretch_mode.addItems(("Both", "LeftRight", "UpDown"))

        self.rotate.addItems(("0", "90", "180", "270", "360"))
        self.rotate.setEditable(True)
        self.rotate.setReg(r"\d+|\d+\.\d+")

        self.transparent.addItems(("0%", "25%", "50%", "75%", "100%"))
        self.transparent.setCurrentText("100%")
        self.transparent.setEditable(True)
        self.transparent.setReg(r"\d+%?|\d+\.\d+%?")

        self.x_pos.addItems(("25%", "50%", "75%", "100%"))
        self.x_pos.setCurrentText("50%")
        self.x_pos.setEditable(True)
        self.x_pos.setReg(r"\d+%?")

        self.y_pos.addItems(("25%", "50%", "75%", "100%"))
        self.y_pos.setCurrentText("50%")
        self.y_pos.setEditable(True)
        self.y_pos.setReg(r"\d+%?")

        self._width.addItems(("25%", "50%", "75%", "100%"))
        self._width.setCurrentText("100%")
        self._width.setEditable(True)
        self._width.setReg(r"\d+%?")

        self._height.addItems(("25%", "50%", "75%", "100%"))
        self._height.setCurrentText("100%")
        self._height.setEditable(True)
        self._height.setReg(r"\d+%?")

        # 打开文件按钮布局
        group1 = QGroupBox("File && Effects")

        layout1 = QGridLayout()

        layout1.addWidget(QLabel("File Name"), 0, 0, 1, 1)
        layout1.addWidget(self.file_name, 0, 1, 1, 4)
        layout1.addWidget(self.open_bt, 0, 5, 1, 1)

        self.stretch.stateChanged.connect(self.stretchChecked)
        self.stretch_mode.setEnabled(False)

        layout1.addWidget(self.mirrorUD, 1, 0)
        layout1.setColumnMinimumWidth(1, 40)

        layout1.addWidget(self.mirrorLR, 2, 0)
        l0 = QLabel("Rotate (0~360):")
        l0.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout1.addWidget(l0, 1, 2)
        layout1.addWidget(self.rotate, 1, 3, 1, 2)

        l_tra = QLabel("Transparent(%):")
        l_tra.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout1.addWidget(l_tra, 2, 2)
        layout1.addWidget(self.transparent, 2, 3, 1, 2)

        layout1.addWidget(self.stretch, 3, 0)
        layout1.addWidget(self.stretch_mode, 3, 2)

        group1.setLayout(layout1)

        group2 = QGroupBox("Geometry")

        layout2 = QGridLayout()
        layout2.setVerticalSpacing(10)

        l_x_pos = QLabel("Center X:")
        l_y_pos = QLabel("Center Y:")
        l_width = QLabel("Maximum Width:")
        l_height = QLabel("Maximum Height:")

        l_x_pos.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_y_pos.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_width.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        l_height.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        layout2.addWidget(l_x_pos, 0, 0, 1, 1)
        layout2.addWidget(self.x_pos, 0, 1)

        layout2.addWidget(l_width, 0, 2, 1, 2)
        layout2.addWidget(self._width, 0, 4)

        layout2.addWidget(l_y_pos, 1, 0, 1, 1)
        layout2.addWidget(self.y_pos, 1, 1)

        layout2.addWidget(l_height, 1, 2, 1, 2)
        layout2.addWidget(self._height, 1, 4)

        group2.setLayout(layout2)

        layout = QVBoxLayout()

        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Find the image file", self.file_name.text(),
                                                   "Image File (*.bmp;*.jpeg;*.jpg;*.png;*.gif)", options=options)
        if file_name:
            self.file_name.setText(file_name)

    def stretchChecked(self, e):
        if e == 2:
            self.stretch_mode.setEnabled(True)
        else:
            self.stretch_mode.setEnabled(False)

    def setAttributes(self, attributes):
        self.attributes = attributes
        self.file_name.setCompleter(QCompleter(self.attributes))
        self.rotate.setCompleter(QCompleter(self.attributes))
        self.transparent.setCompleter(QCompleter(self.attributes))
        self.x_pos.setCompleter(QCompleter(self.attributes))
        self.y_pos.setCompleter(QCompleter(self.attributes))
        self._width.setCompleter(QCompleter(self.attributes))
        self._height.setCompleter(QCompleter(self.attributes))

    def getInfo(self):
        """
        历史遗留函数
        :return:
        """
        self.default_properties.clear()
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Mirror up/down"] = bool(self.mirrorUD.checkState())
        self.default_properties["Mirror left/right"] = bool(self.mirrorLR.checkState())
        self.default_properties["Rotate"] = self.rotate.currentText()
        self.default_properties["Stretch"] = bool(self.stretch.checkState())
        self.default_properties["Stretch mode"] = self.stretch_mode.currentText()
        self.default_properties["Transparent"] = self.transparent.currentText()
        self.default_properties["Center X"] = self.x_pos.currentText()
        self.default_properties["Center Y"] = self.y_pos.currentText()
        self.default_properties["Width"] = self._width.currentText()
        self.default_properties["Height"] = self._height.currentText()

        return self.default_properties

    def getProperties(self):
        self.default_properties.clear()
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Mirror up/down"] = bool(self.mirrorUD.checkState())
        self.default_properties["Mirror left/right"] = bool(self.mirrorLR.checkState())
        self.default_properties["Rotate"] = self.rotate.currentText()
        self.default_properties["Stretch"] = bool(self.stretch.checkState())
        self.default_properties["Stretch mode"] = self.stretch_mode.currentText()
        self.default_properties["Transparent"] = self.transparent.currentText()
        self.default_properties["Center X"] = self.x_pos.currentText()
        self.default_properties["Center Y"] = self.y_pos.currentText()
        self.default_properties["Width"] = self._width.currentText()
        self.default_properties["Height"] = self._height.currentText()
        return self.default_properties

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def setPosition(self, x, y):
        if not self.x_pos.currentText().startswith("["):
            self.x_pos.setCurrentText(str(int(x)))
        if not self.y_pos.currentText().startswith("["):
            self.y_pos.setCurrentText(str(int(y)))

    def loadSetting(self):
        self.file_name.setText(self.default_properties["File name"])
        self.mirrorUD.setChecked(self.default_properties["Mirror up/down"])
        self.mirrorLR.setChecked(self.default_properties["Mirror left/right"])
        self.rotate.setCurrentText(self.default_properties["Rotate"])
        self.stretch.setChecked(self.default_properties["Stretch"])
        self.stretch_mode.setCurrentText(self.default_properties["Stretch mode"])
        self.transparent.setCurrentText(self.default_properties["Transparent"])
        self.x_pos.setCurrentText(self.default_properties["Center X"])
        self.y_pos.setCurrentText(self.default_properties["Center Y"])
        self._width.setCurrentText(self.default_properties["Width"])
        self._height.setCurrentText(self.default_properties["Height"])

    def clone(self):
        clone_page = ImageGeneral()
        clone_page.setProperties(self.default_properties)
        return clone_page
