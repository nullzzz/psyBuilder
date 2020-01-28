from lib import TableWidgetItem


class WeightItem(TableWidgetItem):
    def __init__(self, value: str):
        super(WeightItem, self).__init__(value)
        # a flag
        self.new = True
