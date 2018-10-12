from PyQt5.QtWidgets import QComboBox


class VarChoose(QComboBox):
    def __init__(self, parent=None, parent_value=''):
        super(VarChoose, self).__init__(parent)
        self.parent_value = parent_value
        self.setInsertPolicy(QComboBox.InsertAlphabetically)
        try:
            from ..main import IconTabs
            self.addItems(IconTabs.getAttributes(self.parent_value))
        except Exception:
            pass

    def addAttribute(self, new_attribute):
        self.addItem(new_attribute)

    def changeAttribute(self, old_attribute, new_attribute):
        index = self.findText(old_attribute)
        self.setItemText(index, new_attribute)
