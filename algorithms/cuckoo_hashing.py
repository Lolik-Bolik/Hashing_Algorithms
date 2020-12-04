from .base import Node, BaseHashMap
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
        self.max_knockout = max(int(6 * math.log(elements_amount)), 1)

    def get_search_positions(self, key):
        return self.hash_functions[0](key), self.hash_functions[1](key)

    def insert(self, item):
        assert item is not None
        if self.get(item.key):
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
        self.hash_functions = self._generate_hash_func(self.num_hash_func)
        logger.info("New hash fucntions choosed!")
        temp_1, temp_2 = self._create_maps()
        for i in range(self.size):
            x = self.map_1[i]
            y = self.map_2[i]
            if x is not None:
                temp_1.insert(x)
            if y is not None:
                temp_2.insert(y)
        self.map_1 = temp_1
        self.map_2 = temp_2
        logger.info("Rehashing done!")

    def get(self, key):
        first_index, second_index = self.get_search_positions(key)
        first_node = self.map_1[first_index]
        second_node = self.map_2[second_index]
        if first_node is not None and first_node.key == key:
            return True
        elif second_node is not None and second_node.key == key:
            return True
        else:
            return False

    def get_the_load_factor(self):
        return (
            self.insereted_elements_amount[0] / self.size,
            self.insereted_elements_amount[1] / self.size,
        )

    def delete(self, key):
        first_index, second_index = self.get_search_positions(key)
        first_node = self.map_1[first_index]
        second_node = self.map_2[second_index]
        if first_node is not None and first_node.key == key:
            self.map_1[first_index] = None
            self.insereted_elements_amount[0] -= 1
        elif second_node is not None and second_node.key == key:
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
