from PyQt5.QtWidgets import QVBoxLayout

from lib import TabItemWidget
from .cycle_table import CycleTable


class Cycle(TabItemWidget):
    """

    """

    def __init__(self, widget_id: int, widget_name: str):
        super(Cycle, self).__init__(widget_id, widget_name)
        self.cycle_table = CycleTable()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.cycle_table)
        self.setLayout(layout)

    def getColumnAttributes(self) -> list:
        """
        return [attr1, attr2]
        @return:
        """
        # todo get column attributes
        return []
