from PyQt5.QtCore import QRegExp, Qt
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QComboBox


class ColorListEditor(QComboBox):
    def __init__(self, widget=None):
        super(ColorListEditor, self).__init__(widget)
        self.setEditable(True)
        self.populateList()
        self.currentTextChanged.connect(self.changeColor)
        self.setStyleSheet("background: {}".format(self.currentText()))
        # 支持输入255,255,255及#ffffff格式rgb
        valid_rgb = QRegExp(
            "((2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?),){2}((2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?))|#[0-9A-Fa-f]{6}")
        self.setValidator(QRegExpValidator(valid_rgb, self))
        self.setInsertPolicy(QComboBox.NoInsert)

    # 添加默认颜色，白灰黑、红橙黄绿蓝紫
    def populateList(self):
        for i, colorName in enumerate(
                ("white", "gray", "black", "red", "orange", "yellow", "green", "blue", "purple")):
            color = QColor(colorName)
            self.insertItem(i, colorName)
            self.setItemData(i, color, Qt.DecorationRole)
        self.insertItem(0, "More...", Qt.DecorationRole)
        self.setItemIcon(0, QIcon(".\\.\\image\more_color.png"))

    def changeColor(self, e):
        if e:
            # 取色板
            if e == "More...":
                self.setStyleSheet("background: white;")
                color_rgb = QColorDialog.getColor(Qt.white, self)
                if color_rgb.isValid():
                    color_name = color_rgb.name()
                    try:
                        self.setStyleSheet("background: {}".format(color_name))
                        self.insertItem(1, color_name)
                        self.setItemData(1, color_rgb, Qt.DecorationRole)
                        self.setCurrentIndex(1)
                    except Exception as e:
                        print(e)
                        print(type(e))
                else:
                    self.setCurrentIndex(1)
            # 255,255,255格式rgb
            elif e[0] in "0123456789":
                color_rgb = e.split(",")
                if len(color_rgb) == 3 and color_rgb[2] != "":
                    self.setStyleSheet("background-color: rgb({});".format(e))
                    if self.findText(e) == -1:
                        color = QColor(int(color_rgb[0]), int(color_rgb[1]), int(color_rgb[2]))
                        self.insertItem(1, e)
                        print("add")
                        self.setItemData(1, color, Qt.DecorationRole)
                        self.setCurrentIndex(1)
            # #ffffff格式rgb
            elif e[0] == "#" and len(e) == 7:
                if self.findText(e) == -1:
                    color = QColor(e)
                    self.insertItem(1, e)
                    self.setItemData(1, color, Qt.DecorationRole)
                    self.setCurrentIndex(1)
                self.setStyleSheet("background: {}".format(e))
            else:
                self.setStyleSheet("background: {}".format(self.currentText()))

    # 重写下拉菜单展开
    def showPopup(self):
        self.setStyleSheet("background: white;")
        QComboBox.showPopup(self)

    # 重写下拉菜单收起
    def hidePopup(self):
        color = self.currentText()
        if ',' in color:
            self.setStyleSheet("background: rgb({})".format(color))
        else:
            self.setStyleSheet("background: {};".format(color))
        QComboBox.hidePopup(self)
