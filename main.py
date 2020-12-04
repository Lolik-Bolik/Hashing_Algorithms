from utils import UniversalHashFunction
from algorithms import CuckooHashMap, ChainHashMap
from Crypto.Util import number
import random
from algorithms import Item


def main():
    random.seed(42)
    number_of_bits = 8
    p = number.getPrime(number_of_bits)
    hash_map_size = 3
    assert p > hash_map_size
    h = ChainHashMap(size=hash_map_size)
    digits = [Item(i, i) for i in range(5)]
    for digit in digits:
        h.insert(digit)
    print(h)
    for digit in digits:
        is_found, value = h.get(digit)
        assert value.value == digit.value


if __name__ == "__main__":
    main()
