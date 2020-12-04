from algorithms import ChainHashMap
from algorithms import Item


class TestChainHashing:
    hash_map = ChainHashMap(size=15, random_seed=0)

    def test_insert(self):
        self.hash_map.insert(Item(0, 0))


a = TestChainHashing()
a.test_hash_func()
