# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'textdisplay1.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(881, 862)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_2.setContentsMargins(500, 0, -1, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_6 = QtWidgets.QPushButton(Dialog)
        self.pushButton_6.setObjectName("pushButton_6")
        self.horizontalLayout_2.addWidget(self.pushButton_6)
        self.pushButton_5 = QtWidgets.QPushButton(Dialog)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setCheckable(False)
        self.pushButton_4.setAutoExclusive(False)
        self.pushButton_4.setAutoDefault(True)
        self.pushButton_4.setDefault(False)
        self.pushButton_4.setFlat(False)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        self.QTabWidget = QtWidgets.QTabWidget(Dialog)
        self.QTabWidget.setObjectName("QTabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.textEdit = QtWidgets.QTextEdit(self.tab)
        self.textEdit.setGeometry(QtCore.QRect(180, 10, 511, 311))
        self.textEdit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.textEdit.setFrameShadow(QtWidgets.QFrame.Plain)
        self.textEdit.setLineWidth(1)
        self.textEdit.setObjectName("textEdit")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(130, 20, 41, 20))
        self.label.setObjectName("label")
        self.gridLayoutWidget = QtWidgets.QWidget(self.tab)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 330, 681, 221))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 2, 1, 1)
        self.comboBox_AlignH = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_AlignH.setEditable(True)
        self.comboBox_AlignH.setObjectName("comboBox_AlignH")
        self.comboBox_AlignH.addItem("")
        self.comboBox_AlignH.addItem("")
        self.comboBox_AlignH.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_AlignH, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 1, 0, 1, 1)
        self.comboBox_AlignV = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_AlignV.setEditable(True)
        self.comboBox_AlignV.setObjectName("comboBox_AlignV")
        self.comboBox_AlignV.addItem("")
        self.comboBox_AlignV.addItem("")
        self.comboBox_AlignV.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_AlignV, 1, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 0, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 3, 2, 1, 1)
        self.comboBox_backstyle = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_backstyle.setEditable(True)
        self.comboBox_backstyle.setObjectName("comboBox_backstyle")
        self.comboBox_backstyle.addItem("")
        self.comboBox_backstyle.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_backstyle, 2, 3, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.checkBox.setCheckable(True)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 3, 1, 1, 1)
        self.comboBox_clear = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_clear.setEditable(True)
        self.comboBox_clear.setObjectName("comboBox_clear")
        self.comboBox_clear.addItem("")
        self.comboBox_clear.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_clear, 2, 1, 1, 1)
        self.comboBox_Dname = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_Dname.setEditable(True)
        self.comboBox_Dname.setObjectName("comboBox_Dname")
        self.gridLayout_2.addWidget(self.comboBox_Dname, 3, 3, 1, 1)
        self.comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout_2.addWidget(self.comboBox, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 2, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.comboBox_2.setEditable(True)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_2, 1, 3, 1, 1)
        self.QTabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.groupBox = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox.setGeometry(QtCore.QRect(50, 50, 581, 131))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.comboBox_9 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_9.setEditable(True)
        self.comboBox_9.setObjectName("comboBox_9")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_9, 0, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 0, 2, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.comboBox_8 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_8.setEditable(True)
        self.comboBox_8.setObjectName("comboBox_8")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.comboBox_8.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_8, 0, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.groupBox)
        self.label_11.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.gridLayout_3.addWidget(self.label_11, 1, 0, 1, 1)
        self.comboBox_10 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_10.setEditable(True)
        self.comboBox_10.setObjectName("comboBox_10")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_10, 1, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox)
        self.label_13.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 1, 2, 1, 1)
        self.comboBox_11 = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_11.setEditable(True)
        self.comboBox_11.setObjectName("comboBox_11")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.comboBox_11.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_11, 1, 3, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(50, 250, 581, 111))
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_14 = QtWidgets.QLabel(self.groupBox_2)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_4.addWidget(self.label_14, 0, 2, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.groupBox_2)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 0, 0, 1, 1)
        self.comboBox_12 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_12.setEditable(True)
        self.comboBox_12.setObjectName("comboBox_12")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.comboBox_12.addItem("")
        self.gridLayout_4.addWidget(self.comboBox_12, 0, 1, 1, 1)
        self.comboBox_13 = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_13.setEditable(True)
        self.comboBox_13.setObjectName("comboBox_13")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.comboBox_13.addItem("")
        self.gridLayout_4.addWidget(self.comboBox_13, 0, 3, 1, 1)
        self.QTabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.QTabWidget, 0, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 10)

        self.retranslateUi(Dialog)
        self.QTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton_6.setText(_translate("Dialog", "OK"))
        self.pushButton_5.setText(_translate("Dialog", "Cancel"))
        self.pushButton_4.setText(_translate("Dialog", "Apply"))
        self.textEdit.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Microsoft YaHei,Arial,Helvetica,sans-serif\'; font-size:16px; color:#222222;\">他突然感到快乐无比。他永远都可以回去做个牧羊人，也总是可以回去水晶店工作。也许这个世界上还藏着其他的宝藏，不过他有一个梦，还遇见过一个国王，那可不是每个人都会有的。</span></p></body></html>"))
        self.label.setText(_translate("Dialog", "Text"))
        self.label_5.setText(_translate("Dialog", "BackColor"))
        self.comboBox_AlignH.setCurrentText(_translate("Dialog", "Left"))
        self.comboBox_AlignH.setItemText(0, _translate("Dialog", "Right"))
        self.comboBox_AlignH.setItemText(1, _translate("Dialog", "Left"))
        self.comboBox_AlignH.setItemText(2, _translate("Dialog", "Center"))
        self.label_3.setText(_translate("Dialog", "AlignHorizontal"))
        self.label_4.setText(_translate("Dialog", "AlignVertical"))
        self.comboBox_AlignV.setItemText(0, _translate("Dialog", "Top"))
        self.comboBox_AlignV.setItemText(1, _translate("Dialog", "Center"))
        self.comboBox_AlignV.setItemText(2, _translate("Dialog", "Bottom"))
        self.label_7.setText(_translate("Dialog", "BackStyle"))
        self.label_6.setText(_translate("Dialog", "Clear After"))
        self.label_8.setText(_translate("Dialog", "Display Name"))
        self.comboBox_backstyle.setItemText(0, _translate("Dialog", "opaque"))
        self.comboBox_backstyle.setItemText(1, _translate("Dialog", "transparent"))
        self.checkBox.setText(_translate("Dialog", "WordWrap"))
        self.comboBox_clear.setItemText(0, _translate("Dialog", "No"))
        self.comboBox_clear.setItemText(1, _translate("Dialog", "Yes"))
        self.comboBox.setItemText(0, _translate("Dialog", "Black"))
        self.comboBox.setItemText(1, _translate("Dialog", "Green"))
        self.comboBox.setItemText(2, _translate("Dialog", "Blue"))
        self.comboBox.setItemText(3, _translate("Dialog", "Red"))
        self.comboBox.setItemText(4, _translate("Dialog", "Yellow"))
        self.comboBox.setItemText(5, _translate("Dialog", "More.."))
        self.label_2.setText(_translate("Dialog", "ForeColor"))
        self.comboBox_2.setItemText(0, _translate("Dialog", "White"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "Black"))
        self.comboBox_2.setItemText(2, _translate("Dialog", "Green"))
        self.comboBox_2.setItemText(3, _translate("Dialog", "Blue"))
        self.comboBox_2.setItemText(4, _translate("Dialog", "Red"))
        self.comboBox_2.setItemText(5, _translate("Dialog", "Yellow"))
        self.comboBox_2.setItemText(6, _translate("Dialog", "More.."))
        self.QTabWidget.setTabText(self.QTabWidget.indexOf(self.tab), _translate("Dialog", "General"))
        self.groupBox.setTitle(_translate("Dialog", "Size and Position"))
        self.comboBox_9.setItemText(0, _translate("Dialog", "0"))
        self.comboBox_9.setItemText(1, _translate("Dialog", "25%"))
        self.comboBox_9.setItemText(2, _translate("Dialog", "50%"))
        self.comboBox_9.setItemText(3, _translate("Dialog", "75%"))
        self.comboBox_9.setItemText(4, _translate("Dialog", "100%"))
        self.label_10.setText(_translate("Dialog", "Height"))
        self.label_9.setText(_translate("Dialog", "X"))
        self.comboBox_8.setItemText(0, _translate("Dialog", "left"))
        self.comboBox_8.setItemText(1, _translate("Dialog", "center"))
        self.comboBox_8.setItemText(2, _translate("Dialog", "right"))
        self.comboBox_8.setItemText(3, _translate("Dialog", "0"))
        self.comboBox_8.setItemText(4, _translate("Dialog", "25%"))
        self.comboBox_8.setItemText(5, _translate("Dialog", "50%"))
        self.comboBox_8.setItemText(6, _translate("Dialog", "75%"))
        self.comboBox_8.setItemText(7, _translate("Dialog", "100%"))
        self.label_11.setText(_translate("Dialog", "Y"))
        self.comboBox_10.setItemText(0, _translate("Dialog", "top"))
        self.comboBox_10.setItemText(1, _translate("Dialog", "center"))
        self.comboBox_10.setItemText(2, _translate("Dialog", "bottom"))
        self.comboBox_10.setItemText(3, _translate("Dialog", "0"))
        self.comboBox_10.setItemText(4, _translate("Dialog", "25%"))
        self.comboBox_10.setItemText(5, _translate("Dialog", "50%"))
        self.comboBox_10.setItemText(6, _translate("Dialog", "75%"))
        self.comboBox_10.setItemText(7, _translate("Dialog", "100%"))
        self.label_13.setText(_translate("Dialog", "Width"))
        self.comboBox_11.setItemText(0, _translate("Dialog", "0"))
        self.comboBox_11.setItemText(1, _translate("Dialog", "25%"))
        self.comboBox_11.setItemText(2, _translate("Dialog", "50%"))
        self.comboBox_11.setItemText(3, _translate("Dialog", "75%"))
        self.comboBox_11.setItemText(4, _translate("Dialog", "100%"))
        self.groupBox_2.setTitle(_translate("Dialog", "Border"))
        self.label_14.setText(_translate("Dialog", "BorderWidth"))
        self.label_12.setText(_translate("Dialog", "BorderColor"))
        self.comboBox_12.setItemText(0, _translate("Dialog", "Black"))
        self.comboBox_12.setItemText(1, _translate("Dialog", "Green"))
        self.comboBox_12.setItemText(2, _translate("Dialog", "Blue"))
        self.comboBox_12.setItemText(3, _translate("Dialog", "Red"))
        self.comboBox_12.setItemText(4, _translate("Dialog", "Yellow"))
        self.comboBox_12.setItemText(5, _translate("Dialog", "More.."))
        self.comboBox_13.setItemText(0, _translate("Dialog", "0"))
        self.comboBox_13.setItemText(1, _translate("Dialog", "25"))
        self.comboBox_13.setItemText(2, _translate("Dialog", "50"))
        self.comboBox_13.setItemText(3, _translate("Dialog", "75"))
        self.comboBox_13.setItemText(4, _translate("Dialog", "100"))
        self.QTabWidget.setTabText(self.QTabWidget.indexOf(self.tab_2), _translate("Dialog", "Frame"))

