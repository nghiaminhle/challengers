from cache_item import CacheItem

"""
The algorithm is:
- Build a double linked list
- The first item is the least frequency item
- The last item is the greates frequecy item
- Once accessed a item, if it is not the last, increase frequency, then 
move item to the end of list if it's frequency is greater or equal frequency of the last

The idea behinds this algorithm is: if the last item is the greatest frequency item, don't need increase it
's frequency any more. By doing that, all items between the first and the last have the same frequency, and we're 
easy to find the least frequency item -the first.

"""
class LFUCache:
    maps = {}
    size = 0
    first = None
    last = None

    def __init__(self, size):
        self.size = size
    
    def add(self, key, value):
        if self.first == None:
            item = CacheItem(key, value)
            item.frequency +=1
            self.first = item
            self.last = self.first
            self.maps[key] = item
            return
        
        if key in self.maps.keys():
            item = self.maps[key]
            item.value = value
            if item.key != self.last.key:
                item.frequency +=1
                if item.frequency >= self.last.frequency:
                    self.__move_to_end(item)
        else:
            if (len(self.maps)==self.size):
                self.remove(self.first.key)
            item = CacheItem(key, value)
            item.frequency +=1
            item.next_item = self.first
            self.first.previous_item = item
            self.first = item
            self.maps[key] = item
    
    def get(self, key):
        if not key in self.maps.keys():
            return None
        item = self.maps[key]
        if item.key != self.last.key:
            item.frequency +=1
            if item.frequency >= self.last.frequency:
                self.__move_to_end(item)
        return item.value

    def remove(self, key):
        if not key in self.maps.keys():
            return
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