from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QPushButton, QCheckBox, \
    QApplication, QFileDialog, QCompleter, QFormLayout

from app.func import Func
from app.lib import PigLineEdit, PigComboBox


# image event专属页面
class ImageTab1(QWidget):
    def __init__(self, parent=None):
        super(ImageTab1, self).__init__(parent)

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
            "Clear after": "Yes",
            "Screen name": "screen.0"
        }
        # 打开文件
        self.file_name = PigLineEdit()

        self.open_bt = QPushButton("open file")
        self.open_bt.clicked.connect(self.openFile)

        # 镜像模式
        self.mirrorUD = QCheckBox("Mirror up/down")
        self.mirrorLR = QCheckBox("Mirror left/right")

        # Rotate
        self.rotate = PigLineEdit("0")
        self.rotate.setReg(r"\[\w+\]|\d+")

        # 拉伸模式
        self.stretch = QCheckBox("Stretch")
        self.stretch_mode = PigComboBox()

        # 背景色、透明度、Clear&Screen
        # self.back_color = ColorListEditor()
        self.transparent = PigLineEdit("100%")
        self.transparent.setReg(r"[0-9]%|[1-9][0-9]%|100%|\[\w+\]")

        self.clear_after = PigComboBox()

        self.using_screen_id: str = ""
        self.screen = PigComboBox()
        self.screen_info = Func.getScreenInfo()
        self.screen.addItems(self.screen_info.values())
        self.screen.currentTextChanged.connect(self.changeScreen)

        self.setGeneral()

    def setGeneral(self):
        self.stretch_mode.addItems(("Both", "LeftRight", "UpDown"))
        self.clear_after.addItems(("clear_0", "notClear_1", "doNothing_2"))

        # 打开文件按钮布局
        group1 = QGroupBox("")
        layout1 = QGridLayout()
        layout1.addWidget(QLabel("File Name"), 0, 0, 1, 1)
        layout1.addWidget(self.file_name, 0, 1, 1, 4)
        layout1.addWidget(self.open_bt, 0, 5, 1, 1)

        self.stretch.stateChanged.connect(self.stretchChecked)
        self.stretch_mode.setEnabled(False)

        layout1.addWidget(self.mirrorUD, 1, 0)
        layout1.addWidget(self.mirrorLR, 2, 0)
        l0 = QLabel("Rotate:")
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
        layout2.addRow("Screen Name:", self.screen)

        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group1)
        layout.addWidget(group2)
        self.setLayout(layout)

    def refresh(self):
        self.screen_info = Func.getScreenInfo()
        screen_id = self.using_screen_id
        self.screen.clear()
        self.screen.addItems(self.screen_info.values())
        screen_name = self.screen_info.get(screen_id)
        if screen_name:
            self.screen.setCurrentText(screen_name)
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
        # self.clear_after.setCompleter(QCompleter(self.attributes))
        # self.screen_name.setCompleter(QCompleter(self.attributes))

    def setScreen(self, screen: list):
        selected = self.screen.currentText()
        self.screen.clear()
        self.screen.addItems(screen)
        if selected in screen:
            self.screen.setCurrentText(selected)
        else:
            new_name = Func.getDeviceNameById(self.using_screen_id)
            if new_name:
                self.screen.setCurrentText(new_name)

    def getInfo(self):
        """
        历史遗留函数
        :return:
        """
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Mirror up/down"] = bool(self.mirrorUD.checkState())
        self.default_properties["Mirror left/right"] = bool(self.mirrorLR.checkState())
        self.default_properties["Rotate"] = self.rotate.text()
        self.default_properties["Stretch"] = bool(self.stretch.checkState())
        self.default_properties["Stretch mode"] = self.stretch_mode.currentText()
        self.default_properties["Transparent"] = self.transparent.text()
        self.default_properties["Clear after"] = self.clear_after.currentText()
        if Func.getDeviceNameById(self.using_screen_id):
            self.default_properties["Screen name"] = Func.getDeviceNameById(self.using_screen_id)
        else:
            self.default_properties["Screen name"] = self.screen.currentText()
        return self.default_properties

    def getProperties(self):
        self.default_properties.clear()
        self.default_properties["File name"] = self.file_name.text()
        self.default_properties["Mirror up/down"] = bool(self.mirrorUD.checkState())
        self.default_properties["Mirror left/right"] = bool(self.mirrorLR.checkState())

        self.default_properties["Rotate"] = self.rotate.text()
        self.default_properties["Stretch"] = bool(self.stretch.checkState())
        self.default_properties["Stretch mode"] = self.stretch_mode.currentText()
        # self.default_properties["Back color"] = self.back_color.getColor()
        self.default_properties["Transparent"] = self.transparent.text()
        self.default_properties["Clear after"] = self.clear_after.currentText()
        if Func.getDeviceNameById(self.using_screen_id):
            self.default_properties["Screen name"] = Func.getDeviceNameById(self.using_screen_id)
        else:
            self.default_properties["Screen name"] = self.screen.currentText()
        return self.default_properties

    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    def loadSetting(self):
        self.file_name.setText(self.default_properties["File name"])
        self.mirrorUD.setChecked(self.default_properties["Mirror up/down"])
        self.mirrorLR.setChecked(self.default_properties["Mirror left/right"])
        self.rotate.setText(self.default_properties["Rotate"])
        self.stretch.setChecked(self.default_properties["Stretch"])
        self.stretch_mode.setCurrentText(self.default_properties["Stretch mode"])
        # self.back_color.setCurrentText(self.default_properties["Back color"])
        # self.transparent.setValue(self.default_properties["Transparent"])
        self.transparent.setText(self.default_properties["Transparent"])
        self.clear_after.setCurrentText(self.default_properties["Clear after"])
        self.screen.setCurrentText(self.default_properties["Screen name"])

    def clone(self):
        clone_page = ImageTab1()
        clone_page.setProperties(self.default_properties)
        return clone_page


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = ImageTab1()

    t.show()

    sys.exit(app.exec())
