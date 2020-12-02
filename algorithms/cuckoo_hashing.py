import hashlib


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class CuckooHashMap:
    def __init__(self, size: int, h_1, h_2):
        self.size = size
        self.map_1 = [None] * self.size
        self.map_2 = [None] * self.size
        self.h_1 = h_1
        self.h_2 = h_2
        self.collision_count = 0

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
