from dash.dependencies import Input, Output

from view.pages.viewGraph import layout
from app import app


@app.callback(
    Output('app-2-display-value', 'children'),
    [Input('app-2-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
