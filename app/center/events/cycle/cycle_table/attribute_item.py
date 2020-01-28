from lib import TableWidgetItem


class AttributeItem(TableWidgetItem):
    def __init__(self, value: str):
        super(AttributeItem, self).__init__(value)
        # a flag
        self.new = True
