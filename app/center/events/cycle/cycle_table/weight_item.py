from PyQt5.QtWidgets import QTableWidgetItem


class WeightItem(QTableWidgetItem):
    def __init__(self, value: str):
        super(WeightItem, self).__init__(value)
        # a flag
        self.new = True
