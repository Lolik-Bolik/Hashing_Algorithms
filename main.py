from evaluator import Evaluator
from inspect import getmembers, isclass
import algorithms
import json
from tqdm import tqdm


def main():
    measurement_results = {}
    hashing_classes = [
        o for o in getmembers(algorithms) if isclass(o[1]) if not o[0] == "Item"
    ]
    pbar = tqdm(hashing_classes)
    for name, hashing_table_cls in pbar:
        if name != "CuckooHashMap":
            continue
        pbar.set_description(f"Name: {name}")
        evaluator = Evaluator(1000, 105000, 5000, hashing_table_cls, dtype="tuple")
        measurement_results[name] = evaluator()
    with open("measurement_results_100k_tuple.json", "w") as fp:
        json.dump(measurement_results, fp, indent=4, sort_keys=True)


if __name__ == "__main__":
    main()
