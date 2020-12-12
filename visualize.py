from utils import Visualizer
import json
import argparse
import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from app import app
from dash.dependencies import Input, Output


methods = {
    "Chain Hashing": "ChainHashMap",
    "Cuckoo Hashing": "CuckooHashMap",
    "Open Addressing Hashing": "OpenAddressingHashMap",
    "all": "all",
}

operation_names = ["delete", "get", "insert"]


def main(opts):
    card = dbc.Card(
        dbc.CardBody(
            [
                html.H4(
                    "Hashing Algorithms result visaulization", className="card-title"
                ),
                html.H6("About", className="card-subtitle"),
                html.P(
                    "Here is the link with source code of algorithms and visualization.",
                    className="card-text",
                ),
                dbc.CardLink(
                    "Github link",
                    href="https://github.com/Lolik-Bolik/Hashing_Algorithms/",
                ),
            ]
        ),
        style={"width": "25rem"},
    )

    app.layout = html.Div(
        [
            card,
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
            html.Div(
                [
                    dcc.Dropdown(
                        id="operation-name",
                        options=[{"label": i, "value": i} for i in operation_names],
                        value="get",
                    )
                ],
                style={"width": "48%", "display": "inline-block"},
            ),
            dcc.Graph(id="indicator-graphic"),
        ]
    )

    @app.callback(
        Output("indicator-graphic", "figure"),
        Input("method-name", "value"),
        Input("operation-name", "value"),
    )
    def update_graph(method_name, operation_name):
        method_name = methods[method_name]
        visualizer = Visualizer(opts.data_path)
        fig = visualizer(method_name, operation_name)
        return fig


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Hashing Algorithms visualization.")
    parser.add_argument(
        "--data_path",
        default="measurement_results_10k.json",
        help="path to data with hashing algorithms results",
    )

    args = parser.parse_args()
    main(args)
    app.run_server(debug=True)
