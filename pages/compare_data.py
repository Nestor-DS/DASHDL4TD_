from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from app import app

# Load the original dataset
data_path = "./data/drinking_water_potability.csv"
df = pd.read_csv(data_path)

# Design the tab layout to compare two attributes
layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='/assets/styles.css'  # Ruta al archivo CSS que has creado
    ),
    html.H1("Comparar Atributos", style={'textAlign': 'center', 'color': '#4CAF50'}),
    html.Div([
        html.Label('Seleccionar eje X:', style={'marginRight': '10px'}),
        dcc.Dropdown(
            id='x-axis-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns[:-1]],
            value='Hardness',
            clearable=False
        )
    ], style={'marginBottom': '20px'}),
    html.Div([
        html.Label('Seleccionar eje Y:', style={'marginRight': '10px'}),
        dcc.Dropdown(
            id='y-axis-dropdown',
            options=[{'label': col, 'value': col} for col in df.columns[:-1]],
            value='Conductivity',
            clearable=False
        )
    ], style={'marginBottom': '20px'}),
    dcc.Graph(id='compare-graph')
])

# Callback to update the graph when selecting attributes
@app.callback(
    Output('compare-graph', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_compare_graph(x_axis, y_axis):
    fig = px.scatter(df, x=x_axis, y=y_axis, color='Potability', 
                     title=f"Comparación entre {x_axis} y {y_axis}",
                     labels={'Potability': 'Potabilidad', x_axis: 'Eje X', y_axis: 'Eje Y'})
    return fig
