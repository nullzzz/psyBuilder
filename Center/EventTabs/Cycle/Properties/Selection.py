from PyQt5.QtWidgets import QWidget, QComboBox, QRunBox, QHBoxLayout, QVBoxLayout, QFormLayout, QLabel


class Selection(QWidget):
    def __init__(self, parent=None):
        super(Selection, self).__init__(parent)

        self.order = QRunBox("Order")

        self.orderCombo = QComboBox(self.order)
        self.orderCombo.addItem("Sequential")
        self.orderCombo.addItem("Random")
        self.orderCombo.addItem("Random with Replacement")
        self.orderCombo.addItem("CounterBalance")
        self.orderCombo.addItem("Offset")

        self.noRepeatAfter = QComboBox(self.order)
        self.noRepeatAfter.addItem("N/A")
        self.noRepeatAfter.setEnabled(False)

        form1 = QFormLayout(self.order)

        form1.addRow(self.orderCombo)
        form1.addRow(QLabel(""))
        form1.addRow(QLabel(""))
        form1.addRow(QLabel(""))
        form1.addRow(QLabel("No Repeat After"))
        form1.addRow(self.noRepeatAfter)

        self.order.setLayout(form1)

        self.orderBy = QRunBox("Order By")

        self.orderByCombo = QComboBox(self.orderBy)
        self.orderByCombo.addItem("N/A")
        self.orderByCombo.setEnabled(False)

        form2 = QFormLayout(self.orderBy)
        form2.addRow(self.orderByCombo)

        self.orderBy.setLayout(form2)

        hBox = QHBoxLayout(self)

        hBox.addWidget(self.order)
        hBox.addWidget(self.orderBy)

        self.setLayout(hBox)
        self.setMinimumWidth(500)

        # 信号
        self.orderCombo.currentIndexChanged.connect(self.setComboEnable)

    def setComboEnable(self, index):
        if index == 0 or index == 2:
            self.noRepeatAfter.setEnabled(False)
            self.noRepeatAfter.clear()
            self.noRepeatAfter.addItem("N/A")
            self.orderByCombo.setEnabled(False)
            self.orderByCombo.clear()
            self.orderByCombo.addItem("N/A")
        if index == 1:
            self.noRepeatAfter.setEnabled(True)
            self.noRepeatAfter.clear()
            self.noRepeatAfter.addItem("N/A")
            self.noRepeatAfter.addItem("Yes")
            self.noRepeatAfter.addItem("No")
            self.noRepeatAfter.setCurrentIndex(1)
            self.orderByCombo.setEnabled(False)
            self.orderByCombo.clear()
            self.orderByCombo.addItem("N/A")
        if index in (3, 4, 5):
            self.noRepeatAfter.setEnabled(False)
            self.noRepeatAfter.clear()
            self.noRepeatAfter.addItem("N/A")
            self.orderByCombo.setEnabled(True)
            self.orderByCombo.clear()
            self.orderByCombo.addItem("N/A")
            self.orderByCombo.addItem("Subject")
            self.orderByCombo.addItem("Session")
            self.orderByCombo.addItem("Run")
            self.orderByCombo.setCurrentIndex(1)


