"""
Before running this file, notice that:
1. pathway.png is in the current folder
2. model_result.pickle (if exists in the current folder) will be loaded as result
3. the existence_score_model should be in congruent with that imported in
   match_enzyme.py
"""
import glob
import os
import pickle
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html
from PIL import Image

# model
def existence_score_model(n, x):
    # prob. ver.1
    # x = x[x >= 40]
    # y = 0.18 * np.log(0.15 * (x - 40) + 1) + 0.6
    # y = np.minimum(y, 1)

    # prob. ver.2
    y = 1/(1+np.exp(-1/n * (x - 40)))

    # prob. ver.3
    # y = 1/100 * x
    return (x, y)


def plot_model(n):
    data_x = np.arange(0, 101, 1)
    data_y = existence_score_model(n, data_x)
    fig = go.Figure(data=go.Scatter(x=data_y[0], y=data_y[1]))
    fig.update_layout(title={"text": f"Probablistic model, param:{n}",
                             "x": 0.5, "xanchor": "center"},
                      font_size=14)
    fig.update_layout(xaxis_title="identity",
                      yaxis_title="IAA producing score", font_size=12)
    fig.update_layout(xaxis_range=[-5, 105], yaxis_range=[-0.1, 1.1])
    return fig



# 4. dash application
app = Dash(__name__)


def dash_app(app, model_fig):

    app.layout = html.Div([

        html.H1("Different Copy Numbers and Subpathways in Probablistic Model", style={
                "text-align": "center"}),
        html.Br(),
        html.Div([dcc.Graph(id="model_0", figure=model_fig[0], style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"}),
                 dcc.Graph(id="model_1", figure=model_fig[1], style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"})],
                 style={"display": "flex", "flex-direction": "row"}),
        html.Div([dcc.Graph(id="model_2", figure=model_fig[2], style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"}),
                 dcc.Graph(id="model_3", figure=model_fig[3], style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"})],
                 style={"display": "flex", "flex-direction": "row"}),
        html.Div([dcc.Graph(id="model_4", figure=model_fig[4], style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"})],
                 style={"display": "flex", "flex-direction": "row"}),
        html.Br(),
        # dcc.Dropdown(id="select_copynum",
        #                 options=[
        #                 {"label": "1", "value": 1},
        #                 {"label": "2", "value": 2},
        #                 {"label": "3", "value": 3}
        #                 ],
        #                 multi=False,
        #                 value=1,
        #                 style={"width": "40%", "margin-left": "3%"}),
    ])

    return app

# @app.callback(
#     [Output(component_id="my_graph", component_property="figure")],
#     [Input(component_id="select_copynum", component_property="value")]
# )
# def update_graph(slctd_copynum):
#     print(slctd_copynum)
#     print(type(slctd_copynum))
#     fig = go.Figure()
#     fig = analyze_model_test_result(folder_path, f"copy_{slctd_copynum}_*.txt", slctd_copynum, fig)

#     return [fig]


if __name__ == "__main__":
    model_fig_list = []
    model_fig_list.append(plot_model(1))
    model_fig_list.append(plot_model(3))
    model_fig_list.append(plot_model(10))
    model_fig_list.append(plot_model(30))
    model_fig_list.append(plot_model(100))
    app = dash_app(app, model_fig_list)
    app.run_server(debug=True, use_reloader=False)

    # pathway_fig = go.Figure()
    # pathway_fig.add_layout_image(dict(
    #     source=pic,
    #     xref="paper",
    #     yref="paper",
    #     opacity=0.5
    # ))

    # with open(os.path.join(FOLDER_PATH, "output.html"), "w") as f:
    #     f.write(pathway_fig.to_html(full_html=False))
    #     f.write(model_fig.to_html(full_html=False))
    #     f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))
