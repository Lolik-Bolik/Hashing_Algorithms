from utils import Visualizer
import json
import argparse
import plotly.express as px
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash()


def main(opts):
    vs = Visualizer(opts.data_path)
    fig = vs()

    app.layout = html.Div([dcc.Graph(figure=fig)])

    app.run_server(debug=True, use_reloader=False)
    # print(data_pd.head())
    # print(len(data_pd))
    # df = px.data.gapminder().query("country=='Canada'")
    # fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
    # fig.show()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Hashing Algorithms visualization.")
    parser.add_argument(
        "--data_path",
        default="measurement_results_10k.json",
        help="path to data with hashing algorithms results",
    )

    args = parser.parse_args()
    main(args)
