from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

from app import app
from apps import generateGraph, viewGraph, database, archive

app.layout = html.Div([

        html.Div([
            html.Div([
                html.Ul([

                    html.Li(dcc.Link('Ship Data Analytic System', href='/'), className='nav-li'),
                    html.Li(dcc.Link('Graphs', href='/apps/graph'), className='nav-li'),
                    html.Li(dcc.Link('Archive', href='/apps/archive'), className='nav-li'),
                    html.Li(dcc.Link('Database', href='/apps/database'), className='nav-li'),

                    ], className='nav-ul'),
            ], className='page-width'),
        ], className='nav-wrapper'),

        html.Div([

            dcc.Location(id='url', refresh=False),
            html.Div(id='page-content'),
            html.Div(id='data-content')

        ]),
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])

def display_page(pathname):
    if pathname == '/' or pathname == '/apps/graph':
         return generateGraph.layout
    elif pathname == '/apps/database':
         return database.layout
    elif pathname == '/apps/archive':
         return archive.layout
    elif pathname == '/apps/viewGraph':
         return viewGraph.layout
    else:
        print pathname
        return '404'

if __name__ == '__main__':
    app.run_server(debug=True)
