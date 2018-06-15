from dash.dependencies import Input, Output

# from view.pages.test import layout
from app import app
from view.pages.test import layout
import model.database as db

import dash_html_components as html

# Dash
def generate_table(dataframe, max_rows=10):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


@app.callback(
    Output('table-container', 'children'),
    [Input('big-button', 'n_clicks')])
def test(dummy):
    test_sql = db.SQL()
    df = test_sql.get_table("testtable")
    return generate_table(df)
