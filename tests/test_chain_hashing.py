from algorithms import ChainHashMap
from algorithms import Item


class TestChainHashing:
    hash_map = ChainHashMap(size=1)

    def test_insert(self):
        item = Item(1, 1)
        self.hash_map.insert(item)
        assert self.hash_map.map[0].data == item
        self.hash_map.refresh()

    def test_get(self):
        item = Item(1, 1)
        self.hash_map.insert(item)
        self.hash_map.get()


a = TestChainHashing()
a.test_insert()
