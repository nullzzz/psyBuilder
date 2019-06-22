from app.info import Info
from .tree_node import TreeNode


class WidTree(object):
    def __init__(self, structure: list):
        self.root = TreeNode(widget_id=f"{Info.TIMELINE}.0", widget_name=Info.TIMELINE)
        self.build_tree(self.root, structure[1:])

    def build_tree(self, root: TreeNode, children: list):
        root.addChildren(children)

    def print_tree(self):
        self.root.print_tree()
