from time import time
from algorithms.base import Item
from copy import deepcopy
from tqdm import tqdm
from random import randint


class Evaluator:
    def __init__(self, start_value, max_value, step, hash_table_cls, data=None):
        self.start_value = start_value
        self.hash_table_cls = hash_table_cls
        self.data = data
        self.max_value = max_value
        self.step = step
        self.table_density = [
            0.1,
            0.25,
            0.5,
            0.75,
            0.9,
            0.99,
        ]  # We drop for 1.0 as we assert status and it is false for empty table
        self.results = {}

    def measure(self, hash_table, operation, size):
        hash_table = deepcopy(hash_table)
        method = getattr(hash_table, operation)
        if operation == "insert":
            item = Item(self.max_value + 1, self.max_value + 1)
        else:
            key = randint(0, size)
            item = Item(key, key)
        tic = time()
        if operation != "get":
            status = method(item)
        else:
            status, _ = method(item.key)
        assert status
        return round(time() - tic, 8)

    def __call__(self):
        for size in range(self.start_value, self.max_value, self.step):
            for density in tqdm(self.table_density, desc=f"\tSize: {size}"):
                hash_table = self.hash_table_cls(size=size)
                if self.data is None:
                    data = [Item(i, i) for i in range(int(size * density))]
                else:
                    data = self.data
                for item in data:
                    hash_table.insert(item)
                assert len(hash_table) / size == density
                launch_results = {}
                for operation in ("insert", "get", "delete"):
                    operation_time = self.measure(
                        hash_table, operation, int(size * density)
                    )
                    if operation_time > 60:
                        launch_results[operation] = time
                        return self.results
                self.results[f"{size}, {density}"] = launch_results
        return self.results
