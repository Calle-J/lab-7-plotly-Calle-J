import gradio as gr
import pandas as pd
import plotly.express as px
import json

with open("479379.json", "r") as f:
    raw_adapted_hand_data = json.load(f)

with open("005774.json", "r") as f:
    raw_hand_data = json.load(f)

def extract_points(json_data, root_key):
    """Extracts all x, y, z coordinates from horizontal and vertical phases."""
    all_points = []
    for hand_info in json_data.get(root_key, []):
        all_points.extend(hand_info.get("horizontalCoordinates", []))
        all_points.extend(hand_info.get("verticalCoordinates", []))
    return pd.DataFrame(all_points)

hand_data = extract_points(raw_hand_data, "handData")
adapted_hand_data = extract_points(raw_adapted_hand_data, "adaptedHandData")

# Add a 'Type' column to distinguish between actual movement and the VR target
hand_data["Type"] = "Actual (Hand)"
adapted_hand_data["Type"] = "Adapted (Amplified)"

# Concatenate both datasets into a single DataFrame for plotting
df = pd.concat([hand_data, adapted_hand_data], ignore_index=True)

# 1. 3D Trajectory Plot - Shows the path through the VR space
fig_3d = px.line_3d(
    df, x="x", y="y", z="z", color="Type",
    title="3D Movement Trajectory: Actual vs Amplified",
    labels={"x": "Horizontal", "y": "Vertical", "z": "Depth"}
)

# 2. 2D Range of Motion Plot - Focuses on Horizontal vs Vertical amplification
fig_rom = px.scatter(
    df, x="x", y="y", color="Type",
    title="Range of Motion: Horizontal (X) vs Vertical (Y)",
    labels={"x": "Horizontal Position", "y": "Vertical Position"}
)

with gr.Blocks() as app:
    gr.Markdown("# Motor Amplification")
    gr.Markdown("Comparing actual user hand movement vs the VR-amplified target movement.")
    
    with gr.Row():
        with gr.Column():
            gr.Markdown("### 3. Spatial Path")
            gr.Plot(fig_3d)
        with gr.Column():
            gr.Markdown("### Range of Motion (Horizontal vs Vertical)")
            gr.Plot(fig_rom)

app.launch()