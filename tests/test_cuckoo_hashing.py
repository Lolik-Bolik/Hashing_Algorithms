from algorithms import CuckooHashMap
from algorithms.base import Item
import random

random.seed(42)


class TestCuckooHashing:
    hash_map = CuckooHashMap(size=1, elements_amount=1)

    # def test_adding_elements(self):
    #     self.hash_map.size =
    #     digits_number = random.randint(1, 20)
    #     digits = [i for i in range(digits_number)]
    #     hash_map_size = len(digits)
    #     for digit in digits:
    #         self.hash_map.insert(digit)
    #     for digit in digits:
    #         assert self.hash_map.get(digit)

    def test_insert(self):
        item = Item(1, 1)
        self.hash_map.insert(item)
        print(self.hash_map.map_1[0].key)
        print(item.key)
        assert self.hash_map.map_1[0] == item
        self.hash_map.refresh()


#
# test_class = TestCuckooHashing()
# test_class.test_insert()
