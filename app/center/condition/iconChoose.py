import time

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QComboBox

from app.func import Func
from app.info import Info


class IconChoose(QWidget):
    """
    {
        "stim type": "Image",
        "event name": "",
        "Pro window": {}
    }
    """
    itemAdded = pyqtSignal(str, str)
    itemDeleted = pyqtSignal(str)
    itemNameChanged = pyqtSignal(str, str)

    def __init__(self, parent=None):
        super(IconChoose, self).__init__(parent)

        self.event_types = QComboBox()
        self.event_types.addItems(("None", Info.IMAGE, Info.VIDEO, Info.TEXT, Info.SOUND, Info.SLIDER))

        self.name_line = QLabel()
        self.linkSignal()

        self.icon_label = IconLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.doubleClick.connect(self.openProWindow)

        self.current_sub_wid = ""

        self.pool = {
            "Image": "",
            "Video": "",
            "Text": "",
            "Sound": "",
            "slider": "",
        }

        self.default_properties: dict = {
            "Stim Type": "None",
            "Event Name": "",
            "Sub Wid": "",
        }

        self.event_type = "None"
        self.event_name = ""
        self.widget = None
        self.pro_window = None
        self.setUI()

    def linkSignal(self):
        self.event_types.currentTextChanged.connect(self.changeEventType)
        # self.name_line.textChanged.connect(self.changeName)

    def setUI(self):
        grid_layout = QGridLayout()
        event_tip = QLabel("Stim Type:")
        event_tip.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        name_tip = QLabel("Object Name:")
        name_tip.setAlignment(Qt.AlignVCenter | Qt.AlignRight)
        grid_layout.addWidget(event_tip, 0, 0, 1, 1)
        grid_layout.addWidget(self.event_types, 0, 1, 1, 3)
        grid_layout.addWidget(self.icon_label, 1, 1, 3, 3)
        grid_layout.addWidget(name_tip, 4, 0, 1, 1)
        grid_layout.addWidget(self.name_line, 4, 1, 1, 3)

        self.setLayout(grid_layout)

    def changeEventType(self, current_type):
        """
        1、none->type Add
        2、type->type Del Add
        3、type->none Del
        :param current_type:
        :return:
        """
        if self.event_type == "None" and current_type != "None":
            self.current_sub_wid = self.getSubId(current_type)
            sub_name = self.generateName(current_type)
            self.itemAdded.emit(self.current_sub_wid, sub_name)
        elif self.event_type != "None" and current_type != "None":
            self.itemDeleted.emit(self.current_sub_wid)
            self.current_sub_wid = self.getSubId(current_type)
            sub_name = self.generateName(current_type)
            self.itemAdded.emit(self.current_sub_wid, sub_name)
        elif self.event_type != "None" and current_type == "None":
            self.itemDeleted.emit(self.current_sub_wid)
            self.current_sub_wid = ""
            sub_name = ""
        self.event_type = current_type
        self.icon_label.setIcon(current_type)
        self.name_line.setText(sub_name)

    def getSubId(self, event_type: str = ""):
        """
        获取、更新子控件id
        :param event_type:
        :return:
        """
        if event_type == "":
            event_type = self.event_type
        sub_id = self.pool.get(event_type)
        if sub_id == "":
            sub_id = Func.generateWidgetId(event_type)
            self.pool[event_type] = sub_id
        return sub_id

    def linkWidgetSignal(self):
        if self.event_type == Info.SLIDER:
            self.pro_window = self.widget
        else:
            self.pro_window = self.widget.pro_window
            self.pro_window.ok_bt.clicked.connect(self.ok)
            self.pro_window.cancel_bt.clicked.connect(self.cancel)
            self.pro_window.apply_bt.clicked.connect(self.apply)

    def generateName(self, event_type: str = ""):
        """
        定义event name的命名方式
        :return:
        """
        if event_type == "":
            event_type = self.event_type
        name = f"U_{event_type}_{int(time.time() % 10007)}"
        return name

    def changeName(self, new_name: str):
        if new_name in Info.NAME_WID.keys() and new_name != self.event_name:
            self.name_line.setColor("red")
        else:
            self.name_line.setColor("white")
            if new_name != self.event_name:
                self.event_name = new_name
                self.itemNameChanged.emit(self.current_sub_wid, new_name)

    def ok(self):
        self.apply()
        self.pro_window.close()

    def apply(self):
        self.getInfo()

    def cancel(self):
        self.pro_window.close()

    def openProWindow(self):
        if self.current_sub_wid != "":
            if self.widget is None:
                self.widget = Func.getWidget(self.current_sub_wid)
                self.linkWidgetSignal()
            if self.event_type == Info.SLIDER:
                self.widget.show()
            else:
                self.widget.pro_window.show()

    def getInfo(self):
        self.default_properties.clear()
        self.default_properties["Id Pool"] = self.pool
        self.default_properties["Sub Wid"] = self.current_sub_wid
        self.default_properties["Stim Type"] = self.event_type
        self.default_properties["Event Name"] = self.event_name
        return self.default_properties

    def getProperties(self):
        return self.getInfo()

    # 加载外部属性
    def setProperties(self, properties: dict):
        self.blockSignals(True)
        self.default_properties = properties.copy()
        self.loadSetting()
        self.blockSignals(False)

    # 加载当前属性
    def loadSetting(self):
        self.pool = self.default_properties.get("Id Pool")
        self.current_sub_wid = self.default_properties.get("Sub Wid", "")

        self.event_type = self.default_properties.get("Stim Type", "None")
        self.event_types.setCurrentText(self.event_type)
        self.icon_label.setIcon(self.event_type)

        self.event_name = self.default_properties.get("Event Name", "")
        self.name_line.setText(self.event_name)
        self.name_line.setEnabled(self.current_sub_wid != "")

    def setAttributes(self, attributes: list):
        if self.pro_window:
            if self.event_type == Info.SLIDER:
                self.pro_window.setAttributes([i[1:-1] for i in attributes])
            else:
                self.pro_window.setAttributes(attributes)

    def getWidget(self):
        """
        获取子控件
        :return:
        """
        return self.widget

    def getWidgetId(self) -> str:
        return self.current_sub_wid


class IconLabel(QLabel):
    doubleClick = pyqtSignal()

    def __init__(self, parent=None):
        super(IconLabel, self).__init__(parent)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.doubleClick.emit()
        QLabel.mouseDoubleClickEvent(self, *args, **kwargs)

    def setIcon(self, event_type):
        if event_type == "None":
            self.clear()
        else:
            pix_map = Func.getWidgetImage(event_type, "pixmap")
            self.setPixmap(pix_map.scaled(100, 100))
