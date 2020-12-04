from algorithms import CuckooHashMap
from algorithms.base import Item
import random


def main():
    elements_amount = 3
    digits = [random.randint(0, 100)] * elements_amount
    print(digits)
    hash_map_size = 2 * len(digits)
    h = CuckooHashMap(size=hash_map_size, elements_amount=len(digits))
    for i, digit in enumerate(digits):
        item = Item(i, digit)
        h.insert(item)
    print(h)
    load_factors = h.get_the_load_factor()
    print(
        f"Load factor of first bucket {load_factors[0]}\nLoad factor of second bucket {load_factors[1]}"
    )
    # print(h.get(1))


if __name__ == "__main__":
    main()
