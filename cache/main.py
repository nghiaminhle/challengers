from lru_cache import LRUCache
from lfu_cache import LFUCache

def test_lru():
    cache_store = LRUCache(5)
    
    cache_store.add('1', 1)
    assert cache_store.get('1') == 1
    assert cache_store.first.key == '1'
    assert cache_store.last.key == '1'
    
    cache_store.add('2', 2)
    assert cache_store.get('2') == 2
    assert cache_store.first.key == '1'
    assert cache_store.last.key == '2'
    
    cache_store.add('3', 3)
    assert cache_store.get('3') == 3
    assert cache_store.first.key == '1'
    assert cache_store.last.key == '3'
    
    cache_store.add('4', 4)
    assert cache_store.get('4') == 4
    assert cache_store.first.key == '1'
    assert cache_store.last.key == '4'
    
    cache_store.add('5', 5)
    assert cache_store.get('5') == 5
    assert cache_store.first.key == '1'
    assert cache_store.last.key == '5'

    cache_store.add('5', 6)
    assert cache_store.get('5') == 6
    assert cache_store.first.key == '1'
    assert cache_store.last.key == '5'
    
    cache_store.add('6', 6)
    assert cache_store.get('6') == 6
    assert cache_store.get_cache_space() == 5
    assert cache_store.get('1') == None
    assert cache_store.first.key == '2'
    assert cache_store.last.key == '6'

    cache_store.remove('2')
    assert cache_store.get('2') == None
    assert cache_store.get_cache_space() == 4
    assert cache_store.first.key == '3'
    assert cache_store.first.previous_item == None
    assert cache_store.last.key == '6'
    
    cache_store.add('3', 4)
    assert cache_store.get('3') == 4
    assert cache_store.first.key == '4'
    assert cache_store.first.previous_item == None
    assert cache_store.last.key == '3'
    
    cache_store.add('4', 6)
    assert cache_store.get('4') == 6
    assert cache_store.first.key == '5'
    assert cache_store.last.key == '4'

    cache_store.add('4', 1)
    assert cache_store.get('4') == 1
    assert cache_store.last.key == '4'

    cache_store.add('7', 7)
    assert cache_store.get('7') == 7
    assert cache_store.get_cache_space() == 5
    assert cache_store.last.key == '7'

    cache_store.add('8', 8)
    assert cache_store.get('8') == 8
    assert cache_store.last.key == '8'

    assert cache_store.get('5') == None
   
    cache_store.remove('3')
    assert cache_store.get('3') == None
    cache_store.remove('4')
    assert cache_store.get('4') == None
    cache_store.remove('6')
    assert cache_store.get('6') == None
    cache_store.remove('7')
    assert cache_store.get('7') == None
    cache_store.remove('8')
    assert cache_store.get('8') == None
    
    assert cache_store.get_cache_space() == 0

def test_lfu():
    cache_store = LFUCache(5)
    
    cache_store.add('1', 1)
    assert cache_store.get('1') == 1
    
    cache_store.add('2', 2)
    assert cache_store.get('2') == 2
    
    cache_store.add('3', 3)
    assert cache_store.get('3') == 3
    
    cache_store.add('4', 4)
    assert cache_store.get('4') == 4
    
    cache_store.add('5', 5)
    assert cache_store.get('5') == 5

    cache_store.add('1', 5)
    assert cache_store.get('1') == 5

    cache_store.add('6', 6)
    assert cache_store.get('2') == None

    assert cache_store.get('6') == 6
    assert cache_store.get('6') == 6
    assert cache_store.get('1') == 5
    assert cache_store.get('4') == 4
    assert cache_store.get('4') == 4
    assert cache_store.get('3') == 3
    assert cache_store.get('3') == 3

    cache_store.add('7', 7)
    assert cache_store.get('5') == None
    assert cache_store.get_cache_space() == 5

    cache_store.remove('1')
    assert cache_store.get('1') == None
    cache_store.remove('3')
    assert cache_store.get('3') == None
    cache_store.remove('4')
    assert cache_store.get('4') == None
    cache_store.remove('6')
    assert cache_store.get('6') == None
    cache_store.remove('7')
    assert cache_store.get('7') == None

    assert cache_store.get_cache_space() == 0
    

if __name__ == "__main__":
    test_lru()
    test_lfu()