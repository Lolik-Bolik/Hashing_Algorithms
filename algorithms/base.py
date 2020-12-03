class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class BaseHashMap():
    def __init__(self, size: int, num_maps: int = 1):
        self.size = size
        self.collision_count = 0
        self.maps = self.create_maps(num_maps)

    def __repr__(self):
        for table in self.maps:
            for i in range(self.size):
                print(table[i], end="\n")
            print("----------------------")
        return ""

    def add(self, key):
        pass

    def get(self):
        pass

    def insert(self):
        pass

    def delete(self):
        pass

    def create_maps(self, num_maps):
        return [[None] * self.size for _ in range(num_maps)]