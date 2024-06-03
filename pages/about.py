from dash import html

layout = html.Div(
    className='container d-flex flex-column align-items-center justify-content-center',  # Apply Bootstrap classes for centering content
    children=[
        html.Link(
            rel='stylesheet',
            href='/assets/styles.css'  # Path to your CSS file
        ),
        html.H1("Autores del Proyecto", className='title mt-5 mb-3 text-center'),  # Center the heading with Bootstrap class 'text-center'
        
        html.P("Este proyecto fue desarrollado por:", className='description text-center mb-4'),  # Center the paragraph
        
        html.Ul([
            html.Li("Nestor", className='author-list-item'),  # Add a CSS class to the list item
        ], className='author-list text-center'),  # Center the list
        
        html.Img(src='../images/image.png', className='mt-5', style={'width': '50%', 'max-width': '500px'}),  # Center and limit image width
        
        html.A("Ir a la página de inicio", href='/', className='btn btn-primary mt-5'),  # Add Bootstrap button classes
        
        html.A("Descargar dataset", href='../models/mrd.pkl', download='mrd.pkl', className='btn btn-secondary mt-3'),  # Add Bootstrap button classes
    ]
)
