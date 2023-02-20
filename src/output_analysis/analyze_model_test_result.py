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

FILE_DIR = os.path.dirname(__file__)
MAIN_FILEPATH = os.path.join(
    FILE_DIR, os.path.pardir, os.path.pardir, "main.py")


# 1. generate datasets
def generate_dataset(test_model_dir, enzyme_id, identity_param, copy_number_param):
    os.makedirs(test_model_dir, exist_ok=True)
    for copy_number in range(1, copy_number_param + 1, 1):
        for identity in range(1, identity_param + 1, 1):
            with open(os.path.join(test_model_dir, f"copy_{copy_number}_identity_{identity}.csv"), "w") as f:
                title = f"enzyme_id,identity\n"
                f.writelines(title)
                for id in enzyme_id:
                    to_write = f"{id},{identity}\n"
                    for iter in range(0, copy_number):
                        f.writelines(to_write)


# 2. run match_enzyme
def run_match_enzyme(input_path, output_path):
    match_enzmye_output = subprocess.run(["python", MAIN_FILEPATH, "match_enzyme", "-i", input_path,
                                          "-o", output_path, "--quiet"],
                                         capture_output=False)
    if match_enzmye_output.returncode != 0:
        print("match_enzyme runtime error!")
        sys.exit()


# 3. plot results

# -------------------------
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
# ----------------------------


# model
def existence_score_model(x):
    # prob. ver.1
    # x = x[x >= 40]
    # y = 0.18 * np.log(0.15 * (x - 40) + 1) + 0.6
    # y = np.minimum(y, 1)

    # prob. ver.2
    # y = 1/(1+np.exp(-1/10 * (x - 40)))

    # prob. ver.3
    y = 1/100 * x
    return (x, y)


def plot_model():
    data_x = np.arange(0, 101, 1)
    data_y = existence_score_model(data_x)
    fig = go.Figure(data=go.Scatter(x=data_y[0], y=data_y[1]))
    fig.update_layout(title={"text": "Probablistic model",
                             "x": 0.5, "xanchor": "center"},
                      font_size=14)
    fig.update_layout(xaxis_title="identity",
                      yaxis_title="IAA producing score", font_size=12)
    fig.update_layout(xaxis_range=[-5, 105], yaxis_range=[-0.1, 1.1])
    return fig


def analyze_model_test_result(folder_path, search_pattern, copynum, fig):
    files = find_file(folder_path, search_pattern)
    result_collection = {"identity": [], "iaa_value": []}
    for file in files:
        result = parse_result(file)
        result_collection["identity"].append(result["identity"])
        result_collection["iaa_value"].append(result["iaa_value"])

    df_identity_iaa = pd.DataFrame(data=result_collection, dtype="float64")
    df_identity_iaa.sort_values(by=["identity"], inplace=True)

    fig.add_trace(go.Scatter(
        x=df_identity_iaa["identity"], y=df_identity_iaa["iaa_value"], name=f"copynum_{copynum}"))
    fig.update_layout(title={"text": "Single pathway enzymes",
                      "x": 0.5, "xanchor": "center"}, font_size=16)
    fig.update_layout(xaxis_title="identity",
                      yaxis_title="IAA producing score", font_size=14)
    fig.update_layout(yaxis_range=[0, 1])

    return (fig, df_identity_iaa["identity"], df_identity_iaa["iaa_value"])


def load_model_test_result(fig, model_result_dict):
    for copynum, identity_iaa in model_result_dict.items():
        fig.add_trace(go.Scatter(x=identity_iaa["axis_identity"],
                                 y=identity_iaa["axis_iaa"],
                                 name=f"copynum_{copynum}"))
        fig.update_layout(title={"text": "Single pathway enzymes",
                                 "x": 0.5, "xanchor": "center"}, font_size=16)
        fig.update_layout(xaxis_title="identity",
                          yaxis_title="IAA producing score", font_size=14)
        fig.update_layout(yaxis_range=[0, 1])

    return fig


# 4. dash application
app = Dash(__name__)


def dash_app(app, model_fig, result_fig):
    pil_image = Image.open(os.path.join(FILE_DIR, "pathway.png"))

    app.layout = html.Div([

        html.H1("Different Copy Numbers and Subpathways in Probablistic Model", style={
                "text-align": "center"}),
        html.Br(),
        html.Div([html.Img(src=pil_image, alt="pathway", style={"display": "flex", "margin-left": "auto", "margin-right": "auto"}),
                  dcc.Graph(id="model", figure=model_fig, style={"display": "flex", "width": "50%", "margin-left": "auto", "margin-right": "auto"})],
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
        dcc.Graph(id="my_graph", figure=result_fig)
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
    try:
        f = open(os.path.join(FILE_DIR, "model_result.pickle"), "rb")
        model_result_dict = pickle.load(f)
        f.close()
        result_fig = go.Figure()
        result_fig = load_model_test_result(result_fig, model_result_dict)
    except FileNotFoundError:
        with tempfile.TemporaryDirectory() as temp_dir:
            test_model_dir = os.path.join(temp_dir, "test_model")
            generate_dataset(test_model_dir,
                             enzyme_id=range(3, 6), identity_param=100,
                             copy_number_param=3)
            run_match_enzyme(input_path=test_model_dir, output_path=temp_dir)

            result_fig = go.Figure()
            match_enzyme_dir = os.path.join(temp_dir, "match_enzyme")
            model_result_dict = {}

            # analyze result from copy number 1 to 3
            for i in range(1, 4):
                result_fig, axis_identity, axis_iaa = analyze_model_test_result(
                    match_enzyme_dir, f"copy_{i}_*.txt", i, result_fig)
                model_result_dict[i] = {
                    "axis_identity": axis_identity, "axis_iaa": axis_iaa}

        with open(os.path.join(FILE_DIR, "model_result.pickle"), "wb") as f:
            pickle.dump(model_result_dict, f)

    model_fig = plot_model()
    app = dash_app(app, model_fig, result_fig)
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
