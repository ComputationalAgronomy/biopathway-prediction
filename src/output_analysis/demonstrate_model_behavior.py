import os
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

FILE_DIR = os.path.dirname(__file__)


# 1. single enzyme
def existence_score_model(x):
    # prob. ver.1
    # x = x[x >= 40]
    # y = 0.18 * np.log(0.15 * (x - 40) + 1) + 0.6
    # y = np.minimum(y, 1)

    # prob. ver.2
    y = 1/(1+np.exp(-1/10 * (x - 40)))

    # prob. ver.3
    # y = 1/100 * x
    return y

def cal_single_enzyme(x, y, n):
    # two copies
    score = 1 - ((1 - existence_score_model(x)) ** n) * (1 - existence_score_model(y))

    return score

def plot_heatmap(x, y, z, title_text, x_text, y_text):
    fig = go.Figure(data=go.Heatmap(x=x, y=y, z=z))
    fig.update_layout(title={"text": title_text, "x": 0.5, "xanchor": "center"}, font_size=16)
    fig.update_layout(xaxis_title=x_text, yaxis_title=y_text, font_size=14)
    fig.update_layout(xaxis_range=[0, 100], yaxis_range=[0, 100])
    
    return fig

def plot_surface(x, y, z, title_text, x_text, y_text):
    fig = go.Figure(data=go.Surface(x=x, y=y, z=z))
    fig.update_layout(title={"text": title_text, "x": 0.5, "xanchor": "center"}, font_size=16)
    fig.update_layout(xaxis_title=x_text, yaxis_title=y_text, font_size=14)
    fig.update_layout(xaxis_range=[0, 100], yaxis_range=[0, 100])
    
    return fig

x = np.arange(0, 100, 1)
y = np.arange(0, 100, 1)

# surface
X, Y = np.meshgrid(x, y)
Z = cal_single_enzyme(X, Y, 1)
fig_SE_2_S = plot_surface(x, y, Z, "Single Enzyme_Two Copies", "Copy_1_identity", "Copy_2_identity")

# heatmap
fig_SE_2_H = plot_heatmap(x, y, Z, "Single Enzyme_Two Copies", "Copy_1_identity", "Copy_2_identity")

Z = cal_single_enzyme(X, Y, 2)
fig_SE_3_S = plot_surface(x, y, Z, "Single Enzyme_Three Copies", "Copy_1+2_identity", "Copy_3_identity")
fig_SE_3_H = plot_heatmap(x, y, Z, "Single Enzyme_Three Copies", "Copy_1+2_identity", "Copy_3_identity")



# 2. Single Pathway
# two enzymes in a pathway
def cal_single_pathway(x, y, n):
    score = (1 - (1 - existence_score_model(x)) ** n) * (1 - (1 - existence_score_model(y)) ** 1)
    return score

x = np.arange(0, 100, 1)
y = np.arange(0, 100, 1)
z = np.arange(0, 100, 1)

X, Y = np.meshgrid(x, y)
Z = cal_single_pathway(X, Y, 1)

fig_SP_2_S = plot_surface(x, y, Z, "Single Pathway_Two Enzymes", "Enzyme_1_identity", "Enzyme_2_identity")
fig_SP_2_H = plot_heatmap(x, y, Z, "Single Pathway_Two Enzymes", "Enzyme_1_identity", "Enzyme_2_identity")

Z = cal_single_pathway(X, Y, 2)
fig_SP_3_S = plot_surface(x, y, Z, "Single Pathway_Three Enzymes", "Enzyme_1+2_identity", "Enzyme_3_identity")
fig_SP_3_H = plot_heatmap(x, y, Z, "Single Pathway_Three Enzymes", "Enzyme_1+2_identity", "Enzyme_3_identity")



# Dash

def dash_app(app):

    app.layout = html.Div([

        html.H1("Different Copy Numbers and Subpathways in Probablistic Model", style={
                "text-align": "center"}),
        html.Br(),
        html.Div([dcc.Graph(figure=fig_SE_2_S, style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"}),
                  dcc.Graph(figure=fig_SE_2_H, style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"})],
                 style={"display": "flex", "flex-direction": "row"}),
        html.Br(),
        html.Div([dcc.Graph(figure=fig_SE_3_S, style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"}),
                  dcc.Graph(figure=fig_SE_3_H, style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"})],
                 style={"display": "flex", "flex-direction": "row"}),
        html.Br(),
        html.Div([dcc.Graph(figure=fig_SP_2_S, style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"}),
                  dcc.Graph(figure=fig_SP_2_H, style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"})],
                 style={"display": "flex", "flex-direction": "row"}),
        html.Br(),
        html.Div([dcc.Graph(figure=fig_SP_3_S, style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"}),
                  dcc.Graph(figure=fig_SP_3_H, style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"})],
                 style={"display": "flex", "flex-direction": "row"}),
    ])

    return app

app = Dash(__name__)
app = dash_app(app)
app.run_server(debug=True, use_reloader=False)