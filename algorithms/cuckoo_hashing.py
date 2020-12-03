import hashlib
from utils import UniversalHashFunction
from Crypto.Util import number


class Node:
    def __init__(self, key=None, data=None):
        self.key = key
        self.data = data


class CuckooHashMap:
    def __init__(self, size: int = 20):
        def get_hash_fucntions(hash_functions_number=2):
            hash_fucntions = []
            number_of_bits = 8
            p = number.getPrime(number_of_bits)
            assert p > self.size
            for _ in range(hash_functions_number):
                hash_fucntions.append(UniversalHashFunction(p, self.size))
            return hash_fucntions

        self.size = size
        self.map_1 = [None] * self.size
        self.map_2 = [None] * self.size
        self.collision_count = 0
        self.elements_amount = 0
        self.hash_fucntions = get_hash_fucntions()

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

    def get(self, key):
        first_index = self.hash_fucntions[0](key)
        second_index = self.hash_fucntions[1](key)
        print(first_index, second_index)

    def get_the_load_factor(self):
        return self.elements_amount / self.size

    def insert(self):
        pass

    def delete(self):
        pass

    def __len__(self):
        return self.elements_amount
