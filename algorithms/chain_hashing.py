from .base import Node, BaseHashMap


class NodeChain(Node):
    def __init__(self, data=None):
        super().__init__(data)


class ChainHashMap(BaseHashMap):
    def __init__(self, size: int = 1, num_hash_func: int = 1):
        super().__init__(size, num_hash_func=num_hash_func)
        self.map = self.maps[0]
        self.hash_func = self.hash_functions[0]

    def insert(self, item):
        hash_value = self.hash_func(item.key)
        if self.map[hash_value] is None:
            self.map[hash_value] = NodeChain(item.value)
            return
        else:
            self.collision_count += 1
            record_node = NodeChain(item.value)
            record_node.next = self.map[hash_value]
            self.map[hash_value] = record_node

    def get(self, item):
        hash_value = self.hash_func(item.key)
        if self.map[hash_value] is None:
            return False, None
        else:
            record_node = self.map[hash_value]
            while record_node.next is not None:
                if record_node.data == item.value:
                    return True, record_node.data
                record_node = record_node.next
            if record_node.data == item.value:
                return True, record_node.data
            return False, None

    def delete(self, item):
        hash_value = self.hash_func(item.key)
        record_node = self.map[hash_value]
        previous_node = None
        while record_node.next is not None:
            if record_node.data == item.value:
                if previous_node is not None:
                    previous_node.next = record_node.next
                del record_node
                return
            previous_node = record_node
            record_node = record_node.next