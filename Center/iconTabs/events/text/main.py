from PyQt5 import QtWidgets, QtCore, QtGui
from .textdisplay import Ui_MainWindow
from .textdisplay1 import Ui_Dialog
from .action import MyDialog
from .Preview import *
import time


class TextDisplay(QtWidgets.QMainWindow, Ui_MainWindow):
    propertiesChange = QtCore.pyqtSignal(dict)
    def __init__(self):
        super(TextDisplay, self).__init__()
        self.setupUi(self)
        self.settings.triggered.connect(self.openSettings)
        self.Settings = self.DefaultSettings()
        self.actionPreview.triggered.connect(self.Preview)
        self.dia = MyDialog()
        self.dia.pushButton_6.clicked.connect(self.OK)
        self.dia.pushButton_5.clicked.connect(self.Cancel)
        self.dia.pushButton_4.clicked.connect(self.Apply)
        self.pa = QtGui.QPalette()
        self.pa.setColor(QtGui.QPalette.Base, QtGui.QColor('White'))
        self.textEdit.setPalette(self.pa)

    def openSettings(self):
        self.loadSettings()
        self.dia.show()

    def OK(self):
        if self.dia.validator():
            self.dia.close()
            self.textEdit.setText(self.dia.textEdit.toHtml())
            self.pa = self.dia.textEdit.palette()
            self.textEdit.setPalette(self.pa)
            self.textEdit.setWordWrapMode(self.dia.textEdit.wordWrapMode())
            self.saveSettings()
            # self.textEdit.setGeometry()
            # self.textEdit.setStyleSheet("border: 1px solid red; height:50px; width:100px; font-size: 10px; text-align: center; line-height: 50px; font-weight: bold")
        else:
            self.msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Alert", "Invalid !")
            self.msg_box.show()

    def Apply(self):
        if self.dia.validator():
            self.textEdit.setText(self.dia.textEdit.toHtml())
            self.pa = self.dia.textEdit.palette()
            self.textEdit.setPalette(self.pa)
            self.textEdit.setWordWrapMode(self.dia.textEdit.wordWrapMode())
            self.saveSettings()
            # self.textEdit.setGeometry()
            # self.textEdit.setStyleSheet("border: 1px solid red; height:50px; width:100px; font-size: 10px; text-align: center; line-height: 50px; font-weight: bold")
        else:
            self.msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning, "Alert", "Invalid !")
            self.msg_box.show()

    def Cancel(self):
        self.dia.closequstion()

    def Preview(self):
        self.pre = Mypreview()
        self.pre.textEdit.setText(self.textEdit.toHtml())
        self.pre.textEdit.setPalette(self.textEdit.palette())
        self.pre.textEdit_2.setPalette(self.textEdit.palette())
        self.pre.textEdit_2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pre.textEdit.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pre.textEdit.setWordWrapMode(self.textEdit.wordWrapMode())
        # self.pre.textEdit.setGeometry()
        if self.dia.comboBox_backstyle.currentText() == "transparent":
            self.pre.setWindowOpacity(0.7)
        elif self.dia.comboBox_backstyle.currentText() == "opaque":
            self.pre.setWindowOpacity(100)

    def saveSettings(self):
        self.Settings = {
            'Text': self.dia.textEdit.toHtml(),
            'AlignHorizontal': self.dia.comboBox_AlignH.currentText(),
            'AlignVertical': self.dia.comboBox_AlignV.currentText(),
            'ClearAfter': self.dia.comboBox_clear.currentText(),
            'WordWrap': self.dia.checkBox.isChecked(),
            'ForeColor': self.dia.comboBox.currentText(),
            'BackColor': self.dia.comboBox_2.currentText(),
            'BackStyle': self.dia.comboBox_backstyle.currentText(),
            'DisplayName': '',
            'X': self.dia.comboBox_8.currentText(),
            'Y': self.dia.comboBox_10.currentText(),
            'Height': self.dia.comboBox_9.currentText(),
            'Width': self.dia.comboBox_11.currentText(),
            'BorderColor': self.dia.comboBox_12.currentText(),
            'BorderWidth': self.dia.comboBox_13.currentText(),
        }
        self.propertiesChange.emit(self.getProperties())

    def loadSettings(self):
        self.dia.textEdit.setText(self.Settings['Text'])
        self.dia.comboBox_AlignH.setCurrentText(self.Settings['AlignHorizontal'])
        self.dia.comboBox_AlignV.setCurrentText(self.Settings['AlignVertical'])
        self.dia.checkBox.setChecked(self.Settings['WordWrap'])
        self.dia.comboBox.setCurrentText(self.Settings['ForeColor'])
        self.dia.comboBox_2.setCurrentText(self.Settings['BackColor'])
        self.dia.comboBox_backstyle.setCurrentText(self.Settings['BackStyle'])
        self.dia.comboBox_8.setCurrentText(self.Settings['X'])
        self.dia.comboBox_9.setCurrentText(self.Settings['Height'])
        self.dia.comboBox_10.setCurrentText(self.Settings['Y'])
        self.dia.comboBox_11.setCurrentText(self.Settings['Width'])
        self.dia.comboBox_12.setCurrentText(self.Settings['BorderColor'])
        self.dia.comboBox_13.setCurrentText(self.Settings['BorderWidth'])
        self.dia.textEdit.setPalette(self.pa)

    def DefaultSettings(self):
        x = {
            'Text': '',
            'AlignHorizontal':'Left',
            'AlignVertical':'Top',
            'ClearAfter':'No',
            'WordWrap': True,
            'ForeColor':'Black',
            'BackColor':'White',
            'BackStyle':'opaque',
            'DisplayName':'',
            'X':'left',
            'Y':'top',
            'Height':'0',
            'Width':'0',
            'BorderColor':'Black',
            'BorderWidth':'0',
        }
        return x

    def getProperties(self):
        return self.Settings


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    myshow = TextDisplay()
    myshow.show()
    sys.exit(app.exec_())


