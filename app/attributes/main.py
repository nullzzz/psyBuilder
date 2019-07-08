from PyQt5.QtWidgets import QDockWidget

from app.func import Func
from .attributes_table import AttributesTable


class Attributes(QDockWidget):
    def __init__(self, parent=None):
        super(Attributes, self).__init__(parent)
        self.current_wid = ""
        self.attributes_table = AttributesTable(self)
        self.setWidget(self.attributes_table)

    def showAttributes(self, widget_id, a=0, b=0):
        try:
            attributes = Func.getAttributes(widget_id)
            self.current_wid = widget_id
            # 将attribute table清空
            while self.attributes_table.rowCount():
                self.attributes_table.removeRow(0)
            # 放入新的attributes
            for name in attributes:
                self.attributes_table.addAttribute(name)
        except Exception as e:
            print(f"error {e} happens show timeline attributes. [attributes/main.py]")

    def refresh(self) -> None:
        """
        根据已有的wid进行刷新操作！即重新获取
        :return:
        """
        if self.current_wid:
            self.showAttributes(self.current_wid)
