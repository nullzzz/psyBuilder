import os
import sys

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
        if self.confuse_id != self.local_code:
            self.tip.setText(f"send the code below to get a validation code<br>"
                             f"<b>{self.cpu_id}<\b><br>"
                             f"<a href='mailto:yzhangpsy@suda.edu.cn?Subject=Inquire For Validation Code'>yzhangpsy@suda.edu.cn.")
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
        randOrder = [244, 281, 32, 40, 22, 123, 99, 174, 294, 261, 175, 34, 152, 92, 170, 91, 146, 119, 190, 112, 127,
                    241, 165, 35, 6, 265, 121, 271, 228, 160, 236, 55, 148, 3, 96, 166, 136, 269, 68, 16, 140, 135, 69,
                    115, 11, 101, 54, 105, 296, 176, 218, 30, 133, 291, 186, 149, 224, 45, 184, 216, 77, 280, 211, 235,
                    60, 217, 219, 113, 214, 254, 171, 249, 147, 292, 150, 163, 74, 78, 72, 62, 70, 229, 129, 266, 232,
                    242, 107, 134, 51, 33, 7, 86, 182, 237, 212, 196, 221, 103, 38, 238, 278, 267, 100, 157, 58, 76,
                    205, 143, 81, 172, 259, 187, 159, 202, 89, 42, 162, 28, 258, 128, 145, 164, 230, 151, 17, 239, 223,
                    131, 220, 194, 41, 227, 120, 47, 195, 111, 180, 250, 98, 213, 300, 80, 284, 14, 193, 247, 255, 156,
                    46, 295, 155, 273, 56, 283, 299, 63, 240, 197, 198, 144, 253, 104, 93, 204, 117, 252, 8, 181, 67,
                    84, 139, 208, 90, 97, 169, 290, 248, 138, 83, 59, 210, 231, 106, 233, 286, 79, 287, 142, 209, 256,
                    188, 5, 201, 48, 179, 177, 272, 108, 53, 29, 21, 25, 257, 52, 268, 185, 109, 37, 279, 64, 31, 49,
                    234, 298, 275, 270, 246, 178, 27, 282, 183, 110, 61, 88, 50, 87, 26, 43, 124, 192, 274, 94, 189,
                    161, 19, 102, 200, 44, 264, 130, 15, 243, 289, 203, 73, 1, 125, 199, 173, 36, 116, 82, 71, 215, 23,
                    141, 288, 126, 137, 207, 262, 293, 65, 277, 158, 153, 276, 285, 225, 2, 132, 263, 114, 4, 18, 85,
                    222, 245, 75, 191, 24, 95, 206, 167, 154, 39, 168, 13, 9, 66, 20, 57, 122, 251, 10, 12, 297, 226,
                    260, 118]

        nMinNum = min(len(cpu_id),len(randOrder))

        idInDec = [ord(x) for x in cpu_id]

        randOrder = randOrder[:nMinNum]

        sortedIdx = sorted(range(len(randOrder)), key=randOrder.__getitem__)

        rawIdxInDec = idInDec.copy()
        for i in range(0,nMinNum - 1):
            idInDec[i] = rawIdxInDec[sortedIdx[i]]

        return ''.join(hex(x)[2:] for x in idInDec)

    @staticmethod
    def translate(confuse_cpu_id: str):
        return_code = 0
        for i, v in enumerate(confuse_cpu_id[::-1]):
            return_code += ord(v) * i
            return_code *= 11
        return str(return_code)

    @staticmethod
    def getCpuId():
        os_type = sys.platform.lower()

        if "win" in os_type:
            command = "wmic bios get serialnumber"
        elif "linux" in os_type:
            # hard driver uuid
            command = "blkid | grep UUID= | awk '{print $2}'"
        elif "darwin" in os_type:
            command = "ioreg -l | grep IOPlatformSerialNumber | awk '{print $4}'"

        hardwareId = os.popen(command).read().replace("\n", "").replace(" ", "").replace("|", "")
        hardwareId = hardwareId.replace('SerialNumber', '').replace('UUID', '').replace('=', '').replace('-', '')

        return hardwareId

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
