from dash.dependencies import Input, Output

from view.pages.archive import layout
from app import app


@app.callback(
    Output('archive-display-value', 'children'),
    [Input('archive-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
