class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class BaseHashMap:
    def __init__(self, size: int, num_maps: int = 1):
        self.size = size
        self.collision_count = 0
        self.maps = self._create_maps(num_maps)

    def __repr__(self):
        for table in self.maps:
            for i in range(self.size):
                print(table[i], end="\n")
            print("----------------------")
        return ""

    def add(self, key):
        raise NotImplementedError

    def get(self):
        raise NotImplementedError

    def insert(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def _create_maps(self, num_maps):
        return [[None] * self.size for _ in range(num_maps)]
