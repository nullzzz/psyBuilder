from PyQt5.QtCore import QDataStream, QIODevice, Qt, QRegExp, QSize
from PyQt5.QtGui import QColor, QIcon, QRegExpValidator, QFont, QPen
from PyQt5.QtWidgets import QComboBox, QMessageBox, QColorDialog, QLineEdit, QSpinBox, QMainWindow, QItemDelegate, \
    QStyle, QWidget, QHBoxLayout


class NoDash(QItemDelegate):
    """
    去除table widget item的虚线框
    """

    def __init__(self):
        super(NoDash, self).__init__()

    def drawFocus(self, painter, option, rect):
        try:
            if option.state and QStyle.State_HasFocus:
                pen = QPen()
                pen.setWidth(0)
                painter.setPen(pen)
        except:
            pass


class SizeContainerWidget(QWidget):
    """
    将其设置为dock widget的widget可以设置初始大小
    """

    def __init__(self, parent=None):
        super(SizeContainerWidget, self).__init__(None)

    def setWidget(self, widget: QWidget):
        """
        设置包含的widget
        :param widget:
        :return:
        """
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(widget)
        self.setLayout(layout)

    def sizeHint(self):
        return QSize(10, 150)


class BaseWidget:
    def __init__(self):
        self.default_properties: dict = {}

    def getPropertyByKey(self, key: str):
        return self.default_properties.get(key)

    def getProperties(self):
        return self.default_properties


class PigSinBox(QSpinBox):
    pass


class PigComboBox(QComboBox):
    def __init__(self, parent=None):
        super(PigComboBox, self).__init__(parent)
        self.setAcceptDrops(True)
        self.currentTextChanged.connect(self.findVar)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("attributes/move-attribute"):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        data = e.mimeData().data("attributes/move-attribute")
        stream = QDataStream(data, QIODevice.ReadOnly)
        text = f"[{stream.readQString()}]"
        index = self.findText(text, Qt.MatchExactly)
        if index == -1:
            self.addItem(text)
        self.setCurrentText(text)

    # 检查变量
    def findVar(self, text: str):
        if text.startswith("[") and text.endswith("]"):
            self.setStyleSheet("color: blue")
            self.setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.setStyleSheet("color: black")
            self.setFont(QFont("宋体", 9, QFont.Normal))


class PigLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(PigLineEdit, self).__init__(parent)
        self.setAcceptDrops(True)
        self.textChanged.connect(self.findVar)

    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("attributes/move-attribute"):
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        data = e.mimeData().data("attributes/move-attribute")
        stream = QDataStream(data, QIODevice.ReadOnly)
        text = f"[{stream.readQString()}]"
        self.setText(text)

    # 检查变量
    def findVar(self, text: str):
        if text.startswith("[") and text.endswith("]"):
            self.setStyleSheet("color: blue")
            print(text)
            self.setFont(QFont("Timers", 9, QFont.Bold))
        else:
            self.setStyleSheet("color: black")
            self.setFont(QFont("宋体", 9, QFont.Normal))


