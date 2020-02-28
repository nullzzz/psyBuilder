import platform
import sys

from PyQt5.QtWidgets import QApplication

from app import Psy
from app.kernel import Kernel
from qss import mac_qss
from qss import windows_qss

if __name__ == '__main__':
    app = QApplication(sys.argv)
    psy = Psy()
    # bind psy to Kernel.Psy
    Kernel.Psy = psy
    # init initial timeline
    psy.showMaximized()
    # choose qss
    if platform.system() == "Windows":
        app.setStyleSheet(windows_qss)
    else:
        app.setStyleSheet(mac_qss)
    sys.exit(app.exec_())
