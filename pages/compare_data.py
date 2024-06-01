import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from app import app

# Cargar el dataset original
data_path = "./data/drinking_water_potability.csv"
df = pd.read_csv(data_path)

# Diseño de la pestaña para comparar dos atributos
layout = html.Div([
    html.H1("Comparar Atributos"),
    dcc.Dropdown(
        id='x-axis-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns[:-1]],
        value='Hardness',
        clearable=False
    ),
    dcc.Dropdown(
        id='y-axis-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns[:-1]],
        value='Conductivity',
        clearable=False
    ),
    dcc.Graph(id='compare-graph')
])

# Callback para actualizar el gráfico al seleccionar los atributos
@app.callback(
    Output('compare-graph', 'figure'),
    [Input('x-axis-dropdown', 'value'),
     Input('y-axis-dropdown', 'value')]
)
def update_compare_graph(x_axis, y_axis):
    fig = px.scatter(df, x=x_axis, y=y_axis, color='Potability', 
                     title=f"Comparación entre {x_axis} y {y_axis}")
    return fig
