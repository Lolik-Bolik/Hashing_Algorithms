from algorithms import CuckooHashMap
from algorithms.base import Item
import random
import time


def main():
    elements_amount = 1000000
    digits = [random.randint(0, 100)] * elements_amount
    hash_map_size = len(digits)
    h = CuckooHashMap(size=hash_map_size, elements_amount=len(digits))
    start = time.time()
    for i, digit in enumerate(digits):
        item = Item(i, digit)
        h.insert(item)
    print(f"Insertion time: {round(time.time() - start,2)}s")
    load_factors = h.get_the_load_factor()
    print(
        f"Load factor of first bucket {load_factors[0]}\nLoad factor of second bucket {load_factors[1]}"
    )


if __name__ == "__main__":
    main()
