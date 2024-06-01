from dash import dcc, html
from dash.dependencies import Input, Output
from app import app
from pages import explore_data, make_predictions, compare_data, show_table, about

app.layout = html.Div([
    html.H1("Potabilidad del Agua"),
    dcc.Tabs(id='tabs', value='show_table', children=[
        dcc.Tab(label='Mostrar Tabla', value='show_table'),
        dcc.Tab(label='Explorar Datos', value='explore_data'),
        dcc.Tab(label='Hacer Predicciones', value='make_predictions'),
        dcc.Tab(label='Comparar Datos', value='compare_data'),
        dcc.Tab(label='Acerca de', value='about')
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
    elif tab == 'show_table':
        return show_table.layout
    elif tab == 'about':
        return about.layout

if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
