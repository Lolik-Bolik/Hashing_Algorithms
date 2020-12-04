from collections import Hashable
from typing import Any
from utils import UniversalHashFunction
from Crypto.Util import number


class Item:
    def __init__(self, key: Hashable, value: Any):
        assert key is not None
        assert isinstance(key, Hashable)
        self.key = key
        self.value = value


class Node:
    def __init__(self, data: Item = None):
        self.data = data
        self.next = None

    def __repr__(self):
        if self.next is not None:
            print(self.data, " ->", end=" ")
            next_record = self.next
            while next_record.next is not None:
                print(next_record.data)
                next_record = next_record.next
            print(next_record.data, end="")
        else:
            print(self.data, end="")
        return ""


class BaseHashMap:
    def __init__(self, size: int, num_maps: int = 1, num_hash_func: int = 1):
        self.size = size
        self.collision_count = 0
        self.maps = self._create_maps(num_maps)
        self.hash_functions = self._generate_hash_func(num_hash_func)

    def __repr__(self):
        for table in self.maps:
            for i in range(self.size):
                print(table[i], end="\n")
            print("----------------------")
        return ""

    def insert(self, item: Item):
        raise NotImplementedError

    def get(self, key: Hashable):
        raise NotImplementedError

    def delete(self, item: Item):
        raise NotImplementedError

    def _create_maps(self, num_maps: int):
        return [[None] * self.size for _ in range(num_maps)]

    def _generate_hash_func(self, num_hash_func: int = 1, number_of_bits: int = 8):
        p = number.getPrime(number_of_bits)
        while p < self.size:
            number_of_bits += 2
            p = number.getPrime(number_of_bits)
        hash_functions = [
            UniversalHashFunction(p, self.size) for _ in range(num_hash_func)
        ]
        return hash_functions
