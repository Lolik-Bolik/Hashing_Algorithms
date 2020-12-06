from algorithms import CuckooHashMap
from algorithms.base import Item
import random

random.seed(42)


class TestCuckooHashing:
    hash_map = CuckooHashMap(size=1)

    # def test_adding_elements(self):
    #     digits_number = random.randint(1, 100)
    #     digits = [i for i in range(digits_number)]
    #     self.hash_map.size = 2 * len(digits)
    #     for i, digit in enumerate(digits):
    #         item = Item(i, digit)
    #         self.hash_map.insert(item)
    #     for i, digit in enumerate(digits):
    #         assert self.hash_map.get(i)

    def test_insert(self):
        item = Item(1, 1)
        self.hash_map.insert(item)
        print(self.hash_map.map_1[0].key)
        print(item.key)
        assert self.hash_map.map_1[0] == item
        self.hash_map.refresh()

    def test_get(self):
        item = Item(1, 1)
        self.hash_map.insert(item)
        status, data = self.hash_map.get(1)
        assert status
        assert data == item
        item_link = Item(2, 1)
        self.hash_map.insert(item_link)
        status, data = self.hash_map.get(2)
        assert status
        assert data == item_link
        self.hash_map.refresh()

    # def test_delete(self):
    #     item_1 = Item(1, 1)
    #     self.hash_map.insert(item_1)
    #     self.hash_map.delete(item_1)
    #     status, data = self.hash_map.get(1)
    #     assert not status
    #     item_2 = Item(2, 1)
    #     item_3 = Item(3, 1)
    #     self.hash_map.insert(item_1)
    #     self.hash_map.insert(item_2)
    #     self.hash_map.insert(item_3)
    #     self.hash_map.delete(item_2)
    #     status, data = self.hash_map.get(2)
    #     assert not status
    #     assert self.hash_map.map[0].next.data == item_1
    #     self.hash_map.refresh()

    def test_refresh(self):
        item = Item(1, 1)
        self.hash_map.insert(item)
        self.hash_map.refresh()
        status, data = self.hash_map.get(1)
        assert not status


a = TestCuckooHashing()
a.test_get()
