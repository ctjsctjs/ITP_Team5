import dash_html_components as html

layout = \
    html.Div([
        # header
        html.Div([
            html.H2('Filter Sample', className='header-title')
        ]),
        # body-wrapper
        html.Div([
            # body-Content
            # call method with dataframe as input
            html.Div(id='generate-table')
        ]),
        # hidden-store
        html.Div(id='table-store', style={'display': 'none'}),
    ])
