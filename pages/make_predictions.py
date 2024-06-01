import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objects as go
from tensorflow.keras.models import model_from_json
from app import app

# Load the model once
def load_model():
    try:
        # Load the model architecture from JSON file
        with open("./models/best_model.json", "r") as json_file:
            loaded_model_json = json_file.read()
        # Create the model from loaded architecture
        loaded_model = model_from_json(loaded_model_json)
        # Load the model weights
        loaded_model.load_weights("./models/best_model_weights.h5")
        return loaded_model
    except Exception as e:
        print(f"Error loading the model: {e}")
        return None

loaded_model = load_model()

# Load the original dataset
data_path = "./data/drinking_water_potability.csv"
df = pd.read_csv(data_path)

# Embed CSS styles
app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

# Design the page layout with style
layout = html.Div([
    html.H1("Hacer Predicciones", style={'textAlign': 'center', 'color': '#4CAF50'}),
    
    # Inputs for variables
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
    
    html.Div(
        html.Button('Hacer Predicción', id='predict-button', style={'padding': '10px', 'backgroundColor': '#4CAF50', 'color': 'white', 'border': 'none'}),
        style={'textAlign': 'center'}
    ),
    
    html.Div(id='prediction-output', style={'textAlign': 'center', 'margin': '20px', 'fontSize': '20px'}),
    
    # Space for graph
    dcc.Graph(id='potability-graph', style={'height': '400px'})
])

# Callback to make predictions with the model
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

    # Create potability graph
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

