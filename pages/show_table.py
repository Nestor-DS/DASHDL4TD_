import dash_html_components as html
import dash_table
import pandas as pd
from app import app

# Load the original dataset
data_path = "./data/drinking_water_potability.csv"
df = pd.read_csv(data_path)

# Design the layout to show the interactive table
layout = html.Div(
    [
        html.Link(
            rel='stylesheet',
            href='/assets/styles.css'  # Ruta al archivo CSS que has creado
        ),
        html.H1("Contenido del Archivo CSV"),
        html.P(
            "Este proyecto se centra en la aplicación de métodos de aprendizaje profundo a conjuntos de datos tabulares relacionados con el fin de encontrar los mejores resultados posibles. Se utilizan diferentes enfoques para la exploración de datos, la clasificación con bosques aleatorios y técnicas de aprendizaje profundo.",
            style={'marginBottom': '20px', 'fontSize': '1.5em', 'textAlign': 'lift'}
        ),
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[{"name": col, "id": col} for col in df.columns],
            data=df.to_dict('records'),
            sort_action='native',
            page_size=10,
            filter_action="native",
            style_table={'overflowX': 'auto'},
            style_header={
                'backgroundColor': 'rgb(230, 230, 230)',
                'fontWeight': 'bold'
            },
            style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
                'textAlign': 'left',
                'minWidth': '180px',
                'width': '180px',
                'maxWidth': '180px'
            }
        )
    ],
    style={'margin': '20px'}
)
