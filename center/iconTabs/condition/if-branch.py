from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QGroupBox, QComboBox, QLineEdit, QPushButton, QGridLayout, QApplication, QLabel, \
    QVBoxLayout, QMessageBox


class IfBranch(QWidget):
    def __init__(self, parent=None):
        super(IfBranch, self).__init__(parent)
        self.add_condition = QPushButton("&Add")

        self.var1 = QComboBox()
        self.compare1 = QComboBox()
        self.value1 = QLineEdit()

        self.and_or1 = QComboBox()
        self.var2 = QComboBox()
        self.compare2 = QComboBox()
        self.value2 = QLineEdit()

        self.t_event = QComboBox()
        self.t_event.currentTextChanged.connect(self.changeImage)
        self.t_event_image = MyLabel()
        self.t_event_image.double_click.connect(self.showProperty)

        self.f_event = QComboBox()
        self.f_event.currentTextChanged.connect(self.changeImage)
        self.f_event_image = MyLabel()
        self.f_event_image.double_click.connect(self.showProperty)

        self.setUI()

    def setUI(self):
        self.compare1.addItems((">", "<", "=="))
        self.and_or1.addItems(("and", "or"))
        self.compare2.addItems((">", "<", "=="))

        self.t_event.addItems(["Image", "SoundOut", "Text", "Video"])
        self.t_event.setObjectName("t_event")
        self.f_event.addItems(["Image", "SoundOut", "Text", "Video"])


        group1 = QGroupBox("Condition")
        layout1 = QGridLayout()
        layout1.addWidget(self.var1, 0, 1, 1, 1)
        layout1.addWidget(self.compare1, 0, 2, 1, 1)
        layout1.addWidget(self.value1, 0, 3, 1, 1)
        layout1.addWidget(self.add_condition, 0, 4, 1, 1)

        layout1.addWidget(self.and_or1, 1, 0, 1, 1)
        layout1.addWidget(self.var2, 1, 1, 1, 1)
        layout1.addWidget(self.compare2, 1, 2, 1, 1)
        layout1.addWidget(self.value2, 1, 3, 1, 1)

        group1.setLayout(layout1)

        group2 = QGroupBox("True")
        layout2 = QVBoxLayout()
        layout2.addWidget(self.t_event)
        layout2.addWidget(self.t_event_image, Qt.AlignHCenter)
        group2.setLayout(layout2)

        group3 = QGroupBox("False")
        layout3 = QVBoxLayout()
        layout3.addWidget(self.f_event)
        layout3.addWidget(self.f_event_image, Qt.AlignHCenter)
        group3.setLayout(layout3)

        layout = QGridLayout()
        layout.addWidget(group1, 0, 0, 1, 2)
        layout.addWidget(group2, 1, 0, 2, 1)
        layout.addWidget(group3, 1, 1, 2, 1)
        self.setLayout(layout)

    def changeImage(self, event_name):
        pix = QPixmap()
        pix.load(r"D:\PsyDemo\image\{}".format(event_name))
        if self.sender() == self.t_event:
            self.t_event_image.setPixmap(pix)
        else:
            self.f_event_image.setPixmap(pix)

    def showProperty(self):
        QMessageBox.warning(self, "todo", "set the properties of the event", QMessageBox.Ok)

    def getInfo(self):
        return {

        }
class MyLabel(QLabel):
    double_click = pyqtSignal()

    def __init__(self, parent=None):
        super(MyLabel, self).__init__(parent)
        self.setAlignment(Qt.AlignCenter)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.double_click.emit()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    t = IfBranch()

    t.show()

    sys.exit(app.exec())
