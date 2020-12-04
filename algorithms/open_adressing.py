from algorithms.base import BaseHashMap, Item
import logging as logger


class OpenAdressingHashMap(BaseHashMap):
    def __init__(
        self,
        size: int = 20,
        num_maps: int = 1,
        elements_amount: int = None,
        num_hash_func: int = 1,
    ):
        super().__init__(size, num_maps, num_hash_func=num_hash_func)
        self.map = self.maps[0]
        self.collision_count = 0
        self.insereted_elements_amount = 0
        self.elements_amount = elements_amount

    def linear_probing(self, search_index, offset_index, stride: int = 1):
        """
        (hash(x) + ik) mod hash_map_size
        k - offset
        i - offset from search index
        hash(x) - search_index
        """
        return (search_index + offset_index * stride) % self.size

    def insert(self, item: Item):
        if self.insereted_elements_amount == self.size:
            self.rehash()
        search_index = self.hash_functions[0](item.key)
        if self.map[search_index] is None:
            self.map[search_index] = item
            self.insereted_elements_amount += 1
        else:
            for offset_index in range(1, self.size):
                new_search_index = self.linear_probing(search_index, offset_index)
                if self.map[new_search_index] is None:
                    self.map[new_search_index] = item
                    self.insereted_elements_amount += 1
                    break

    def refresh(self):
        super().refresh()
        self.map = self.maps[0]

    def rehash(self):
        logger.info("New hash fucntions choosed!")
        temp = OpenAdressingHashMap(
            size=self.size * 2, elements_amount=self.elements_amount
        )
        for i in range(self.size):
            x = self.map[i]
            if x is not None:
                temp.insert(x)
        self.map = temp.map
        self.hash_functions = temp.hash_functions
        logger.info("Rehashing done!")

    def get(self, key):
        pass
