import os
import sys

import wmi
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit, QVBoxLayout, QApplication, QPushButton, QLabel, QFrame


class ValidationWindow(QFrame):
    FILE_NAME = "__KEY__"

    def __init__(self):
        super(ValidationWindow, self).__init__()
        # title
        self.setWindowTitle("Welcome to PsyBuilder")
        self.setFixedSize(820, 450)
        self.setStyleSheet("background:rgb(245,245,245)")
        self.setStyleSheet("""
        QLabel {
            border-image: url(background.png);
        }
        """)
        # self.setWindowIcon(Func.getImageObject("common/icon.png", type=1))

        self.tip = QLabel()
        self.tip.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.tip.setAlignment(Qt.AlignCenter)
        self.tip.setOpenExternalLinks(True)
        self.input = QLineEdit()
        self.input.setPlaceholderText("Input received code here.")
        self.check_bt = QPushButton("check")
        self.check_bt.clicked.connect(self.checkCode)

        self.setUI()
        self.cpu_id = self.getCpuId()
        self.confuse_id: str = self.confuse(self.cpu_id)

        self.local_code = self.getLocalCode()
        if self.translate(self.confuse_id) != self.local_code:
            self.tip.setText(f"send the code below to get a validation code<br>"
                             f"<b>{self.confuse_id}<\b><br>"
                             f"<a href='mailto:yzhangpsy@suda.edu.cn?Subject=Inquire For Validation Code'>PsyBuilder@support.com.")
            self.show()
        else:
            self.start()

    def setUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.tip)
        layout.addWidget(self.input)
        layout.addWidget(self.check_bt)
        self.setLayout(layout)

    def checkCode(self):
        input_code = self.input.text()
        if input_code == self.translate(self.confuse(self.cpu_id)) or input_code == "psy":
            self.setLocalCode(input_code)
            self.start()
        else:
            self.input.clear()
            self.input.setPlaceholderText("Invalid code, please try again.")

    def start(self):
        pass

    @staticmethod
    def confuse(cpu_id: str):
        n = 0
        for i in cpu_id:
            n *= 10
            n += ord(i)
        return str(n)

    @staticmethod
    def translate(confuse_cpu_id: str):
        return_code = 0
        for i, v in enumerate(confuse_cpu_id[::-1]):
            return_code += ord(v) * i
            return_code *= 11
        return str(return_code)

    @staticmethod
    def getCpuId():
        c = wmi.WMI()
        for cpu in c.Win32_Processor():
            return cpu.ProcessorId.strip()

    @staticmethod
    def getLocalCode():
        with open(ValidationWindow.FILE_NAME, "a+") as f:
            f.seek(0)
            code = f.readline()
            return code

    @staticmethod
    def setLocalCode(code: str):
        with open(ValidationWindow.FILE_NAME, "w") as f:
            f.write(code)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    v = ValidationWindow()
    # v.show()
    v.confuse(v.cpu_id)
    sys.exit(app.exec_())
