from PyQt5.QtWidgets import QTableWidgetItem


class AttributeItem(QTableWidgetItem):
    def __init__(self, value: str):
        super(AttributeItem, self).__init__(value)
        # a flag
        self.new = True
