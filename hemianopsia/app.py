import gradio as gr
import pandas as pd
import plotly.express as px
import json

with open("data.json", "r") as f:
    raw_data = json.load(f)

seen_df = pd.DataFrame(raw_data.get("seenPoints", []))
seen_df["Status"] = "Seen Points"

unseen_df = pd.DataFrame(raw_data.get("unSeenPoints", []))
unseen_df["Status"] = "Unseen Points"

df = pd.concat([seen_df, unseen_df], ignore_index=True)

fig = px.scatter_3d(
    df, x="x", y="y", z="z", color="Status",
    color_discrete_map={"Seen Points": "blue", "Unseen Points": "red"},
    title="3D Scatterplot of Seen and Unseen Points",
    range_x=[-40, 40],
    range_y=[-40, 40]
)

fig.update_traces(marker=dict(size=3))
fig.update_layout(
    margin=dict(l=0, r=0, b=0, t=0),
    scene=dict(
        xaxis=dict(dtick=20), 
        yaxis=dict(dtick=20),
        aspectmode="cube"
    )
)

with gr.Blocks() as app:
    gr.Markdown("# Hemianopsia data")
    with gr.Row():
        gr.Plot(value=fig)

app.launch()