class TreeNode(object):
    def __init__(self, widget_id: str, widget_name: str, parent=None):
        self.widget_id = widget_id
        self.widget_name = widget_name
        self.parent = parent
        self.children = []

    def addChildren(self, children: list):
        for child in children:
            if type(child) == list:
                node = TreeNode(widget_id=child[0][1], widget_name=child[0][0], parent=self)
                node.addChildren(child[1:])
            else:
                node = TreeNode(widget_id=child[1], widget_name=child[0], parent=self)
            self.children.append(node)

    def print_tree(self, layer=0):
        print("\t" * layer + f"{self.widget_name} : [{self.widget_id}]")
        for child in self.children:
            child.print_tree(layer + 1)