class ColorListEditor(PigComboBox):
    def __init__(self, widget=None):
        super(ColorListEditor, self).__init__(widget)
        self.setEditable(True)
        self.isValid = True
        self.isShow = False
        self.isChoose = False
        self.default_color = ("white", "gray", "black", "red",
                              "orange", "yellow", "green", "blue", "purple")
        self.populateList()

        self.currentTextChanged.connect(self.changeColor)
        self.setStyleSheet("background: {}".format(self.currentText()))
        # 支持输入255,255,255及#ffffff格式rgb
        valid_rgb = QRegExp(
            "((2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?),){2}((2[0-4][0-9]|25[0-5]|[01]?[0-9][0-9]?))|#[0-9A-Fa-f]{"
            "6}|white|gray|black|red|orange|yellow|green|blue|purple")
        self.setValidator(QRegExpValidator(valid_rgb, self))
        self.setInsertPolicy(QComboBox.NoInsert)

    # 添加默认颜色，白灰黑、红橙黄绿蓝紫
    def populateList(self):
        for i, colorName in enumerate(self.default_color):
            color = QColor(colorName)
            self.insertItem(i, colorName)
            self.setItemData(i, color, Qt.DecorationRole)
        self.insertItem(0, "More...", Qt.DecorationRole)
        self.setItemIcon(0, QIcon("image/more_color.png"))

    def changeColor(self, e):
        if e:
            if e.startswith("["):
                self.setStyleSheet("color: blue")
                self.setFont(QFont("Timers", 9, QFont.Bold))
            else:
                self.setStyleSheet("color: black")
                self.setFont(QFont("宋体", 9, QFont.Normal))
                # 取色板
                if e == "More...":
                    self.isChoose = True
                    self.setStyleSheet("background: white;")
                    color_rgb = QColorDialog.getColor(Qt.white, self)
                    # 选了颜色
                    if color_rgb.isValid():
                        color_name = color_rgb.name()
                        color_name_ = f"{int(color_name[1:3], 16)},{int(color_name[3:5], 16)},{int(color_name[5:], 16)}"
                        self.setStyleSheet("background: {}".format(color_name))
                        self.insertItem(1, color_name_)
                        self.setItemData(1, color_rgb, Qt.DecorationRole)
                        self.setCurrentIndex(1)
                    # 未选颜色
                    else:
                        self.setCurrentIndex(1)
                    self.isValid = True
                    self.isChoose = False
                # 255,255,255格式rgb
                elif e[0] in "0123456789":
                    color_rgb = e.split(",")
                    if len(color_rgb) == 3 and color_rgb[2] != "":
                        self.setStyleSheet("background-color: rgb({});".format(e))
                        # 添加到下拉菜单
                        if self.findText(e, Qt.MatchExactly) == -1:
                            color = QColor(int(color_rgb[0]), int(
                                color_rgb[1]), int(color_rgb[2]))
                            self.insertItem(1, e)
                            self.setItemData(1, color, Qt.DecorationRole)
                            self.setCurrentIndex(1)
                        self.isValid = True
                    else:
                        self.isValid = False
                        self.setStyleSheet("background: white")
                # #ffffff格式rgb
                elif e[0] == "#" and len(e) == 7:
                    if self.findText(e) == -1:
                        color = QColor(e)
                        self.insertItem(1, e)
                        self.setItemData(1, color, Qt.DecorationRole)
                        self.setCurrentIndex(1)
                    self.setStyleSheet("background: {}".format(e))
                    self.isValid = True
                elif e in self.default_color:
                    self.isValid = True
                    self.setStyleSheet("background: {}".format(self.currentText()))
                else:
                    self.isValid = False
                    self.setStyleSheet("background: white")
        else:
            self.isValid = False
            self.setStyleSheet("background: white")

    # 重写下拉菜单展开
    def showPopup(self):
        self.isShow = True
        self.setStyleSheet("background: white;")
        QComboBox.showPopup(self)

    # 重写下拉菜单收起
    def hidePopup(self):
        self.isShow = False
        color = self.currentText()
        if self.isValid:
            if ',' in color:
                self.setStyleSheet("background: rgb({})".format(color))
            else:
                self.setStyleSheet("background: {};".format(color))
        else:
            self.setStyleSheet("background: white;")
        QComboBox.hidePopup(self)

    def focusOutEvent(self, e):
        if not self.isChoose:
            if not self.isShow:
                if not self.isValid:
                    self.setStyleSheet("background: white;")
                    self.setCurrentText("white")
                    QMessageBox.warning(
                        self, "Warning", "Invalid Color!", QMessageBox.Ok)
                    # self.lineEdit().clear()
                    # self.setFocus()
                else:
                    pass
        QComboBox.focusOutEvent(self, e)

    # 返回当前QColor对象
    def getColor(self):
        if self.isValid:
            return QColor(self.currentText())
        else:
            return Qt.white


class T(QMainWindow, BaseWidget):
    def __init__(self, parent=None):
        super(T, self).__init__(parent)
