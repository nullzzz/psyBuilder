from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QComboBox, QStackedWidget, QListWidget, QPushButton, QLabel, QGroupBox, \
    QHBoxLayout, QGridLayout, QVBoxLayout, QCompleter, QMessageBox

from .deviceChooseDialog import DeviceOutDialog, DeviceInDialog
from .deviceItem import DeviceOutItem, DeviceInItem


class DurationPage(QWidget):
    OUTPUT_DEVICES = {}
    INPUT_DEVICES = {}

    def __init__(self, parent=None):
        super(DurationPage, self).__init__(parent)

        self.attributes = []
        # top
        self.duration = QComboBox()
        # output device
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

        # input device
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

        self.setUI()

    # 生成duration页面
    def setUI(self):
        group0 = QGroupBox()
        self.duration.addItems(["(Infinite)", "100", "250", "500", "1000", "2000", "3000", "4000", "5000"])
        self.duration.setEditable(True)
        self.duration.lineEdit().textChanged.connect(self.findVar)
        self.duration.lineEdit().returnPressed.connect(self.finalCheck)

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

    # 检查变量
    def findVar(self, text):
        if text in self.attributes:
            self.sender().setStyleSheet("color: blue")
        else:
            self.sender().setStyleSheet("color:black")

    def finalCheck(self):
        temp = self.sender()
        text = temp.text()
        if text not in self.attributes:
            if text and text[0] == "[":
                QMessageBox.warning(self, "Warning", "Invalid Attribute!", QMessageBox.Ok)
                temp.clear()

    # 弹出输入设备选择框
    def showInDevices(self):
        self.in_devices_dialog = DeviceInDialog()
        self.in_devices_dialog.addDevices(DurationPage.INPUT_DEVICES)
        self.in_devices_dialog.ok_bt.clicked.connect(self.selectIn)
        self.in_devices_dialog.cancel_bt.clicked.connect(self.in_devices_dialog.close)
        self.in_devices_dialog.setWindowModality(Qt.ApplicationModal)
        self.in_devices_dialog.show()

    # 添加输入设备
    def selectIn(self, e):
        # 选中设备，默认为0号位置
        temp = self.in_devices_dialog.devices_list.currentItem()
        if temp:
            device_name = temp.text()
            # 占位提示
            if self.in_devices.count() == 0:
                self.in_tip1.hide()
                self.in_tip2.hide()
            item = DeviceInItem(device_name)
            self.in_devices.addItem(item)
            # 设置可选变量
            item.setAttributes(self.attributes)
            # 添加可选trigger输出设备
            for i in range(self.out_devices.count()):
                name = self.out_devices.item(i).name
                self.in_devices.item(self.in_devices.count() - 1).resp_trigger_out.addItem(name)
            self.in_stack1.addWidget(item.pro1)
            self.in_stack2.addWidget(item.pro2)
            # 设置remove按钮可用性
            if self.in_devices.count():
                self.in_del_bt.setEnabled(True)
        self.in_devices_dialog.close()

    # 弹出输出设备选择框
    def showOutDevices(self):
        self.out_devices_dialog = DeviceOutDialog()
        self.out_devices_dialog.ok_bt.clicked.connect(self.selectOut)
        self.out_devices_dialog.cancel_bt.clicked.connect(self.out_devices_dialog.close)
        self.out_devices_dialog.setWindowModality(Qt.ApplicationModal)
        self.out_devices_dialog.show()

    # 添加输出设备
    def selectOut(self, e):
        temp = self.out_devices_dialog.devices_list.currentItem()
        if temp:
            device_name = temp.text()
            if self.out_devices.count() == 0:
                self.out_tip.hide()
            item = DeviceOutItem(device_name)
            self.out_devices.addItem(item)
            # 设置可选变量
            item.setAttributes(self.attributes)
            # 设置trigger输出设备
            for i in range(self.in_devices.count()):
                self.in_devices.item(i).resp_trigger_out.addItem(device_name)
            self.out_stack.addWidget(item.pro)
            if self.out_devices.count():
                self.out_del_bt.setEnabled(True)
        self.out_devices_dialog.close()

    # 移除输入设备
    def removeInDevices(self):
        index = self.in_devices.currentRow()
        # 选中有效
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
            # 移除trigger可选输出设备
            for i in range(self.in_devices.count()):
                self.in_devices.item(i).resp_trigger_out.removeItem(index)
            if self.out_devices.count() == 0:
                self.out_del_bt.setEnabled(False)
                self.out_tip.show()
            # 限制输出设备数为4
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
        self.duration.setCompleter(QCompleter(self.attributes))
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

        return {
            "Duration": self.duration.currentText(),
            "Input devices": in_info,
            "Output device": out_info
        }
