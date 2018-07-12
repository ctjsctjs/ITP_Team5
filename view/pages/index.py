import dash_html_components as html
import dash_core_components as dcc

from view.templates.navbar import navbar

layout = \
    html.Div([
        navbar,
        dcc.Location(id='url', refresh=False),
        html.Div(id='page-content'),
        html.Div(id='data-content')
    ])
