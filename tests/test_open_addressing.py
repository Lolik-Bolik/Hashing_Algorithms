from algorithms import OpenAddressingHashMapLinear
from algorithms import Item


class TestChainHashing:
    hash_map = OpenAddressingHashMapLinear(size=1)

    def test_insert(self):
        item = Item(1, 1)
        self.hash_map.insert(item)
        assert self.hash_map.map[0].data == item
        assert self.hash_map.size == 1
        assert self.hash_map.inserted_elements_amount == 1
        self.hash_map.refresh()

    def test_rehash(self):
        item_1 = Item(1, 1)
        item_2 = Item(2, 1)
        self.hash_map.insert(item_1)
        assert self.hash_map.size == 1
        assert self.hash_map.inserted_elements_amount == 1
        self.hash_map.insert(item_2)
        assert self.hash_map.size == 2
        assert self.hash_map.inserted_elements_amount == 2

    def test_get(self):
        item = Item(1, 1)
        self.hash_map.insert(item)
        status, data = self.hash_map.get(1)
        assert status
        assert data == item
        item_1 = Item(2, 1)
        self.hash_map.insert(item_1)
        status, data = self.hash_map.get(2)
        assert status
        assert data == item_1
        self.hash_map.refresh()

    def test_delete(self):
        self.hash_map = OpenAddressingHashMapLinear(size=4)
        item_1 = Item(1, 1)
        self.hash_map.insert(item_1)
        self.hash_map.delete(item_1)
        status, data = self.hash_map.get(1)
        assert not status
        item_2 = Item(2, 1)
        item_3 = Item(3, 1)
        self.hash_map.insert(item_1)
        self.hash_map.insert(item_2)
        self.hash_map.insert(item_3)
        self.hash_map.delete(item_2)
        status, data = self.hash_map.get(2)
        assert not status
        self.hash_map.size = 1
        self.hash_map.rehash(1)
        self.hash_map.refresh()
        self.hash_map.insert(item_1)
        assert not self.hash_map.delete(item_2)
        self.hash_map.delete(item_1)
        assert self.hash_map.map[0].deleted

    def test_refresh(self):
        item = Item(1, 1)
        self.hash_map.insert(item)
        self.hash_map.refresh()
        status, data = self.hash_map.get(1)
        assert not status
