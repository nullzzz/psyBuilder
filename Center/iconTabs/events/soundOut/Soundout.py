from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import re
from .SoundOutui import *


class MySound(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton_4.clicked.connect(self.openFile)
        self.checkBox.stateChanged.connect(self.volume)
        self.checkBox_2.stateChanged.connect(self.Pan)
        self.lineEdit_2.setEnabled(False)
        self.lineEdit_6.setEnabled(False)

    def openFile(self):
        # directory1 = QtWidgets.QFileDialog.getExistingDirectory(self, "选取文件夹", "C:/")  # 起始路径
        # print(directory1)

        fileName1, filetype = QtWidgets.QFileDialog.getOpenFileName(self, "选取文件","C:/", "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        # print(fileName1, filetype)
        self.lineEdit.setText(fileName1)
        # files, ok1 = QtWidgets.QFileDialog.getOpenFileNames(self, "多文件选择", "C:/", "All Files (*);;Text Files (*.txt)")
        # print(files, ok1)
        # fileName2, ok2 = QtWidgets.QFileDialog.getSaveFileName(self, "文件保存", "C:/", "All Files (*);;Text Files (*.txt)")

    def volume(self):
        if self.checkBox.isChecked():
            self.lineEdit_2.setEnabled(True)
        else:
            self.lineEdit_2.setEnabled(False)

    def Pan(self):
        if self.checkBox_2.isChecked():
            self.lineEdit_6.setEnabled(True)
        else:
            self.lineEdit_6.setEnabled(False)
