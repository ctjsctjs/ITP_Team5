from dash.dependencies import Input, Output

from view.pages.database import layout
from app import app


#@app.callback(
#Output('app-graph-display-value', 'children'),
#[Input('app-graph-dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)
