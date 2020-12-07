import random
from algorithms.base import Union


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
            return (
                sum([self.a * v ** i for i, v in enumerate(k)])
                % self.p
                % self.hash_map_size
            )
        elif isinstance(k, str):
            # TODO: implement
            raise NotImplementedError
        else:
            raise TypeError("Key should be from supported types: int, tuple, str")
