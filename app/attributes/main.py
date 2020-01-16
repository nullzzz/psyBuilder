from app.func import Func
from lib import DockWidget
from .attributes_table import AttributesTable


class Attributes(DockWidget):
    """

    """

    def __init__(self, parent=None):
        super(Attributes, self).__init__(parent)
        # attributes table
        self.attributes_table = AttributesTable()
        self.setWidget(self.attributes_table)
        # current widget id
        self.current_widget_id = -1

    def showAttributes(self, widget_id: int):
        """
        show widget's attributes
        @param widget_id:
        @return:
        """
        if self.current_widget_id != widget_id:
            # we should clear firstly
            self.clearAttributes()
            # add
            self.current_widget_id = widget_id
            attributes: dict = Func.getWidgetAttributes(widget_id)
            for attribute in attributes:
                self.attributes_table.addAttribute(attribute)

    def clearAttributes(self):
        """
        show widget's attributes
        @return:
        """
        while self.attributes_table.rowCount():
            self.attributes_table.removeRow(0)
