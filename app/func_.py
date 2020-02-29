import os
import re

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QPixmap, QIcon

from .info import Info
from .kernel import Kernel


class Func(object):
    """
    some common func
    """

    @staticmethod
    def getWidget(widget_id: str):
        """
        get widget through its widget id
        """
        return Kernel.Widgets[widget_id]

    @staticmethod
    def getNode(widget_id: str):
        """
        get node through its widget id
        """
        return Kernel.Nodes[widget_id]

    @staticmethod
    def generateWidgetId(widget_type: str) -> str:
        """
        generate a valid widget id
        """
        count = Kernel.WidgetTypeCount[widget_type]
        widget_id = f"{widget_type}.{count}"
        Kernel.WidgetTypeCount[widget_type] += 1
        return widget_id

    @staticmethod
    def generateWidgetName(widget_type: str) -> str:
        """
        generate a valid widget name
        """
        while True:
            # widget name = 'widget_type' _ 'count'
            widget_name = f"{widget_type}_{Kernel.WidgetNameCount[widget_type]}"
            # inc count of this widget type
            Kernel.WidgetNameCount[widget_type] += 1
            # check name's validity
            if widget_name not in Kernel.Names:
                return widget_name

    @staticmethod
    def checkWidgetNameValidity(widget_name: str) -> (bool, str):
        """
        check the validity of widget name.
        It should be unique, unless it's a reference.
        """
        if not re.match(r"^[a-zA-Z][a-zA-Z0-9_]*$", widget_name):
            return False, "Name must start with a letter and contain only letters, numbers and _."
        if widget_name in Kernel.Names:
            return False, "Name already exists."
        return True, ""

    @staticmethod
    def getWidgetType(widget_id: str):
        """
        get widget's type through its widget id
        """
        return widget_id.split('.')[0]

    @staticmethod
    def getWidgetName(widget_id: str):
        """
        get widget's name
        """
        return Kernel.Widgets[widget_id].widget_name

    @staticmethod
    def checkWidgetNameExisted(widget_name: str) -> bool:
        """
        check widget name whether existed
        """
        return widget_name in Kernel.Names

    @staticmethod
    def getWidgetReference(widget_id: str) -> list:
        """
        get list of reference widget's widget id
        @param widget_id:
        @return:
        """
        widget_name = Func.getWidgetName(widget_id)
        return Kernel.Names[widget_name]

    @staticmethod
    def getWidgetParent(widget_id: str) -> str:
        """
        get parent's widget id
        @param widget_id:
        @return:
        """
        return Kernel.Nodes[widget_id].parent().widget_id

    @staticmethod
    def getWidgetChild(widget_id: str, index: int) -> (str, str):
        """

        @param widget_id:
        @param index:
        @return: child's widget id and widget name
        """
        child = Kernel.Nodes[widget_id].child(index)
        return child.widget_id, child.text(0)

    @staticmethod
    def getWidgetChildren(widget_id: int) -> list:
        """

        @param widget_id:
        @return: list of children's widget id and widget name
        """
        root = Kernel.Nodes[widget_id]
        children = []
        for i in range(root.childCount()):
            child = root.child(i)
            children.append((child.widget_id, child.text(0)))
        return children

    @staticmethod
    def getWidgetIndex(widget_id: str) -> int:
        """
        get widget's index in timeline
        @param widget_id:
        @return:
        """
        if Func.isWidgetType(widget_id, Info.TIMELINE):
            return -1
        node = Kernel.Nodes[widget_id]
        if node.parent():
            return node.parent().indexOfChild(node)
        else:
            return -1

    @staticmethod
    def isWidgetType(widget_id: str, widget_type: str):
        """
        check widget's type
        """
        return Func.getWidgetType(widget_id) == widget_type

    @staticmethod
    def getWidgetProperties(widget_id: str):
        """
        get widget's properties through its widget id
        """

    @staticmethod
    def getWidgetAttributes(widget_id: str):
        """
        get widget's attributes through its widget id
        """

    @staticmethod
    def getImage(image_path: str, type: int = 0, size: QSize = None) -> QPixmap or QIcon:
        """
        get image from its relative path, return qt image object, include QPixmap or QIcon.
        @param image_path: its relative path
        @param type: 0: pixmap (default),
                     1: icon
        @return: Qt image object
        """
        path = os.path.join(Info.Image_Path, image_path)
        if not type:
            if size:
                return QPixmap(path).scaled(size, transformMode=Qt.SmoothTransformation)
            return QPixmap(path)
        return QIcon(path)

    @staticmethod
    def startWait():
        """
        show loading window
        """
        Kernel.Psy.startWait()

    @staticmethod
    def endWait():
        """
        close loading window
        """
        Kernel.Psy.endWait()

    @staticmethod
    def print(information: str, information_type: int = 0):
        """
        print information in output.
        information_type: 0 none
                          1 success
                          2 fail
        """
        Kernel.Psy.output.print(information, information_type)
