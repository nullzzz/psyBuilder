import sys

from quamash import QApplication

from app import Psy
from app.kernel import Kernel
from qss import mac_qss

if __name__ == '__main__':
    app = QApplication(sys.argv)
    psy = Psy()
    # bind psy to Kernel.Psy
    Kernel.Psy = psy
    psy.initInitialTimeline()
    psy.showMaximized()
    app.setStyleSheet(mac_qss)
    sys.exit(app.exec_())
