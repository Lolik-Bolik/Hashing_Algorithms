from utils import Visualizer
import json
import argparse
import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
from app import app
from dash.dependencies import Input, Output


methods = {
    "Chain Hashing": "ChainHashMap",
    "Cuckoo Hashing": "CuckooHashMap",
    "Open Addressing Hashing": "OpenAddressingHashMap",
}


def main(opts):

    app.layout = html.Div(
        [
            html.Div(
                [
                    dcc.Dropdown(
                        id="method-name",
                        options=[{"label": i, "value": i} for i in methods.keys()],
                        value="Chain Hashing",
                    )
                ],
                style={"width": "48%", "display": "inline-block"},
            ),
            dcc.Graph(id="indicator-graphic"),
        ]
    )

    @app.callback(Output("indicator-graphic", "figure"), Input("method-name", "value"))
    def update_graph(method_name):
        method_name = methods[method_name]
        visualizer = Visualizer(opts.data_path)
        fig = visualizer(method_name)
        return fig

    app.run_server(debug=True)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Hashing Algorithms visualization.")
    parser.add_argument(
        "--data_path",
        default="measurement_results_10k.json",
        help="path to data with hashing algorithms results",
    )

    args = parser.parse_args()
    main(args)
