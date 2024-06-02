from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from app import app

# Load the original dataset
data_path = "./data/drinking_water_potability.csv"
df = pd.read_csv(data_path)

# Define the graph types
graph_types = ['Histograma', 'Gráfico de Dispersión', 'Gráfico de Violín', 'Gráfico de Cajas']

# Design the page layout
layout = html.Div(
    style={'backgroundColor': '#f8f9fa', 'padding': '2rem'},
    children=[
        html.Div(
            className='container',
            children=[
                html.H1(
                    "Explorar Datos de Potabilidad del Agua",
                    className='text-center my-4',
                    style={'font-size': '2.5rem', 'font-weight': 'bold', 'color': '#4CAF50','align':'center'}
                ),
                html.Div(
                    className='row justify-content-center',
                    children=[
                        html.Div(
                            className='col-md-6 d-flex justify-content-between',
                            style={'align':'center', },
                            children=[
                                dcc.Dropdown(
                                    id='feature-dropdown',
                                    options=[{'label': col, 'value': col} for col in df.columns[:-1]],
                                    value='ph',
                                    clearable=False,
                                    className='form-control mb-2',
                                    style={'width': '48%', 'display': 'inline-block'}
                                ),
                                dcc.Dropdown(
                                    id='graph-type-dropdown',
                                    options=[{'label': graph_type, 'value': graph_type} for graph_type in graph_types],
                                    value='Histograma',
                                    clearable=False,
                                    className='form-control',
                                    style={'width': '48%', 'display': 'inline-block'}
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className='row mt-4 justify-content-center',  # Centro las gráficas horizontalmente
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

# Define the callback to update the graph based on selected feature and graph type
@app.callback(
    Output('feature-graph', 'figure'),
    [Input('feature-dropdown', 'value'),
     Input('graph-type-dropdown', 'value')]
)
def update_graph(selected_feature, selected_graph_type):
    color_map = {0: 'red', 1: 'blue'}  # 0 for non-potable (red), 1 for potable (blue)
    if selected_graph_type == 'Histograma':
        fig = px.histogram(
            df, 
            x=selected_feature, 
            color='Potability', 
            barmode='overlay',
            title=f"Distribución de {selected_feature} por Potabilidad",
            color_discrete_map=color_map
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
            color='Potability',
            color_discrete_map=color_map
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
            color_discrete_map=color_map
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
            color='Potability',
            color_discrete_map=color_map
        )
        fig.update_layout(
            title={'x':0.5, 'xanchor': 'center'},
            xaxis_title='Potabilidad',
            yaxis_title=selected_feature,
            legend_title_text='Potabilidad'
        )
    return fig
