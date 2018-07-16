import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt

from view.templates.navbar import navbar

layout = \
    html.Div([
        navbar,
        dcc.Location(id='url', refresh=False),
        html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
        html.Div(id='page-content'),
        html.Div(id='data-content')
    ])
