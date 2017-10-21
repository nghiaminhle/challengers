class LFUCacheItem:
    key = None
    value = None
    frequency = 0
    node = None

    def __init__(self):
        self.key = None
        self.value = None
        self.frequency = 0
        self.node = None

class LFUNode:
    next_node = None
    prev_node = None
    frequency = 0
    items = {}

    def __init__(self):
        self.next_node = None
        self.prev_node = None
        self.frequency = 0
        self.items = {}

    def add_item(self, item: LFUCacheItem):
        self.items[item.key] = item
    
    def remove_item(self, key):
        if key in self.items.keys():
            del self.items[key]
    
    def get_item(self):
        return next(iter(self.items.values()))
    
    def is_empty(self):
        return len(self.items) == 0

"""
The LFU use a double linked list to store a bucket cache key with the same frequency access.
Once a cache item is accessed, increase it's frequency by one and move it to the next node in the linked list.
If a node is empty, it's removed from the linked list. The head of list is always the least frequency node.
"""

class LFUCache:
    maps = {}
    size = 0
    head = None

    def __init__(self, size):
        self.maps = {}
        self.head = None
        self.size = size
    
    def add(self, key, value):
        if key in self.maps.keys():
            item = self.maps[key]
            item.value = value
            item.frequency +=1
            self.__move_to_next_node(item)
            return

        if len(self.maps) == self.size:
            item = self.head.get_item()
            self.remove(item.key)
        
        item = LFUCacheItem()
        item.key = key
        item.value = value
        item.frequency = 1

        self.maps[key] = item
        if self.head == None:
            node = LFUNode()
            node.frequency = item.frequency
            node.add_item(item)
            item.node = node    
            self.head = node
            return

        if self.head.frequency == 1:
            self.head.add_item(item)
            item.node = self.head
        else:
            node = LFUNode()
            node.frequency = item.frequency
            node.add_item(item)
            item.node = node
            node.next_node = self.head
            self.head.prev_node = node
            self.head = node
    
    def get(self, key):
        if not key in self.maps.keys():
            return None
        item = self.maps[key]
        item.frequency +=1
        self.__move_to_next_node(item)
        
        return self.maps[key].value

    def remove(self, key):
        if not key in self.maps.keys():
            return
        item = self.maps[key]
        item.node.remove_item(item.key)
        if(item.node.is_empty()):
            self.__remove_empty_node(item.node)
        item.node = None
        del self.maps[key]
    
    def __move_to_next_node(self, item: LFUCacheItem):
        current_node = item.node
        next_node = current_node.next_node
        if next_node != None:
            if next_node.frequency == item.frequency:
                next_node.add_item(item)
                item.node = next_node
            else:
                inserted_node = LFUNode()
                inserted_node.frequency = item.frequency
                inserted_node.add_item(item)
                item.node = inserted_node

                current_node.next_node = inserted_node
                inserted_node.prev_node = current_node
                
                next_node.prev_node = inserted_node
                inserted_node.next_node = next_node
        else:
            inserted_node = LFUNode()
            inserted_node.frequency = item.frequency
            inserted_node.add_item(item)
            item.node = inserted_node

            current_node.next_node = inserted_node
            inserted_node.prev_node = current_node 

        current_node.remove_item(item.key)

        if current_node.is_empty():
            self.__remove_empty_node(current_node)
    
    def __remove_empty_node(self, empty_node: LFUNode):
        if empty_node.prev_node == None:
            self.head = empty_node.next_node
            if self.head != None:
                self.head.prev_node = None
            empty_node.next_node = None
        else:
            empty_node.prev_node.next_node = empty_node.next_node
            if empty_node.next_node != None:
                empty_node.next_node.prev_node = empty_node.prev_node
            empty_node.prev_node = None
            empty_node.next_node = None

    def get_cache_space(self):
        return len(self.maps)