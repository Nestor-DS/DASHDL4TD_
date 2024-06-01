Tengo este proyecto:
Uso un dataset llamado "drinking_water_potability.csv".
Ejemplo de datos:
ph,Hardness,Solids,Chloramines,Sulfate,Conductivity,Organic_carbon,Trihalomethanes,Turbidity,Potability
7.080794504263196,204.8904555,20791.31898,7.300211873,368.5164413,564.3086542,10.37978308,86.99097046,2.963135381,0
3.716080075,129.4229205,18630.05786,6.635245884,333.775776610501,592.8853591,15.18001312,56.32907628,4.500656275,0
8.099124189,224.2362594,19909.54173,9.275883603,333.775776610501,418.6062131,16.86863693,66.42009251,3.05593375,0
8.316765884,214.3733941,22018.41744,8.059332377,356.8861356,363.2665162,18.4365245,100.3416744,4.628770537,0
8.628301074,185.9267231,31548.00646,7.079462297,333.775776610501,342.3556975,18.24836789,62.18868705,5.100857854,1
6.26011129,211.5941125,18577.62397,7.154890694,340.792574,357.0983955,7.992209971,82.36537826,5.403614892,1
10.80815694,198.5967508,29614.34879,5.782417746,304.6220612,383.2694104,14.90282034,47.89640649,4.362542227,1
7.371914156,148.1936976,42059.38042,7.966710439,324.5462621,544.8484318,17.16650385,62.67775632,4.338957326,1
4.825591458,234.7839038,11142.39263,6.442769292,370.416831,370.1889481,13.04635458,46.31599219,3.463097154,1

Quiero hacer una pagina web sobre esto
```
mi_aplicacion_dash/
│
├── assets/
│   └── styles.css
│
├── data/
│   └── drinking_water_potability.csv
│
├── models/
│   ├── best_model.json
│   └── best_model_weights.h5
│
├── pages/
│   ├── __init__.py
│   ├── explore_data.py
│   └── make_predictions.py
│
├── app.py
└── requirements.txt
```

```app.py:
from dash import dcc, html, Dash

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
```
```index.py
from dash import dcc, html
from dash.dependencies import Input, Output
from app import app
from pages import explore_data, make_predictions, compare_data

app.layout = html.Div([
    html.H1("Potabilidad del Agua"),
    dcc.Tabs(id='tabs', value='explore_data', children=[
        dcc.Tab(label='Explorar Datos', value='explore_data'),
        dcc.Tab(label='Hacer Predicciones', value='make_predictions'),
        dcc.Tab(label='Comparar Datos', value='compare_data')
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'explore_data':
        return explore_data.layout
    elif tab == 'make_predictions':
        return make_predictions.layout
    elif tab == 'compare_data':
        return compare_data.layout

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)

```

```compare_data.py:
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

```
```explore_data.py:
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
                    style={'font-size': '2.5rem', 'font-weight': 'bold', 'color': '#4CAF50'}
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
            template='plotly_dark'  # Cambiado a un tema oscuro
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
            template='plotly_dark'  # Cambiado a un tema oscuro
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
            template='plotly_dark'  # Cambiado a un tema oscuro
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
            template='plotly_dark'  # Cambiado a un tema oscuro
        )
        fig.update_layout(
            title={'x':0.5, 'xanchor': 'center'},
            xaxis_title='Potabilidad',
            yaxis_title=selected_feature,
            legend_title_text='Potabilidad'
        )
    return fig


```

