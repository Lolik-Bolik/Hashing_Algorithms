from evaluator import Evaluator
from inspect import getmembers, isclass
import algorithms
import json
from tqdm import tqdm
import argparse
import os
import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="Argument parser for Hashing Lab")
    parser.add_argument(
        "-cd",
        "--collect-data",
        action="store_true",
        help="Perform measurements on generated data",
    )
    parser.add_argument(
        "-rd",
        "--real-data",
        action="store_true",
        help="Measure time on real data",
    )
    return parser.parse_args()


def run(pbar, dtype, additional_save_path="", **kwargs):
    measurement_results = {}
    for name, hashing_table_cls in pbar:
        kwargs["use_k_independent"] = False
        pbar.set_description(f"Name: {name}")
        if name == "CuckooHashMap":
            kwargs["use_k_independent"] = True
        evaluator = Evaluator(hashing_table_cls, dtype=dtype, **kwargs)
        measurement_results[name] = evaluator()
    with open(
        f"data/measurement_results_100k_2_power_{dtype}{additional_save_path}.json", "w"
    ) as fp:
        json.dump(measurement_results, fp, indent=4, sort_keys=False)


def main():
    args = parse_args()
    hashing_classes = reversed(
        [o for o in getmembers(algorithms) if isclass(o[1]) if not o[0] == "Item"]
    )
    if args.collect_data:
        pbar = tqdm(hashing_classes)
        for dtype in ("int", "tuple", "str"):
            run(
                pbar,
                dtype,
                start_value=1000,
                max_value=106000,
                step=5000,
                number_of_bits=63,
            )

    if args.real_data:
        save_path = "data/bbc-text-preprocessed.csv"
        if not os.path.exists(save_path):
            from utils.process_book import preprocess_text

            preprocess_text(save_path)
        data = pd.read_csv(save_path)
        all_text = []
        for _, text in data["text"].items():
            all_text.extend(text.split())
        all_text = set(all_text)
        all_text = [algorithms.Item(word, word) for word in all_text]
        pbar = tqdm(hashing_classes)
        run(
            pbar,
            "str",
            "_real_data",
            external_data=all_text,
            start_value=1000,
            max_value=25000,
            step=1000,
            number_of_bits=63,
        )


if __name__ == "__main__":
    main()
