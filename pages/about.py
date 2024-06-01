import dash_html_components as html
import dash_table
import pandas as pd
from app import app

layout = html.Div([
    html.Link(
        rel='stylesheet',
        href='/assets/styles.css'  # Ruta al archivo CSS que has creado
    ),
    html.H1("Autores del Proyecto"),
    html.P("Este proyecto fue desarrollado por "),
])