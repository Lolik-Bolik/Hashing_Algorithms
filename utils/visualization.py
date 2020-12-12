from .create_useful_dataframe import get_data
import plotly.express as px


class Visualizer:
    def __init__(self, path):
        self.data = get_data(path)
        self.methods = ["ChainHashMap", "CuckooHashMap", "OpenAddressingHashMap"]

    def __call__(self, method_name):
        assert method_name in self.methods
        cur_data = self.data.query(f"method=='{method_name}'")
        print(cur_data.head())
        fig = px.line(cur_data, x="elements_amount", y="get", title=f"{method_name}")
        return fig
