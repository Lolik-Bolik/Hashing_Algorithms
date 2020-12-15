from .base import Node, BaseHashMap


class DictHashMap(BaseHashMap):
    def __init__(self, size: int = 0, num_hash_func: int = 0, **kwargs):
        super().__init__(size, num_hash_func=num_hash_func, **kwargs)
        self.map = dict()
        self.hash_func = None
        self.inserted_elements_amount = 0

    def insert(self, item):
        if self.map.get(item.key) is None:
            self.map[item.key] = item
            self.inserted_elements_amount += 1
            return True
        return False

    def get(self, key):
        item = self.map.get(key)
        status = False if item is None else True
        return status, item

    def delete(self, item):
        if self.get(item.key)[0]:
            self.map.pop(item.key)
            self.inserted_elements_amount -= 1
            return True
        else:
            return False
