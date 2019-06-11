import time

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel

from app.center.widget_tabs.events.slider.Slider import Slider
from app.func import Func
from app.info import Info
from app.lib import PigComboBox, PigLineEdit


class IconChoose(QWidget):
    """
    {
        "stim type": "Image",
        "event name": "",
        "pro window": {}
    }
    """
    # 发送到上一层, 由上一层再转至properties (properties)
    propertiesShow = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(IconChoose, self).__init__(parent)

        self.attributes: list = []

        self.event_types = PigComboBox()
        self.event_types.addItem("None")
        self.event_types.addItem(Info.IMAGE)
        self.event_types.addItem(Info.VIDEO)
        self.event_types.addItem(Info.TEXT)
        self.event_types.addItem(Info.SOUND)
        self.event_types.addItem(Info.SLIDER)
        self.event_types.currentTextChanged.connect(self.changeIcon)
        self.name_line = PigLineEdit()
        self.name_line.setEnabled(False)
        self.name_line.textChanged.connect(self.changeName)
        self.icon_label = IconLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        self.icon_label.doubleClick.connect(self.openPro)

        self.widget_id = ""

        self.default_properties: dict = {
            "stim type": "None",
            "event name": "",
            "pro window": None
        }

        self.event_type = "None"
        self.event_name = ""
        self.widget = None
        self.pro_window = None

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

    def changeIcon(self, current_type):
        self.event_type = current_type
        pix_map = Func.getWidgetImage(self.event_type, "pixmap")
        self.icon_label.setPixmap(pix_map)

        Func.delWidget(self.widget_id)

        if current_type == "None":
            self.name_line.clear()
            self.name_line.setEnabled(False)
            self.widget = None
            return

        self.widget_id = Func.generateWidgetId(current_type)
        self.widget = Func.createWidget(self.widget_id)
        assert self.widget is not None

        if self.event_type == Info.SLIDER:
            self.pro_window = self.widget
        else:
            self.pro_window = self.widget.pro_window
            # if self.event_type == "Image":
            #     self.pro_window = ImageProperty()
            #     self.pro_window.setAttributes(self.attributes)
            # elif self.event_type == "Sound":
            #     self.pro_window = SoundProperty()
            #     self.pro_window.setAttributes(self.attributes)
            # elif self.event_type == "Text":
            #     self.pro_window = TextProperty()
            #     self.pro_window.setAttributes(self.attributes)
            # elif self.event_type == "Video":
            #     self.pro_window = VideoProperty()
            #     self.pro_window.setAttributes(self.attributes)
            # else:
            #     self.pro_window = None
            #     self.name_line.clear()
            #     self.name_line.setEnabled(False)
            #     return
            # if self.event_type == "Image":
            #     event = ImageProperty()
            # elif self.event_type == "Sound":
            #     self.pro_window = SoundProperty()
            #     self.pro_window.setAttributes(self.attributes)
            # elif self.event_type == "Text":
            #     self.pro_window = TextProperty()
            #     self.pro_window.setAttributes(self.attributes)
            # elif self.event_type == "Video":
            #     self.pro_window = VideoProperty()
            #     self.pro_window.setAttributes(self.attributes)
            # else:
            #     self.pro_window = None
            #     self.name_line.clear()
            #     self.name_line.setEnabled(False)
            #     return
            self.pro_window.ok_bt.clicked.connect(self.ok)
            self.pro_window.cancel_bt.clicked.connect(self.cancel)
            self.pro_window.apply_bt.clicked.connect(self.apply)

        self.name_line.setText(f"Untitled-{self.event_type}{int(time.time() % 10000)}")
        self.name_line.setEnabled(True)

    def changeName(self, new_name: str):
        self.event_name = new_name

    def ok(self):
        self.apply()
        self.pro_window.close()

    def apply(self):
        self.getInfo()

    def cancel(self):
        self.pro_window.close()

    def openPro(self):
        if self.pro_window:
            if hasattr(self.pro_window, "general"):
                if hasattr(self.pro_window.general, "setScreen"):
                    screen_devices = Func.getScreen()
                    self.pro_window.general.setScreen(screen_devices)
            # self.pro_window.setWindowModality(Qt.ApplicationModal)
            self.pro_window.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.pro_window.show()

    def getInfo(self):
        if self.pro_window:
            self.default_properties["pro window"] = self.pro_window.getInfo().copy()
        else:
            self.default_properties["pro window"] = {}
        self.default_properties["stim type"] = self.event_type
        self.default_properties["event name"] = self.event_name
        return self.default_properties

    def getProperties(self):
        return self.getInfo()

    # 加载外部属性
    def setProperties(self, properties: dict):
        if properties:
            self.default_properties = properties.copy()
            self.loadSetting()

    # 加载当前属性
    def loadSetting(self):
        self.event_types.setCurrentText(self.default_properties.get("stim type", "None"))
        self.name_line.setText(self.default_properties.get("event name", ""))

        if self.default_properties.get("pro window", None):
            if isinstance(self.pro_window, Slider):
                self.pro_window.restore(self.default_properties.get("pro window", {}))
            else:
                self.pro_window.setProperties(self.default_properties.get("pro window", {}))

    def setPro(self, pro):
        del self.pro_window
        self.pro_window = pro
        self.pro_window.ok_bt.clicked.connect(self.ok)
        self.pro_window.cancel_bt.clicked.connect(self.cancel)
        self.pro_window.apply_bt.clicked.connect(self.apply)

    def setAttributes(self, attributes: list):
        self.attributes = attributes
        if self.pro_window:
            self.pro_window.setAttributes(attributes)

    # 返回当前选择attributes
    def getUsingAttributes(self):
        using_attributes: list = []
        self.findAttributes(self.default_properties, using_attributes)
        return using_attributes

    def findAttributes(self, properties: dict, using_attributes: list):
        for v in properties.values():
            if isinstance(v, dict):
                self.findAttributes(v, using_attributes)
            elif isinstance(v, str):
                if v.startswith("[") and v.endswith("]"):
                    using_attributes.append(v[1:-1])

    def clone(self):
        clone_icon = IconChoose()
        clone_icon.setProperties(self.default_properties)
        return clone_icon

    def getWidget(self):
        """
        获取子控件
        :return:
        """
        return self.widget

    def getWidgetId(self) -> str:
        return self.widget_id


class IconLabel(QLabel):
    doubleClick = pyqtSignal()

    def __init__(self, parent=None):
        super(IconLabel, self).__init__(parent)

    def mouseDoubleClickEvent(self, *args, **kwargs):
        self.doubleClick.emit()
        QLabel.mouseDoubleClickEvent(self, *args, **kwargs)
