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
