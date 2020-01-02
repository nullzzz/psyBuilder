import sys

from quamash import QApplication

from app import Psy
from qss import mac_qss

if __name__ == '__main__':
    app = QApplication(sys.argv)
    psy = Psy()
    psy.showMaximized()
    app.setStyleSheet(mac_qss)
    sys.exit(app.exec_())
