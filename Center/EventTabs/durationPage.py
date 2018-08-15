from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QStackedWidget, QListWidget, QPushButton, QLabel, QLineEdit, \
    QGroupBox, \
    QHBoxLayout, QGridLayout, QVBoxLayout

from Center.EventTabs.deviceChooseDialog import DeviceOutDialog, DeviceInDialog
from Center.EventTabs.deviceItem import DeviceOutItem, DeviceInItem


class Tab3(QWidget):
    def __init__(self, parent=None):
        super(Tab3, self).__init__(parent)
        self.attributes = []
        # top
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
        self.out_devices_dialog = DeviceOutDialog()
        self.out_devices_dialog.ok_bt.clicked.connect(self.selectOut)
        self.out_devices_dialog.cancel_bt.clicked.connect(self.out_devices_dialog.close)
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
        self.in_devices_dialog = DeviceInDialog()
        self.in_devices_dialog.ok_bt.clicked.connect(self.selectIn)
        self.in_devices_dialog.cancel_bt.clicked.connect(self.in_devices_dialog.close)
        # bottom
        self.allowable = QLineEdit()
        self.correct = QLineEdit()
        self.RT_window = QComboBox()
        self.end_action = QComboBox()
        self.device_label = QLabel("——")
        self.setUI()

    # 生成duration页面
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
        self.in_devices_dialog.setWindowModality(Qt.ApplicationModal)
        self.in_devices_dialog.show()

    # 添加输入设备
    def selectIn(self, e):
        temp = self.in_devices_dialog.devices_list.currentItem()
        device_name = temp.text()
        if self.in_devices.count() == 0:
            self.in_tip1.hide()
            self.in_tip2.hide()
        item = DeviceInItem(device_name)
        self.in_devices.addItem(item)
        for i in range(self.out_devices.count()):
            name = self.out_devices.item(i).name
            self.in_devices.item(self.in_devices.count() - 1).resp_trigger_out.addItem(name)
        self.in_stack1.addWidget(item.pro1)
        self.in_stack2.addWidget(item.pro2)
        if self.in_devices.count():
            self.in_del_bt.setEnabled(True)
        self.in_devices_dialog.close()

    # 弹出输出设备选择框
    def showOutDevices(self):
        self.out_devices_dialog.setWindowModality(Qt.ApplicationModal)
        self.out_devices_dialog.show()

    # 添加输出设备
    def selectOut(self, e):
        temp = self.out_devices_dialog.devices_list.currentItem()
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
        self.out_devices_dialog.close()
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

    # 设置可选参数
    def setAttributes(self, attributes):
        self.attributes = attributes
        for i in range(self.in_devices.count()):
            self.in_devices.item(i).setAttributes(attributes)
        for i in range(self.out_devices.count()):
            self.out_devices.item(i).setAttributes(attributes)

    # 返回参数
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
        return {"duration": self.duration.currentText(), "input devices": in_info, "output device": out_info}
