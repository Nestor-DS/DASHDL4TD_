import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from app import app

# Cargar el dataset original
data_path = "./data/drinking_water_potability.csv"
df = pd.read_csv(data_path)

# Diseñar el layout de la página
layout = html.Div([
    html.H1("Explorar Datos"),
    dcc.Dropdown(
        id='feature-dropdown',
        options=[{'label': col, 'value': col} for col in df.columns[:-1]],
        value='ph',
        clearable=False
    ),
    dcc.Graph(id='feature-graph')
])

# Definir la callback para actualizar el gráfico según la característica seleccionada
@app.callback(
    Output('feature-graph', 'figure'),
    [Input('feature-dropdown', 'value')]
)
def update_graph(selected_feature):
    fig = px.histogram(df, x=selected_feature, color='Potability', barmode='overlay',
                       title=f"Distribución de {selected_feature} por Potabilidad")
    return fig
