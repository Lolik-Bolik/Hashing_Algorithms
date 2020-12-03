from Crypto.Util import number
from utils import UniversalHashFunction


class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class BaseHashMap:
    def __init__(self, size: int, num_maps: int = 1):
        self.size = size
        self.collision_count = 0
        self.num_maps = num_maps
        self.maps = self._create_maps(self.num_maps)

    def get_hash_functions(self, hash_functions_number=2, number_of_bits=8):
        hash_fucntions = []
        p = number.getPrime(number_of_bits)
        if p < self.size:
            number_of_bits += 2
            self.get_hash_functions(number_of_bits=number_of_bits)
        for _ in range(hash_functions_number):
            hash_fucntions.append(UniversalHashFunction(p, self.size))
        return hash_fucntions

    def __repr__(self):
        for table in self.maps:
            for i in range(self.size):
                print(table[i], end="\n")
            print("----------------------")
        return ""

    def insert(self, value):
        raise NotImplementedError

    def get(self, value):
        raise NotImplementedError

    def delete(self, value):
        raise NotImplementedError

    def _create_maps(self, num_maps):
        return [[None] * self.size for _ in range(num_maps)]
