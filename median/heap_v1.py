
class HeapNode:
    value = 0
    left = None
    right = None
    is_right = True
    left_count = 0
    right_count = 0

    def __init__(self, value, is_right=True):
        self.value = value
        self.is_right = is_right

    def add_node(self, node):
        if node.is_right:
            self.right_count += 1
            self.__add_right(node)
        else:
            self.left_count += 1
            self.__add_left(node)

    def __add_right(self, node):
        if self.right == None:
            self.right = node
            return
        if self.right.value< node.value:
            self.right.add_node(node)
            return
        node.right = self.right
        node.right_count = self.right.right_count + 1
        self.right = node
    
    def __add_left(self, node):
        if self.left == None:
            self.left = node
            return
        if self.left.value>node.value:
            self.left.add_node(node)
            return
        node.left = self.left
        node.left_count = self.left.left_count + 1
        self.left = node

class MedianHeap:

    center = None

    def add_number(self, value):
        if self.center == None:
            self.center = HeapNode(value)
            return
        if value > self.center.value:
            self.center.add_node(HeapNode(value))
        else:
            self.center.add_node(HeapNode(value, is_right=False))

        if self.center.left_count < self.center.right_count -1:
            self.__move_center_to_right()
        elif self.center.right_count< self.center.left_count -1:
            self.__move_center_to_left()
    
    def get_median(self):
        if self.center.left_count == self.center.right_count:
            return self.center.value
        elif self.center.left_count > self.center.right_count:
            return (self.center.left.value + self.center.value)/2
        else:
            return (self.center.value + self.center.right.value)/2
        
    def __move_center_to_right(self):
        self.center.right.left = self.center
        self.center.right.left_count = self.center.left_count + 1
        self.center.right_count = 0
        right = self.center.right
        self.center.right = None
        self.center = right
    
    def __move_center_to_left(self):
        self.center.left.right = self.center
        self.center.left.right_count = self.center.right_count + 1
        self.center.left_count = 0
        left = self.center.left
        self.center.left = None
        self.center = left

def main():
    
    testcases = [
        [[1, 3, 9, 5, 7, 5, 0, 4, 3, 2, 9, 1, 0], [1, 2, 3, 4, 5, 5, 5, 4.5, 4, 3.5, 4, 3.5, 3]],
        [[6, 1, 2], [6, 3.5, 2]],
        [[3, 9, 2, 5, 2], [3, 6, 3, 4, 3]],
        [[5, 5, 5, 5], [5, 5, 5, 5]],
        [[9, 6, 4, 3, 1], [9, 7.5, 6, 5, 4]],
        [[1, 2, 3, 4], [1, 1.5, 2, 2.5]],
        [[1, 3, 2], [1, 2, 2]],
        [[1], [1]]
    ]

    for case in testcases:
        median_list = MedianHeap()
        print('Executing test case %s' % case[0])
        for k, number in enumerate(case[0]):
            median_list.add_number(number)
            assert median_list.get_median() == case[1][k]


if __name__ == "__main__":
    main()
