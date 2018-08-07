from PyQt5.QtCore import QRegExp, Qt, pyqtProperty
from PyQt5.QtGui import QColor
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QColorDialog
from PyQt5.QtWidgets import QComboBox


class ColorListEditor(QComboBox):
    def __init__(self, widget=None):
        super(ColorListEditor, self).__init__(widget)
        self.setEditable(True)
        self.populateList()
        self.currentIndexChanged.connect(self.changeColor)
        self.setStyleSheet("background: {}".format(self.currentText()))
        valid_rgb = QRegExp("#[0-9A-Fa-f]{6}")

        self.setValidator(QRegExpValidator(valid_rgb, self))
        self.setInsertPolicy(QComboBox.NoInsert)

    def getColor(self):
        color = self.itemData(self.currentIndex(), Qt.DecorationRole)
        return color

    def setColor(self, color):
        self.setCurrentIndex(self.findData(color, Qt.DecorationRole))

    color = pyqtProperty(QColor, getColor, setColor, user=True)

    def populateList(self):
        for i, colorName in enumerate(QColor.colorNames()):
            color = QColor(colorName)
            self.insertItem(i, colorName)
            self.setItemData(i, color, Qt.DecorationRole)

        self.insertItem(0, "More...", Qt.DecorationRole)

    def changeColor(self, e):
        if e:
            self.setStyleSheet("background: {}".format(self.currentText()))
        else:
            self.setStyleSheet("background: white;")
            color = QColorDialog.getColor(Qt.white, self)
            if color.isValid():
                colorName = color.name()
                try:
                    self.setStyleSheet("background: {}".format(colorName))
                    self.insertItem(1, colorName)
                    self.setItemData(1, color, Qt.DecorationRole)
                    self.setCurrentIndex(1)
                except Exception as e:
                    print(e)
                    print(type(e))
            else:
                self.setCurrentIndex(1)