import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def assign_rank(file):
    df = pd.read_csv(file)
    df["rank"] = df["score"].rank(method="average", ascending=False)
    return df

def compare_rank(df1, df2):
    join_df = df1.join(df2.set_index("species"), on="species", lsuffix='_1', rsuffix='_2')
    return join_df


file1 = r"D:\zye21\special\biofertilizer_prediction\temp_res\log_model_10\mapping_analysis\prediction_output.csv"
file2 = r"D:\zye21\special\biofertilizer_prediction\temp_res\log_model_100\mapping_analysis\prediction_output.csv"

df1 = assign_rank(file1)
df2 = assign_rank(file2)

df = compare_rank(df1, df2)
df.index += 1
df_rows = len(df.index)
fig_total = px.scatter(df, x=df.index, y="rank_2", labels={"index": "logistic_10", "rank_2": "logistic_100"})
fig_total.update_layout(xaxis=dict(dtick=200, range=[0, df_rows]), yaxis=dict(dtick=200, range=[0, df_rows]))
fig_total.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1))
fig_total.update_layout(title={"text": "Total predictions in rank", "x": 0.5, "xanchor": "center"})
fig_total.add_annotation(
  x=0,  # arrows' head
  y=0,  # arrows' head
  ax=df_rows,  # arrows' tail
  ay=df_rows,  # arrows' tail
  xref='x',
  yref='y',
  axref='x',
  ayref='y',
  text='',  # if you want only the arrow
  showarrow=True,
  arrowhead=0,
  arrowsize=1,
  arrowwidth=1,
  arrowcolor='red'
)
fig_total

df = df.head(30)
df_rows = len(df.index)
fig_30 = px.scatter(df, x=df.index, y="rank_2", labels={"index": "logistic_10", "rank_2": "logistic_100"})
fig_30.update_layout(xaxis=dict(dtick=5, range=[0, df_rows]), yaxis=dict(dtick=5, range=[0, df_rows]))
fig_30.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1))
fig_30.update_layout(title={"text": "Top 30 predictions in rank", "x": 0.5, "xanchor": "center"})
fig_30.add_annotation(
  x=0,  # arrows' head
  y=0,  # arrows' head
  ax=df_rows,  # arrows' tail
  ay=df_rows,  # arrows' tail
  xref='x',
  yref='y',
  axref='x',
  ayref='y',
  text='',  # if you want only the arrow
  showarrow=True,
  arrowhead=0,
  arrowsize=1,
  arrowwidth=1,
  arrowcolor='red'
)
fig_30

with open("./logistic_10_100.html", "w") as f:
    f.write(fig_total.to_html(full_html=False))
    f.write(fig_30.to_html(full_html=False, include_plotlyjs="cdn"))
