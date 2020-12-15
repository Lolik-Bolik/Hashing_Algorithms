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
from inspect import getmembers, isclass
from dash.dependencies import Input, Output
import algorithms

algos = [o[0] for o in getmembers(algorithms) if isclass(o[1]) if not o[0] == "Item"]

algos.append("all")

data_types = {
    "int": "data/measurement_results_100k_int.json",
    "strings": "data/measurement_results_100k_str.json",
    "tuples": "data/measurement_results_100k_tuple.json",
    "real_life_data": "data/measurement_results_100k_str_real_data.json",
}

operation_names = ["delete", "get", "insert"]
density_values = ["0.1", "0.25", "0.5", "0.75", "0.9", "0.99", "all"]


def main():
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
                    html.H6("Hashing Method"),
                    dcc.Dropdown(
                        id="method-name",
                        options=[{"label": i, "value": i} for i in algos],
                        value="CuckooHashMap",
                    ),
                ],
                style={"width": "48%", "display": "inline-block"},
            ),
            html.Div(
                [
                    html.H6("Operation name"),
                    dcc.Dropdown(
                        id="operation-name",
                        options=[{"label": i, "value": i} for i in operation_names],
                        value="get",
                    ),
                ],
                style={"width": "48%", "display": "inline-block"},
            ),
            html.Div(
                [
                    html.H6("Table density"),
                    dcc.Dropdown(
                        id="density",
                        options=[{"label": i, "value": i} for i in density_values],
                        value="0.1",
                    ),
                ],
                style={"width": "48%", "display": "inline-block"},
            ),
            html.Div(
                [
                    html.H6("Data type"),
                    dcc.Dropdown(
                        id="data-type",
                        options=[{"label": i, "value": i} for i in data_types.keys()],
                        value="int",
                    ),
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
        Input("density", "value"),
        Input("data-type", "value"),
    )
    def update_graph(method_name, operation_name, density, data_type):
        method_name = method_name
        path_to_data = data_types[data_type]
        visualizer = Visualizer(path_to_data)
        fig = visualizer(method_name, operation_name, density)
        return fig


if __name__ == "__main__":
    main()
    app.run_server(debug=True)
