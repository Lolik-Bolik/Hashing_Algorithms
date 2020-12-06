from .base import BaseHashMap
import math
import logging as logger

logger.basicConfig(level=logger.NOTSET)


class CuckooHashMap(BaseHashMap):
    def __init__(
        self,
        size: int = 20,
        num_maps: int = 2,
        elements_amount: int = None,
        num_hash_func: int = 2,
    ):
        super().__init__(size, num_maps, num_hash_func=num_hash_func)
        self.map_1, self.map_2 = self.maps
        self.collision_count = 0
        self.insereted_elements_amount = [0] * self.num_maps
        self.max_knockout = max(int(6 * math.log(elements_amount)), 2)
        self.elements_amount = elements_amount

    def get_search_positions(self, key):
        return self.hash_functions[0](key), self.hash_functions[1](key)

    def insert(self, item):
        if self.get(item.key)[0]:
            return False
        first_index, second_index = self.get_search_positions(item.key)
        # look up in first bucket
        search_position = first_index
        bucket = self.map_1

        for _ in range(self.max_knockout):
            # if slot is free, insert key here
            if bucket[search_position] is None:
                bucket[search_position] = item
                if search_position == first_index:
                    self.insereted_elements_amount[0] += 1
                else:
                    self.insereted_elements_amount[1] += 1
                return True
            # if slot is not empty, kick out old key and replaced it with query key
            item, bucket[search_position] = bucket[search_position], item
            self.collision_count += 1
            # search new slot for kicked out key
            if search_position == first_index:
                first_index, second_index = self.get_search_positions(item.key)
                search_position = second_index
                bucket = self.map_2
            else:
                first_index, second_index = self.get_search_positions(item.key)
                search_position = first_index
                bucket = self.map_1
        logger.info("Knockout limit was reached! Rehashing ...")
        self.rehash()
        self.insert(item)
        return True

    def rehash(self):
        # self.hash_functions = self._generate_hash_func(self.num_hash_func)
        logger.info("New hash fucntions choosed!")
        temp = CuckooHashMap(size=self.size, elements_amount=self.elements_amount)
        for i in range(self.size):
            x = self.map_1[i]
            y = self.map_2[i]
            if x is not None:
                temp.insert(x)
            if y is not None:
                temp.insert(y)
        self.__dict__.update(temp.__dict__)
        logger.info("Rehashing done!")

    def get(self, key):
        first_index, second_index = self.get_search_positions(key)
        first_item = self.map_1[first_index]
        second_item = self.map_2[second_index]
        if first_item is not None and first_item.key == key:
            return True, first_item
        elif second_item is not None and second_item.key == key:
            return True, second_item
        else:
            return False, None

    def get_the_load_factor(self):
        return (
            self.insereted_elements_amount[0] / self.size,
            self.insereted_elements_amount[1] / self.size,
        )

    def delete(self, key):
        first_index, second_index = self.get_search_positions(key)
        first_item = self.map_1[first_index]
        second_item = self.map_2[second_index]
        if first_item is not None and first_item.key == key:
            self.map_1[first_index] = None
            self.insereted_elements_amount[0] -= 1
        elif second_item is not None and second_item.key == key:
            self.map_2[second_index] = None
            self.insereted_elements_amount[1] -= 1
        else:
            return False
        return True

    def refresh(self):
        super().refresh()
        self.map_1, self.map_2 = self.maps

    def __len__(self):
        return sum(self.insereted_elements_amount)
