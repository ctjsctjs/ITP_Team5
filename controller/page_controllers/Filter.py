from dash.dependencies import Input, Output

from view.pages.filter import layout
from view.templates.table import generate_table
from model.database import SQL
from app import app


@app.callback(
    Output('generate-table', 'children'),
    [Input('table-store', 'children')])
def get_table(dummy):
    sql = SQL()
    df = sql.get_table('testtable')

    return generate_table(df)

