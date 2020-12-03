from .base import BaseHashMap
import math
import logging as logger

logger.basicConfig(level=logger.NOTSET)


class Node:
    def __init__(self, key=None, data=None):
        self.key = key
        self.data = data


class CuckooHashMap(BaseHashMap):
    def __init__(self, size: int = 20, num_maps: int = 2, elements_amount: int = None):
        super().__init__(size, num_maps)
        self.map_1, self.map_2 = self.maps
        self.collision_count = 0
        self.insereted_elements_amount = 0
        self.hash_fucntions = self.get_hash_functions()
        self.max_knockout = int(6 * math.log(elements_amount))

    def get_search_positions(self, key):
        return self.hash_fucntions[0](key), self.hash_fucntions[1](key)

    def insert(self, key):
        if key is None:
            return False

        if self.get(key):
            return False
        first_index, second_index = self.get_search_positions(key)
        # look up in first bucket
        search_position = first_index
        bucket = self.map_1

        for _ in range(self.max_knockout):
            # if slot is free, insert key here
            if bucket[first_index] is None:
                bucket[first_index] = key
                self.insereted_elements_amount += 1
                return True
            # if slot is not empty, kick out old key and replaced it with query key
            key, bucket[search_position] = bucket[search_position], key
            # search new slot for kicked out key
            if search_position == first_index:
                if key is None:
                    continue
                first_index, second_index = self.get_search_positions(key)
                search_position = second_index
                bucket = self.map_2
            else:
                if key is None:
                    continue
                first_index, second_index = self.get_search_positions(key)
                search_position = first_index
                bucket = self.map_1
        logger.info("Knockout limit was reached! Rehashing ...")
        self.rehash()
        self.insert(key)
        return True

    def rehash(self):
        self.hash_fucntions = self.get_hash_functions()
        logger.info("New hash fucntions choosed!")
        self.map_1, self.map_2 = self._create_maps(self.num_maps)
        logger.info("Rehashing done!")
        return True

    def get(self, key):
        first_index, second_index = self.get_search_positions(key)
        first_value = self.map_1[first_index]
        second_value = self.map_2[second_index]
        if first_value is not None and first_value == key:
            return True
        elif second_value is not None and second_value == key:
            return True
        else:
            return False

    def get_the_load_factor(self):
        return self.insereted_elements_amount / self.size

    def delete(self):
        pass

    def __len__(self):
        return self.insereted_elements_amount
