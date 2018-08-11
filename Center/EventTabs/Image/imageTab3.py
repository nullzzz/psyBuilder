from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidgetItem, QWidget, QDialog, QComboBox, QStackedWidget, QListWidget, \
    QPushButton, QLabel, QLineEdit, QGroupBox, QHBoxLayout, QGridLayout, QVBoxLayout, QListView, QFormLayout


# 重写上方输出设备list widget的item
class DeviceOutItem(QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super(DeviceOutItem, self).__init__(name, parent)
        self.name = name
        self.devices = []
        self.pro = QWidget()
        self.value1 = QLineEdit()
        self.value1.textChanged.connect(self.findVar)
        self.attributes = []
        self.value = ""
        self.pulse_dur = QComboBox()
        self.pulse_dur.setEditable(True)
        self.pulse_dur.addItem("End of Duration")
        self.setPro()

    def setPro(self):
        layout = QGridLayout()
        l1 = QLabel("Value or Message:")
        l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(l1, 0, 0)
        layout.addWidget(self.value1, 0, 1)
        l2 = QLabel("Pulse Dur:")
        l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        layout.addWidget(l2, 1, 0)
        layout.addWidget(self.pulse_dur, 1, 1)
        layout.setVerticalSpacing(40)
        # 左、上、右、下
        layout.setContentsMargins(10, 3, 10, 0)
        self.pro.setLayout(layout)

    def findVar(self):
        self.value = self.value1.text()
        if len(self.value) > 2 and self.value[0] == "[" and self.value[-1] == "]" and self.value[1:-1] in self.attributes:
            print(self.value[1:-1])
            self.value1.setStyleSheet("color:blue")
        else:
            self.value1.setStyleSheet("color:black")

    # 设置可选属性
    def setAttributes(self, attributes):
        self.attributes = attributes

    def getInfo(self):
        return {
            "Device name": self.name,
            "Value or msg": self.value,
            "Pulse Duration": self.pulse_dur.currentText()
        }


# 下部list widget的item重写
class DeviceInItem(QListWidgetItem):
    def __init__(self, name=None, parent=None):
        super(DeviceInItem, self).__init__(name, parent)
        self.name = name
        self.attributes = []
        self.pro1 = QWidget()
        self.device_label = QLabel(name)
        self.allowable = QLineEdit()
        self.allowable.textChanged.connect(self.findVar1)
        self.correct = QLineEdit()
        self.correct.textChanged.connect(self.findVar2)
        self.RT_window = QComboBox()
        self.RT_window.editTextChanged.connect(self.findVar3)
        self.RT_window.addItems(["(Same as duration)",
                                 "(End of timeline)",
                                 "1000",
                                 "2000",
                                 "3000",
                                 "4000",
                                 "5000"])
        self.end_action = QComboBox()
        self.end_action.addItems(["Terminate", "(None)"])

        self.action = QComboBox()
        self.action.addItems(["Fixation", "Saccade"])
        self.ROA = QLineEdit()
        self.ROA.textChanged.connect(self.findVar4)
        self.ROA2 = QComboBox()
        self.ROA2.addItems(["Outside", "Inside"])

        self.pro2 = QWidget()
        self.right = QLineEdit()
        self.right.textChanged.connect(self.findVar5)
        self.wrong = QLineEdit()
        self.wrong.textChanged.connect(self.findVar6)
        self.ignore = QLineEdit()
        self.ignore.textChanged.connect(self.findVar7)
        self.resp_trigger_out = QComboBox()
        self.setPro()

    def setPro(self):
        self.RT_window.setEditable(True)
        if "eye" not in self.name:
            layout1 = QFormLayout()
            layout1.addRow("Response:", self.device_label)
            layout1.addRow("Allowable:", self.allowable)
            layout1.addRow("Correct:", self.correct)
            layout1.addRow("RT window:", self.RT_window)
            layout1.addRow("End action:", self.end_action)
            layout1.setLabelAlignment(Qt.AlignRight)
        else:
            layout1 = QGridLayout()
            l1 = QLabel("Response:")
            l1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout1.addWidget(l1, 0, 0, 1, 1)
            layout1.addWidget(self.device_label, 0, 1, 1, 2)
            l2 = QLabel("Action:")
            l2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout1.addWidget(l2, 1, 0, 1, 1)
            layout1.addWidget(self.action, 1, 1, 1, 2)
            l3 = QLabel("ROA:")
            l3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout1.addWidget(l3, 2, 0, 1, 1)
            layout1.addWidget(self.ROA, 2, 1, 1, 1)
            layout1.addWidget(self.ROA2, 2, 2, 1, 1)
            l4 = QLabel("Duration:")
            l4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout1.addWidget(l4, 3, 0, 1, 1)
            layout1.addWidget(self.RT_window, 3, 1, 1, 2)
            l5 = QLabel("End Action:")
            l5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            layout1.addWidget(l5, 4, 0, 1, 1)
            layout1.addWidget(self.end_action, 4, 1, 1, 2)
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
        layout2.addWidget(QLabel("Device:"), 1, 6)
        layout2.addWidget(self.resp_trigger_out, 1, 7)
        self.pro2.setLayout(layout2)

    def getInfo(self):
        if "eye" not in self.name:
            return {
                "Device name": self.name,
                "Allowable": self.allowable.text(),
                "Correct": self.correct.text(),
                "RT window": self.RT_window.currentText(),
                "End action": self.end_action.currentText(),
                "Right": self.right.text(),
                "Wrong": self.wrong.text(),
                "No resp": self.ignore.text(),
                "Output device": self.resp_trigger_out
            }
        else:
            return {
                "Device name": self.name,
                "Action": self.action.currentText(),
                "XX": self.ROA.text(),
                "IOA": self.action.currentText(),
                "duration": self.RT_window.currentText(),
                "End action": self.end_action.currentText(),
                "Right": self.right.text(),
                "Wrong": self.wrong.text(),
                "No resp": self.ignore.text(),
                "Output device": self.resp_trigger_out
            }

    def findVar1(self):
        value = self.allowable.text()
        if value:
            if value[0] == "[" and value[-1] == "]" and value[1:-1] in self.attributes:
                self.allowable.setStyleSheet("color:blue")
            else:
                self.allowable.setStyleSheet("color:black")

    def findVar2(self):
        value = self.correct.text()
        if value:
            if value[0] == "[" and value[-1] == "]" and value[1:-1] in self.attributes:
                self.correct.setStyleSheet("color:blue")
            else:
                self.correct.setStyleSheet("color:black")

    def findVar3(self, e):
        value = e
        if value:
            if value[0] == "[" and value[-1] == "]" and value[1:-1] in self.attributes:
                self.RT_window.setStyleSheet("color:blue")

        #     self.RT_window.setStyleSheet("color:black")

    def findVar4(self):
        value = self.ROA.text()
        if value:
            if value[0] == "[" and value[-1] == "]" and value[1:-1] in self.attributes:
                self.ROA.setStyleSheet("color:blue")
            else:
                self.ROA.setStyleSheet("color:black")

    def findVar5(self):
        value = self.right.text()
        if value:
            if value[0] == "[" and value[-1] == "]" and value[1:-1] in self.attributes:
                self.right.setStyleSheet("color:blue")
            else:
                self.right.setStyleSheet("color:black")

    def findVar6(self):
        value = self.wrong.text()
        if value:
            if value[0] == "[" and value[-1] == "]" and value[1:-1] in self.attributes:
                self.wrong.setStyleSheet("color:blue")
            else:
                self.wrong.setStyleSheet("color:black")

    def findVar7(self):
        value = self.ignore.text()
        if value:
            if value[0] == "[" and value[-1] == "]" and value[1:-1] in self.attributes:
                self.ignore.setStyleSheet("color:blue")
            else:
                self.ignore.setStyleSheet("color:black")

    # 设置可选属性
    def setAttributes(self, attributes):
        self.attributes = attributes


class Tab3(QWidget):
    def __init__(self, parent=None):
        super(Tab3, self).__init__(parent)
        # up
        self.duration = QComboBox()
        self.out_stack = QStackedWidget()
        self.out_stack.setStyleSheet("{border: 2px; background-color: white}")
        self.out_devices = QListWidget()
        self.out_devices.currentItemChanged.connect(self.deviceOutChanged)
        self.out_add_bt = QPushButton("+")
        self.out_add_bt.clicked.connect(self.showOutDevices)
        self.out_del_bt = QPushButton("-")
        self.out_del_bt.clicked.connect(self.removeOutDevices)
        self.out_del_bt.setEnabled(False)
        self.out_tip = QLabel("Add output device(s) first")
        self.out_tip.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.outDevices = DeviceOutDialog()
        self.outDevices.ok_bt.clicked.connect(self.selectOut)
        self.outDevices.cancel_bt.clicked.connect(self.outDevices.close)
        # down
        self.in_stack1 = QStackedWidget()
        self.in_stack2 = QStackedWidget()
        self.in_tip1 = QLabel("Add input device(s) first")
        self.in_tip2 = QLabel("Resp Trigger:")
        self.in_tip1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.in_tip2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.in_devices = QListWidget()
        self.in_devices.currentItemChanged.connect(self.deviceInChanged)
        self.in_add_bt = QPushButton("&Add...")
        self.in_del_bt = QPushButton("&Remove...")
        self.inDevices = DeviceInDialog()
        self.inDevices.ok_bt.clicked.connect(self.selectIn)
        self.inDevices.cancel_bt.clicked.connect(self.inDevices.close)
        # bottom
        self.allowable = QLineEdit()
        self.correct = QLineEdit()
        self.RT_window = QComboBox()
        self.end_action = QComboBox()
        self.device_label = QLabel("——")
        self.setUI()

    # 生成action页面
    def setUI(self):
        group0 = QGroupBox()
        self.duration.addItems(
            ["(Infinite)", "100", "250", "500", "1000", "2000", "3000", "4000", "5000"])
        self.duration.setEditable(True)
        layout0 = QHBoxLayout()
        layout0.addWidget(QLabel("Duration(ms):"), 1)
        layout0.addWidget(self.duration, 4)
        group0.setLayout(layout0)

        group1 = QGroupBox("Stim Trigger")
        layout1 = QGridLayout()
        layout1.addWidget(QLabel("Output Devices"), 0, 0, 1, 2)
        layout1.addWidget(QLabel("Trigger Info"), 0, 2, 1, 1)
        layout1.addWidget(self.out_devices, 1, 0, 2, 2)
        layout1.addWidget(self.out_add_bt, 3, 0, 1, 1)
        layout1.addWidget(self.out_del_bt, 3, 1, 1, 1)
        layout1.addWidget(QListWidget(), 1, 2, 3, 2)
        layout1.addWidget(self.out_tip, 1, 2, 2, 2)
        layout1.addWidget(self.out_stack, 1, 2, 2, 2)
        layout1.setVerticalSpacing(0)
        group1.setLayout(layout1)

        group2 = QGroupBox("Input Devices")
        layout2 = QGridLayout()
        self.in_add_bt.clicked.connect(self.showInDevices)
        self.in_del_bt.setEnabled(False)
        self.in_del_bt.clicked.connect(self.removeInDevices)

        self.end_action.addItems(["(None)", "Terminate"])
        self.in_devices.setStyleSheet("background-color: white;")
        layout2.addWidget(QLabel("Device(s)"), 0, 0, 1, 1)
        layout2.addWidget(self.in_devices, 1, 0, 3, 2)
        layout2.addWidget(self.in_add_bt, 4, 0, 1, 1)
        layout2.addWidget(self.in_del_bt, 4, 1, 1, 1)
        layout2.addWidget(self.in_tip1, 1, 2, 5, 2)

        layout2.addWidget(self.in_stack1, 0, 2, 5, 2)
        layout2.addWidget(self.in_tip2, 5, 0, 2, 4)
        layout2.addWidget(self.in_stack2, 5, 0, 2, 4)

        layout2.setVerticalSpacing(0)
        group2.setLayout(layout2)

        layout = QVBoxLayout()
        layout.addWidget(group0, 1)
        layout.addWidget(group1, 6)
        layout.addWidget(group2, 6)
        self.setLayout(layout)

    # 弹出输入设备选择框
    def showInDevices(self):
        self.inDevices.setWindowModality(Qt.ApplicationModal)
        self.inDevices.show()

    # 添加输入设备
    def selectIn(self, e):
        temp = self.inDevices.devices_list.currentItem()
        device_name = temp.text()
        if self.in_devices.count() == 0:
            self.in_tip1.hide()
            self.in_tip2.hide()
        item = DeviceInItem(device_name)
        self.in_devices.addItem(item)
        for i in range(self.out_devices.count()):
            try:
                name = self.out_devices.item(i).name
                self.in_devices.item(self.in_devices.count() - 1).resp_trigger_out.addItem(name)
            except Exception as e:
                print(e)
        self.in_stack1.addWidget(item.pro1)
        self.in_stack2.addWidget(item.pro2)
        if self.in_devices.count():
            self.in_del_bt.setEnabled(True)
        self.inDevices.close()

    # 弹出输出设备选择框
    def showOutDevices(self):
        self.outDevices.setWindowModality(Qt.ApplicationModal)
        self.outDevices.show()

    # 添加输出设备
    def selectOut(self, e):
        temp = self.outDevices.devices_list.currentItem()
        device_name = temp.text()
        if self.out_devices.count() == 0:
            self.out_tip.hide()
        item = DeviceOutItem(device_name)
        self.out_devices.addItem(item)
        for i in range(self.in_devices.count()):
            try:
                self.in_devices.item(i).resp_trigger_out.addItem(device_name)
            except Exception as e:
                print(e)
        self.out_stack.addWidget(item.pro)
        if self.out_devices.count():
            self.out_del_bt.setEnabled(True)
        self.outDevices.close()
        self.getInfo()

    # 移除输入设备
    def removeInDevices(self):
        index = self.in_devices.currentRow()
        if index != -1:
            item = self.in_devices.takeItem(index)
            self.in_stack1.removeWidget(item.pro1)
            self.in_stack2.removeWidget(item.pro2)
            if not self.in_devices.count():
                self.in_del_bt.setEnabled(False)
                self.in_tip1.show()
                self.in_tip2.show()

    # 移除输出设备
    def removeOutDevices(self):
        index = self.out_devices.currentRow()
        if index != -1:
            item = self.out_devices.takeItem(index)
            self.out_stack.removeWidget(item.pro)
            for i in range(self.in_devices.count()):
                try:
                    self.in_devices.item(i).resp_trigger_out.removeItem(index)
                except Exception as e:
                    print(e)
            if self.out_devices.count() == 0:
                self.out_del_bt.setEnabled(False)
                self.out_tip.show()
            elif self.out_devices.count() < 4:
                self.out_add_bt.setEnabled(True)

    # 选中输入设备改变
    def deviceInChanged(self, e):
        if e:
            index = self.in_devices.row(e)
            self.in_stack1.setCurrentIndex(index)
            self.in_stack2.setCurrentIndex(index)

    # 选中输出设备改变
    def deviceOutChanged(self, e):
        if e:
            index = self.out_devices.row(e)
            self.out_stack.setCurrentIndex(index)

    # 从菜单栏添加待选设备
    def add_devices(self, devices):
        pass

    def getInfo(self):
        in_info = {}
        out_info = {}
        for i in range(self.in_devices.count()):
            key = self.in_devices.item(i).text()
            if key in in_info.keys():
                key += "_another"
            in_info[key] = self.in_devices.item(i).getInfo()

        for i in range(self.out_devices.count()):
            key = self.out_devices.item(i).text()
            if key in out_info.keys():
                key += "_another"
            out_info[key] = self.out_devices.item(i).getInfo()
        return in_info, out_info


# 重写输入设备选择弹窗
class DeviceInDialog(QDialog):
    def __init__(self, parent=None):
        super(DeviceInDialog, self).__init__(parent)
        self.devices_list = QListWidget()
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.setUI()

    def setUI(self):
        self.resize(500, 350)
        self.setWindowTitle("Choose Input Device(s)")
        self.devices_list.setViewMode(QListView.IconMode)
        self.devices_list.setSortingEnabled(True)
        self.devices_list.setAcceptDrops(False)
        self.devices_list.setAutoFillBackground(True)
        self.devices_list.setWrapping(False)
        self.devices_list.setSpacing(20)

        item1 = QListWidgetItem("eye")
        item1.setIcon(QIcon(".\\.\\image\\1"))
        self.devices_list.addItem(item1)
        item2 = QListWidgetItem("device2")
        item2.setIcon(QIcon(".\\.\\image\\2"))
        self.devices_list.addItem(item2)
        item3 = QListWidgetItem("device1")
        item3.setIcon(QIcon(".\\.\\image\\3"))
        self.devices_list.addItem(item3)

        layout = QGridLayout()
        layout.addWidget(self.devices_list, 0, 0, 1, 4)
        layout.addWidget(self.ok_bt, 1, 2, 1, 1)
        layout.addWidget(self.cancel_bt, 1, 3, 1, 1)
        self.setLayout(layout)

    # 从菜单栏添加待选设备
    def add_devices(self, devices):
        pass


# 重写输出设备选择弹窗
class DeviceOutDialog(QDialog):
    def __init__(self, parent=None):
        super(DeviceOutDialog, self).__init__(parent)
        self.devices_list = QListWidget()
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.setUI()

    def setUI(self):
        self.resize(500, 350)
        self.setWindowTitle("Choose Output Device(s)")
        self.devices_list.setViewMode(QListView.IconMode)
        self.devices_list.setSortingEnabled(True)
        self.devices_list.setAcceptDrops(False)
        self.devices_list.setAutoFillBackground(True)
        self.devices_list.setWrapping(False)
        self.devices_list.setSpacing(20)

        item1 = QListWidgetItem("eye")
        item1.setIcon(QIcon(".\\.\\image\\1"))
        self.devices_list.addItem(item1)
        item2 = QListWidgetItem("device2")
        item2.setIcon(QIcon(".\\.\\image\\2"))
        self.devices_list.addItem(item2)
        item3 = QListWidgetItem("device1")
        item3.setIcon(QIcon(".\\.\\image\\3"))
        self.devices_list.addItem(item3)

        layout = QGridLayout()
        layout.addWidget(self.devices_list, 0, 0, 1, 4)
        layout.addWidget(self.ok_bt, 1, 2, 1, 1)
        layout.addWidget(self.cancel_bt, 1, 3, 1, 1)
        self.setLayout(layout)