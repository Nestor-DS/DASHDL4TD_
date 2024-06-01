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
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from tensorflow.keras.models import model_from_json
import os
# Obtener la ruta absoluta del directorio actual
current_directory = os.path.dirname(os.path.abspath(__file__))

# Cargar el modelo final
def load_model():
    # Cargar la arquitectura del modelo desde el archivo JSON
    with open("best_model.json", "r") as json_file:
        loaded_model_json = json_file.read()
    # Crear el modelo a partir de la arquitectura cargada
    loaded_model = model_from_json(loaded_model_json)
    # Cargar los pesos del modelo
    loaded_model.load_weights("best_model_weights.h5")
    return loaded_model

# Definir la ruta del archivo CSV
data_file_path = os.path.join(current_directory, 'data', 'drinking_water_potability.csv')

# Verificar si el archivo CSV existe
if os.path.exists(data_file_path):
    # Cargar los datos
    df = pd.read_csv(data_file_path)
else:
    # Mostrar un mensaje de error si el archivo no se encuentra
    raise FileNotFoundError(f"No se encontró el archivo CSV: {data_file_path}")

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Diseñar el layout de la aplicación con pestañas
app.layout = html.Div([
    html.H1("Potabilidad del Agua"),
    dcc.Tabs([
        dcc.Tab(label='Explorar Datos', children=[
            html.Div([
                dcc.Dropdown(
                    id='feature-dropdown',
                    options=[{'label': col, 'value': col} for col in df.columns[:-1]],
                    value='ph',
                    clearable=False
                ),
                dcc.Graph(id='feature-graph'),
            ])
        ]),
        dcc.Tab(label='Hacer Predicciones', children=[
            html.Div([
                html.Div(id='prediction-output')
            ])
        ])
    ])
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

# Definir la callback para hacer predicciones con el modelo
@app.callback(
    Output('prediction-output', 'children'),
    [Input('feature-dropdown', 'value')]
)
def make_prediction(selected_feature):
    # Supongamos que tienes un nuevo dato para hacer predicciones
    new_data = df.sample(1)  # Selecciona una fila aleatoria del dataframe
    X_new = new_data.drop(columns=['Potability']).values
    loaded_model = load_model()
    prediction = loaded_model.predict(X_new)
    potability = "Potable" if prediction[0][0] > 0.5 else "No Potable"
    return f"Según el modelo, este agua es: {potability}"

# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
```

```compare_data.py:
# compare_data.py

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from app import app

# Cargar el dataset original
data_path = "../data/drinking_water_potability.csv"
df = pd.read_csv(data_path)

# Diseño de la pestaña para comparar dos atributos
compare_layout = html.Div([
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
# explore_data.py

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from app import app  # Importar la aplicación Dash

# Cargar el dataset original
data_path = "../data/drinking_water_potability.csv"
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

```

```make_predictions.py:
# make_predictions.py

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
from tensorflow.keras.models import model_from_json

from app import app  # Importar la aplicación Dash

# Cargar el modelo final
def load_model():
    # Cargar la arquitectura del modelo desde el archivo JSON
    with open("../models/best_model.json", "r") as json_file:
        loaded_model_json = json_file.read()
    # Crear el modelo a partir de la arquitectura cargada
    loaded_model = model_from_json(loaded_model_json)
    # Cargar los pesos del modelo
    loaded_model.load_weights("../models/best_model_weights.h5")
    return loaded_model

# Cargar el dataset original
data_path = "../data/drinking_water_potability.csv"
df = pd.read_csv(data_path)

# Diseñar el layout de la página
layout = html.Div([
    html.H1("Hacer Predicciones"),
    html.Div(id='prediction-output')
])

# Definir la callback para hacer predicciones con el modelo
@app.callback(
    Output('prediction-output', 'children'),
    [Input('feature-dropdown', 'value')]
)
def make_prediction(selected_feature):
    # Supongamos que tienes un nuevo dato para hacer predicciones
    new_data = df.sample(1)  # Selecciona una fila aleatoria del dataframe
    X_new = new_data.drop(columns=['Potability']).values
    loaded_model = load_model()
    prediction = loaded_model.predict(X_new)
    potability = "Potable" if prediction[0][0] > 0.5 else "No Potable"
    return f"Según el modelo, este agua es: {potability}"

```