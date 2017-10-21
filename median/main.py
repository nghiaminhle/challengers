from node import Node

class MedianStore:
    count = 0
    index_values = {}
    value_index = {}
    root = None

    def add_number(self, number: int):
        node = Node('{}-{}'.format(self.count, number), number)
        if self.root == None:
            self.root = node
            self.index_values[self.count] = node
            self.value_index[node.label] = self.count
        else:
            appended_node = self.root.add_node(node)
            index_of_append_node = self.value_index[appended_node.label]
            
            if appended_node.value < number:
                if index_of_append_node < self.count - 1:
                    self.shift_index(index_of_append_node + 1)
                self.index_values[index_of_append_node + 1] = node
                self.value_index[node.label] = index_of_append_node + 1
            else:
                self.shift_index(index_of_append_node)
                self.index_values[index_of_append_node] = node
                self.value_index[node.label] = index_of_append_node
            
        self.count += 1

    def get_median(self):
        if self.count == 1:
            return self.index_values[self.count - 1].value
        center = int(self.count/2)
        if int(self.count % 2) == 0:
            return (self.index_values[center].value + self.index_values[center-1].value)/2
        else:
            return self.index_values[center].value
        
    def shift_index(self, from_index):
        t1 = self.index_values[from_index]
        t2 = None
        for i in range(from_index, self.count+1):
            if i < self.count - 1:
                t2 = self.index_values[i + 1]
            self.index_values[i + 1] = t1
            t1 = t2
            self.value_index[self.index_values[i].label] += 1

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
        median_list = MedianStore()
        print('Executing test case %s' % case[0])
        for k, number in enumerate(case[0]):
            median_list.add_number(number)
            assert median_list.get_median() == case[1][k]
    
if __name__ == "__main__":
    main()
