import random


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

    def __init__(self, p, m):
        self.hash_map_size = m
        self.p = p
        # create two set for picking a and b, naming from Cormen
        self.a = random.choice(tuple(range(0, self.p - 1)))
        self.b = random.choice(tuple(range(1, self.p - 1)))

    def __call__(self, k):
        return ((self.a * k + self.b) % self.p) % self.hash_map_size
