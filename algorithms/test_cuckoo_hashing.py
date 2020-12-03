from .cuckoo_hashing import CuckooHashMap
import random

random.seed(42)


def test_adding_elements():
    digits_number = random.randint(1, 20)
    digits = [i for i in range(digits_number)]
    hash_map_size = len(digits)
    h = CuckooHashMap(size=hash_map_size, elements_amount=len(digits))
    for digit in digits:
        h.insert(digit)
    for digit in digits:
        assert h.get(digit)
