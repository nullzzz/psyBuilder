import sys

from quamash import QApplication

from app.main.main import PsyApplication
from conf.psy_qss import style_sheet

if __name__ == '__main__':
    app = QApplication(sys.argv)
    psy_application = PsyApplication()
    psy_application.initialize()
    psy_application.showMaximized()

    app.setStyleSheet(style_sheet)
    sys.exit(app.exec_())
