from .base import Node, BaseHashMap
import logging as logger

logger.basicConfig(level=logger.NOTSET)


class NodeChain(Node):
    def __init__(self, data=None):
        super().__init__(data)


class ChainHashMap(BaseHashMap):
    def __init__(
        self,
        size: int = 1,
        num_hash_func: int = 1,
        ignore_max_elements: bool = False,
        **kwargs
    ):
        super().__init__(size, num_hash_func=num_hash_func, **kwargs)
        self.map = self.maps[0]
        self.hash_func = self.hash_functions[0]
        self.inserted_elements_amount = 0
        self.ignore_max_elements = ignore_max_elements

    def insert(self, item):
        if self.inserted_elements_amount == self.size and not self.ignore_max_elements:
            return False
        hash_value = self.hash_func(item.key)
        if self.map[hash_value] is None:
            self.map[hash_value] = NodeChain(item)
            self.inserted_elements_amount += 1
            return True
        else:
            self.collision_count += 1
            record_node = NodeChain(item)
            record_node.next = self.map[hash_value]
            self.map[hash_value] = record_node
            self.inserted_elements_amount += 1
            return True

    def get(self, key):
        hash_value = self.hash_func(key)
        if self.map[hash_value] is None:
            return False, None
        else:
            record_node = self.map[hash_value]
            while record_node.next is not None:
                if record_node.data.key == key:
                    return True, record_node.data
                record_node = record_node.next
            if record_node.data.key == key:
                return True, record_node.data
            return False, None

    def delete(self, item):
        hash_value = self.hash_func(item.key)
        record_node = self.map[hash_value]
        if record_node is None:
            return False
        previous_node = None
        while record_node.next is not None:
            if record_node.data == item:
                if previous_node is not None:
                    previous_node.next = record_node.next
                self.inserted_elements_amount -= 1
                del record_node
                return True
            previous_node = record_node
            record_node = record_node.next
        if record_node.data == item:
            if previous_node is not None:
                previous_node.next = record_node.next
            else:
                self.map[hash_value] = None
            self.inserted_elements_amount -= 1
            del record_node
            return True
        return False

    def refresh(self):
        super().refresh()
        self.map = self.maps[0]
