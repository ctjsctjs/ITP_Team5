import dash_html_components as html
import dash_core_components as dcc

layout = \
    html.Div([
        html.H1("GRAPH"),
        html.Div(id='graph-table-container'),

        # Dropdown for Axis-Selection
        html.Div([
            # Dropdown for X-Axis
            html.Label('Select X'),
            dcc.Dropdown(
                id='graph-dropdown-x',
                clearable=False,
            ),

            # Dropdown for Y-Axis
            html.Label('Select Y'),
            dcc.Dropdown(
                id='graph-dropdown-y',
                clearable=False,
            ),

            # Dropdown for Y2-Axis
            html.Label('Select Y2'),
            dcc.Dropdown(
                id='graph-dropdown-y2',
                clearable=False,
            ),
            # Graph
            html.Div(dcc.Graph(id='graph-graph'), className="")

        ], className=""),

        # Generated Graph
        html.Div([

        ]),

        # Hidden Elements
        html.Div(id='graph-dummy', style={'display': 'none'}),
        html.Div(id='graph-table-store', style={'display': 'none'}),
        html.Div(id='different',style={'display': 'none'})
    ])
