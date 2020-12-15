import pandas as pd


def get_data(path=""):
    data_pd = pd.read_json(path, orient="index")
    hash_map_sizes_capacities = data_pd.columns
    data = []
    for index, name in enumerate(list(data_pd.index)):
        for results, size in zip(data_pd.iloc[index, :], hash_map_sizes_capacities):
            data.append(
                [
                    name,
                    size.split(",")[0],
                    float(size.split(",")[1]),
                    results["insert"],
                    results["delete"],
                    results["get"],
                ]
            )
    df = pd.DataFrame(
        data,
        columns=["method", "elements_amount", "density", "insert", "delete", "get"],
    )
    return df
