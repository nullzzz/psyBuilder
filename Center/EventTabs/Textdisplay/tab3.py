import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *


# 重写上方输出设备list widget的item
class DeviceOutItem(QListWidgetItem):
    def __init__(self, parent=None):
        super(DeviceOutItem, self).__init__(parent)
        self.pro = QWidget()

        self.value = QComboBox()
        self.value.setEditable(True)
        self.tri_dur = QComboBox()
        self.tri_dur.setEditable(True)
        self.tri_dur.addItem("End of Duration")
        self.setPro()

    def setPro(self):
        layout = QFormLayout()
        layout.addRow("Value:", self.value)
        layout.addRow("Pulse Dur:", self.tri_dur)
        layout.setLabelAlignment(Qt.AlignRight)
        layout.setVerticalSpacing(40)
        # 左、上、右、下
        layout.setContentsMargins(10, 40, 10, 0)
        self.pro.setLayout(layout)


# 下部list widget的item重写
class DeviceInItem(QListWidgetItem):
    def __init__(self, text=None, parent=None):
        super(DeviceInItem, self).__init__(text, parent)
        self.pro1 = QWidget()
        self.device_label = QLabel(text)
        self.allowable = QLineEdit()
        self.correct = QLineEdit()
        self.RT_window = QComboBox()
        self.RT_window.addItems(["(same as action)",
                                 "(until feedback)",
                                 "(end of proc)",
                                 "(infinite)",
                                 "1000",
                                 "2000",
                                 "3000",
                                 "4000",
                                 "5000"])
        self.end_action = QComboBox()

        self.pro2 = QWidget()
        self.device = QComboBox()
        self.right = QLineEdit()
        self.wrong = QLineEdit()
        self.ignore = QLineEdit()
        self.setPro()

    def setPro(self):
        layout1 = QFormLayout()
        layout1.addRow("Response:", self.device_label)
        layout1.addRow("Allowable:", self.allowable)
        layout1.addRow("Correct:", self.correct)
        layout1.addRow("RT window:", self.RT_window)
        layout1.addRow("End action:", self.end_action)
        layout1.setLabelAlignment(Qt.AlignRight)
        layout1.setVerticalSpacing(20)
        layout1.setContentsMargins(10, 0, 0, 0)
        self.pro1.setLayout(layout1)

        layout2 = QGridLayout()
        layout2.addWidget(QLabel("Resp Trigger"), 0, 0, 1, 2)
        layout2.addWidget(QLabel("Right:"), 1, 0)
        layout2.addWidget(self.right, 1, 1)
        layout2.addWidget(QLabel("Wrong:"), 1, 2)
        layout2.addWidget(self.wrong, 1, 3)
        layout2.addWidget(QLabel("No resp:"), 1, 4)
        layout2.addWidget(self.ignore, 1, 5)
        self.pro2.setLayout(layout2)


