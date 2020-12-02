import random


class UniversalHashFunction:
    def __init__(self, p, m):
        self.hash_map_size = m
        self.p = p
        # create two set for picking a and b, naming from Cormen
        self.zet_p = set(i for i in range(0, p - 1))
        self.zet_p2 = set(i for i in range(1, p - 1))

    def __call__(self, k):
        a = random.choice(tuple(self.zet_p2))
        b = random.choice(tuple(self.zet_p))
        return ((a * k + b) % self.p) % self.hash_map_size
