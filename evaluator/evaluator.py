from time import time
from algorithms.base import Item
from copy import deepcopy
from tqdm import tqdm
from random import choice, sample
import math


class Evaluator:
    def __init__(
        self,
        hash_table_cls,
        external_data=None,
        start_value=-1,
        max_value=-1,
        step=-1,
        dtype="int",
        **kwargs,
    ):
        self.start_value = start_value
        self.hash_table_cls = hash_table_cls
        self.max_value = max_value
        self.step = step
        self.table_density = [
            0.1,
            0.25,
            0.5,
            0.75,
            0.9,
            0.99,
        ]  # We drop for 1.0 as we assert status and it is false for full table
        self.results = {}
        self.dtype = dtype
        self.data = None
        self.kwargs = kwargs
        self.external_data = external_data

    def generate_data(self, n_elements):
        if self.external_data is None:
            data = [self.generate_dtype_item(i) for i in range(n_elements)]
        else:
            data = self.generate_data_subset(n_elements)
        return data

    def generate_dtype_item(self, key: int):
        if self.dtype == "int":
            item = Item(key, key)
        elif self.dtype == "str":
            item = Item(f"{key}", key)
        elif self.dtype == "tuple":
            item = Item((key, key + 2, key + 4), key)
        else:
            raise TypeError("Data type should be either int, str, or tuple")
        return item

    def measure(self, hash_table, operation):
        method = getattr(hash_table, operation)
        if operation == "insert":
            item = (
                self.generate_dtype_item(self.max_value + 1)
                if self.external_data is None
                else Item("dummyword", "dummyword")
            )
        else:
            item = choice(self.data)

        tic = time()
        if operation != "get":
            status = method(item)
        else:
            status, _ = method(item.key)
        operation_time = round(time() - tic, 8)
        assert status
        if operation == "insert":
            assert hash_table.delete(item)
        elif operation == "delete":
            assert hash_table.insert(item)
        return operation_time

    def generate_data_subset(self, n_elements):
        data = sample(self.external_data, k=n_elements)
        return data

    def __call__(self):
        for size in range(self.start_value, self.max_value, self.step):
            for density in tqdm(self.table_density, desc=f"\tSize: {size}"):
                hash_table = self.hash_table_cls(size=size, **self.kwargs)
                self.data = self.generate_data(int(size * density))
                for item in self.data:
                    hash_table.insert(item)
                launch_results = {}
                for operation in ("insert", "get", "delete"):
                    operation_time = self.measure(hash_table, operation)
                    assert len(hash_table) / size == density
                    if operation_time > 60:
                        launch_results[operation] = operation_time
                        self.results[f"{size}, {density}"] = launch_results
                        return self.results
                    launch_results[operation] = operation_time
                self.results[f"{size}, {density}"] = launch_results
        return self.results
