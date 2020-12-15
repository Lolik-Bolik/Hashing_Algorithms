from algorithms.base import BaseHashMap, Item, Node


class OpenNode(Node):
    def __init__(self, item):
        super().__init__(item)
        self.deleted = False

    def __repr__(self):
        if self.deleted is None:
            print(self.data, end="")
        else:
            print(None, end="")
        return ""


class OpenAddressingHashMap(BaseHashMap):
    def __init__(
        self, size: int = 20, num_maps: int = 1, num_hash_func: int = 1, **kwargs
    ):
        super().__init__(
            size,
            num_maps,
            num_hash_func=num_hash_func,
            **kwargs,
        )
        self.map = self.maps[0]
        self.inserted_elements_amount = 0

    def linear_probing(self, search_index, offset_index, stride: int = 1):
        """
        (hash(x) + ik) mod hash_map_size
        k - offset
        i - offset from search index
        hash(x) - search_index
        """
        return (search_index + offset_index * stride) % self.size

    def quadratic_probing(self, search_index, offset_index):

        return (search_index + offset_index * offset_index) % self.size

    def insert(self, item: Item):
        if self.inserted_elements_amount == self.size:
            self.rehash()
        search_index = self.hash_functions[0](item.key)
        if self.map[search_index] is None or self.map[search_index].deleted:
            self.map[search_index] = OpenNode(item)
            self.inserted_elements_amount += 1
            return True
        else:
            self.collision_count += 1
            for offset_index in range(1, self.size):
                new_search_index = self.linear_probing(search_index, offset_index)
                if (
                    self.map[new_search_index] is None
                    or self.map[new_search_index].deleted
                ):
                    self.map[new_search_index] = OpenNode(item)
                    self.inserted_elements_amount += 1
                    return True
        return False

    def get(self, key):
        search_index = self.hash_functions[0](key)
        if self.map[search_index] is None:
            return False, None
        elif (
            self.map[search_index].data.key == key
            and not self.map[search_index].deleted
        ):
            return True, self.map[search_index].data
        else:
            for offset_index in range(1, self.size):
                new_search_index = self.linear_probing(search_index, offset_index)
                if self.map[new_search_index] is None:
                    return False, None
                elif (
                    self.map[new_search_index].data.key == key
                    and not self.map[search_index].deleted
                ):
                    return True, self.map[new_search_index].data
        return False, None

    def delete(self, item):
        search_index = self.hash_functions[0](item.key)
        if self.map[search_index] is None:
            return False
        elif self.map[search_index].data == item:
            self.map[search_index].deleted = True
            self.inserted_elements_amount -= 1
            return True
        else:
            for offset_index in range(1, self.size):
                new_search_index = self.linear_probing(search_index, offset_index)
                if self.map[new_search_index] is None:
                    return False
                elif self.map[new_search_index].data == item:
                    self.map[search_index].deleted = True
                    self.inserted_elements_amount -= 1
                    return True

    def refresh(self):
        super().refresh()
        self.map = self.maps[0]
        self.inserted_elements_amount = 0

    def rehash(self, k: int = 2):
        temp = OpenAddressingHashMap(size=self.size * k)
        for i in range(self.size):
            x = self.map[i]
            if x is not None:
                temp.insert(x.data)
        self.__dict__.update(temp.__dict__)
