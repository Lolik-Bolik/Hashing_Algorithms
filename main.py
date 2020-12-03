from utils import UniversalHashFunction
from algorithms import CuckooHashMap
from Crypto.Util import number


def main():
    digits = [i for i in range(15)]
    hash_map_size = len(digits) * 2
    print(hash_map_size)
    h = CuckooHashMap(size=hash_map_size, elements_amount=len(digits))
    for digit in digits:
        h.insert(digit)

    # digits = [0, 1, 2]
    # for digit in digits:
    #     h.add(digit)
    print(h)
    print(h.get_the_load_factor())
    print(h.get(12))


if __name__ == "__main__":
    main()
