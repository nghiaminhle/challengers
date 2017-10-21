class Node:
    value = 0
    label = ''
    left = None
    rigt = None

    def __init__(self, label, value=0):
        self.label = label
        self.value = value

    def add_node(self, node):
        if node.value <= self.value:
            return self.__add_left_node(node)
        return self.__add_right_node(node)

    def __add_left_node(self, node):
        if self.left == None:
            self.left = node
            return self
        return self.left.add_node(node)

    def __add_right_node(self, node):
        if self.rigt == None:
            self.rigt = node
            return self
        return self.rigt.add_node(node)