class Tab3(QWidget):
    def __init__(self, parent=None):
        super(Tab3, self).__init__(parent)
        # action
        # up
        self.duration = QComboBox()
        self.out_stack = QStackedWidget()
        self.out_stack.setStyleSheet("{border: 2px; background-color: white}")
        self.up_list = QListWidget()
        self.up_list.currentItemChanged.connect(self.deviceOutChanged)
        self.up_add_bt1 = QPushButton("+")
        self.up_add_bt1.clicked.connect(self.showOutDevices)
        self.up_del_bt2 = QPushButton("-")
        self.up_del_bt2.clicked.connect(self.removeOutDevices)
        self.up_del_bt2.setEnabled(False)
        self.up_tip = QLabel("Add output device(s) first")
        self.up_tip.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # down
        self.in_stack1 = QStackedWidget()
        self.in_stack2 = QStackedWidget()
        self.down_tip = QLabel("Add input device(s) first")
        self.down_tip2 = QLabel("Resp Trigger:")
        self.down_tip.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.down_tip2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.devices = QListWidget()
        self.devices.currentItemChanged.connect(self.deviceInChanged)
        self.devices_bt1 = QPushButton("&Add...")
        self.devices_bt2 = QPushButton("&Remove...")

        self.allowable = QLineEdit()
        self.correct = QLineEdit()
        self.RT_window = QComboBox()
        self.end_action = QComboBox()
        self.device_label = QLabel("——")
        self.setAction()

        a = """
        QPushButton:hover{
        border: 4px solid forestgreen;
        border-radius: 10px;
        padding: 2px;
        background-color: beige;
        }
        """
        self.setStyleSheet(a)

    # 生成action页面
    def setAction(self):
        group0 = QGroupBox()
        self.duration.addItems(
            ["(infinite)", "100", "250", "500", "1000", "2000", "3000", "4000", "5000"])
        self.duration.setEditable(True)
        layout0 = QHBoxLayout()
        layout0.addWidget(QLabel("Duration"), 1)
        layout0.addWidget(self.duration, 4)
        group0.setLayout(layout0)

        group1 = QGroupBox("Stim Trigger")
        layout1 = QGridLayout()
        layout1.addWidget(QLabel("Output Devices"), 0, 0, 1, 2)
        layout1.addWidget(QLabel("Trigger Info"), 0, 2, 1, 1)
        layout1.addWidget(self.up_list, 1, 0, 2, 2)
        layout1.addWidget(self.up_add_bt1, 3, 0, 1, 1)
        layout1.addWidget(self.up_del_bt2, 3, 1, 1, 1)
        layout1.addWidget(QListWidget(), 1, 2, 3, 2)
        layout1.addWidget(self.up_tip, 1, 2, 2, 2)
        layout1.addWidget(self.out_stack, 1, 2, 2, 2)
        layout1.setVerticalSpacing(0)
        group1.setLayout(layout1)

        group2 = QGroupBox("Input Masks")
        layout2 = QGridLayout()
        self.devices_bt1.clicked.connect(self.showInDevices)
        self.devices_bt2.setEnabled(False)
        self.devices_bt2.clicked.connect(self.removeInDevices)

        self.end_action.addItems(["(none)", "Terminate"])
        self.devices.setStyleSheet("background-color: white;")
        layout2.addWidget(QLabel("Device(s)"), 0, 0, 1, 1)
        layout2.addWidget(self.devices, 1, 0, 3, 2)
        layout2.addWidget(self.devices_bt1, 4, 0, 1, 1)
        layout2.addWidget(self.devices_bt2, 4, 1, 1, 1)
        # layout2.addWidget(QListWidget(), 1, 2, 5, 2)
        layout2.addWidget(self.down_tip, 1, 2, 5, 2)

        layout2.addWidget(self.in_stack1, 0, 2, 5, 2)
        layout2.addWidget(self.down_tip2, 5, 0, 2, 4)
        layout2.addWidget(self.in_stack2, 5, 0, 2, 4)
        # self.in_stack1.setStyleSheet("background-color: black;")
        # self.in_stack2.setStyleSheet("background-color: black;")

        layout2.setVerticalSpacing(0)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group0, 1)
        layout.addWidget(group1, 6)
        layout.addWidget(group2, 6)
        self.setLayout(layout)

    # 弹出输入设备选择框
    def showInDevices(self):
        items = ("Mouse", "Keyboard")
        text, ok = QInputDialog.getItem(
            self, "Choose device", "Device:", items, 0, False)
        if ok and text:
            if self.devices.count() == 0:
                self.down_tip.hide()
                self.down_tip2.hide()
            item = DeviceInItem(text)
            self.devices.addItem(item)
            self.in_stack1.addWidget(item.pro1)
            self.in_stack2.addWidget(item.pro2)
        if self.devices.count():
            self.devices_bt2.setEnabled(True)

    def showOutDevices(self):
        items = ("Mouse", "Keyboard")
        text, ok = QInputDialog.getItem(
            self, "Choose device", "Device:", items, 0, False)
        if ok and text:
            if self.up_list.count() < 4:
                print(self.up_list.count())
                if self.up_list.count() == 0:
                    self.up_tip.hide()
                    print("remove")
                item = DeviceOutItem(text)
                self.up_list.addItem(item)
                self.out_stack.addWidget(item.pro)
                if self.up_list.count() == 4:
                    self.up_add_bt1.setEnabled(False)
        if self.up_list.count():
            self.up_del_bt2.setEnabled(True)

    # 移除输入设备
    def removeInDevices(self):
        index = self.devices.currentRow()
        if index != -1:
            item = self.devices.takeItem(index)
            self.in_stack1.removeWidget(item.pro1)
            self.in_stack2.removeWidget(item.pro2)
            if not self.devices.count():
                self.devices_bt2.setEnabled(False)
                self.down_tip.show()
                self.down_tip2.show()

    # 移除输出设备
    def removeOutDevices(self):
        index = self.up_list.currentRow()
        if index != -1:
            item = self.up_list.takeItem(index)
            self.out_stack.removeWidget(item.pro)
            if self.up_list.count() == 0:
                self.up_del_bt2.setEnabled(False)
                self.up_tip.show()
            elif self.up_list.count() < 4:
                self.up_add_bt1.setEnabled(True)

    # 选中设备改变
    def deviceInChanged(self, e):
        if e:
            index = self.devices.row(e)
            self.in_stack1.setCurrentIndex(index)
            self.in_stack2.setCurrentIndex(index)

    # 选择输出设备改变

    def deviceOutChanged(self, e):
        if e:
            index = self.up_list.row(e)
            self.out_stack.setCurrentIndex(index)

# TODO：重写设备选择弹窗


if __name__ == "__main__":
    app = QApplication(sys.argv)

    t = Tab3()

    t.show()

    sys.exit(app.exec())
