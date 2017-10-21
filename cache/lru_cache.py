class CacheItem:
    next_item = None
    previous_item = None
    key = None
    value = None

    def __init__(self, key, value):
        self.key = key
        self.value = value

class LRUCache:
    maps = {}
    size = 0
    first = None
    last = None

    def __init__(self, size):
        self.size = size

    def add(self, key, value):
        if self.first == None:
            item = CacheItem(key, value)
            self.first = item
            self.last = item
            self.maps[key] = item
            return
        
        if key in self.maps:
            item = self.maps[key]            
            self.__move_to_end(item)
            item.value = value
        else:
            if (len(self.maps)==self.size):
                self.remove(self.first.key)
            item = CacheItem(key, value)
            item.previous_item = self.last
            self.last.next_item = item
            self.last = item
            self.maps[key] = item
    
    def get(self, key):
        if key in self.maps.keys():
            item = self.maps[key]
            self.__move_to_end(item)
            return item.value
        return None

    def remove(self, key):
        if key in self.maps.keys():
            item = self.maps[key]
            self.__move_to_end(item)
            if item.previous_item !=None:
                self.last = item.previous_item
                item.previous_item.next_item = None
                item.previous_item = None
            else:
                self.first = None
                self.last = None
            del self.maps[key]
    
    def __move_to_end(self, item):
        if item.next_item == None:
            return
        item.next_item.previous_item = item.previous_item
        if item.previous_item != None:
            item.previous_item.next_item = item.next_item            
        else:
            self.first = item.next_item
        self.last.next_item = item
        item.previous_item = self.last
        item.next_item = None
        self.last = item

    def get_cache_space(self):
        return len(self.maps)