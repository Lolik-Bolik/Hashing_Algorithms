from .base import BaseHashMap


class CuckooHashMap(BaseHashMap):
    def __init__(self, h_1, h_2, size: int = 20, num_maps: int = 2):
        super().__init__(size, num_maps)
        self.map_1, self.map_2 = self.maps
        self.h_1, self.h_2 = h_1, h_2

    def __repr__(self):
        for i in range(self.size):
            print(self.map_1[i], end="\n")
        print("----------------------")
        for i in range(self.size):
            print(self.map_2[i], end="\n")
        return ""

    def add(self, key):
        key_hash = self.h_1(key)
        if self.map_1[key_hash] is None:
            self.map_1[key_hash] = key
        else:
            self.map_2[key_hash] = key

    def get(self):
        pass

    def insert(self):
        pass

    def delete(self):
        pass
