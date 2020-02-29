from app.func_ import Func
from app.info import Info
from lib import DockWidget
from .attributes_table import AttributesTable


class Attributes(DockWidget):
    """
    To show widget's attributes
    """

    def __init__(self):
        super(Attributes, self).__init__()
        # title
        self.setWindowTitle("Attributes")
        # attributes table
        self.attributes_table = AttributesTable()
        self.setWidget(self.attributes_table)
        # current widget id
        self.current_widget_id = Info.ERROR_WIDGET_ID

    def showAttributes(self, widget_id: str):
        """
        show widget's attributes
        """
        if self.current_widget_id != widget_id:
            # we should clear firstly
            self.clearAttributes()
            # add
            self.current_widget_id = widget_id
            attributes: list = Func.getWidgetAttributes(widget_id)
            for attribute in attributes:
                self.attributes_table.addAttribute(attribute)

    def clearAttributes(self):
        """
        show widget's attributes
        """
        while self.attributes_table.rowCount():
            self.attributes_table.removeRow(0)
