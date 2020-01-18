from PyQt5.QtWidgets import QTableWidgetItem


class AttributeItem(QTableWidgetItem):
    def __init__(self):
        super(AttributeItem, self).__init__(None)
        # a flag
        self.new = True
