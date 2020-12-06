from algorithms import ChainHashMap
from algorithms import Item


class TestChainHashing:
    hash_map = ChainHashMap(size=1, ignore_max_elements=True)

    def test_insert(self):
        item = Item(1, 1)
        self.hash_map.insert(item)
        assert self.hash_map.map[0].data == item
        item_link = Item(2, 2)
        self.hash_map.insert(item_link)
        assert self.hash_map.map[0].next is not None
        assert self.hash_map.map[0].next.data == item
        assert self.hash_map.collision_count == 1
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

    def test_delete(self):
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
        assert self.hash_map.map[0].next.data == item_1
        self.hash_map.refresh()

    def test_refresh(self):
        item = Item(1, 1)
        self.hash_map.insert(item)
        self.hash_map.refresh()
        status, data = self.hash_map.get(1)
        assert not status
