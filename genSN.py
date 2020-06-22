import hashlib
import sys

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QApplication, QPushButton, QFrame, QDesktopWidget

from app.info import Info


class genKeyWindow(QFrame):

    def __init__(self):
        super(genKeyWindow, self).__init__()
        # title

        # if getattr(sys, 'frozen', False): # we are running in a |PyInstaller| bundle 
        #     basedir = sys._MEIPASS 
        # else: # we are running in a normal Python environment 
        #     basedir = os.path.dirname(__file__)

        self.setWindowTitle("KeyGen for PsyBuilder")
        self.setWindowIcon(QIcon(r"source/images/common/icon.png"))

        if Info.OS_TYPE ==2:
            self.setMinimumSize(400, 200)
        else:
            self.setFixedSize(400, 120)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Input your hardware sn here")

        self.output = QLineEdit()
        self.input.setPlaceholderText("")

        self.check_bt = QPushButton("Generate")
        self.check_bt.clicked.connect(self.generateCode)

        self.setUI()
        self.show()

    def generateCode(self):
        input_code = self.input.text()
        output_code = self.confuse(input_code)

        self.output.clear()
        self.output.setText(output_code)
		

    def setUI(self):
        # self.setFixedSize(200, 200)
        layout = QFormLayout()
        layout.addRow("Hardware  SN:",self.input)
        layout.addRow("Generated SN:",self.output)
        layout.addRow("",self.check_bt)
        self.setLayout(layout)

        self.input.setPlaceholderText("Input your hardware sn here")
        self.moveToCenter()

    def moveToCenter(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    @staticmethod
    def confuse(cpu_id: str):

        cpu_id = 'gfweas12' + cpu_id + 'sc'

        hl = hashlib.md5()
        hl.update(cpu_id.encode(encoding='utf-8'))

        return hl.hexdigest()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    v = genKeyWindow()

    sys.exit(app.exec_())
