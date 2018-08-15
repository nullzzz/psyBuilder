from PyQt5 import QtGui
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *

from .textdisplay1 import Ui_Dialog
from ..durationPage import Tab3


class MyDialog(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        tab3 = Tab3()
        self.setupUi(self)
        self.Color = ['black']
        self.QTabWidget.addTab(tab3, "Duration")
        self.comboBox_AlignH.activated[str].connect(self.SetAlignH)
        self.comboBox_AlignH.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^Left|Right|Center|left|right|center$")))
        self.comboBox_AlignV.activated[str].connect(self.SetAlignV)
        self.comboBox_AlignV.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^Left|Right|Center|left|right|center$")))
        self.checkBox.stateChanged.connect(self.WordWrap)
        self.comboBox.activated[str].connect(self.SetFcolor)
        self.comboBox_2.activated[str].connect(self.SetBcolor)
        self.comboBox_backstyle.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^opaque|Opaque|Transparent|transparent$")))
        # self.comboBox_8.activated[str].connect(self.SetPX)
        self.comboBox_8.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^\d+$")))
        self.comboBox_9.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^\d+$")))
        self.comboBox_10.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^\d+$")))
        self.comboBox_11.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^\d+$")))
        self.comboBox_12.setValidator(QtGui.QRegExpValidator(QtCore.QRegExp("^\d+$")))
        # self.comboBox_9.activated[str].connect(self.SetPH)
        # self.comboBox_10.activated[str].connect(self.SetPY)
        # self.comboBox_11.activated[str].connect(self.SetPW)
        self.comboBox_12.activated[str].connect(self.SetBC)
        # self.comboBox_13.activated[str].connect(self.SetBW)

    def SetAlignH(self, text):
        if text == "Left":
            self.textEdit.setAlignment(QtCore.Qt.AlignLeft)
        elif text == "Right":
            self.textEdit.setAlignment(QtCore.Qt.AlignRight)
        elif text == "Center":
            self.textEdit.setAlignment(QtCore.Qt.AlignCenter)

    def SetAlignV(self, text):
        if text == "Top":
            self.textEdit.setAlignment(QtCore.Qt.AlignTop)
        elif text == "Center":
            self.textEdit.setAlignment(QtCore.Qt.AlignVCenter)
        elif text == "Bottom":
            self.textEdit.setAlignment(QtCore.Qt.AlignBottom)

    def WordWrap(self):
        if self.checkBox.isChecked():
            self.textEdit.setWordWrapMode(QtGui.QTextOption.WordWrap)
        else:
            self.textEdit.setWordWrapMode(QtGui.QTextOption.NoWrap)

    def SetFcolor(self, text):
        if text == "More..":
            col = QColorDialog.getColor()
            if col.isValid():
                self.textEdit.setTextColor(col)

            else:
                self.msg_box = QMessageBox(QMessageBox.Warning, "Alert", "Invalid !")
                self.msg_box.show()
        else:
            if QtGui.QColor(text).isValid():
                self.textEdit.setTextColor(QtGui.QColor(text))
            else:
                self.msg_box = QMessageBox(QMessageBox.Warning, "Alert", "Invalid !")
                self.msg_box.show()

    def SetBcolor(self, text):
        palette1 = QtGui.QPalette()
        if text == "More..":
            col = QColorDialog.getColor()
            if col.isValid():
                # self.textEdit.setTextBackgroundColor(col)
                palette1.setColor(QtGui.QPalette.Base, col)
                self.textEdit.setPalette(palette1)
            else:
                self.msg_box = QMessageBox(QMessageBox.Warning, "Alert", "Invalid !")
                self.msg_box.show()
        else:
            if QtGui.QColor(text).isValid():
                palette1.setColor(QtGui.QPalette.Base, QtGui.QColor(text))
                self.textEdit.setPalette(palette1)
            else:
                self.msg_box = QMessageBox(QMessageBox.Warning, "Alert", "Invalid !")
                self.msg_box.show()

    def SetBC(self, text):
        if text == "More..":
            col = QColorDialog.getColor()
            self.Color[0] = col.name()
        else:
            if QtGui.QColor(text).isValid():
                self.Color[0] = text
            else:
                self.msg_box = QMessageBox(QMessageBox.Warning, "Alert", "Invalid !")
                self.msg_box.show()

    # def validator(self):
    #     x = ['Left', 'Right', 'Center']
    #     y = ['Top', 'Center', 'Bottom']
    #     m = ['Yes', 'No']
    #     n = ['transparent', 'opaque']
    #     if (self.comboBox_AlignH.currentText() in x) and (self.comboBox_AlignV.currentText() in y) and \
    #             (self.comboBox_backstyle.currentText() in n) and (QtGui.QColor(self.comboBox.currentText()).isValid() or self.comboBox.currentText()=='More..')\
    #         and (QtGui.QColor(self.comboBox_2.currentText()).isValid() or self.comboBox_2.currentText()=='More..') and (re.match(r'^\d+$', self.comboBox_8.currentText()) != None)\
    #         and (re.match(r'^\d+$', self.comboBox_10.currentText()) != None) and (re.match(r'^\d+$', self.comboBox_9.currentText()) != None)\
    #         and (re.match(r'^\d+$', self.comboBox_11.currentText()) != None)\
    #         and (QtGui.QColor(self.comboBox_12.currentText()).isValid() or self.comboBox_12.currentText() == 'More..')\
    #         and (re.match(r'^\d+$', self.comboBox_13.currentText()) != None):
    #         return True
    #     else:
    #         return False

    def closequstion(self):
        reply = QtWidgets.QMessageBox.question(self, '确认', '确认退出吗',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.close()
        else:
            pass
