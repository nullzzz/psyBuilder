from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QPushButton, QCheckBox, \
    QFileDialog, QCompleter, QFormLayout

from app.func import Func
from lib import VarLineEdit, VarComboBox


# image event专属页面
class ImageTab1(QWidget):
    def __init__(self, parent=None):
        super(ImageTab1, self).__init__(parent=parent)

        # 当前页面属性
        self.default_properties = {
            "File Name": "",
            "Mirror Up/Down": False,
            "Mirror Left/Right": False,
            "Rotate": "0",
            "Stretch": False,
            "Stretch Mode": "Both",
            "Back Color": "white",
            "Transparent": "100%",
            "Clear After": "Yes",
            "Screen Name": "screen.0"
        }
        # 打开文件
        self.file_name = VarLineEdit()
        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        # 镜像模式
        self.mirrorUD = QCheckBox("Mirror Up/Down")
        self.mirrorLR = QCheckBox("Mirror Left/Right")

        # Rotate
        self.rotate = VarLineEdit("0")
        self.rotate.setReg(r"\[\w+\]|\d+")

        # 拉伸模式
        self.stretch = QCheckBox("Stretch")
        self.stretch_mode = VarComboBox()
        self.stretch_mode.addItems(("Both", "LeftRight", "UpDown"))
        self.stretch.stateChanged.connect(self.stretchChecked)
        self.stretch_mode.setEnabled(False)

        # 透明度、Clear&Screen
        self.transparent = VarLineEdit("100%")
        self.transparent.setReg(r"[0-9]%|[1-9][0-9]%|100%|\[\w+\]")
        self.clear_after = VarComboBox()
        self.clear_after.addItems(("clear_0", "notClear_1", "doNothing_2"))

        self.using_screen_id: str = ""
        self.screen_name = VarComboBox()
        self.screen_info = Func.getDeviceInfo("screen")
        self.screen_name.addItems(self.screen_info.values())
        self.screen_name.currentTextChanged.connect(self.changeScreen)

        self.setUI()

    def setUI(self):
        # 打开文件按钮布局
        group1 = QGroupBox("")
        layout1 = QGridLayout()
        layout1.addWidget(QLabel("File Name"), 0, 0, 1, 1)
        layout1.addWidget(self.file_name, 0, 1, 1, 4)
        layout1.addWidget(self.open_bt, 0, 5, 1, 1)

        layout1.addWidget(self.mirrorUD, 1, 0)
        layout1.addWidget(self.mirrorLR, 2, 0)
        l0 = QLabel("Rotate:0-360°")
        l0.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        layout1.addWidget(l0, 1, 2)
        layout1.addWidget(self.rotate, 1, 3)

        layout1.addWidget(self.stretch, 3, 0)
        layout1.addWidget(self.stretch_mode, 3, 2)
        group1.setLayout(layout1)

        group2 = QGroupBox("")
        layout2 = QFormLayout()
        layout2.setVerticalSpacing(10)
        layout2.setLabelAlignment(Qt.AlignRight)
        layout2.addRow("Transparent:", self.transparent)
        layout2.addRow("Dont Clear After:", self.clear_after)
        layout2.addRow("Screen Name:", self.screen_name)

        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    def refresh(self):
        """
        update completer and device information.
        :return:
        """
        self.screen_info = Func.getDeviceInfo("screen")
        screen_id = self.using_screen_id
        self.screen_name.clear()
        self.screen_name.addItems(self.screen_info.values())
        screen_name = self.screen_info.get(screen_id)
        if screen_name:
            self.screen_name.setCurrentText(screen_name)
            self.using_screen_id = screen_id

    def changeScreen(self, screen):
        for k, v in self.screen_info.items():
            if v == screen:
                self.using_screen_id = k
                break

    # 打开文件夹
    def openFile(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Find the image file", self.file_name.text(),
                                                   "Image File (*.bmp;*.jpeg;*.jpg;*.png)", options=options)
        if file_name:
            self.file_name.setText(file_name)

    def stretchChecked(self, e):
        if e == 2:
            self.stretch_mode.setEnabled(True)
        else:
            self.stretch_mode.setEnabled(False)

    def setAttributes(self, attributes: list):
        self.file_name.setCompleter(QCompleter(attributes))
        self.rotate.setCompleter(QCompleter(attributes))
        self.transparent.setCompleter(QCompleter(attributes))

    def updateInfo(self):
        """
        历史遗留函数
        :return:
        """
        self.default_properties["File Name"] = self.file_name.text()
        self.default_properties["Mirror Up/Down"] = bool(self.mirrorUD.checkState())
        self.default_properties["Mirror Left/Right"] = bool(self.mirrorLR.checkState())
        self.default_properties["Rotate"] = self.rotate.text()
        self.default_properties["Stretch"] = bool(self.stretch.checkState())
        self.default_properties["Stretch Mode"] = self.stretch_mode.currentText()
        self.default_properties["Transparent"] = self.transparent.text()
        self.default_properties["Clear After"] = self.clear_after.currentText()
        if Func.getDeviceNameById(self.using_screen_id):
            self.default_properties["Screen Name"] = Func.getDeviceNameById(self.using_screen_id)
        else:
            self.default_properties["Screen Name"] = self.screen_name.currentText()

    def getProperties(self):
        self.updateInfo()
        return self.default_properties

    def setProperties(self, properties: dict):
        self.default_properties.clear()
        self.default_properties.update(properties)
        self.loadInfo()

    def loadInfo(self):
        self.file_name.setText(self.default_properties["File Name"])
        self.mirrorUD.setChecked(self.default_properties["Mirror Up/Down"])
        self.mirrorLR.setChecked(self.default_properties["Mirror Left/Right"])
        self.rotate.setText(self.default_properties["Rotate"])
        self.stretch.setChecked(self.default_properties["Stretch"])
        self.stretch_mode.setCurrentText(self.default_properties["Stretch Mode"])
        self.transparent.setText(self.default_properties["Transparent"])
        self.clear_after.setCurrentText(self.default_properties["Clear After"])
        self.screen_name.setCurrentText(self.default_properties["Screen Name"])
