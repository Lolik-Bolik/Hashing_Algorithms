from .create_useful_dataframe import get_data
import plotly.express as px


class Visualizer:
    def __init__(self, path):
        self.data_path = path

    def __call__(self):
        data = get_data(self.data_path)
        data = data.query("method=='OpenAddressingHashMap'")
        fig = px.line(data, x="elements_amount", y="insert", title="Hashing")
        return fig
