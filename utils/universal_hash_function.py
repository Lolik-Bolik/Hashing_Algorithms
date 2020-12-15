import random
from algorithms.base import Union
from math import log
import numpy as np


class UniversalHashFunction:
    """
    UniversalHashFunction generates example from Universe Hashing class fucntions

        - For integers
            h_a,b(x) = ((a*x+b) mod p) mod m

       Args:
           p (int): Prime number for hash function generation.
           m (m): Hash Map size.
       Note:
           p must be > m

       Attributes:
           (Look Carmen 3 edition 11.3.3 Universal hashing )
           zet_p (set): Set for randomly picking b
           zet_p2 (set): Set for randomly picking a

    """

    def __init__(self, p: int, m: int):
        self.hash_map_size = m
        self.p = p
        # Naming from Corman
        self.a = random.randint(0, self.p - 1)
        self.b = random.randint(1, self.p - 1)

    def __call__(self, k: Union[int, tuple, str]):
        if isinstance(k, int):
            return ((self.a * k + self.b) % self.p) % self.hash_map_size
        elif isinstance(k, tuple):
            assert all(
                isinstance(v, int) for v in k
            )  # Could be slow, but we should check that there are ints in vector
            # Note: This is (len(k) / p) + 1 / size universal hash function, so we need to choose quite bit prime number!
            # TODO: проверить, т.к кукушка выдает одинаковые хеши для векторов (0, 0, 0) и (1, 0, 0)
            return (
                sum([(self.a ** i) * v for i, v in enumerate(k)])
                % self.p
                % self.hash_map_size
            )
        elif isinstance(k, str):
            h = self(0)
            for char in k:
                h = (h * self.a + ord(char)) % self.p
            return h % self.hash_map_size
        else:
            raise TypeError("Key should be from supported types: int, tuple, str")


class FastUniversalHashFunction:
    """
    Fast UniversalHashFunction generates example from Universe Hashing class fucntions
        - For integers
            h_a,b(x) = ((a*x+b) mod p) mod m

       Args:
           p (int): Prime number for hash function generation.
           m (m): Hash Map size. Should be a power of two.
       Note:
           p must be > m

    """

    def __init__(self, p: int, m: int):
        self.hash_map_size = m
        self.p = p
        self.a = (
            2 * np.random.randint(0, (np.iinfo(np.int32).max - 2) // 2, dtype=np.int32)
            + 1
        )
        # Naming from Corman
        # self.a = 2 * (random.randint(1, 2 ** 32 - 2) // 2) + 1
        assert 0 < self.a < np.iinfo(np.int32).max
        self.b = np.random.randint(
            0, 2 ** (32 - int(log(self.hash_map_size, 2))), dtype=np.int32
        )
        assert 0 <= self.b < 2 ** (32 - int(log(self.hash_map_size, 2)))

    def __call__(self, k: Union[int, tuple, str]):
        if isinstance(k, int):
            k = np.int32(k)
            return (self.a * k + self.b) >> (32 - int(log(self.hash_map_size, 2)))
        elif isinstance(k, tuple):
            assert all(
                isinstance(v, int) for v in k
            )  # Could be slow, but we should check that there are ints in vector
            # Note: This is (len(k) / p) + 1 / size universal hash function, so we need to choose quite bit prime number!
            # TODO: проверить, т.к кукушка выдает одинаковые хеши для векторов (0, 0, 0) и (1, 0, 0)
            return (
                sum([self.a * v ** i for i, v in enumerate(k)])
                % self.p
                % self.hash_map_size
            )
        elif isinstance(k, str):
            h = self(0)
            for char in k:
                h = (h * self.a + ord(char)) % self.p
            return h % self.hash_map_size
        else:
            raise TypeError("Key should be from supported types: int, tuple, str")
