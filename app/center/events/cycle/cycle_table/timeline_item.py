from PyQt5.QtWidgets import QTableWidgetItem


class TimelineItem(QTableWidgetItem):
    def __init__(self):
        super(TimelineItem, self).__init__(None)
        # a flag
        self.new = True



