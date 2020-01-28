from lib import TableWidgetItem


class TimelineItem(TableWidgetItem):
    def __init__(self):
        super(TimelineItem, self).__init__(None)
        # a flag
        self.new = True
