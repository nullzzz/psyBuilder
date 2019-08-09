from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor,QFont
from PyQt5.QtWidgets import QGridLayout, QLabel, QGroupBox, QVBoxLayout, QWidget, QFontComboBox,QComboBox,QCheckBox,QPushButton,QHBoxLayout
from PyQt5.QtGui import QIntValidator
from app.func import Func
from app.lib import PigComboBox, ColorListEditor


class TextTab2(QWidget):
    def __init__(self, parent=None):
        super(TextTab2, self).__init__(parent)

        self.attributes = []

        self.default_properties = {
             'family': 'SimSun',
            'size': 1,
            'B': False,
            'I': False,
            'U': False,
            'font color': "black",
            'back color': "white",
            'x_pos': 1,
            'y_pos': 1
        }

        self.below = QWidget()
        self.top = QWidget()

        self.x_pos = PigComboBox()
        self.y_pos = PigComboBox()
        self.x_pos.addItems(["0", "25", "50", "75", "100"])
        self.x_pos.setEditable(True)
        self.y_pos.addItems(["0", "25", "50", "75", "100"])
        self.y_pos.setEditable(True)
        self.font_color = ColorListEditor()
        self.back_color = ColorListEditor()
        self.family = QFontComboBox()

        self.font_size = QComboBox()
        self.font_size.setEditable(True)
        for i in range(8, 30, 2):
            self.font_size.addItem(str(i))
        validator = QIntValidator(2, 64, self)
        self.font_size.setValidator(validator)

        self.Bold = QCheckBox("Bold")
        self.Italic = QCheckBox("Italic")
        self.Underline = QCheckBox("Underline")
        self.ok_bt = QPushButton("OK")
        self.cancel_bt = QPushButton("Cancel")
        self.apply_bt = QPushButton("Apply")
        self.setButtons()


        self.setUI()

    def setUI(self):
        #上面的布局
        al00 = QLabel("Position X:")
        al10 = QLabel("Position Y:")

        al02 = QLabel("Font Color:")
        al12 = QLabel("Back Color:")
        al50 = QLabel("Font Family:")
        fs = QLabel("Font Size:")

        # l0.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        al00.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        al02.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        al10.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        al12.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        al50.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        fs.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        group2 = QGroupBox("")
        layout2 = QGridLayout()
        layout2.addWidget(al00, 0, 0)
        layout2.addWidget(self.x_pos, 0, 1)
        layout2.addWidget(al10, 0, 2)
        layout2.addWidget(self.y_pos, 0, 3)

        layout2.addWidget(al02, 1, 0)
        layout2.addWidget(self.font_color, 1, 1)
        layout2.addWidget(al12, 1, 2)
        layout2.addWidget(self.back_color, 1, 3)

        layout2.addWidget(al50, 2, 0)
        layout2.addWidget(self.family, 2, 1)
        layout2.addWidget(fs, 2, 2)
        layout2.addWidget(self.font_size, 2, 3)

        layout2.addWidget(self.Bold, 3, 0)
        layout2.addWidget(self.Italic, 3, 1)
        layout2.addWidget(self.Underline, 3, 2)
        group2.setLayout(layout2)


        layout = QVBoxLayout()
        # layout.addWidget(group1, 1)
        layout.addWidget(group2)
        self.top.setLayout(layout)

        #总体的布局
        self.setWindowTitle("Property")
        self.resize(600, 800)
        # self.setFixedSize(600, 800)
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.top, 6)
        # main_layout.addStretch(2)
        main_layout.addWidget(self.below, 1)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

    def setButtons(self):
        below_layout = QHBoxLayout()
        below_layout.addStretch(10)
        below_layout.addWidget(self.ok_bt, 1)
        below_layout.addWidget(self.cancel_bt, 1)
        below_layout.addWidget(self.apply_bt, 1)
        below_layout.setContentsMargins(0, 0, 0, 0)
        self.below.setLayout(below_layout)

    def setAttributes(self, attributes):
        self.attributes = attributes

    def getInfo(self):
        self.default_properties["x_pos"] = self.x_pos.currentText()
        self.default_properties["y_pos"] = self.y_pos.currentText()
        self.default_properties["family"] = self.family.currentText()
        self.default_properties["size"] = self.font_size.currentText()
        self.default_properties["font color"] = self.font_color.getColor()
        self.default_properties["back color"] = self.back_color.getColor()
        self.default_properties["B"] = self.Bold.isChecked()
        self.default_properties["I"] = self.Italic.isChecked()
        self.default_properties["U"] = self.Underline.isChecked()


        return self.default_properties

    def setProperties(self, properties: dict,font):
        self.default_properties = properties
        self.loadSetting(font)

    def loadSetting(self, font):
        self.x_pos.setCurrentText(str(self.default_properties["x_pos"]))
        self.y_pos.setCurrentText(str(self.default_properties["y_pos"]))
        self.family.setCurrentFont(font)
        self.font_size.setEditText(str(font.pointSize()))
        self.Bold.setChecked(font.weight() == QFont.Bold)
        self.Italic.setChecked(font.italic())
        self.Underline.setChecked(font.underline())
        self.font_color.setCurrentText(self.default_properties["font color"])
        self.back_color.setCurrentText(self.default_properties["back color"])




