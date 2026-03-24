import gradio as gr
import pandas as pd
import plotly.express as px

sites = {
    2004: {"Norway": 5, "Denmark": 4, "Sweden": 13},
    2022: {"Norway": 8, "Denmark": 10, "Sweden": 15}
}

rows = []
for year, countries in sites.items():
    for country, value in countries.items():
        rows.append({"Year": year, "Country": country, "Number of world heritage sites": value})

data = pd.DataFrame(rows)

data_2004 = pd.DataFrame({
    "Country": list(sites[2004].keys()),
    "Number of world heritage sites": list(sites[2004].values())
})
data_2022 = pd.DataFrame({
    "Country": list(sites[2022].keys()),
    "Number of world heritage sites": list(sites[2022].values())
})

colors = {"Norway": "#283250", "Denmark": "#F05440", "Sweden": "#3274D8"}

with gr.Blocks() as app:
    gr.Markdown("# World Heritage Sites in Scandinavia")
    with gr.Row():
        gr.Markdown("<h2 style='text-align: center'>2004</h2>")
        gr.Markdown("<h2 style='text-align: center'>2022</h2>")

    with gr.Row():
        bar_chart = gr.BarPlot(
            data_2004,
            color_map=colors,
            color="Country",
            x="Country",
            y="Number of world heritage sites",
            x_title="Country",
            y_title="Number of world heritage sites",
            y_lim=[0, None]
        )

        bar_chart = gr.BarPlot(
            data_2022,
            color_map=colors,
            color="Country",
            x="Country",
            y="Number of world heritage sites",
            x_title="Country",
            y_title="Number of world heritage sites",
            y_lim=[0, None]
        )
    
    with gr.Row():
        fig_2004 = px.pie(
            data_2004,
            values="Number of world heritage sites",
            names="Country",
            color="Country",
            hole=0.5,
            color_discrete_map=colors
        )
        fig_2004.update_layout(annotations=[dict(text='2004', x=0.5, y=0.5, font_size=20, showarrow=False)])
        gr.Plot(value=fig_2004)

        fig_2022 = px.pie(
            data_2022,
            values="Number of world heritage sites",
            names="Country",
            color="Country",
            hole=0.5,
            color_discrete_map=colors
        )
        fig_2022.update_layout(annotations=[dict(text='2022', x=0.5, y=0.5, font_size=20, showarrow=False)])
        gr.Plot(value=fig_2022)
    
    with gr.Row():
        fig = px.bar(
            data,
            x="Country",
            y="Number of world heritage sites",
            color="Country",
            facet_col="Year",
            color_discrete_map=colors,
            text="Number of world heritage sites"
        )
        fig.update_layout(showlegend=False)
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        fig.update_xaxes(title_text="")
        fig.update_yaxes(showticklabels=False)
        fig.update_traces(textposition="inside", insidetextanchor="start")
        gr.Plot(value=fig)
    
    with gr.Row():
        fig = px.bar(
            data,
            x="Year",
            y="Number of world heritage sites",
            color="Country",
            color_discrete_map=colors,
            text="Number of world heritage sites"
        )
        fig.update_traces(textposition="inside", insidetextanchor="start")
        gr.Plot(value=fig)
    
    with gr.Row():
        fig = px.line(
            data,
            x="Year",
            y="Number of world heritage sites",
            color="Country",
            color_discrete_map=colors
        )
        gr.Plot(value=fig)

app.launch()