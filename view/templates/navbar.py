import dash_html_components as html
import dash_core_components as dcc

from config.routes import pathname
from app import app
from dash.dependencies import Input, Output, State

navbar = \
    html.Div([
        html.Nav([
            html.Div([
                html.Ul([
                    html.Li(dcc.Link(html.Img(src='/static/img/APL-logo.svg', className='logo'), href=pathname['Home']), className='nav-li'),
                    html.Li(dcc.Link('Graphs', href=pathname['Graphs']), className='nav-li'),
                    # html.Li(dcc.Link('Archive', href=pathname['Archive']), className='nav-li'),
                    html.Li(dcc.Link('Database', href=pathname['Database']), className='nav-li'),
                ], className='nav-ul'),
            ], className='page-width'),
        ], id='nav-wrapper', className='nav-wrapper'),
        html.Div(id='nav-dummy', className='nav-dummy')
    ])

@app.callback(Output('nav-wrapper', 'style'),
              [Input('url', 'pathname')])
def display_navbar(path):
    if (path==pathname['Home']):
        return {'background-color': 'transparent'}
    else:
        return {'background-color': '#33bbb0'}

@app.callback(Output('nav-dummy', 'style'),
              [Input('url', 'pathname')])
def display_navbar(path):
    if (path==pathname['Home']):
        return {'display': 'none'}
    else:
        return {'display': 'block'}
