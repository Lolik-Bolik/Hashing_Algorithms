from utils import UniversalHashFunction
from algorithms import CuckooHashMap
from random import randint
from Crypto.Util import number


def main():
    number_of_bits = 8
    p = number.getPrime(number_of_bits)
    hash_map_size = 1
    assert p > hash_map_size
    h_1 = UniversalHashFunction(p, hash_map_size)
    h_2 = UniversalHashFunction(p, hash_map_size)
    h = CuckooHashMap(size=hash_map_size, h_1=h_1, h_2=h_2)
    digits = [0, 1, 2]
    for digit in digits:
        h.add(digit)
    print(h)


if __name__ == "__main__":
    main()
