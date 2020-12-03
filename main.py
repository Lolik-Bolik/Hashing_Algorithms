from utils import UniversalHashFunction
from algorithms import CuckooHashMap
from random import randint
from Crypto.Util import number


def main():
    hash_map_size = 5
    h = CuckooHashMap(size=hash_map_size)
    h.get(5)
    print(h.get_the_load_factor())
    # digits = [0, 1, 2]
    # for digit in digits:
    #     h.add(digit)
    # print(h)


if __name__ == "__main__":
    main()
