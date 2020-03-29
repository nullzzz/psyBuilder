from PyQt5.QtCore import Qt, QRegExp, pyqtSignal
from PyQt5.QtGui import QColor, QIcon, QRegExpValidator, QFont
from PyQt5.QtWidgets import QComboBox, QColorDialog, QMessageBox

from .var_combo_box import VarComboBox


class ColorListEditor(VarComboBox):
    colorChanged = pyqtSignal(str)
    color_map: dict = {
        "white": "255,255,255",
        "gray": "128,128,128",
        "black": "0,0,0",
        "red": "255,0,0",
        "orange": "255,165,0",
        "yellow": "255,255,0",
        "green": "0,255,0",
        "blue": "0,0,255",
        "purple": "128,0,128",
        "transparent": "0,0,0,0"
    }

    def __init__(self, widget=None):
        super(ColorListEditor, self).__init__(widget)
        self.setEditable(True)
        self.is_valid: int = 1
        self.is_showing = False
        self.is_chose = False
        self.default_color = ("white", "gray", "black", "red",
                              "orange", "yellow", "green", "blue", "purple")
        self.init()

        self.setStyleSheet("background: {}".format(self.getRGB()))
        # 支持输入255,255,255及#ffffff格式rgb
        valid_rgb = QRegExp(
            r"((2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?),){2}((2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?))|#[0-9A-Fa-f]{6}|"
            r"white|gray|black|red|orange|yellow|green|blue|purple|\[\w+\]")
        self.setValidator(QRegExpValidator(valid_rgb, self))
        self.setInsertPolicy(QComboBox.NoInsert)

    # 添加默认颜色，白灰黑、红橙黄绿蓝紫
    def init(self):
        for i, color_name in enumerate(self.default_color):
            color = QColor(color_name)
            self.insertItem(i, color_name)
            self.setItemData(i, color, Qt.DecorationRole)
        self.insertItem(0, "More...", Qt.DecorationRole)
        self.setItemIcon(0, QIcon("image/more_color.png"))

    def addTransparent(self):
        color_name = "transparent"
        color = QColor(color_name)
        self.insertItem(1, color_name)
        self.setItemData(1, color, Qt.DecorationRole)
        self.setCurrentIndex(1)

    def findVar(self, text: str):
        if text:
            if text.startswith("["):
                self.setStyleSheet("color: blue")
                self.setFont(QFont("Timers", 9, QFont.Bold))
                self.is_valid = 2
            else:
                self.setStyleSheet("color: black")
                self.setFont(QFont("宋体", 9, QFont.Normal))
                # 取色板
                if text == "More...":
                    self.is_chose = True
                    self.setStyleSheet("background: white;")
                    color_rgb = QColorDialog.getColor(Qt.white, self)
                    # 选了颜色
                    if color_rgb.isValid():
                        color_name = color_rgb.name()
                        color_name_ = f"{int(color_name[1:3], 16)},{int(color_name[3:5], 16)},{int(color_name[5:], 16)}"
                        self.setStyleSheet("background: {}".format(color_name))
                        # if self.findText(color_name_, Qt.MatchExactly) == -1:
                        #     self.insertItem(1, color_name_)
                        #     self.setItemData(1, color_rgb, Qt.DecorationRole)
                        #     self.setCurrentIndex(1)
                        # else:
                        self.setCurrentText(color_name_)
                    # 未选颜色
                    else:
                        self.setCurrentIndex(1)
                    self.is_valid = 1
                    self.is_chose = False
                # 255,255,255格式rgb
                elif text[0].isdigit():
                    color_rgb = text.split(",")
                    if len(color_rgb) >= 3 and color_rgb[2] != "":
                        self.setStyleSheet("background-color: rgb({});".format(text))
                        # 添加到下拉菜单
                        if self.findText(text, Qt.MatchExactly) == -1:
                            color = QColor(int(color_rgb[0]), int(
                                color_rgb[1]), int(color_rgb[2]))
                            self.insertItem(1, text)
                            self.setItemData(1, color, Qt.DecorationRole)
                            self.setCurrentIndex(1)
                        self.is_valid = 1
                    else:
                        self.is_valid = 0
                        self.setStyleSheet("background: white")
                # #ffffff格式rgb
                elif text[0] == "#" and len(text) == 7:
                    if self.findText(text) == -1:
                        color = QColor(text)
                        self.insertItem(1, text)
                        self.setItemData(1, color, Qt.DecorationRole)
                        self.setCurrentIndex(1)
                    self.setStyleSheet("background: {}".format(text))
                    self.is_valid = 1
                elif text in self.default_color:
                    self.is_valid = 1
                    self.setStyleSheet("background: rgb({})".format(self.color_map.get(text)))
                elif text == "transparent":
                    self.is_valid = 1
                    self.setStyleSheet("background: white")
                else:
                    self.is_valid = 0
                    self.setStyleSheet("background: white")
        else:
            self.is_valid = 0
            self.setStyleSheet("background: white")

        if self.is_valid == 1:
            self.colorChanged.emit(self.getColor())

    # 重写下拉菜单展开
    def showPopup(self):
        self.is_showing = True
        self.setStyleSheet("background: white;")
        QComboBox.showPopup(self)

    # 重写下拉菜单收起
    def hidePopup(self):
        self.is_showing = False
        color = self.currentText()
        if self.is_valid == 1:
            if ',' in color:
                self.setStyleSheet("background: rgb({})".format(color))
            else:
                self.setStyleSheet("background: {};".format(color))
        else:
            self.setStyleSheet("background: white;")
        QComboBox.hidePopup(self)

    def focusOutEvent(self, e):
        if not self.is_chose:
            if not self.is_showing:
                if not self.is_valid:
                    self.setStyleSheet("background: white;")
                    self.setCurrentText("white")
                    QMessageBox.warning(
                        self, "Warning", "Invalid Color!", QMessageBox.Ok)
                else:
                    pass
        QComboBox.focusOutEvent(self, e)

    def setCurrentText(self, text: str) -> None:
        for k, v in self.color_map.items():
            if text == v:
                text = k
                break
        return QComboBox.setCurrentText(self, text)

    def getColor(self):
        """
        返回当前颜色R,G,B
        :return:
        """
        color_name = self.currentText()
        if color_name.startswith("["):
            return color_name
        elif color_name.startswith("#"):
            color_name = f"{int(color_name[1:3], 16)},{int(color_name[3:5], 16)},{int(color_name[5:], 16)}"
        return self.color_map.get(color_name, color_name)

    def getRGB(self):
        color_name = self.currentText()
        if color_name.startswith("["):
            color_name = '255,255,255'
        elif color_name.startswith("#"):
            color_name = f"{int(color_name[1:3], 16)},{int(color_name[3:5], 16)},{int(color_name[5:], 16)}"
        elif color_name == "transparent":
            color_name = '255,255,255'
        return self.color_map.get(color_name, color_name)

    def getRGBA(self):
        color_name = self.currentText()
        if color_name.startswith("["):
            return color_name
        elif color_name.startswith("#"):
            color_name = f"{int(color_name[1:3], 16)},{int(color_name[3:5], 16)},{int(color_name[5:], 16)}"
        return self.color_map.get(color_name, color_name)
