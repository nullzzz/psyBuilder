import sys

from quamash import QApplication

from app import Psy

if __name__ == '__main__':
    app = QApplication(sys.argv)
    psy = Psy()
    psy.showMaximized()
    sys.exit(app.exec_())