```make_predictions.py:
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from tensorflow.keras.models import model_from_json
from app import app

# Cargar el modelo final una sola vez
def load_model():
    try:
        # Cargar la arquitectura del modelo desde el archivo JSON
        with open("./models/best_model.json", "r") as json_file:
            loaded_model_json = json_file.read()
        # Crear el modelo a partir de la arquitectura cargada
        loaded_model = model_from_json(loaded_model_json)
        # Cargar los pesos del modelo
        loaded_model.load_weights("./models/best_model_weights.h5")
        return loaded_model
    except Exception as e:
        print(f"Error al cargar el modelo: {e}")
        return None

loaded_model = load_model()

# Cargar el dataset original
data_path = "./data/drinking_water_potability.csv"
df = pd.read_csv(data_path)

# Estilos CSS embebidos
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# Diseñar el layout de la página con estilo
layout = html.Div([
    html.H1("Hacer Predicciones", style={'textAlign': 'center', 'color': '#4CAF50'}),
    
    # Entradas para las variables
    html.Div([
        html.Div([
            html.Label("pH:"),
            dcc.Input(id='input-ph', type='number', step=0.01, style={'width': '100%'}),
        ], style={'padding': 10, 'flex': 1}),
        
        html.Div([
            html.Label("Hardness:"),
            dcc.Input(id='input-hardness', type='number', step=0.01, style={'width': '100%'}),
        ], style={'padding': 10, 'flex': 1}),
        
        html.Div([
            html.Label("Solids:"),
            dcc.Input(id='input-solids', type='number', step=0.01, style={'width': '100%'}),
        ], style={'padding': 10, 'flex': 1}),
        
        html.Div([
            html.Label("Chloramines:"),
            dcc.Input(id='input-chloramines', type='number', step=0.01, style={'width': '100%'}),
        ], style={'padding': 10, 'flex': 1}),
        
        html.Div([
            html.Label("Sulfate:"),
            dcc.Input(id='input-sulfate', type='number', step=0.01, style={'width': '100%'}),
        ], style={'padding': 10, 'flex': 1}),
        
        html.Div([
            html.Label("Conductivity:"),
            dcc.Input(id='input-conductivity', type='number', step=0.01, style={'width': '100%'}),
        ], style={'padding': 10, 'flex': 1}),
        
        html.Div([
            html.Label("Organic Carbon:"),
            dcc.Input(id='input-organic-carbon', type='number', step=0.01, style={'width': '100%'}),
        ], style={'padding': 10, 'flex': 1}),
        
        html.Div([
            html.Label("Trihalomethanes:"),
            dcc.Input(id='input-trihalomethanes', type='number', step=0.01, style={'width': '100%'}),
        ], style={'padding': 10, 'flex': 1}),
        
        html.Div([
            html.Label("Turbidity:"),
            dcc.Input(id='input-turbidity', type='number', step=0.01, style={'width': '100%'}),
        ], style={'padding': 10, 'flex': 1}),
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'}),
    
    html.Button('Hacer Predicción', id='predict-button', style={'width': '100%', 'padding': '10px', 'backgroundColor': '#4CAF50', 'color': 'white', 'border': 'none', 'margin': '10px 0'}),
    
    html.Div(id='prediction-output', style={'textAlign': 'center', 'margin': '20px', 'fontSize': '20px'}),
    
    # Espacio para el gráfico
    dcc.Graph(id='potability-graph', style={'height': '400px'})
])

# Definir la callback para hacer predicciones con el modelo
@app.callback(
    [Output('prediction-output', 'children'),
     Output('potability-graph', 'figure')],
    [Input('predict-button', 'n_clicks')],
    [State('input-ph', 'value'),
     State('input-hardness', 'value'),
     State('input-solids', 'value'),
     State('input-chloramines', 'value'),
     State('input-sulfate', 'value'),
     State('input-conductivity', 'value'),
     State('input-organic-carbon', 'value'),
     State('input-trihalomethanes', 'value'),
     State('input-turbidity', 'value')]
)
def make_prediction(n_clicks, ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity):
    if n_clicks is None or n_clicks == 0:
        return "", {}

    if None in [ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]:
        return "Por favor, completa todas las entradas.", {}

    new_data = pd.DataFrame([{
        'ph': ph,
        'Hardness': hardness,
        'Solids': solids,
        'Chloramines': chloramines,
        'Sulfate': sulfate,
        'Conductivity': conductivity,
        'Organic_carbon': organic_carbon,
        'Trihalomethanes': trihalomethanes,
        'Turbidity': turbidity
    }])

    if loaded_model is None:
        return "Error al cargar el modelo.", {}

    prediction = loaded_model.predict(new_data.values)
    potability_percentage = prediction[0][0] * 100
    potability = "Potable" if potability_percentage > 50 else "No Potable"

    # Crear gráfico de potabilidad
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=potability_percentage,
        title={'text': "Porcentaje de Potabilidad"},
        gauge={'axis': {'range': [None, 100]},
               'bar': {'color': "darkblue"},
               'steps': [
                   {'range': [0, 50], 'color': "red"},
                   {'range': [50, 100], 'color': "green"}]}
    ))

    result_text = f"Según el modelo, este agua es: {potability} ({potability_percentage:.2f}% de potabilidad)"
    return result_text, fig

```