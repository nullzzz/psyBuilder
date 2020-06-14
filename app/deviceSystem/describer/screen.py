from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QRegExpValidator
from PyQt5.QtWidgets import QLineEdit, QFormLayout, QVBoxLayout

from app.deviceSystem.describer.basis import Shower
from lib import ColComboBox


class Screen(Shower):
    def __init__(self, parent=None):
        super(Screen, self).__init__(parent=parent)
        self.device_index = QLineEdit()
        self.device_index.setToolTip("Screen index as returned by Screen('screens') in MATLAB")
        self.device_index.textEdited.connect(self.showAddressTip)
        self.bg_color = ColComboBox()
        self.mu_sample = QLineEdit()
        self.mu_sample.setToolTip("Number of samples are computed and combined into a single output pixel. \n A value greater than zero enables automatic hardware anti-aliasing of the display.")
        self.resolution = QLineEdit("auto")
        self.resolution.setValidator(QRegExpValidator(QRegExp(r"\d+x\d+|auto")))
        self.resolution.setToolTip("WidthxHeight (e.g., 1920x1080, \"x\" is the letter in the alphabet)")
        self.refresh_rate = QLineEdit("auto")
        self.refresh_rate.setToolTip("Refresh rate of the monitor (e.g., 60)")
        self.physic_size = QLineEdit()
        self.physic_size.setToolTip("Physical size of the monitor (e.g., 50x30, \"x\" is the letter in the alphabet)")
        self.viewing_distance = QLineEdit()
        self.viewing_distance.setToolTip("For eyetracker only (e.g., 50)")

        self.device_index.setValidator(QRegExpValidator(QRegExp(r"\d+")))
        self.mu_sample.setValidator(QRegExpValidator(QRegExp(r"\d+")))
        self.physic_size.setValidator(QRegExpValidator(QRegExp(r"\d+\.\d+|\d+\.\d+x\d+\.\d+|NaN")))
        self.viewing_distance.setValidator(QRegExpValidator(QRegExp(r"\d+\.\d+|\d+\.\d+,\d+\.\d+|NaN")))

        # self.index_tip.setHtml("About the \"x\" in Resolution and Physic size:"
        #                        "<br><br><b>Device index</b>: Screen index as returned by Screen('screens') in MATLAB."
        #                        "<br><br><b>Resolution</b>: WidthxHeight e.g., 1024x768"
        #                        "<br><br><b>physic size</b> (for Eyetracker Only) mm: WdithxHeight, e.g., 30x50"
        #                        "<br><br><b>Viewing distance</b> (for Eyetracker Only) mm: e.g., 50"
        #                        "<br><br><b>!x is the char before y</b>")

        self.setUI()

    def setUI(self):
        layout = QFormLayout()
        layout.setLabelAlignment(Qt.AlignLeft)
        layout.addRow("Device Type:", self.device_type)
        layout.addRow("Device Name:", self.device_name)
        layout.addRow("Device Index:", self.device_index)
        layout.addRow("Background Color:", self.bg_color)
        layout.addRow("Multiple Sampling:", self.mu_sample)
        layout.addRow("Resolution:", self.resolution)
        layout.addRow("Refresh Rate (Hz):", self.refresh_rate)
        layout.addRow("Physical Size (mm):", self.physic_size)
        layout.addRow("Viewing Distance (mm):", self.viewing_distance)

        vLayout = QVBoxLayout()
        vLayout.addLayout(layout)
        vLayout.addWidget(self.port_tip)
        vLayout.addWidget(self.index_tip)

        self.setLayout(vLayout)

    def describe(self, info: dict):
        super().describe(info)
        self.device_index.setText(info.get("Device Index", "0"))
        self.bg_color.setCurrentText(info.get("Back Color", "255,255,255"))
        self.mu_sample.setText(info.get("Multi Sample", ""))
        self.resolution.setText(info.get("Resolution", "auto"))
        self.refresh_rate.setText(info.get("Refresh Rate", "auto"))
        self.physic_size.setText(info.get("Physic Size", ""))
        self.viewing_distance.setText(info.get("Viewing Distance", ""))

    def getInfo(self):
        properties: dict = {
            "Device Type": self.device_type.text(),
            "Device Name": self.device_name.text(),
            "Device Index": self.device_index.text(),
            "Back Color": self.bg_color.getRGB(),
            "Multi Sample": self.mu_sample.text(),
            "Resolution": self.resolution.text(),
            "Refresh Rate": self.refresh_rate.text(),
            "Physic Size": self.physic_size.text(),
            "Viewing Distance": self.viewing_distance.text(),
        }
        return properties
