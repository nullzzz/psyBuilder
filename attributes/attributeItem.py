from PyQt5.QtWidgets import QTableWidgetItem


class AttributeItem(QTableWidgetItem):
    def __init__(self, name='', value=''):
        super(AttributeItem, self).__init__(name)
        # 此value为attribute value, 非特征值
        self.value = value
