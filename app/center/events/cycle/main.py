from lib import TabItemWidget


class Cycle(TabItemWidget):
    """

    """

    def __init__(self, widget_id: int, widget_name: str):
        super(Cycle, self).__init__(widget_id, widget_name)

    def getColumnAttributes(self) -> list:
        """
        return [attr1, attr2]
        @return:
        """
        # todo get column attributes
        return []
