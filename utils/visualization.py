from .create_useful_dataframe import get_data
import plotly.express as px


class Visualizer:
    def __init__(self, path):
        self.data = get_data(path)
        self.methods = ["ChainHashMap", "CuckooHashMap", "OpenAddressingHashMap"]

    def __call__(self, method_name, operation_name):
        if method_name != "all":
            assert method_name in self.methods
            cur_data = self.data.query(f"method=='{method_name}'")
            fig = px.line(
                cur_data,
                x="elements_amount",
                y=f"{operation_name}",
                title=f"{method_name}",
            )
        else:
            fig = px.line(
                self.data,
                x="elements_amount",
                y=f"{operation_name}",
                title=f"{method_name}",
                color="method",
            )

        return fig
