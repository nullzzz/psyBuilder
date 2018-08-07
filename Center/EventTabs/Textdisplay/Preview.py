from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Preview(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        # Dialog.setStyleSheet("QDialog#Dialog{background-color:gray;}")
        self.textEdit_2 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_2.setObjectName("textEdit_2")
        self.textEdit_2.setFixedHeight(200)
        self.textEdit_2.setFixedWidth(1000)
        # self.textEdit_2.setStyleSheet('{background-color:gray;}')
        # self.textEdit_2.setAutoFillBackground(True)
        # self.gridLayout.addWidget(self.textEdit_2, 0, 0, 1, 1)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.move(500, 500)
        self.textEdit.resize(500, 500)

        # self.gridLayout.addWidget(self.textEdit, 1, 0, 1, 1)
        # self.gridLayout.setRowStretch(0, 1)
        # self.gridLayout.setRowStretch(1, 20)
        # self.gridLayout.setSpacing(0)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.textEdit_2.setHtml(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:28pt;\"\
>Please enter ESC to exit !</span></p></body></html>"))


class Mypreview(QtWidgets.QDialog, Ui_Preview):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.showFullScreen()
        self.t = QtCore.QTimer()
        self.t.timeout.connect(self.close)
        self.t.start(8000)
        self.t.setSingleShot(True)


