import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import joblib
import numpy as np
import plotly.graph_objs as go
from app import app


# Función para predecir potabilidad
def predecir_potabilidad(model, ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity):
    # Crear un array con los valores ingresados
    features = np.array([[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])

    # Realizar la predicción
    prediction = model.predict(features)
    
    # Interpretar la predicción
    if prediction[0] == 1:
        return "El agua es potable."
    else:
        return "El agua no es potable."

# Cargar el modelo desde el archivo
model_filename = "./models/mrd.pkl"
loaded_model = joblib.load(model_filename)
print("Modelo cargado exitosamente.")

# Diseño de la página web
layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='/assets/styles.css'  # Ruta al archivo CSS que has creado style={'textAlign': 'light', 'color': '#4CAF50'}
    ),
    html.Div(
        style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center', 'gap': '10px'},
        children=[
            html.H1("Hacer Predicciones", id='titleMakePredictions', className='pixelify-sans'),
            #html.Button('?', id='info-button', n_clicks=0, )
        ]
    ),

    
    html.P([
        "Ingresa los valores de las variables para hacer una predicción de potabilidad del agua.",
        html.Br(),
        "Los valores por defecto son los promedios de las variables en el conjunto de datos.",
        html.Br(),
        "Restricciones:",
        html.Br(),
        "** Solo acepta valores con dos puntos decimales. (Ando en eso)**",
    ], style={'textAlign': 'center', 'fontSize': '1.2em', 'margin': '20px', 'color': 'gray'}),

   # Inputs for variables
    html.Div([
        html.Div([
            html.Label("pH:", className='pixelify-sans'),
            dcc.Input(id='input-ph', type='number', step=0.01, style={'width': '100%'}, value=7.87),
        ], className='input-container',),
        
        html.Div([
            html.Label("Hardness:", className='pixelify-sans'),
            dcc.Input(id='input-hardness', type='number', step=0.01, style={'width': '100%'}, value=195.10),
        ], className='input-container',),
        
        html.Div([
            html.Label("Solids:", className='pixelify-sans'),
            dcc.Input(id='input-solids', type='number', step=0.01, style={'width': '100%'}, value = 17404.17),
        ], className='input-container',),
        
        html.Div([
            html.Label("Chloramines:", className='pixelify-sans'),
            dcc.Input(id='input-chloramines', type='number', step=0.01, style={'width': '100%'}, value = 7.50),
        ], className='input-container',),
        
        html.Div([
            html.Label("Sulfate:", className='pixelify-sans'),
            dcc.Input(id='input-sulfate', type='number', step=0.01, style={'width': '100%'}, value = 333.77),
        ], className='input-container',),
        
        html.Div([
            html.Label("Conductivity:", className='pixelify-sans'),
            dcc.Input(id='input-conductivity', type='number', step=0.01, style={'width': '100%'}, value = 327.45),
        ], className='input-container',),
        
        html.Div([
            html.Label("Organic Carbon:", className='pixelify-sans'),
            dcc.Input(id='input-organic_carbon', type='number', step=0.01, style={'width': '100%'}, value = 16.14),
        ], className='input-container',),
        
        html.Div([
            html.Label("Trihalomethanes:", className='pixelify-sans'),
            dcc.Input(id='input-trihalomethanes', type='number', step=0.01, style={'width': '100%'}, value  = 78.69),
        ], className='input-container',),
        
        html.Div([
            html.Label("Turbidity:", className='pixelify-sans'),
            dcc.Input(id='input-turbidity', type='number', step=0.01, style={'width': '100%'}, value=2.30),
        ], className='input-container',),
        
    ], style={'display': 'flex', 'flexWrap': 'wrap', 'justifyContent': 'space-around'}),
    
    html.Div(
        html.Button('Hacer Predicción',n_clicks=0, id='submit-val', ),
        style={
            'textAlign': 'center', 
            'border': 'none', 
        }
    ),
    
    html.Div([
        html.Div(id='result_text', className='pixelify-sans'),
        dcc.Graph(id='probabilidad-grafica'),
        dcc.Graph(id='potabilidad-grafica')  # Agregar esta línea para la gráfica de potabilidad
    ], style={'textAlign': 'center', 'margin': '20px'}),
    
])

@app.callback(
    [Output('result_text', 'children'),
     Output('probabilidad-grafica', 'figure'),
     Output('potabilidad-grafica', 'figure')],
    [Input('submit-val', 'n_clicks')],
    [dash.dependencies.State('input-ph', 'value'),
     dash.dependencies.State('input-hardness', 'value'),
     dash.dependencies.State('input-solids', 'value'),
     dash.dependencies.State('input-chloramines', 'value'),
     dash.dependencies.State('input-sulfate', 'value'),
     dash.dependencies.State('input-conductivity', 'value'),
     dash.dependencies.State('input-organic_carbon', 'value'),
     dash.dependencies.State('input-trihalomethanes', 'value'),
     dash.dependencies.State('input-turbidity', 'value')])
def update_output(n_clicks, ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity):
    result = ""
    fig_prob = go.Figure()
    fig_pot = go.Figure()
    if n_clicks > 0:
        result = predecir_potabilidad(loaded_model, ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity)
        probabilities = loaded_model.predict_proba([[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])
        
        # Crear la figura de la gráfica de barras
        fig_prob.add_trace(go.Bar(
            x=['No Potable', 'Potable'],
            y=probabilities[0],
            marker_color=['red', 'green']
        ))
        fig_prob.update_layout(title='Probabilidad de Potabilidad del Agua',
                          xaxis_title='Clases',
                          yaxis_title='Probabilidad')
        
        prediction = loaded_model.predict([[ph, hardness, solids, chloramines, sulfate, conductivity, organic_carbon, trihalomethanes, turbidity]])
        
        # Create potability graph
        fig_pot = go.Figure(go.Indicator(
            mode="gauge+number",
            value=prediction[0] * 100,
            title={'text': "Porcentaje de Potabilidad"},
            gauge={'axis': {'range': [None, 100]},
                   'bar': {'color': "darkblue"},
                   'steps': [
                       {'range': [0, 50], 'color': "red"},
                       {'range': [50, 100], 'color': "green"}]}
        ))

    return html.Div(result, className='pixelify-sans'), fig_prob, fig_pot

