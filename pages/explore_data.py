import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from app import app

# Cargar el dataset original
data_path = "./data/drinking_water_potability.csv"
df = pd.read_csv(data_path)

# Estilos CSS personalizados
external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css']

# Lista de opciones de gráficos
graph_types = ['Histograma', 'Gráfico de Dispersión', 'Gráfico de Violín', 'Gráfico de Cajas']

# Diseñar el layout de la página
layout = html.Div(
    style={'backgroundColor': '#f8f9fa', 'padding': '2rem'},
    children=[
        html.Div(
            className='container',
            children=[
                html.H1(
                    "Explorar Datos de Potabilidad del Agua",
                    className='text-center my-4',
                    style={'font-size': '2.5rem', 'font-weight': 'bold'}
                ),
                html.Div(
                    className='row justify-content-center',
                    children=[
                        html.Div(
                            className='col-md-6',
                            children=[
                                dcc.Dropdown(
                                    id='feature-dropdown',
                                    options=[{'label': col, 'value': col} for col in df.columns[:-1]],
                                    value='ph',
                                    clearable=False,
                                    className='form-control mb-2',
                                    style={'width': '100%', 'display': 'inline-block'}
                                ),
                                dcc.Dropdown(
                                    id='graph-type-dropdown',
                                    options=[{'label': graph_type, 'value': graph_type} for graph_type in graph_types],
                                    value='Histograma',
                                    clearable=False,
                                    className='form-control',
                                    style={'width': '100%', 'display': 'inline-block'}
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className='row mt-4',
                    children=[
                        html.Div(
                            className='col-12',
                            children=[
                                dcc.Graph(
                                    id='feature-graph',
                                    config={'displayModeBar': False}
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
    ],
)

# Definir la callback para actualizar el gráfico según la característica y el tipo de gráfico seleccionados
@app.callback(
    Output('feature-graph', 'figure'),
    [Input('feature-dropdown', 'value'),
     Input('graph-type-dropdown', 'value')]
)
def update_graph(selected_feature, selected_graph_type):
    if selected_graph_type == 'Histograma':
        fig = px.histogram(
            df, 
            x=selected_feature, 
            color='Potability', 
            barmode='overlay',
            title=f"Distribución de {selected_feature} por Potabilidad",
            template='simple_white'
        )
        fig.update_layout(
            title={'x':0.5, 'xanchor': 'center'},
            xaxis_title=selected_feature,
            yaxis_title='Cantidad',
            legend_title_text='Potabilidad'
        )
    elif selected_graph_type == 'Gráfico de Dispersión':
        fig = px.scatter(
            df,
            x=selected_feature,
            y='Potability',
            title=f"{selected_feature} vs Potabilidad",
            template='simple_white'
        )
        fig.update_layout(
            title={'x':0.5, 'xanchor': 'center'},
            xaxis_title=selected_feature,
            yaxis_title='Potabilidad',
            legend_title_text='Potabilidad'
        )
    elif selected_graph_type == 'Gráfico de Violín':
        fig = px.violin(
            df,
            y=selected_feature,
            box=True,
            points='all',
            color='Potability',
            title=f"Distribución de {selected_feature} por Potabilidad",
            template='simple_white'
        )
        fig.update_layout(
            title={'x':0.5, 'xanchor': 'center'},
            yaxis_title=selected_feature,
            xaxis_title='Potabilidad',
            legend_title_text='Potabilidad'
        )
    elif selected_graph_type == 'Gráfico de Cajas':
        fig = px.box(
            df,
            x='Potability',
            y=selected_feature,
            title=f"{selected_feature} por Potabilidad",
            template='simple_white'
        )
        fig.update_layout(
            title={'x':0.5, 'xanchor': 'center'},
            xaxis_title='Potabilidad',
            yaxis_title=selected_feature,
            legend_title_text='Potabilidad'
        )
    return fig
