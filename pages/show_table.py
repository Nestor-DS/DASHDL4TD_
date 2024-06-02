import dash_html_components as html
import dash_table
import dash_core_components as dcc
import pandas as pd
import plotly.express as px
from app import app

# Load the original dataset
data_path = "./data/drinking_water_potability.csv"
df = pd.read_csv(data_path)

# Create a bar chart for potable and non-potable water data
potability_counts = df['Potability'].value_counts().reset_index()
potability_counts.columns = ['Potability', 'Count']

fig = px.bar(
    potability_counts,
    x='Potability',
    y='Count',
    labels={'Potability': 'Potabilidad', 'Count': 'Cantidad'},
    color='Potability',
    barmode='group'
)

# Update the layout of the figure to include custom font and center the title
fig.update_layout(
    font=dict(
        family='Pixelify Sans, sans-serif',
        size=18,
        color='#333'
    ),
    title=dict(
        text='Cantidad de Datos Potables y No Potables',
        x=0.5,  # Centro el título horizontalmente
        font=dict(
            family='Pixelify Sans, sans-serif',
            size=24,
            color='#333'
        )
    ),
    xaxis=dict(
        title=dict(
            font=dict(
                family='Pixelify Sans, sans-serif',
                size=20,
                color='#333'
            )
        )
    ),
    yaxis=dict(
        title=dict(
            font=dict(
                family='Pixelify Sans, sans-serif',
                size=20,
                color='#333'
            )
        )
    )
)

# Design the layout to show the interactive table and the bar chart
layout = html.Div(
    [
        html.Link(
            rel='stylesheet',
            href='/assets/styles.css'  # Ruta al archivo CSS que has creado
        ),
        html.H1("Contenido del Archivo CSV", className='pixelify-sans'),
        html.P(
        "El conjunto de datos utilizado en este proyecto se centra en la potabilidad del agua. Contiene datos de diferentes características del agua, como el pH, la dureza, la turbidez, la alcalinidad, la dureza del calcio, la dureza del magnesio, el cloruro, el sulfato, el sólido disuelto, el carbono orgánico, el trihalometano, el cloro, el sulfato de trihalometano y la potabilidad del agua. Los datos se dividen en dos clases: potable y no potable.",
            style={
                'marginBottom': '20px', 
                'marginTop': '20px',
                'marginRight': '50px',
                'marginLeft': '50px',
                'fontSize': '1.5em', 
                'textAlign': 'left', 
                'fontFamily': 'Pixelify Sans, sans-serif'},
            className='pixelify-sans'
        ),
      
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict('records'),
            sort_action='native',
            page_size=10,
            filter_action="native",
            style_table={
                'overflowX': 'auto',
                'padding': '10px',
                'width': '90%',
                'margin': 'auto'
            },
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold',
                'font-family': 'Pixelify Sans, sans-serif',
                'textAlign': 'center'
            },
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left',
                'font-family': 'Pixelify Sans, sans-serif',
                'minWidth': '150px', 'width': '150px', 'maxWidth': '150px'
            }
        ),
        html.P(
            "El gráfico de barras muestra la cantidad de datos potables y no potables en el conjunto de datos. Los datos potables se representan en azul y los no potables en naranja.",
            style={
                'marginBottom': '20px', 
                'marginLeft': '50px',
                'marginRight': '50px',
                'fontSize': '1.5em', 
                'textAlign': 'left', 
                'fontFamily': 'Pixelify Sans, sans-serif'},
            className='pixelify-sans'    
        ),
        dcc.Graph(
            id='potability-bar-chart',
            figure=fig,
            style={'width': '80%', 'margin': 'auto'}
        )
    ],
    style={'margin': '20px'}
)
