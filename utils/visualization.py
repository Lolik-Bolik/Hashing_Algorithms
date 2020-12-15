from .create_useful_dataframe import get_data
from inspect import getmembers, isclass
import plotly.express as px
import algorithms
import dash_html_components as html


class Visualizer:
    def __init__(self, path):
        self.data = get_data(path)
        print(self.data)
        self.methods = [
            o[0] for o in getmembers(algorithms) if isclass(o[1]) if not o[0] == "Item"
        ]
        print(self.methods)

    def __call__(self, method_name, operation_name, density):
        if method_name != "all" and density != "all":
            assert method_name in self.methods
            cur_data = self.data.query(
                f"method=='{method_name}' & density=='{density}'"
            )
            fig = px.line(
                cur_data,
                x="elements_amount",
                y=f"{operation_name}",
                title=f"{method_name}",
            )
        elif method_name != "all" and density == "all":
            assert method_name in self.methods
            cur_data = self.data.query(f"method=='{method_name}'")
            fig = px.line(
                cur_data,
                x="elements_amount",
                y=f"{operation_name}",
                color="density",
                title=f"{method_name}",
            )
        elif method_name == "all" and density != "all":
            cur_data = self.data.query(f"density=='{density}'")
            fig = px.line(
                cur_data,
                x="elements_amount",
                y=f"{operation_name}",
                color="method",
                title=f"{method_name}",
            )
        else:
            return {
                "layout": {
                    "xaxis": {"visible": "false"},
                    "yaxis": {"visible": "false"},
                    "annotations": [
                        {
                            "text": "Please don't choose 'all' for method and 'all' for density",
                            "xref": "paper",
                            "yref": "paper",
                            "showarrow": "false",
                            "font": {"size": 28},
                        }
                    ],
                }
            }

        return fig
