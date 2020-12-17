from collections import Hashable
from typing import Any, Union
from .universal_hash_function import (
    UniversalHashFunction,
    FastUniversalHashFunction,
    KIndependentUniversalHashFunction,
)
from Crypto.Util import number
from copy import deepcopy


class Item:
    def __init__(self, key: Hashable, value: Any):
        assert key is not None
        assert isinstance(key, Hashable)
        self.key = key
        self.value = value

    def __repr__(self):
        print(f"{self.key}: {self.value}", end="\n")
        return ""

    def __eq__(self, other):
        return (self.key == other.key) and (self.value == other.value)

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


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

    def __eq__(self, other):
        return self.data == other.data

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


class BaseHashMap:
    def __init__(
        self,
        size: int,
        num_maps: int = 1,
        num_hash_func: int = 1,
        number_of_bits: int = 8,
        use_k_independent: bool = False,
    ):
        self.size = size
        self.collision_count = 0
        self.num_maps = num_maps
        self.num_hash_func = num_hash_func
        self.maps = self._create_maps()
        self.use_k_independent = use_k_independent
        self.hash_functions = self._generate_hash_func(num_hash_func, number_of_bits)
        self.inserted_elements_amount = 0

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

    def delete(self, item: Union[Item, Hashable]):
        raise NotImplementedError

    def _create_maps(self):
        return [[None] * self.size for _ in range(self.num_maps)]

    def _generate_hash_func(self, num_hash_func: int, number_of_bits: int):
        p = number.getPrime(number_of_bits)
        while p < self.size:
            number_of_bits += 2
            p = number.getPrime(number_of_bits)
        function = (
            UniversalHashFunction
            if not self.use_k_independent
            else KIndependentUniversalHashFunction
        )
        hash_functions = [function(p, self.size) for _ in range(num_hash_func)]
        return hash_functions

    def refresh(self):
        self.maps = self._create_maps()
        self.collision_count = 0

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def __len__(self):
        return self.inserted_elements_amount

    def __getitem__(self, key):
        status, item = self.get(key)
        if status:
            return item
        else:
            return None
