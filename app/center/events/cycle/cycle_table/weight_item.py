from PyQt5.QtWidgets import QTableWidgetItem


class WeightItem(QTableWidgetItem):
    def __init__(self):
        super(WeightItem, self).__init__(None)
        # a flag
        self.new = True



