import glob
import os
import sys

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, Input, Output, dcc, html

from PIL import Image

FOLDER_PATH = os.path.dirname(__file__)

# parse match enzyme result
def parse_filename(filename):
    basename = os.path.basename(filename).rsplit(".", 1)[0]
    copy_number = basename.split("_")[1]
    identity = basename.split("_")[3]
    return copy_number, identity


def parse_result(filename):
    copy_number, identity = parse_filename(filename)
    with open(filename, "r") as f:
        for line in f.readlines():
            line = line.strip("\n")
            if not line.startswith("iaa"):
                continue
            iaa_value = float(line.split(" ")[1])
            break
    return {"copy_number": copy_number, "identity": identity,
            "iaa_value": iaa_value}


def find_file(input_path, pattern):
    file_list = glob.glob(os.path.join(input_path, pattern), recursive=True)
    return file_list


def analyze_model_test_result(folder_path, search_pattern, copynum, fig):
    files = find_file(folder_path, search_pattern)
    result_collection = []
    for file in files:
        result_collection.append(parse_result(file))

    axis_identity = [result["identity"] for result in result_collection]
    axis_iaa = [result["iaa_value"] for result in result_collection]
    
    fig.add_trace(go.Scatter(x=axis_identity, y=axis_iaa, name=copynum))
    fig.update_layout(title=f"Single pathway enzymes", font_size=16)
    fig.update_layout(xaxis_title="identity", yaxis_title="IAA producing score", font_size=14)
    fig.update_layout(yaxis_range=[0, 1])
    
    return fig

# probablistic model
def existence_score_model(x):
    x = x[x >= 40]
    y = 0.18 * np.log(0.15 * (x - 40) + 1) + 0.6
    y = np.minimum(y, 1)
    return (x, y)

def plot_model(fig=None):
    data_x = np.arange(0, 101, 1)
    data_y = existence_score_model(data_x)
    fig = go.Figure(data=go.Scatter(x=data_y[0], y=data_y[1]))
    fig.update_layout(title={"text": "Probablistic model", "x": 0.5, "xanchor": "center"},  font_size=14)
    fig.update_layout(xaxis_title="identity", yaxis_title="IAA producing score", font_size=12)
    fig.update_layout(xaxis_range=[-5, 105], yaxis_range=[-0.1, 1.1])
    return fig


# dash plotting

app = Dash(__name__)
pil_image = Image.open(os.path.join(FOLDER_PATH, "pathway.png"))
model_fig = plot_model()
app.layout = html.Div([

    html.H1("Different Copy Numbers and Subpathways in Probablistic Model", style={"text-align": "center"}),
    html.Br(),
    html.Div([html.Img(src=pil_image, alt="pathway", style={"display": "flex", "margin-left": "auto", "margin-right": "auto"}),
              dcc.Graph(id="model", figure=model_fig, style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"})],
              style={"display": "flex", "flex-direction": "row"}),
    html.Br(),
    dcc.Dropdown(id="select_copynum",
                    options=[
                    {"label": "1", "value": 1},
                    {"label": "2", "value": 2},
                    {"label": "3", "value": 3}
                    ],
                    multi=False,
                    value=1,
                    style={"width": "40%", "margin-left": "3%"}),
    html.Br(),
    dcc.Graph(id="my_graph")
])


@app.callback(
    [Output(component_id="my_graph", component_property="figure")],
    [Input(component_id="select_copynum", component_property="value")]
)
def update_graph(slctd_copynum):
    print(slctd_copynum)
    print(type(slctd_copynum))
    fig = analyze_model_test_result(folder_path, f"copy_{slctd_copynum}_*.txt", slctd_copynum)

    return [fig]


if __name__ == "__main__":
    folder_path = sys.argv[1]
    # app.run_server(debug=True, use_reloader=False)

    fig = go.Figure()
    for i in range(1, 4):
        fig = analyze_model_test_result(folder_path, f"copy_{i}_*.txt", i, fig)
    fig.show()    
    # with open(f"{FOLDER_PATH}/output.html", "w") as f:
    #     for fig in fig_list:
    #         f.write(fig.to_html(full_html=False, include_plotlyjs="cdn"))


