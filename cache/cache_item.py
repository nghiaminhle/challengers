class CacheItem:
    next_item = None
    previous_item = None
    key = None
    value = None
    frequency = 0

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.frequency = 0